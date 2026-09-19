#!/usr/bin/env python3
"""Build the static site into dist/ with minified inline CSS and JavaScript."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


STYLE_RE = re.compile(r"(<style\b[^>]*>)(.*?)(</style>)", re.IGNORECASE | re.DOTALL)
SCRIPT_RE = re.compile(
    r"(<script\b([^>]*)>)(.*?)(</script>)", re.IGNORECASE | re.DOTALL
)
CSS_PUNCTUATION = frozenset("{}:;,>+~")
JS_OPERATOR_CHARS = frozenset("=+-*/%<>!&|^~?")
JS_MULTI_OPERATORS = frozenset(
    {
        "===",
        "!==",
        ">>>=",
        "**=",
        "&&=",
        "||=",
        "??=",
        "<<=",
        ">>=",
        "=>",
        "==",
        "!=",
        "<=",
        ">=",
        "++",
        "--",
        "&&",
        "||",
        "??",
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
        "**",
        "<<",
        ">>",
        ">>>",
        "?.",
        "&=",
        "|=",
        "^=",
    }
)
REGEX_PREFIXES = frozenset(
    {
        "=",
        "(",
        "[",
        "{",
        ",",
        ":",
        ";",
        "!",
        "&&",
        "||",
        "??",
        "?",
        "=>",
        "return",
        "throw",
        "case",
        "delete",
        "void",
        "typeof",
        "new",
        "in",
        "of",
    }
)


def _read_quoted(source: str, start: int) -> tuple[str, int]:
    quote = source[start]
    index = start + 1

    while index < len(source):
        if source[index] == "\\":
            index += 2
            continue
        if source[index] == quote:
            return source[start : index + 1], index + 1
        index += 1

    raise ValueError(f"Unterminated {quote} string in inline JavaScript")


def _read_regex(source: str, start: int) -> tuple[str, int]:
    index = start + 1
    in_character_class = False

    while index < len(source):
        character = source[index]
        if character == "\\":
            index += 2
            continue
        if character == "[":
            in_character_class = True
        elif character == "]":
            in_character_class = False
        elif character == "/" and not in_character_class:
            index += 1
            while index < len(source) and (source[index].isalpha() or source[index].isdigit()):
                index += 1
            return source[start:index], index
        index += 1

    raise ValueError("Unterminated regular expression in inline JavaScript")


def _can_start_regex(previous: str | None) -> bool:
    return previous is None or previous in REGEX_PREFIXES


def _tokenize_js(source: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    index = 0

    while index < len(source):
        character = source[index]

        if character.isspace():
            index += 1
            continue

        if source.startswith("//", index):
            newline = source.find("\n", index + 2)
            index = len(source) if newline == -1 else newline + 1
            continue

        if source.startswith("/*", index):
            end = source.find("*/", index + 2)
            if end == -1:
                raise ValueError("Unterminated comment in inline JavaScript")
            index = end + 2
            continue

        if character in "'\"`":
            value, index = _read_quoted(source, index)
            tokens.append(("literal", value))
            continue

        previous = tokens[-1][1] if tokens else None
        if character == "/" and _can_start_regex(previous) and index + 1 < len(source):
            value, index = _read_regex(source, index)
            tokens.append(("literal", value))
            continue

        if character.isalpha() or character in "_$":
            end = index + 1
            while end < len(source) and (source[end].isalnum() or source[end] in "_$"):
                end += 1
            tokens.append(("word", source[index:end]))
            index = end
            continue

        if character.isdigit():
            end = index + 1
            while end < len(source) and (source[end].isalnum() or source[end] in "._"):
                end += 1
            tokens.append(("number", source[index:end]))
            index = end
            continue

        operator = next(
            (
                candidate
                for candidate in sorted(JS_MULTI_OPERATORS, key=len, reverse=True)
                if source.startswith(candidate, index)
            ),
            character,
        )
        token_type = "operator" if all(character in JS_OPERATOR_CHARS for character in operator) else "punctuation"
        tokens.append((token_type, operator))
        index += len(operator)

    return tokens


def _needs_js_space(previous: tuple[str, str], current: tuple[str, str]) -> bool:
    previous_type, previous_value = previous
    current_type, current_value = current

    if previous_type in {"word", "number"} and current_type in {"word", "number"}:
        return True

    if previous_value in {"+", "-"} and current_value == previous_value:
        return True

    if previous_type == "operator" and current_type == "operator":
        if previous_value[-1] in JS_OPERATOR_CHARS and current_value[0] in JS_OPERATOR_CHARS:
            return previous_value + current_value in JS_MULTI_OPERATORS

    if previous_type == "number" and current_value == ".":
        return True

    if previous_value == "/" and current_value in {"/", "*"}:
        return True

    return False


def minify_js(source: str) -> str:
    tokens = _tokenize_js(source)
    output: list[str] = []

    for token in tokens:
        if output and _needs_js_space(previous_token, token):
            output.append(" ")
        output.append(token[1])
        previous_token = token

    return "".join(output).strip()


def minify_css(source: str) -> str:
    output: list[str] = []
    quote: str | None = None
    pending_space = False
    index = 0

    while index < len(source):
        character = source[index]

        if quote:
            output.append(character)
            if character == "\\" and index + 1 < len(source):
                output.append(source[index + 1])
                index += 2
                continue
            if character == quote:
                quote = None
            index += 1
            continue

        if source.startswith("/*", index):
            end = source.find("*/", index + 2)
            if end == -1:
                raise ValueError("Unterminated comment in inline CSS")
            index = end + 2
            pending_space = bool(output)
            continue

        if character in "'\"":
            if pending_space and output and output[-1] not in CSS_PUNCTUATION:
                output.append(" ")
            pending_space = False
            quote = character
            output.append(character)
            index += 1
            continue

        if character.isspace():
            pending_space = bool(output)
            index += 1
            continue

        if pending_space and output:
            if output[-1] not in CSS_PUNCTUATION and character not in CSS_PUNCTUATION:
                output.append(" ")
        pending_space = False
        output.append(character)
        index += 1

    return "".join(output).strip()


def minify_html(source: str) -> str:
    style_count = 0

    def replace_style(match: re.Match[str]) -> str:
        nonlocal style_count
        style_count += 1
        return f"{match.group(1)}{minify_css(match.group(2))}{match.group(3)}"

    result = STYLE_RE.sub(replace_style, source)
    if style_count == 0:
        raise ValueError("No inline style block found in source HTML")

    script_count = 0

    def replace_script(match: re.Match[str]) -> str:
        nonlocal script_count
        attributes = match.group(2)
        if re.search(r"\btype\s*=\s*['\"]application/ld\+json['\"]", attributes, re.IGNORECASE):
            return match.group(0)
        if re.search(r"\bsrc\s*=", attributes, re.IGNORECASE):
            return match.group(0)
        script_count += 1
        return f"{match.group(1)}{minify_js(match.group(3))}{match.group(4)}"

    result = SCRIPT_RE.sub(replace_script, result)
    if script_count == 0:
        raise ValueError("No inline JavaScript block found in source HTML")

    return result


def build(source: Path, output_dir: Path) -> None:
    html = source.read_text(encoding="utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(minify_html(html), encoding="utf-8")

    for filename in ("robots.txt", "llms.txt"):
        metadata_file = source.parent / filename
        if not metadata_file.is_file():
            raise FileNotFoundError(f"Required file not found: {metadata_file}")
        shutil.copy2(metadata_file, output_dir / filename)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("index.html"))
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    args = parser.parse_args()

    build(args.source, args.output_dir)
    print(f"Built {args.output_dir / 'index.html'}")
    print(f"Copied {args.output_dir / 'robots.txt'}")
    print(f"Copied {args.output_dir / 'llms.txt'}")


if __name__ == "__main__":
    main()
