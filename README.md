# abbosov.com

Static multilingual website for Azizbek Abbosov, built with HTML, CSS and vanilla JavaScript for GitHub Pages. English lives at `/`; Uzbek and Russian have separate translated pages. The original prototype remains at `design-reference/index.html`. Phase 3 retains its palette and cinematic atmosphere while improving mobile link affordances, adding marked draft copy, and providing reviewed English, Uzbek, and Russian route sets.

## Structure

- `index.html` — English homepage at `/`, SEO metadata and structured data.
- `css/` — exact design tokens and reference styles, with responsive fallbacks and menu styling.
- `js/` — starfield, scroll choreography, navigation and bootstrap.
- `about/`, `education/`, `experience/`, `developer/`, `timeline/`, `journal/`, `gallery/`, `future/` — English inner pages.
- `uz/` and `ru/` — localized copies of the home page and all eight inner routes; slugs stay in English.
- `data/` — factual education, project and timeline records; plus an unpublished article template.
- `assets/fonts/` — self-hosted Inter and DejaVu Sans Mono WOFF2 fonts.
- `assets/images/` — social preview image assets.
- `assets/icons/` — favicon and application icon assets.
- `design-reference/index.html` — locked, original single-file prototype.
- `404.html`, `robots.txt`, `sitemap.xml`, `site.webmanifest`, `CNAME`, `.nojekyll` — GitHub Pages and search metadata.

## Run locally

From the repository root:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/`. A local server is needed for absolute-root asset paths and clean URLs to behave as on GitHub Pages.

## Deploy

Commit the root homepage and all supporting files and directories listed above, including `CNAME` and `.nojekyll`, and push them to the `main` branch at the repository root. GitHub Pages should publish the repository root. The `CNAME` file must contain exactly `abbosov.com`; leave DNS settings unchanged.

## Add a language or page

Create a separate HTML file for the translation or page. Give it the correct `lang`, unique title and description, self-referencing canonical, and reciprocal hreflang links only for language versions that exist. Add its URL to `sitemap.xml`, including matching `xhtml:link` alternates. Add a language switcher link only when its destination exists. Each language switcher preserves the current route. Uzbek and Russian text is marked `data-review="needs-native-review"` for native-speaker proofreading.

## Replace placeholders

Replace the marked sample passages listed in `SAMPLE_CONTENT.md` before announcing the site. Add a portrait only when a real photograph is supplied. The empty `data-contact-email` attribute is a configuration placeholder; add a contact link only after a public email is provided. Do not add personal details, project metrics, achievements, or education claims that have not been confirmed.

## Page and placeholder workflow

Every English page uses a trailing-slash route backed by `<slug>/index.html`. To add a page, copy the structure and shared navigation from an existing inner page, then set its unique title, description, canonical, breadcrumb and structured data. Add substantive, indexable pages to `sitemap.xml`; keep empty states marked `noindex` and out of the sitemap until real content is published. The current `/journal/` and `/gallery/` pages are intentionally noindex. Replace marked sample prose only after Azizbek reviews it; retain placeholder tiles until real photographs or project screenshots are provided. The JSON files in `data/` remain the factual reference for education, projects and timeline copy; update the matching page HTML at the same time.

## Planned phases

1. Phase 1 static English homepage and production foundation.
2. English inner pages (completed).
3. Uzbek and Russian versions plus Phase 3 UX and sample content (completed; native review remains).
4. Local-only `/admin/` content prototype with JSON export/import (completed).
5. Final SEO, accessibility, performance and deployment QA (not started).

## Replace sample content before announcing the site

- [ ] Review every `data-sample="true"` block with `grep -R 'data-sample' .` or open any page with `?samples=1`.
- [ ] Replace draft descriptions, role/technology assumptions, and personal reflections with Azizbek-confirmed wording in English, Uzbek, and Russian.
- [ ] Confirm the employment center name and dates only if Azizbek wants them public; the current text does not name an employer.
- [ ] Confirm the project roles, technologies, and descriptions before presenting them as final.
- [ ] Keep Journal and Gallery `noindex` and out of `sitemap.xml` until real articles and photographs are ready.
- [ ] Arrange native-speaker review of all Uzbek and Russian blocks marked `data-review="needs-native-review"`.

`SAMPLE_CONTENT.md` lists every route carrying draft copy and its current marker count. The sample outline is a visual owner tool only; it does not change what is published.

## Admin workspace

`/admin/` is a local content-preparation prototype, not a protected publishing system. GitHub Pages serves every repository file publicly. The interface has no authentication, and `robots.txt` is public guidance rather than access control; `noindex,nofollow` does not make a URL private. Never put secrets, credentials, private information, or confidential drafts in this repository.

Edits stay in the visitor's own browser using IndexedDB (with localStorage fallback). Browser data is not secure and does not sync between devices; browser storage can be cleared. Exports and imported files are ordinary JSON. The workspace does not change the live site. Public pages are hand-authored HTML for SEO, so use this workflow: edit locally → export JSON or copy an HTML snippet → paste approved content into the relevant repository page → commit and push. Export backups regularly and keep them outside the repository. Local content should be checked for private details before copying it into a public file.

The data format and seed record fields are documented in [data/README.md](data/README.md). Top-level admin exports use `schemaVersion: 1`, `exportedAt`, and plain arrays in `collections`; records carry `id`, `lang`, `status`, `translationGroup`, `createdAt`, and `updatedAt`. `/admin/selftest.html` runs local validation and storage assertions.
