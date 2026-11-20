# CODEX — FIX ROUND 1 (bugs only — NO new phase, NO new features)

Read `CODEX_PROMPT.md`, `CODEX_PHASE2.md`, `CODEX_PHASE3.md` and your current code. This round **only fixes the bugs below** on **all 27 pages (EN, UZ, RU)**. Do not build `/admin/`. Do not add features. Do not start another phase.

## RULES FOR THIS ROUND

- **Do NOT try to run a real browser, Playwright, Chrome, Firefox, or bind a local server.** The owner already tests on `http://localhost:8000` himself. Do not mention browser verification as a limitation. Verify with **static scripts only** (grep/HTML parsing/CSS rule checks) and say plainly what you checked.
- The design system (colors, mood, 3D starfield, glass surfaces, typography) stays. Layout/components may change as needed to fix the bugs properly.
- Fix the **root cause in the shared CSS/markup**, then confirm it is applied identically on every page and language. No page-by-page patches that leave other pages broken.

---

## BUG 1 — Remove text decoration everywhere (except inside paragraph text)

- No underline/text-decoration on **any** link or button: nav pill, language switcher (EN · UZ · RU), menu overlay, buttons, link rows, cards, breadcrumbs, footer, social links, 404 page.
- Add a global rule: `a, a:hover, a:focus, a:active, a:visited { text-decoration: none; }` and remove any other `text-decoration`/`border-bottom` underline hacks on non-prose links.
- The **only** allowed underline-style effect is for links **inside running paragraph text** (class `.prose a` or links within `<p>` body copy): a 2px ember-gradient underline. Everything else: none.
- Static check: grep all CSS for `text-decoration`, list every remaining occurrence, and justify each (should be only the prose-link rule).

## BUG 2 — Language switcher moves/jumps when the language changes

Cause to investigate and remove: different text widths per language, active state changing font-weight/letter-spacing/padding, the pill/menu layout depending on content width, or the logo/links changing width in UZ/RU.

Fix:
- Build the nav pill header as a **fixed three-part layout** (CSS grid): `logo | language switcher | menu button`, identical in all languages. The logo stays the same Latin text "AZIZBEK ABBOSOV" on every language version (no Cyrillic swap) so widths never change.
- Language switcher: three **equal-width, fixed-size cells** (`EN`, `UZ`, `RU`), monospace, same font-size/weight/letter-spacing in active and inactive states. The active language is shown only by a **filled pill/background** (ember gradient with dark text, or white-glass) — **no change in size, padding, weight, or width** between states. Use `box-sizing: border-box` and reserve the same border width on all cells (transparent border on inactive).
- The nav pill keeps the same width and horizontal position on all pages and languages. Same for the language switcher inside the full-screen menu.
- Static check: compare the header HTML across all 27 pages — structure and class names must be identical except `href`s and the active/`aria-current` markers. Report any difference.

## BUG 3 — Link rows/cards don't look like buttons, and arrows cover the text

Two problems: (a) nobody can tell these are tappable; (b) the round arrow button is positioned **on top of** the text (absolute positioning), hiding titles/usernames. This affects: the homepage "journey" link rows, the "Next: …" rows, contextual link rows (Timeline / Education / Experience / Future), project cards, social/contact rows, and any similar element on inner pages.

Fix — redesign **one shared "link-row / link-card" component** and use it everywhere:

1. **Layout:** CSS grid or flexbox, **never absolute positioning for the arrow.** Columns: `[icon (optional)] [text block: title + small caption] [arrow chip]`. The text block has `min-width: 0` and wraps (or truncates with ellipsis only for long handles) — the arrow chip lives in its **own column** and can never overlap text. Reserve space for it (`grid-template-columns: auto 1fr auto`).
2. **Obviously a button:** each row/card is a **bordered, rounded (20–24px) surface** with a visible glass background (`rgba(255,255,255,.05)`), a brighter 1px border (`rgba(255,255,255,.16)`), generous padding (≥ 18px, min-height ≥ 68px on mobile), and the **arrow chip filled with the ember gradient by default** (48px circle, near-black arrow) — not only on hover/press. This high-contrast chip is what tells people "tap me". Add a small mono caption on the row (e.g. "OPEN PAGE" for internal, "OPEN ↗ GITHUB" style for external) so purpose is explicit.
3. **Press feedback** (keep from Phase 3, but fix): on touch-down scale ~0.985, gradient wash sweeps across, chip scales up slightly/arrow nudges; smooth release. Also hover/focus-visible on desktop. Reduced-motion: no movement, only color change.
4. **Internal vs external:** internal → `→`, external → `↗` + `target="_blank" rel="noopener noreferrer"` + visually hidden "(opens in a new tab)".
5. **Project cards (`.pc`):** the arrow must not sit over the project name (e.g. "ShokMarket.uz", "FaslMarket.uz"). Put the title row and the arrow chip in a footer row (title left, chip right, in separate grid columns), allow long titles to wrap to two lines on narrow screens.
6. **Rule for the whole site:** no decorative element (arrow, glow, chip, badge) may overlap readable text. Audit all `position:absolute/fixed` elements in the CSS, list each one, and confirm none covers text at 320–430px and at desktop widths (reason it through from the CSS: sizes, paddings, wrapping).
7. Non-link elements (info cards, chips, labels) must stay visually different: no arrow chip, no gradient chip, no hover/press effect.

## BUG 4 — Contact / social rows: arrows block the usernames

Use the same component as Bug 3: `[platform logo in round glass icon] [platform name + @handle (wraps/ellipsis-safe)] [arrow chip ↗]`. The handle (`@azbea`, `a-abbosov`, `@azbe_plt`, `@azbe.plt`) must be fully visible at 320px. Handle goes under the platform name in small mono text (not on the far right), so nothing competes for space.

## BUG 5 — Social logos missing in the footer on inner pages and on UZ/RU pages

Cause (verify): the SVG sprite with the icon `<symbol>`s exists only in the homepage HTML, so `<use href="#github">` fails everywhere else; and/or the footer markup differs per page.

Fix:
- Move the sprite into one file: `assets/icons/sprite.svg` and reference it identically on every page: `<svg aria-hidden="true"><use href="/assets/icons/sprite.svg#github"></use></svg>` (same-origin external `<use>` works).
- Make the **footer identical on all 27 pages** (only text language, internal links' language prefix and `aria-current` differ): four icon buttons (GitHub, LinkedIn, Telegram, Instagram) with accessible names, plus the copyright line. Same for the contact section, the menu overlay and the 404 page.
- Static check script: for every HTML page assert (a) the footer contains exactly the four social links with the correct URLs, (b) every `<use href>` points to an existing `#id` inside `assets/icons/sprite.svg`, (c) no page still depends on an inline sprite that exists only on the homepage. Print a pass/fail table of all 27 pages.

## BUG 6 — Make some text smaller on desktop (≥ 1024px)

Mobile sizes stay as they are. On desktop the oversized type should be reduced by roughly 25–35%. Adjust the `clamp()` maxima (not the mobile minimums), e.g.:
- Hero H1: max ≈ 170px (was 260px). Inner-page H1: max ≈ 120px.
- Section H2 ("Things I've built", "Let's talk", etc.): max ≈ 96px (was 170px).
- Journey card year: max ≈ 120px; card title max ≈ 40px; chapter counter max ≈ 150px.
- Big statement paragraph: max ≈ 64px (was 96px). Marquee: max ≈ 40px.
- Project card titles: max ≈ 34px; social/link row titles: max ≈ 32px.
- Keep generous whitespace; desktop content max-width stays comfortable (≈ 1200px).
Verify UZ/RU headings (longer words, Cyrillic) still don't overflow at 320–430px and at 1024–1920px.

---

## DELIVERABLES

1. All fixes applied in the shared CSS/JS/markup and propagated to all 27 pages.
2. A short **static audit report** (tables): underline rules left; header-structure diff across pages; list of `position:absolute/fixed` elements and why each is safe; footer/sprite pass-fail table for all 27 pages; new desktop type sizes.
3. A one-paragraph summary of what changed visually in the link-row/button design.

**Then stop.** Do not start any further phase and do not attempt browser verification.
