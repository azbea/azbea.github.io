# Phase 4 report — Parts 1–3

## Part 1 — Fixes

| Item | Finding | Fix |
|---|---|---|
| Language switcher | Active cells used a filled gradient, separators consumed width, and legacy styles could change visual state. | Removed separator spans from all 30 public documents; fixed three equal 38×44px cells in the header and menu. Active state changes only its color to ember; size, weight, padding and tracking stay the same. |
| Header width and wordmark | The fixed header needed a stable three-column layout and explicit space between the Latin name. | Kept the Latin wordmark in every language, added a fixed flex gap, and reserved columns for logo, 114px language switcher and 44px menu button. |
| Link rows and project cards | Several older rules positioned arrows independently of copy and did not give actions a consistent touch affordance. | Consolidated the shared link-row presentation in `css/fix1.css`: glass surface, separate copy/action grid tracks, 48px ember arrow chip, wrapping text and press/focus feedback. Project titles and arrows occupy separate footer columns. |
| Social rows | Handles could compete with arrows for horizontal space. | Set rows to icon / name-and-handle / arrow columns; handles wrap in the text column and remain visible at narrow widths. |
| External/internal direction | Arrow styles were inconsistent and footer arrows could cover icon content. | Internal action rows use `→`; external project/profile actions use `↗`. Footer arrows sit at the icon button corner; external anchors retain `noopener noreferrer` and accessible new-tab text. |
| Footer sprite | The same-origin sprite was already present in the public pages but needed to be verified across locales and 404 pages. | Confirmed every page’s icons resolve to the shared `assets/icons/sprite.svg` symbols; normalized the 404 menu profile rows. |
| Menu overlay | The overlay could center a tall menu and clip its lower controls on short screens. | Made it an opaque, top-aligned, vertically scrollable panel with safe-area bottom padding. Menu and page background use inert state; focus, Escape, and body scroll state are restored on close. |
| Text and padding | Long localized headings and tightly tracked display type could collide or exceed a narrow column. | Applied `overflow-wrap:anywhere`, explicit mobile side padding and less aggressive display tracking with optical sizing disabled for large headings. Desktop maxima now match the requested reduced scale. |
| Decoration and motion | Legacy selectors contained duplicate transitions and `!important` declarations. | Kept a global no-decoration rule, the prose-link ember underline, removed obsolete duplicate Phase 3 interaction rules, and removed unnecessary `!important` declarations. Reduced-motion behavior remains in shared styles and motion scripts. |

**Corrected header arithmetic** (border-box): viewport 320px → pill 312px → inner grid 297px → logo track 131px; 360px → 352px → 337px → 171px; 390px → 382px → 367px → 201px; 430px → 422px → 407px → 241px. The 297px grid at 320px subtracts two 1px borders and 13px horizontal padding from the pill, then reserves two 4px gaps, 114px for languages and 44px for the menu. All language cells are 38×44px, exceeding the 36px minimum while keeping equal dimensions.

The design lock’s other FIX1 checks were applied to the shared component styles, not page-specific patches. `CODEX_FIX2.md` is absent from this workspace, so its additional, unavailable requirements could not be read or verified.

## Part 2 — Audit and bug log

| File(s) | Finding | Fix / result |
|---|---|---|
| `css/components.css`, `css/fix1.css` | Older Phase 3 link-row, social and footer overrides duplicated the newer layout and created conflicting arrows. | Removed the old interaction block; retained one shared row implementation and explicit utility styles. |
| `css/global.css`, `css/fix1.css` | Grain covered four viewports’ worth of area; layered z-index values were undocumented; mobile card blur/shadows were heavy. | Grain is limited to the viewport at lower opacity; a documented layer scale now covers canvas, atmosphere, content, grain, header, overlay and toast; mobile card effects are reduced. |
| `css/fix1.css`, `css/menu.css` | Narrow text could wrap into arrows, and the menu’s lower controls could be clipped. | Grid tracks reserve arrow space; headings and handles wrap; overlay scrolls and keeps bottom safe-area padding. |
| `css/components.css`, `css/pages.css`, `css/inner.css` | Absolute decoration required review for text collisions. | Background orbs/rings sit behind hero content; card glow is clipped by its card; timeline line/nodes use a separate gutter; chapter counter is noninteractive; stage label/count and cards have separate stacking. Link arrows no longer use absolute positioning. |
| `js/menu.js` | Scroll locking discarded prior body styles; page/header remained reachable behind the open menu. | Saves/restores scroll styles and focus, makes main/header inert, traps Tab, closes on Escape, and restores the trigger focus. |
| `js/main.js` | The previous affordance observer remained after the corresponding animation styles became redundant. | Removed the unused observer; reveal behavior and sample outlining remain. |
| 27 public pages + 3 404 pages | Skip targets were missing; 404 menus used a different profile-row structure and localized 404 actions led to English. | Added localized visible-on-focus skip links and `main-content` targets; matched menu link/profile structure and localized 404 destinations. |
| `SAMPLE_CONTENT.md` | Counts were maintained manually. | Regenerated inventory from current `data-sample="true"` markers: 123 total (41 per language). |
| `robots.txt`, `sitemap.xml` | Admin needed exclusion controls. | Added `Disallow: /admin/`; sitemap remains 21 indexable localized routes and contains no admin URL. |

### Absolute/fixed positioning review

| Element | Safety reason |
|---|---|
| Fixed public header | Top-centered, width capped at 560px, with 44px menu control; hero top padding leaves room below it. |
| Fixed canvas, vignette and grain | Decorative full-viewport layers with pointer events disabled and documented stacking; content remains above them. |
| Hero orb and rings | Centered decorative layers behind the hero content; bounded by the hero’s clipped box. |
| Sticky-stage label and chapter count | Label occupies the top inset; counter is bottom-right, noninteractive and below chapter cards. |
| Journey cards | Positioned inside the `100svh` sticky stage and transformed by the scroll controller; card copy is contained and cards are not links. |
| Timeline line and nodes | Draw in the dedicated left gutter outside the timeline text column. |
| Project glow | Pseudo-element is clipped to the project card and paints behind its content. |
| Menu close control | Fixed to the overlay’s top corner; overlay content begins below it and can scroll. |
| New-tab helper text | Clipped to a 1px visually-hidden box while remaining available to assistive technology. |
| Skip link | Fixed above the page while focused; otherwise positioned offscreen. |
| Footer external arrow | Confined to the outer corner of a 44px icon button; does not cover a text label. |
| Admin sidebar/scrim/toast | Sidebar width is reserved on desktop and becomes a drawer on mobile; scrim intentionally dims the workspace; toast stays in a viewport-bounded bottom corner. |

The public muted token `#8b8a93` on `#050507` computes to a 5.97:1 contrast ratio. At 320px the header has a 131px logo track; at 430px it has 241px. Localized headings use wrapping, and cards/rows reserve a separate 48px arrow track. Desktop type caps are 170px hero, 120px inner hero, 96px section headings, 120px journey year, 40px journey title, 150px counter, 64px statement, 40px marquee, 34px project title and 32px social-row title.

### Static audit results

`python3 scripts/static-audit.py` passed:

- 27 localized content routes plus 3 404 documents audited.
- 633 internal anchor references resolve; local stylesheets, scripts, fonts, icons and images resolve.
- Header, menu and footer normalized-structure comparisons pass across EN/UZ/RU and 404 shells.
- All 27 content pages have complete reciprocal EN/UZ/RU/x-default hreflang and parseable JSON-LD (27 blocks); titles and descriptions are unique.
- 348 sprite references resolve to the four shared symbols: GitHub, LinkedIn, Telegram and Instagram.
- 21 sitemap routes resolve to files; journal/gallery remain excluded and admin is absent.
- One H1, landmarks, skip target, IDs, image alt/dimensions/loading, localized link prefixes, external `rel`, native-review markers and sample totals passed the static checks.
- Admin noindex metadata, robots disallow and public-page/sitemap exclusion passed.
- `node --check` passed for each JavaScript file. JSON seed files parse; `sitemap.xml` parses with REXML.
- Header geometry at 320/360/390/430px is calculated above; long localized headings wrap rather than expand the grid.

## Part 3 — Admin prototype

Created `/admin/` as a public, local-only content workspace with no password screen or access-control claim. Its UI states that edits do not update the live site, browser storage is local and not secure/synchronized, and the public pages must be updated and committed separately.

- Built dashboard, biography, timeline, education, projects, journal, gallery, translations, SEO, settings and sample-tracker modules.
- IndexedDB uses schema version 1 and per-module collections; localStorage is the fallback. Records carry IDs, language/status/translation group and timestamps. Existing project, education and timeline JSON seed the store; file-open failure uses a small embedded seed and a notice.
- Added debounced local drafts, explicit saves, per-module and whole-site JSON export, validated import preview with merge/replace, typed replace confirmation, beforeunload warning, 10 recovery snapshots, confirmed delete with an 8-second undo, snippet export, local image compression/download, and storage controls.
- Preview content uses a whitelist sanitizer. Imported records are checked for schema version, supported values, lengths, language and HTTPS URLs. KAU/TSUE completion, gallery alt text, slug uniqueness and SEO limits have explicit validation.
- The sample tracker scans all 27 localized routes with same-origin `fetch`, totals marker counts and explains its localhost requirement for `file://` use.
- Added `/admin/selftest.html` for storage CRUD, export/import, schema rejection, HTTPS validation, Uzbek/Russian transliteration, sanitizer and translation-matrix checks.

Files added for Phase 4 include 20 files under `admin/`, `data/README.md`, and `scripts/static-audit.py`; `README.md`, `SAMPLE_CONTENT.md`, public styles/scripts/HTML and `robots.txt` were updated. `CNAME` still contains only `abbosov.com` plus its trailing newline.

## Open items

`CODEX_FIX2.md` was referenced but is not present. The workspace also has no `.git` directory, so there is no Git status/diff available here. This work stopped after Phase 4; no Phase 5 tasks were started. Verification was static only.
