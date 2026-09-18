# thefullstackdev.com

Personal website for [Yoga Hanggara](https://www.linkedin.com/in/yoga-hanggara/), a Lead Full Stack Developer focused on SaaS product engineering, cloud-native platforms, reliable delivery, and engineering leadership.

## Overview

The site is a lightweight, mobile-first static page built without frameworks or build dependencies. HTML, CSS, JavaScript, SEO metadata, JSON-LD, and the favicon are all contained in [`index.html`](./index.html).

Key features include:

- Responsive SaaS-inspired design
- Professional experience and selected case studies
- Career outcomes and colleague recommendations
- Accessible navigation and semantic markup
- Open Graph, X/Twitter, canonical, and structured-data metadata
- Public Sans and IBM Plex Mono typography

## Run Locally

Start a static file server from the repository root:

```sh
python3 -m http.server 4173
```

Then open [http://127.0.0.1:4173/](http://127.0.0.1:4173/).

No package installation or build command is required.

## Deploy

The repository is designed for Cloudflare Pages:

1. Connect this GitHub repository to a Cloudflare Pages project.
2. Select the static HTML or no-framework preset.
3. Leave the build command empty.
4. Set the output directory to the repository root.

The custom domain is expected to be `thefullstackdev.com`.

## Contributing

See [`AGENTS.md`](./AGENTS.md) for repository structure, coding conventions, testing expectations, and commit guidelines.
