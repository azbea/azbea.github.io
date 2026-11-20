# CODEX PROMPT — abbosov.com (Official Website of Azizbek Abbosov)

You are a senior frontend engineer, motion designer and technical-SEO specialist. Build the official personal website of **Azizbek Abbosov** as a static site (plain HTML + CSS + vanilla JS) for GitHub Pages.

Three non-negotiables, in this order:

1. **SEO for the name "Azizbek Abbosov"** — the site must become the authoritative result for his name.
2. **Mobile-first.** About 90% of visitors are on phones. Mobile is designed and tested first; desktop is the adaptation.
3. **Pixel-faithful design.** The visual design is already approved and LOCKED (section 2).

---

## 0. FILES YOU MUST READ FIRST

- `design-reference/index.html` — the approved design (a working single-file prototype). It is the **single source of truth** for look, layout, typography, colors, spacing, copy style and all animation behavior.
- `MASTER_PROJECT_PROMPT.md` — the full project brief (facts about the person, content rules, SEO rules, admin plans, translations). Read it fully.

If this prompt and the master prompt conflict, **this prompt wins** (the design lock, URL structure and phase plan are decided here).

---

## 1. PROJECT FACTS

- Domain: https://abbosov.com — GitHub Pages, repo `azbea/azbea.github.io`, `main` branch, repo root. Spaceship DNS is already set. **Do not touch DNS.** Create a `CNAME` file containing exactly `abbosov.com` and add `.nojekyll`.
- Stack: **HTML5, CSS3, vanilla JavaScript only.** No frameworks, no TypeScript, no Node backend, no database, no PHP, no build step, no npm dependencies shipped to the site, no CDN-loaded libraries, no external requests at runtime (self-host fonts).
- Work from scratch in an empty repo. Do not delete anything that already exists without explaining why.

---

## 2. DESIGN LOCK — REPRODUCE `design-reference/index.html` EXACTLY

The owner loved this design and wants it **exactly**: no restyling, no "improvements", no changed colors, no changed type scale, no extra decoration, no changed animation feel. Your job is to turn it into a production, multi-page, multi-language, SEO-ready site while it looks and moves **identically**.

### 2.1 Design tokens (copy exactly)

```
--bg:#050507; --bg2:#0b0b10; --ink:#f3efe9; --mute:#8b8a93; --line:rgba(255,255,255,.09);
--e1:#ff4d1c; --e2:#ff9a3d; --e3:#ffd27a;
--grad:linear-gradient(100deg,var(--e1),var(--e2) 55%,var(--e3));
Display font: Inter Display (Inter with optical size) — weights 600/700/800, tight negative letter-spacing (-.035em to -.06em), uppercase for hero/section titles.
Body font: Inter.
Mono labels: monospace, 10–11px, letter-spacing .15–.22em, uppercase, color var(--mute).
```

Fonts: **self-host** woff2 files in `assets/fonts/` (Inter variable incl. optical-size axis so large headings match the "Inter Display" look from the reference; one monospace). `font-display:swap`, preload the critical files, **no Google Fonts requests**. The metrics must match the reference so layouts don't shift.

### 2.2 Elements and behaviors that must be preserved

- **Fixed starfield canvas** behind everything: perspective 3D star tunnel; ~22% of stars are ember-colored; stars stretch into streaks proportional to scroll velocity; smoothed (lerp) scroll; vignette overlay; film-grain overlay.
- **Floating glass navigation pill** (top, centered, blurred, rounded): logo "AZIZBEK ABBOSOV" (second word in ember gradient), `EN · UZ · RU` switcher, round off-white menu button.
- **Hero:** tag pill "Official website", giant two-line H1 (`AZIZBEK` in --ink, `ABBOSOV` in the ember gradient with glow), lead paragraph, two pill buttons, scroll hint. Glowing orb + three tilted 3D rings behind the name. On scroll: the hero block moves back in Z, rotates on X, fades; the orb scales and drifts; the rings rotate at different speeds.
- **Marquee strip** with outlined words and ember ✦ separators; shifts horizontally with scroll.
- **3D journey tunnel:** a tall scroll section (~560vh) with a sticky stage; glass cards fly toward the viewer along Z as you scroll (translate3d + rotateX/Y, opacity and blur falloff), with the "dwell" easing so each card rests sharp before the next arrives; giant outlined chapter counter `01…05` bottom-right.
- **Project cards** with ember glow orb, tilt-in 3D reveal on scroll, round arrow button.
- **Language pills**, the big statement paragraph with gradient emphasis, **Contact** section with huge "Let's talk" and the large social link rows, footer.
- Exact copy of the homepage sections as in the reference (hero text, journey cards, project cards, languages, statement, contact). Only change copy where section 5 or 6 requires it (translations, link targets, real hrefs).

### 2.3 Performance rules (implementation may change, appearance must not)

The look stays identical; make the **implementation** efficient for mid-range phones:

- Cap canvas DPR at 2 (1.5 on small/low-power screens), fewer stars on mobile (reference already uses ~520 on narrow screens), pause the animation loop when the tab is hidden (`visibilitychange`) and when the canvas is fully covered.
- Only animate `transform` and `opacity` in rAF; avoid layout reads/writes interleaved per frame (batch reads, then writes). Use `will-change` sparingly.
- `backdrop-filter` and the per-card `filter: blur()` are expensive: keep them visually identical but reduce blur radius/steps on mobile if needed to hold 60fps. Never change the look noticeably.
- One shared `main.js` (+ small per-feature modules), `defer` loaded, no inline blocking scripts. CSS split per `css/` files, critical hero CSS inlined in `<head>` if it helps LCP.
- **`prefers-reduced-motion`:** render the starfield static, disable scroll-driven 3D, show journey cards as a normal vertical stack, no marquee movement.
- **No-JS / crawler fallback:** all text content (including all journey cards) must exist in the HTML and be readable without JavaScript. The 3D motion is an enhancement only. With JS off, the tunnel degrades to a stacked list of cards.
- Targets (mobile, Lighthouse): Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95, SEO 100. LCP < 2.5s, CLS < 0.05, INP < 200ms.

### 2.4 Mobile specifics (crucial)

- Design and verify at **320, 360, 375, 390, 414, 430** first; then 768, 1024, 1280, 1440, 1920. Stress-test **360, 375, 390, 414**.
- No horizontal scroll at any width. Hero name must fit on 320px without clipping (reference uses `clamp(56px, 18.4vw, 260px)`).
- Touch targets ≥ 44px. Buttons stack on narrow screens as in the reference.
- Use `100svh` units (not `100vh`) so mobile browser toolbars don't break the hero and the sticky tunnel stage.
- Menu: full-screen overlay opened by the round menu button — same visual language (near-black, huge Inter Display links stacked, ember-gradient on active/hover, mono labels, language switcher, social links at the bottom). One-handed reachable. Focus trap, `Esc` to close, `aria-expanded`, body scroll lock while open.

---

## 3. URL STRUCTURE & INTERNATIONALIZATION (DECIDED — differs from the master prompt)

To avoid duplicate-content between `/` and `/en/`, **English lives at the root.** No `/en/` folder.

```
/                      English homepage  (canonical, x-default)
/about/  /education/  /experience/  /developer/  /timeline/  /journal/  /gallery/  /future/
/uz/                   Uzbek homepage (Latin script)  + /uz/about/ … same set
/ru/                   Russian homepage               + /ru/about/ … same set
/admin/                later phase (local-only prototype)
```

- Every page has a real, separate HTML file per language (no JS-translated text).
- Each page: correct `<html lang>` (`en`, `uz`, `ru`), unique `<title>` and meta description in that language, self-referencing `<link rel="canonical">`, full `hreflang` set (`en`, `uz`, `ru`, `x-default` → English URL), `og:locale` and alternates.
- The language switcher links to the **same page in the other language** (e.g. `/about/` ⇄ `/uz/about/` ⇄ `/ru/about/`), never to the homepage. If a translation doesn't exist yet, don't output the link and don't output its hreflang.
- Use trailing-slash clean URLs (`/about/` = `about/index.html`). All internal links absolute-root-relative (`/about/`).
- Uzbek: natural modern Latin-script Uzbek. Russian: natural modern Russian. **Not word-for-word translations.** Mark every UZ/RU text block with a `data-review="needs-native-review"` attribute so the owner can proofread.

---

## 4. SEO — THE TOP PRIORITY

Goal: when people search "Azizbek Abbosov" (and variants: "Abbosov Azizbek", "Azizbek Abbosov official website / biography / education / projects / developer"), abbosov.com is the primary result. You cannot promise rankings; build the best possible foundation.

### 4.1 On-page

- Homepage `<title>`: `Azizbek Abbosov | Official Website`
- Homepage meta description: `Official website of Azizbek Abbosov, featuring his personal story, education, projects, experiences and ongoing journey.`
- **One `<h1>` per page.** Homepage H1 text is exactly `Azizbek Abbosov` (visually two lines as in the design — the H1 contains the real text "Azizbek Abbosov" in the markup, not an image or CSS content). The header logo is NOT an H1.
- Developer page title: `Azizbek Abbosov — Software Development & Projects`. Other pages: `<Page> — Azizbek Abbosov`. The name appears naturally in every title, H1/H2 where sensible, and in internal anchor text — no keyword stuffing.
- Logical heading hierarchy, semantic landmarks (`header`, `nav`, `main`, `section`, `article`, `footer`), descriptive link text (not "click here"), descriptive `alt` on all meaningful images, `aria-hidden` on purely decorative layers (canvas, orbs, rings, marquee, grain).
- Strong internal linking: every page links to the others via the nav and contextual links; breadcrumbs on inner pages.
- All important content is in the initial HTML (not injected by JS).

### 4.2 Technical

- `sitemap.xml` listing every public URL **with `xhtml:link` hreflang alternates**, `lastmod` dates; `robots.txt` allowing all and pointing to `https://abbosov.com/sitemap.xml`. `/admin/` must be `noindex` (meta + robots disallow).
- Open Graph + Twitter Card on every page (`og:title`, `og:description`, `og:url`, `og:type` = `profile` on home / `website` elsewhere / `article` for journal posts, `og:image`, `og:locale`, `og:site_name`). Create a **1200×630 `assets/images/og-image.png`** in the same style as the design (near-black background, ember glow, the name set in the display font) — typography and glow only, no fake photos.
- Favicon set + `site.webmanifest` + `theme-color` `#050507`. Simple SVG/PNG favicon using the "A.A" gradient mark; no external assets.
- A custom `404.html` in the same design (GitHub Pages serves it).
- `<meta name="viewport" content="width=device-width,initial-scale=1">`, `color-scheme: dark`, correct charset, no render-blocking third-party anything.
- Fast: preload hero fonts, `preconnect` nothing external (there is nothing external), lazy-load below-the-fold images, `width`/`height` on all images, modern formats (WebP/AVIF) when real images arrive.
- Prepared for Google Search Console (stable URLs, sitemap, canonicals). Do not claim anything is indexed.

### 4.3 Structured data (JSON-LD, accurate only)

- Homepage: `WebSite` (`name`, `url`, `inLanguage`) and `Person` / `ProfilePage` with `name: "Azizbek Abbosov"`, `url`, `description`, `sameAs` = exactly these four:
  - https://github.com/azbea
  - https://linkedin.com/in/a-abbosov
  - https://t.me/azbe_plt
  - https://instagram.com/azbe.plt
- Optional, only if factual: `birthPlace` (Chust, Uzbekistan), `nationality` Uzbekistan, `knowsLanguage` (`uz`, `en`, `ru`, `tg`, `ko`), `alumniOf` limited to institutions he **actually completed**: Chust District Polytechnic No. 2 only.
- **Never** list Korea Aerospace University or TSUE as `alumniOf` (not graduated). No `image` until a real portrait exists. No invented `jobTitle`, `worksFor`, awards, or ratings.
- `BreadcrumbList` on inner pages; `Article` on journal posts (when they exist).
- Validate that JSON-LD parses (no syntax errors).

---

## 5. CONTENT RULES (from the master prompt — enforce strictly)

**Use only these facts.** Never invent anything else.

- Name: Azizbek Abbosov (public display name; do not show the patronymic in branding). Born 19 June 2007, Chust, Uzbekistan.
- School: Secondary School No. 3, Chust, 2014–2023.
- Polytechnic: Chust District Polytechnic No. 2, 2023–2025, graduated with honors (red diploma).
- Korea Aerospace University (KAU), South Korea — Aviation Management (Pilot Program), started 2025, completed first academic year (two semesters), then took academic leave. **Not a graduate. Not a pilot. Not "currently attending."**
- Tashkent State University of Economics (TSUE) — Banking, online (some exams offline), started 2025. **Not a graduate.**
- About three years in South Korea (international exposure — do not invent cities/events).
- IELTS Academic 7.0. Languages: Uzbek (native), English (advanced), Russian (fluent), Tajik (high), Korean (beginner). Site languages: EN, UZ, RU only.
- Worked as an English teacher at an education center in Tashkent (no employer name, dates, student numbers, or results — placeholders only).
- Tech he has worked with/explored (do not call all of it "expert"): HTML, CSS, JavaScript, TypeScript, React, Next.js, Vue, React Native, Node.js, Express, NestJS, Python, FastAPI, PHP, REST APIs, MongoDB, PostgreSQL, Git, GitHub, Docker, Figma, Tailwind CSS, SCSS.
- Projects: BekeDu.uz (https://bekedu.uz — "Done for good learning."), ShokMarket.uz (https://shokmarket.uz), FaslMarket.uz (https://faslmarket.uz). Plus an education-center management SaaS — **in development / planning, not launched** (platform admin, center owner/admin, teachers, students, attendance, homework, grades, schedules, finance, payment tracking). No user numbers, revenue, clients, or metrics ever.
- Interests/ambitions (not achievements): aviation, international education, technology, software, entrepreneurship, building useful digital products, opportunities in the US and internationally.
- Public profiles: only the four URLs in 4.3. **No email shown** — use a config placeholder (`data-contact-email` empty) and render nothing until the owner provides one.

**Never publish:** family details, relationships, health, habits, finances, documents, passport/ID, private addresses, credentials, or anything private.

**Placeholders:** where a personal memory/detail is unknown, show a styled, clearly marked placeholder such as `[Add a personal memory about this period.]` — never fabricate. **No fake photos, no stock photos presented as his life.** Where an image would go, use a designed placeholder in this site's style (dark glass card with a faint ember glow and a mono label like `PORTRAIT — COMING SOON`).

Writing style: mature, natural, confident editorial voice. No corporate buzzwords ("visionary", "world-class", "revolutionary"). No motivational clichés.

---

## 6. INNER PAGES (Phase 2+ — reuse the homepage components)

Build every inner page from the **same component set and CSS as the homepage** (tag pill, mono labels, huge uppercase H2 with gradient `em`, glass `card3d`, `pc` project cards, language pills, social rows, starfield background, marquee). Nothing new stylistically. Each inner page opens with a compact hero (mono label + giant H1 in the display font, gradient on the second word) instead of the full orb hero.

- `/about/` — editorial biography in chapters (Where it began; Early education; Learning; Discovering aviation; Studying in South Korea; New directions; Technology; Teaching & communication; International ambitions; The road ahead) — facts only, placeholders for missing memories.
- `/education/` — vertical timeline (mobile-first) of the four institutions above, with exact statuses.
- `/experience/` — teaching + international experience (placeholders for unknowns).
- `/developer/` — the four project cards + stack list; each card supports title, description, role, tech, status, image, live link, repo link.
- `/timeline/` — chronological life events (only confirmed items; no invented months).
- `/journal/` — empty-state page now ("Writing coming soon") using the same style; structure ready for posts. No fake articles.
- `/gallery/` — empty-state/placeholder grid, ready for real uploads.
- `/future/` — flexible "What's next" page, phrased as ambitions not achievements.

---

## 7. FILE STRUCTURE

```
/ (repo root)
├── index.html                 English homepage
├── about/ education/ experience/ developer/ timeline/ journal/ gallery/ future/   (each with index.html)
├── uz/…  ru/…                 same set, translated
├── admin/                     later phase
├── assets/ fonts/ images/ icons/
├── css/   variables.css reset.css global.css components.css pages.css (+ menu.css)
├── js/    space.js (starfield) scroll3d.js (hero/tunnel/cards) menu.js lang.js main.js
├── data/                      structured JSON for future admin/CMS (kept separate from presentation)
├── 404.html  robots.txt  sitemap.xml  site.webmanifest  CNAME  .nojekyll  README.md
└── design-reference/index.html   (keep the original prototype for comparison)
```

No empty folders just for show.

---

## 8. WORKFLOW — DO ONLY PHASE 1 NOW, THEN STOP AND REPORT

**Phase 1 (this run):**
1. Read both reference files. Summarize in 5 lines what you will build. Do not ask questions unless truly blocked.
2. Create the repo scaffold, `CNAME`, `.nojekyll`, self-hosted fonts, token/reset/global CSS.
3. Build the **English homepage `/index.html`** to match `design-reference/index.html` **exactly**: starfield, hero, orb/rings, marquee, 3D journey tunnel, projects, languages/statement, contact, footer, nav pill **and the full-screen mobile menu overlay**.
4. Add full SEO head (title, description, canonical, hreflang for pages that exist, OG/Twitter, JSON-LD), `robots.txt`, `sitemap.xml`, `site.webmanifest`, favicons, OG image, `404.html`.
5. Implement reduced-motion + no-JS fallbacks and the performance rules in 2.3.
6. **Verify with a real browser (Playwright/Chromium headless):**
   - Screenshot the new homepage and `design-reference/index.html` at 360, 390, 430, 768, 1440 px, at scroll positions: top, journey 50%, journey 75%, projects, bottom. **Compare them and fix any visual difference.** Report the comparison.
   - No horizontal overflow at 320–430px; no console errors; no broken links.
   - Run Lighthouse (mobile) and report scores.
   - Validate JSON-LD, sitemap XML, and hreflang symmetry.
7. Write a `README.md`: structure, how to run locally (`python3 -m http.server`), how to deploy (exactly which files to commit/push to `main`; do not change DNS/CNAME), how to add a language/page, how to replace placeholders, and a note that `/admin/` will be a local-only prototype (GitHub Pages is static and public — no real authentication possible).
8. **Stop.** Output: what's done, what differs from the reference (should be nothing), Lighthouse scores, the open placeholders the owner must fill, and the planned next phases.

**Later phases (do not start yet):** 2 inner pages (EN) → 3 Uzbek & Russian versions → 4 `/admin/` local prototype (localStorage + JSON export/import, clearly documented limits) → 5 final SEO/QA pass.

Do not change the design, the stack, or the URL decisions without asking. If something in the reference is technically problematic (e.g., a perf issue), keep the **appearance** identical and fix the **implementation**, then tell me.
