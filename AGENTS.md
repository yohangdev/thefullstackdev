# Repository Guidelines

## Project Structure & Module Organization

This is a dependency-free, single-page personal website. All production code lives in `index.html`:

- `<head>` contains SEO, social metadata, the embedded favicon, and JSON-LD.
- `<style>` contains the complete mobile-first design system and responsive layout.
- `<body>` contains semantic page sections such as `#about`, `#work`, and `#experience`.
- The final `<script>` provides navigation and active-section behavior.

There are currently no separate assets, generated files, or test directories. Preserve the single-file architecture unless a change clearly requires otherwise.

## Build, Test, and Development Commands

No build step or package installation is required.

```sh
python3 -m http.server 4173
```

Serves the repository locally at `http://127.0.0.1:4173/`. Do not rely only on opening the file directly; the local server better matches production behavior.

```sh
git diff --check
```

Checks edited files for whitespace errors before committing.

## Coding Style & Naming Conventions

Use two-space indentation in HTML, CSS, and JavaScript. Prefer semantic HTML, accessible labels, and native browser features over new dependencies. Use kebab-case for CSS classes and IDs, such as `.case-study` and `#recommendations`. Add reusable colors, spacing, or typography values to `:root` instead of repeating literals.

Keep CSS mobile-first. Existing layout breakpoints are `700px` and `960px`. JavaScript should remain small, framework-free, and wrapped to avoid globals. Preserve Public Sans for interface text and IBM Plex Mono for labels and metadata.

## Testing Guidelines

There is no automated test framework. For every change:

1. Load the page through the local server.
2. Check desktop and a roughly `390px` mobile viewport.
3. Verify navigation, external links, keyboard focus, and browser console output.
4. Confirm there is no horizontal overflow and only one `<h1>`.

Metadata edits should also keep the canonical URL, Open Graph fields, X/Twitter fields, and JSON-LD consistent.

## Commit & Pull Request Guidelines

Use concise Conventional Commit-style messages, matching the existing history: `chore: checkpoint personal website`. Prefer prefixes such as `feat:`, `fix:`, `docs:`, `style:`, and `chore:`.

Pull requests should include a short purpose statement, testing notes, and desktop/mobile screenshots for visual changes. Call out copy, metrics, or SEO changes that need factual review. Never commit credentials, private profile data, generated caches, or local environment files.
