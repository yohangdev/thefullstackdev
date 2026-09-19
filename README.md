# thefullstackdev.com

Personal website for [Yoga Hanggara](https://www.linkedin.com/in/yoga-hanggara/), a Lead Full Stack Developer focused on SaaS product engineering, cloud-native platforms, reliable delivery, and engineering leadership.

## Overview

The site is a lightweight, mobile-first static page built without frameworks or build dependencies. The main page’s HTML, CSS, JavaScript, SEO metadata, JSON-LD, and favicon are contained in [`index.html`](./index.html), with a standalone [`404.html`](./404.html) for invalid paths.

Key features include:

- Responsive systems-oriented design
- Professional experience and selected case studies
- Career outcomes and colleague recommendations
- Accessible navigation and semantic markup
- Open Graph, X/Twitter, canonical, and structured-data metadata
- Public Sans typography with a reserved, commented mono-font variable for future code UI

## Design System

The visual language is deliberately editorial, technical, and restrained: a plain white canvas, strong black typography, structured borders, dark information panels, and a single electric-blue accent. The design should feel precise and calm rather than decorative.

### Brand Direction

- Use clear hierarchy and generous whitespace to make complex experience easy to scan.
- Prefer square, rectangular components. The site currently has no `border-radius` declarations.
- Keep surfaces flat and plain. Cards use white backgrounds and borders instead of shadows, gradients, or illustrations.
- Use dark panels for dense supporting information, metrics, and calls to action.
- Keep the blue accent purposeful for emphasis, links, indexes, and primary actions.
- Keep the green status color limited to the live/building indicator.

### Color Roles

| Role | Value | Usage |
| --- | --- | --- |
| Paper / surface | `#ffffff` | Page background and cards |
| Ink | `#111111` | Primary text and dark controls |
| Muted | `#5a5a5a` | Supporting text and metadata |
| Line | `#d8d8d8` | Standard borders and dividers |
| Strong line | `#bcbcbc` | Structural section borders |
| Dark | `#111111` | Profile, metric, featured work, and contact panels |
| Dark line | `#2d2d2d` | Dividers on dark panels |
| Accent | `#2457ff` | Text and controls on light surfaces |
| Accent on dark | `#849cff` | Accent text on dark surfaces; maintains readable contrast |
| Status | `#73e3a0` | Building status indicator only |

Avoid introducing tinted grays, colored gradients, or additional accent colors without a clear product or accessibility reason. The only intentional non-neutral colors are the blue accent and green status indicator.

### Typography

- Use Public Sans for all visible page content: headings, body copy, labels, metadata, navigation, buttons, and footer text.
- Keep the page mobile-first and use the existing type scale and `clamp()` patterns before adding new sizes.
- Use tight display headings with negative letter spacing and a line height close to `1`.
- Use uppercase labels sparingly for structure and wayfinding.
- The `--mono` variable remains commented in `index.html` for a future code showcase or technical component. Do not re-enable or load the mono font for general page typography.

### Layout and Components

- Keep the single-file architecture in `index.html` unless a change clearly requires a separate asset.
- Use a maximum content width of `1180px` and the existing responsive breakpoints at `700px` and `960px`.
- Use one-pixel borders and consistent spacing tokens rather than rounded cards or ornamental shadows.
- Preserve semantic HTML, one page-level `<h1>`, visible keyboard focus, and descriptive link labels.
- Dark components must use the light-on-dark text variants and the `--accent-on-dark` token where applicable.

### Accessibility and Theme

- The page intentionally remains a light theme, including when the user’s system prefers dark mode.
- Keep `color-scheme: light` and the light `theme-color` metadata aligned with the visual design.
- Check text contrast whenever a color or background changes. Small supporting text on dark panels should remain comfortably above WCAG AA contrast requirements.
- Test the page at desktop and roughly `390px` mobile widths. Confirm there is no horizontal overflow and that navigation and keyboard focus remain usable.

## Build

Generate the deployable site in `dist/`. The build keeps the HTML structure and metadata intact while minifying the inline CSS and JavaScript, then copies `404.html`, `robots.txt`, and `llms.txt`:

```sh
python3 build.py
```

The output directory can be changed when needed:

```sh
python3 build.py --output-dir /path/to/output
```

## Run Locally

Start a static file server from the repository root:

```sh
python3 -m http.server 4173
```

Then open [http://127.0.0.1:4173/](http://127.0.0.1:4173/).

No package installation is required.

## Deploy

The repository is designed for Cloudflare Pages:

1. Connect this GitHub repository to a Cloudflare Pages project.
2. Select the static HTML or no-framework preset.
3. Set the build command to `python3 build.py`.
4. Set the output directory to `dist`.

The custom domain is expected to be `thefullstackdev.com`.

## Contributing

See [`AGENTS.md`](./AGENTS.md) for repository structure, coding conventions, testing expectations, and commit guidelines.
