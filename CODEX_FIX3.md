# CODEX — FIX ROUND 3: LINK ROWS (all pages, all languages) — bugs only

Read `CODEX_FIX1.md`, `CODEX_FIX2.md`, `CODEX_PHASE4.md` and your current code. **This round fixes ONE component family and makes it identical on every page in EN, UZ and RU.** No new features, no new phase. If `/admin/` (Phase 4) is already built, leave it alone.

## RULES

- **Do not run any browser, Playwright, Chrome, Firefox or server.** The owner tests at `http://localhost:8000`. Verify with static scripts and by reasoning from the CSS. Never mention browser limitations.
- Colors/mood stay. Do not redesign anything else.

---

## WHAT THE OWNER SEES (symptoms, from real screenshots at ~390px)

1. **Route-link rows** (`<nav class="soc route-links">` on the homepage, and the same pattern on inner pages): the text column collapses to ~85px wide. Titles break mid-word one fragment per line (`Expl / ore / Aziz / bek / Abb / oso / v's / time / line`), the caption wraps one word per line (`A / dated / accoun / t of`), the card becomes very tall, and the arrow chip floats in the middle-right with a big empty gap. This happens even in English because the titles are long.
2. **`<nav class="next-page affordance-list inner-content">` rows** ("Next: Future"): fine in **English** (short text), but broken in **Uzbek and Russian** on every page (longer text triggers the same collapse).
3. **Contact/social rows** (looks good): the **arrow chip is not at the right end** of the card — there is ~150px of empty space to its right. It must sit at the far right edge inside the card padding.
4. Rows are stacked with **no gap**, borders touching, and the first row touches the divider line above it.

## ROOT CAUSE (investigate and confirm in the code)

- The text block (`.row-copy`) is not told to take the remaining width. It sits in an `auto`/shrink-to-fit track while another track absorbs the free space, so the title and caption get squeezed. The `overflow-wrap:anywhere` that was requested in FIX2 makes this worse: it lets the column shrink to nearly zero, so words break into fragments. **Remove `overflow-wrap:anywhere` and any `word-break:break-all/break-word` from these components.**
- The chip (the `::after` arrow, or an element) is positioned by a grid track that includes extra empty space on its right.
- UZ/RU: also check whether those pages have **different markup, class names, CSS files or CSS rules** than EN for these components (e.g. language-specific selectors like `html[lang="uz"]`, an older generated template, different class names, a different stylesheet link). Explain what you find.

---

## THE FIX — use ONE shared component, flex-based (tested, works at 320px and 390px in EN/UZ/RU)

Replace the current layout rules for **all** of these selectors with the block below, merged into the shared components CSS (keep your existing arrow glyph/gradient styling; adapt selectors to your real class names; delete the old conflicting rules rather than overriding them):

Selectors it must cover: `.soc > a`, `.route-links > a`, `.next-page > a`, `.affordance-list > a`, any contact/social rows, any other "link row" on any page (footer link groups excluded). If a row has an icon (social platforms), the icon is the first flex child.

```css
/* container: rows get a real gap, no borders touching, no divider collision */
.soc, .route-links, .next-page, .affordance-list { display:grid; gap:12px; margin:0; padding:0; border:0; }
.soc { padding-top:8px; }                 /* if a divider line sits above, keep clear space below it */

/* the row = flex: [icon?] [text takes ALL remaining width] [chip pinned to the right end] */
.soc > a, .route-links > a, .next-page > a, .affordance-list > a {
  display:flex; align-items:center; gap:16px;
  width:100%; min-width:0; min-height:72px; box-sizing:border-box;
  padding:16px 16px 16px 20px;
  border:1px solid rgba(255,255,255,.16); border-radius:22px;
  background:rgba(255,255,255,.05);
  color:var(--ink); text-decoration:none;
  -webkit-tap-highlight-color:transparent;
}

/* icon (social rows) */
.row-ico { flex:none; width:48px; height:48px; border-radius:50%; display:grid; place-items:center; }

/* text block: fills remaining width, can shrink, never collapses */
.row-copy { display:block; flex:1 1 0%; min-width:0; width:auto; max-width:none; }
.row-copy strong {
  display:block; color:var(--ink); font-weight:600;
  font-size:clamp(20px,5.6vw,30px); line-height:1.12; letter-spacing:-.02em;
  overflow-wrap:break-word;               /* NOT "anywhere" */
  hyphens:auto;                            /* needs correct <html lang> — it is set per language */
}
.row-copy small { display:block; margin-top:6px; font-size:13px; line-height:1.4; color:var(--mute); white-space:normal; overflow-wrap:break-word; }
.row-copy .row-action-label { font:11px/1.4 var(--mono); letter-spacing:.14em; text-transform:uppercase; color:var(--e3); }

/* arrow chip: own flex item, never absolute, always at the right end */
.soc > a::after, .route-links > a::after, .next-page > a::after, .affordance-list > a::after {
  content:"→"; flex:none; margin-left:auto;
  width:48px; height:48px; border-radius:50%;
  display:grid; place-items:center;
  background:var(--grad); color:#0a0a0a; font-size:22px; font-weight:700;
}
.soc > a[target="_blank"]::after { content:"↗"; }   /* external only */
```

Notes:
- If your chip is a real element or an SVG instead of `::after`, give it `flex:none; margin-left:auto; width:48px; height:48px`. The rule is: **no `position:absolute`, no grid tracks, no `justify-self` tricks for the chip.**
- Keep the press/hover/focus-visible animations you already have (scale, gradient wash, arrow nudge); just make sure they use `transform`/`opacity` and don't change the layout.
- Keep the internal → / external ↗ rule: internal rows use →, external (`target="_blank"`) use ↗. Currently some internal rows show ↗ — fix them.
- Shorten caption labels so they rarely wrap: internal `OPEN PAGE` (no `· Next: Timeline` suffix); external `OPEN ↗ GITHUB` etc. (this applies to all three languages; translate the label, don't append the destination).
- Desktop (≥1024px): rows get `max-width:880px`, title `font-size:clamp(22px,2.2vw,30px)`; chip stays pinned right.

---

## EXPAND TO EVERY PAGE (this is the main job — "every page perfect")

1. **List every link-row-like element** in all 27 HTML pages + `404.html`: route links, next-page rows, contact/social rows, project cards' link area, breadcrumb-adjacent rows, anything with an arrow chip. Give a table: page → selector → before (layout rule) → after.
2. **EN, UZ and RU must be structurally identical for these components.** Write a script that extracts, for each page, the normalized DOM structure of every `nav.soc`, `nav.route-links`, `nav.next-page`, `.affordance-list` (tag names + class names + attribute names, text removed) and asserts **UZ and RU equal their EN counterpart**. Print a pass/fail table for all 9 pages × 3 languages. Fix every mismatch **in the markup**, not with language-specific CSS.
3. **Delete any language-specific CSS** (`[lang=…]`, `.uz`, `.ru`) that touches these components. All three languages use the same CSS files via the same absolute paths (`/css/...`). Verify that every UZ/RU page links the same stylesheet set as EN with root-absolute paths and the same cache-busting query string (if any).
4. **Text-length stress test by reasoning/script:** for each row, take the longest title/caption among EN/UZ/RU and confirm the layout holds at 320px (content width = 320 − 2×20 page padding − 2px border − 36px padding − 16px gap − 48px chip = **~198px for text**). Titles must wrap on word boundaries (a word longer than 198px at the clamp size is the only case allowed to break; list any such word — for UZ/RU `hyphens:auto` should handle it).
5. **Contact/social rows:** same component; chip at the right end; handle fully visible; icon 48px round on the left. Check the footer's compact icon buttons and the menu overlay's social buttons use the same icon sprite and are unaffected.
6. **Static scan:** grep all CSS for `overflow-wrap:anywhere`, `word-break`, `position:absolute` inside link rows, `width`/`max-width` on `.row-copy`, `grid-template-columns` on link rows — each must be gone or justified.
7. Report: root cause (one paragraph), what differed between EN and UZ/RU (if anything), the tables from steps 1 and 2, the scan from step 6.

---

## SOCIAL LOGOS — must appear on EVERY page, in EVERY language (part of this round)

Everything in this fix round applies to **all 27 pages + `404.html`** (EN, UZ, RU). The social logos are part of it.

**Where logos must appear (identical on every page and language):**
1. **Footer:** four round icon buttons (44px, `1px` border, 20–22px glyph) for GitHub, LinkedIn, Telegram, Instagram, plus the copyright line. These are compact icon buttons, **not** link-rows (exclude them from the link-row CSS above).
2. **Contact section** (homepage and any page that has it): the four rows from the shared link-row component, each with the platform logo in a 48px round icon on the left (`.row-ico`), name + full handle in the text block, `↗` chip at the right end.
3. **Full-screen menu overlay:** bottom bar with the same four icon buttons.
4. **404 page:** same footer.
5. Optional: About page. Do not add logos anywhere else.

**Implementation (must be the same on all pages):**
- One sprite file `/assets/icons/sprite.svg` with `<symbol id="github">`, `#linkedin`, `#telegram`, `#instagram` (each with its own `viewBox`, `fill="currentColor"`, no hard-coded colors). Reference everywhere as `<svg class="ico" aria-hidden="true" focusable="false"><use href="/assets/icons/sprite.svg#github"></use></svg>` — root-absolute path, so it works from `/`, `/about/`, `/uz/about/`, `/ru/about/` and `404.html` alike. **No page may depend on an inline sprite that exists only in the homepage HTML.**
- **Redraw the LinkedIn glyph:** in the owner's screenshot the contact-row LinkedIn icon reads like "inl" (the "in" mark is malformed). Use the standard LinkedIn "in" mark (a clean "in" inside the usual rounded-square, or a clean "in" glyph) so it is instantly recognisable. Check that GitHub, Telegram and Instagram glyphs are also clean and consistent in stroke weight/size.
- Icon buttons: `<a class="soc-btn" href="https://github.com/azbea" target="_blank" rel="noopener noreferrer" aria-label="GitHub — opens in a new tab">…svg…</a>` (translate the aria-label per language: "GitHub — yangi oynada ochiladi", "GitHub — откроется в новой вкладке", etc.). Exact URLs only: `https://github.com/azbea`, `https://linkedin.com/in/a-abbosov`, `https://t.me/azbe_plt`, `https://instagram.com/azbe.plt`.
- Press/hover/focus-visible: ring/gradient fill with the glyph turning near-black, using `transform`/`opacity`/`background` only, reduced-motion safe.
- Switching language must never remove or change the logos: the footer, contact and menu markup is **identical across EN/UZ/RU** apart from translated text and `aria-label`s.

**Static check script (print a pass/fail table for all 27 pages + 404):**
- Footer contains exactly the 4 social links with the exact URLs above, `target="_blank"`, `rel="noopener noreferrer"`, an `aria-label`.
- Every `<use href="…#id">` points to an existing `<symbol id>` in `/assets/icons/sprite.svg`; the sprite file exists and is valid XML.
- Contact section (where present) has 4 rows, each with `.row-ico` containing the right symbol.
- Menu overlay has the 4 icon buttons.
- No page contains a `<symbol>` definition inline, and none uses a relative `href` to the sprite.
- UZ and RU footers/contact/menu structure equal the EN structure (normalized, text removed).

Add these results to the report.

**Then stop.** No other changes, no new phase, no browser.
