# CODEX — ROUND 3: FIX EVERYTHING → FULL AUDIT → PHASE 4 (/admin/)

Do the parts **in order**. Do not skip Part 1 or 2 to get to Part 3. Read first: `CODEX_PROMPT.md`, `CODEX_PHASE2.md`, `CODEX_PHASE3.md`, `CODEX_FIX1.md`, `CODEX_FIX2.md`, `SAMPLE_CONTENT.md` and **all of your current code**.

## GLOBAL RULES

- **Do NOT try to run any browser, Playwright, Chrome, Firefox, or local server. Never mention browser verification as a limitation.** The owner tests on `http://localhost:8000` himself. Verify with static scripts, CSS/HTML analysis and careful reasoning from the CSS (compute real widths at 320/360/390/430px), and say exactly what you checked.
- Colors/mood stay (dark, ember gradient, off-white, starfield, 3D motion). Layout/components can change if needed to fix problems.
- Public site stays plain HTML/CSS/vanilla JS, no external requests, no build step.

---

## PART 1 — FIXES (execute now)

### 1A. Execute everything in `CODEX_FIX1.md` and `CODEX_FIX2.md` that is not done or not fully correct, with ONE AMENDMENT (overrides both files):

**Language switcher (nav pill AND menu overlay): no circle, no filled background.**
- Remove the circled/filled gradient background from the active language. The **active language is shown only by coloring its text** with the ember color (use the gradient text `background-clip:text` or solid `#ff9a3d`), and slightly brighter weight is NOT allowed (no weight change). Inactive languages are muted text (`--mute`) and become `--ink` on hover/press.
- All three items keep **identical size, padding, font, letter-spacing** so nothing moves when the language changes. Each is a fixed-width cell (~38×36px, ≥ 36px tall hit area, extended to 44px tap area with padding/pseudo-element if needed). No dots/separators between them. No text-decoration.
- The nav pill must still fit at 320px (show the width arithmetic).

### 1B. Re-verify the bugs listed in FIX1/FIX2 against the **current** code and fix any that are still present: text-decoration; language switcher shifting; nav pill overflow and clipped logo/menu button and missing space between "AZIZBEK" and "ABBOSOV"; hero/section left padding; overlapping letters (Inter optical size/letter-spacing); link-row grid, wrapping and arrow overlap; internal links using → and external using ↗; social rows (logo + name + full handle + arrow, no overlap); footer social logos on **all** pages/languages via the shared sprite file; menu overlay opaque, not clipped, scrollable, bottom bar visible; smaller desktop typography.

---

## PART 2 — FULL AUDIT OF EVERY PAGE AND EVERY CSS FILE

Go through **all 27 HTML pages, `404.html`, and every CSS and JS file, line by line.** Fix everything you find. Report findings in a table (file → problem → fix). Check at least:

**CSS**
1. Every rule: remove dead/duplicate/conflicting rules, `!important` abuse, rules overridden later, unused selectors. Consolidate into the structure from the earlier prompts (`variables, reset, global, components, pages, menu`). One source of truth per component.
2. Overflow safety: find every element that can exceed `100vw` at 320–430px (fixed widths in px, `vw` widths, large transforms, absolute offsets, wide grids, long unbroken words like emails/URLs/handles, Cyrillic words, `white-space:nowrap`). Contain or wrap each.
3. Every `position:absolute/fixed` element: confirm it cannot cover readable text.
4. Touch targets ≥ 44px for all interactive elements; focus-visible styles exist for all; reduced-motion handled for every animation/transition; no `cursor:pointer` on non-links; no hover-only information.
5. z-index scale: define a small documented scale (canvas, content, header, overlay, toasts) and remove arbitrary values.
6. Fluid type: each `clamp()` has sane min/max; desktop sizes reduced as specified before; verify longest UZ/RU strings per heading class still fit at 320px.
7. Contrast: text/background pairs meet WCAG AA (muted text `#8b8a93` on `#050507` for body-size text; fix where it fails).
8. Performance: no expensive CSS (huge blur radii, many stacked backdrop-filters, large box-shadows on many elements) applied to mobile; keep visuals but lighten the heavy cases on small screens.

**HTML (every page, every language)**
1. One `<h1>`, no skipped heading levels, landmarks (`header/nav/main/footer`), a visible "skip to content" link, `lang`, canonical, hreflang reciprocity, OG/Twitter, JSON-LD valid and factual, unique title/description.
2. All internal links resolve to existing files; correct language prefix per language; no `localhost` or absolute dev URLs; no broken `href="#"`; external links have `rel="noopener noreferrer"` and ↗; internal links use →.
3. No duplicate `id`s; labels/`aria-label`s present on icon-only controls; images have `alt` (decorative → `alt=""`/`aria-hidden`), `width`/`height`, lazy loading where appropriate.
4. Header, menu overlay and footer markup **identical across all pages** except language strings, link prefixes and `aria-current`. Write a script that diffs the normalized structure and fails on any mismatch.
5. UZ/RU pages: no untranslated English leftover (except names, tech terms, URLs); `data-review="needs-native-review"` present; `data-sample` markers consistent with `SAMPLE_CONTENT.md` (regenerate that file).
6. The 404 page uses the same shell and works from any depth (root-absolute asset URLs).

**JS**
1. Syntax-check every file (`node --check` if Node exists, otherwise static reading), remove dead code, ensure every `querySelector` target exists on every page that loads the script (guard nulls so a missing element never throws), event listeners cleaned/passive where appropriate, `requestAnimationFrame` loop paused when hidden/off-screen, no memory leaks, no layout thrash.
2. Menu: focus trap, Esc, `inert` on background, scroll lock restore, works with the language switcher and links inside.

Deliver a **bug log** (what was wrong, where, how fixed) and the results of the static scripts (header/footer diff, link crawl, hreflang matrix, sprite check, JSON-LD parse, sitemap vs files).

---

## PART 3 — PHASE 4: `/admin/` LOCAL CONTENT-MANAGER PROTOTYPE

Build `/admin/` as a **static, local-only content-management prototype**. Remember: GitHub Pages is static and **everything in the repo is public**, so:

- **No fake security.** No password/login screen pretending to protect anything. State this clearly in the UI and README.
- Never store secrets, credentials, private data or confidential drafts in the repo. The admin only stores data in the **visitor's own browser** (IndexedDB/localStorage) and exports/imports JSON files.
- `/admin/` must be `noindex,nofollow` (meta + `X-Robots`-style meta), `Disallow: /admin/` in `robots.txt`, **excluded from `sitemap.xml`**, and **not linked from any public page, menu, footer or sitemap**. (Mention in the README that `robots.txt` is public and `noindex` is not access control.)
- Do not claim edits change the live website. Do not claim localStorage syncs across devices or is secure.

### 3.1 Design

Different from the public site, as the master prompt says: **light neutral background** (`#f4f3f0`-ish), **dark sidebar** (`#0e0e11`) with small ember accents, white minimal cards (radius ≤ 14px, subtle borders, almost no shadows), clean Inter typography (reuse the self-hosted fonts), clear status chips (Draft / Published / Needs review / Sample), professional tables and forms. **Excellent on mobile**: the sidebar becomes a slide-in drawer, tables become stacked cards, all controls ≥ 44px, editors usable one-handed. Accessible (labels, focus rings, keyboard, `aria-live` for toasts). No starfield, no 3D effects here.

### 3.2 Architecture (no build tools)

```
admin/index.html            single page, hash routing (#/dashboard, #/timeline …)
admin/selftest.html         in-browser self-tests the owner can open at /admin/selftest.html
admin/css/admin.css
admin/js/app.js  router.js  store.js  ui.js  validate.js  export.js
admin/js/modules/ dashboard.js biography.js timeline.js education.js projects.js journal.js gallery.js translations.js seo.js settings.js samples.js
data/*.json                 existing JSON files are the seed/source of truth for the schema
```

- `store.js`: IndexedDB (fallback localStorage) with a versioned schema (`schemaVersion`), collections per module, `createdAt/updatedAt`, `id`, `lang`, `status`, `translationGroup` (links EN/UZ/RU versions of the same item). **Keep the JSON structure backend-ready** (plain, flat, documented in `data/README.md`).
- Seed: on first run, load the existing `data/*.json` via `fetch` (works on `http://localhost:8000`); if `fetch` fails (opened as `file://`), fall back to a small embedded seed and show a notice. All counts/stats shown are **computed from real stored data — no fake statistics**.
- Image handling: no uploads to a server. Allow choosing an image file, downscale/compress in a canvas (max 1600px, WebP/JPEG), store as a Blob in IndexedDB for preview, and export the **filename + a "download image" action** so the owner can put the file into `assets/images/`. Warn about size.
- **Sanitization:** never inject user-entered or imported content with `innerHTML` unsanitized. Use `textContent`, or a small whitelist-based renderer for the preview (paragraphs, headings, bold/italic, links with `rel="noopener noreferrer"`, lists). Imported JSON is validated (schema version, field types, lengths, URL protocols `https:` only) before it replaces anything.

### 3.3 Modules (fields exactly as in the master prompt)

1. **Dashboard** — real counts: published pages (from the known route list), draft items, timeline entries, projects, gallery items, translation completion per language (EN/UZ/RU), last export date, **"Not exported yet" warning** when there are unsaved changes since the last export. Plus the **Sample-content tracker** (see `samples.js`) and a prominent "Local prototype — changes do not update the live site" banner with the 4-step workflow (edit → export JSON/HTML → copy into repo → commit & push).
2. **Biography manager** — chapters: Title, Slug, Language, Introduction, Main content (textarea with a small formatting toolbar + live preview), Cover image, Status (Draft/Published), Last updated.
3. **Timeline manager** — Event title, Description, Year, Optional exact date, Category, Image, Language, Visibility; **add, edit, drag-or-button reorder (up/down buttons work on touch), delete with confirmation**.
4. **Education manager** — Institution, Program, Location, Start year, End year or "Current", Description, Qualification status (Completed / In progress / Academic leave / Not completed), Supporting image. Show a warning when an entry is marked "Completed" for KAU/TSUE ("he is not a graduate").
5. **Projects manager** — Name, Description, Role, Technologies (chips), Status, Website URL, Repository URL, Image, Featured. URL validation (`https://` only).
6. **Journal manager** — Title, Slug (auto-generated from title with Latin transliteration for UZ/RU, editable, uniqueness check), Category, Excerpt, Content (editor + preview), Cover image, Language, SEO title, SEO description (live character counters: title ≤ 60, description ≤ 155), Draft/Published.
7. **Gallery manager** — Image, Caption, Date, Location (optional; show a hint "don't enter private/sensitive places"), Category, Alt text (required to publish), Visibility.
8. **Translation manager** — table of every translatable item with EN / UZ / RU cells: ✓ exists, ✗ missing, "needs review" (from `data-review`/status). Click a missing cell → creates a draft copy in that language linked by `translationGroup`. Side-by-side editor for EN ↔ UZ/RU.
9. **SEO manager** — per page/language: Page title, Meta description, Canonical URL (validated, must start with `https://abbosov.com/`), Social share image, Indexing preference (index/noindex), with a **SERP-style preview** and a checklist (unique, length, name present). Highlights duplicates.
10. **Settings** — site name, default language, public contact email (empty by default; **warn that anything entered and pushed is public**), social profile URLs (the 4 known), theme-color, "Reset local data" (typed confirmation), "Request persistent storage" (`navigator.storage.persist()`), storage usage estimate.
11. **Sample-content tracker (`samples.js`)** — scans all 27 routes (list embedded from the sitemap + noindex pages) with `fetch`, counts `data-sample` blocks per page/language, shows a table with "Open with ?samples=1" links and a total; fails gracefully on `file://` with a clear message. This is how the owner finds what still needs real text.

### 3.4 Persistence, export/import, safety

- Autosave drafts while typing (debounced); explicit **Save**; **Export all as JSON** (single file with `schemaVersion`, `exportedAt`, all collections) and **Export per module**; **Import JSON** with validation, a preview of changes (added/updated/removed counts) and a choice: *Merge* or *Replace* (typed confirmation for replace). Keep the last **10 automatic snapshots** in IndexedDB with one-click restore.
- Deleting always asks for confirmation (modal, keyboard accessible); offer **Undo** toast for 8 seconds.
- **"Copy HTML snippet"** buttons on biography, timeline, education, projects and journal items: generates ready-to-paste HTML that uses the public site's own component classes (same markup as the pages), so the owner can paste content into the static pages. Mention clearly that the public pages are hand-authored HTML (SEO), so JSON export alone does not change them.
- Warn before leaving the page with unexported changes (`beforeunload`).
- Keyboard shortcuts optional; no external libraries; no network requests except same-origin `fetch` for seed/sample scan.

### 3.5 Self-test page

`admin/selftest.html` runs in-browser assertions the owner can open at `/admin/selftest.html` (no libraries): store create/read/update/delete round-trip, export → import round-trip equality, schema validation rejects bad JSON, URL validator, slug generator (UZ/RU transliteration), HTML sanitizer strips `<script>`/`onerror`, translation matrix computation. Show a green/red list on the page.

### 3.6 Docs

Update `README.md` with an **Admin** section: purpose, limits (public, not secure, local-only), the edit → export → paste → push workflow, how to back up (export regularly; browser storage can be cleared), schema documentation, and "never put private data in the repo". Add `data/README.md` describing every JSON schema.

---

## FINAL REPORT (then stop)

1. Part 1: confirmation list of every FIX1/FIX2 item + the language-switcher change, with the nav-width arithmetic at 320/360/390px.
2. Part 2: the audit table (file → problem → fix) and static-script results (diff/links/hreflang/sprite/JSON-LD/sitemap/overflow list).
3. Part 3: modules built, storage design, how the sample tracker works, the self-test list, files added.
4. Anything you were unsure about.

**Do not start Phase 5. Do not attempt browser verification.**
