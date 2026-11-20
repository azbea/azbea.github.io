# CODEX — PHASE 3: UX/DESIGN FIXES + SAMPLE CONTENT + UZBEK & RUSSIAN (abbosov.com)

Phases 1 and 2 are done (English homepage + 8 inner pages). Read `CODEX_PROMPT.md`, `CODEX_PHASE2.md`, `MASTER_PROJECT_PROMPT.md` and your own code first. **This prompt overrides them wherever they conflict** — especially on the design lock and content rules (see Parts A and B).

Do the parts in order: **A (UX/design fixes) → B (sample content) → C (Uzbek + Russian)**. Apply A and B to **every page in every language**. Then stop and report.

---

## PART A — UX & DESIGN FIXES (all pages)

### A0. The design lock is relaxed

The owner said: "exact" meant the **colors and the mood** were right, not that every layout must stay identical. So:

- **Keep:** the palette (`#050507` background, off-white `#f3efe9`, ember gradient `#ff4d1c → #ff9a3d → #ffd27a`, muted `#8b8a93`), the dark cinematic atmosphere, big bold Inter Display typography, the 3D starfield, scroll-driven 3D motion, glass surfaces, film grain.
- **Free to change:** layouts, spacing, component shapes, section structure, copy layout, interaction patterns, iconography, anything that makes the site clearer, more usable, more beautiful and more premium — especially on mobile. Improve things you find lacking. Do not leave a weak element only because it came from the reference.
- Keep changes coherent as one design system. Keep performance targets (mobile LCP < 2.5s, 60fps scroll, no layout shift). In the final report list **every** notable design change you made and why.

### A1. Everything clickable must LOOK clickable (the main problem)

Problem: on the homepage, rows like *"Explore Azizbek Abbosov's timeline — Next ↗"*, *"Education ↗"*, *"Experience ↗"*, *"Explore what comes next"* and the social rows (*GitHub @azbea ↗* …) read like plain information. Visitors on phones don't realise they can tap them. Fix this site-wide with one consistent **link/affordance system**:

1. **Visible tap target on every link row/card:** a round **arrow button** (44–56px circle, `--line` border, arrow icon inside) at the right edge of every row/card that links somewhere — the same idea as the project cards' round arrow, reused everywhere. Rows get comfortable height (≥ 64px on mobile), a visible bottom border/glass background, and clear label + short secondary description.
2. **Correct arrow semantics:** internal links use **→** (right arrow). External links (other sites) use **↗** and open in a new tab with `rel="noopener noreferrer"`. Never use ↗ for internal links. Replace labels like "Next ↗" with explicit text, e.g. **"Next: Education"**.
3. **Press/tap animation (mobile-friendly, no hover dependence):** on `:active`/touch down the row scales slightly (~0.985), an ember-gradient wash fills from the left, the label shifts a few px right, and the arrow button fills with the gradient and rotates/nudges (→ moves right; ↗ moves up-right). Release animates back smoothly (~250ms). Add the same on `:hover` and `:focus-visible` for desktop/keyboard. Use `transform`/`opacity` only; no layout thrash. Provide `-webkit-tap-highlight-color: transparent` and a custom tap feedback so it feels intentional.
4. **Idle hint (once):** when a link row first scrolls into view, play one subtle arrow "nudge" (small shift and back) to signal interactivity. Not repeating, not distracting. Respect `prefers-reduced-motion` (no movement; keep static arrow).
5. **Inline text links** inside paragraphs: ember-gradient underline (2px), slightly brighter on press.
6. **Buttons** (`Explore my story`, `Discover my work`, etc.): clear pressed state; icon arrow inside.
7. **Non-links must not look like links.** Chips, labels, and info cards stay visually passive (no arrow, no border-highlight on hover) so the contrast between "tappable" and "just info" is obvious.
8. **Accessibility:** min 44×44px targets, visible `:focus-visible` ring using the ember gradient, link text descriptive, `aria-label` where the visible text is short, external links get a visually-hidden "(opens in a new tab)".
9. **Audit step:** walk through **every page in every language** and list each element that is interactive or should be. Make sure all are consistent with the system above. Report the audit table (page → element → before → after).

### A2. Social links with platform logos

- Add proper **platform logos** (GitHub, LinkedIn, Telegram, Instagram) as **inline SVG symbols** in a single sprite (no external requests, no icon fonts, no libraries). Draw/provide clean, recognisable monochrome logo glyphs (`currentColor`, `aria-hidden="true"`).
- Each social row/button: logo in a round glass icon container on the left (44–56px, `--line` border; fills with the ember gradient on press/hover and the glyph turns near-black), platform name + handle, and the external-link arrow button on the right (↗).
- Use them everywhere socials appear: the contact section, the footer (compact icon-only buttons with `aria-label`), the full-screen menu, and optionally the About page. Keep exactly these four URLs: `https://github.com/azbea`, `https://linkedin.com/in/a-abbosov`, `https://t.me/azbe_plt`, `https://instagram.com/azbe.plt`.
- Icon-only buttons need an accessible name ("GitHub — opens in a new tab").

---

## PART B — SAMPLE CONTENT (the owner will replace it later)

New owner instruction: wherever the "dream perfect website" needs content and there is no source, **do not leave empty placeholders. Write plausible sample content based on his real background** (Chust → school → polytechnic → Korea/aviation → TSUE banking → English teaching in Tashkent → software projects). The owner will rewrite it himself later. Rules:

**Allowed (write it, make it good, in the mature, natural editorial voice — no clichés):**
- Personal-story prose for the biography chapters, short "memory" passages, descriptions of what studying/living in Korea or teaching English may have felt like, reflections, "what I learned" paragraphs.
- Descriptions, roles ("Full-stack developer", "Designer & developer", etc.), tech lists and status for BekeDu.uz, ShokMarket.uz, FaslMarket.uz; fuller description of the education-center SaaS (as in development).
- Teaching experience details in generic terms (levels taught, what he focused on) **without** inventing an employer name, student numbers, or results.
- 2–3 **short draft journal posts** (reflections on moving abroad, learning English, building first projects) so the journal template is visible. Journal and Gallery stay `noindex` and out of the sitemap.
- Personal philosophy/statement copy, "What's next" details, hero/lead variants, Alt texts, captions for image slots.
- Any other missing section the design needs (e.g. FAQ-style "Quick facts", "How I work" short text), as long as it stays plausible and modest.

**Hard limits (never, even as samples):**
- No claim that he **completed** KAU or TSUE, holds a **pilot licence**, or has any **degree/certificate/award/ranking** beyond: polytechnic red diploma, IELTS Academic 7.0.
- No invented **numbers or metrics**: users, revenue, downloads, clients, investors, company ownership, student counts, grades, test scores other than IELTS 7.0.
- No invented **real employer/school/company names**, no named real people, no **fake quotes or testimonials/reviews** attributed to anyone.
- No **fake photos** (no stock photos, no generated "memories"). Image slots stay as designed placeholder tiles.
- No private info (family, relationships, health, finances, documents, addresses, email/phone).
- Don't touch `Person` structured data with sample claims — JSON-LD stays strictly factual (name, url, sameAs, description, knowsLanguage, birthPlace, alumniOf = polytechnic only).

**How to mark and track samples (mandatory):**
1. Wrap every sample passage in an element with `data-sample="true"` (e.g. `<p data-sample="true">…`).
2. Add one line of CSS: `body.show-samples [data-sample]{outline:1px dashed #ff9a3d;outline-offset:3px}` and a tiny script that adds `show-samples` to `<body>` when the URL has `?samples=1`, so the owner can instantly see everything that is still sample content on any page.
3. Create `SAMPLE_CONTENT.md` in the repo root listing **every file and section containing samples**, one line each, plus how to find them (`grep -R 'data-sample' .`). Update the README with a "Replace sample content before announcing the site" checklist.
4. When sample text is present in a language, the same applies to Uzbek and Russian.

---

## PART C — UZBEK & RUSSIAN VERSIONS

Create full translations of **all 9 pages** (home + 8 inner) in two languages, as separate static HTML files:

```
/uz/  /uz/about/ /uz/education/ /uz/experience/ /uz/developer/ /uz/timeline/ /uz/journal/ /uz/gallery/ /uz/future/
/ru/  /ru/about/ /ru/education/ /ru/experience/ /ru/developer/ /ru/timeline/ /ru/journal/ /ru/gallery/ /ru/future/
```
English stays at the root. Keep **English slugs** in all languages (stable, simple).

**Translation quality:**
- **Uzbek:** natural modern Uzbek in **Latin script**, with the standard letters `oʻ` and `gʻ` (U+02BB modifier apostrophe) used consistently, e.g. "Oʻzbekiston", "Chust". Not word-for-word.
- **Russian:** natural modern Russian, warm but mature editorial tone.
- Translate **everything**: nav, menu, buttons, aria-labels, alt text, page copy (including samples), footer, 404 text, form/placeholder labels, JSON-LD `inLanguage`/`description`.
- Every UZ/RU block gets `data-review="needs-native-review"` (owner will proofread).

**SEO for the languages (important):**
- Each page: `<html lang="uz">` / `<html lang="ru">`, unique localized `<title>` + meta description, self-referencing canonical, **full reciprocal hreflang cluster** on all 3 versions (`en`, `uz`, `ru`, `x-default` → English URL), `og:locale` (`uz_UZ`, `ru_RU`, `en_US`) + `og:locale:alternate`.
- The name must stay findable in every language:
  - Uzbek pages use "Azizbek Abbosov".
  - **Russian pages must include both forms:** Cyrillic **"Азизбек Аббосов"** in H1/titles where natural, and the Latin "Azizbek Abbosov" in the lead/description/first paragraph and in the JSON-LD (`name: "Azizbek Abbosov"`, `alternateName: ["Азизбек Аббосов", "Abbosov Azizbek"]` on every language version).
- Localized JSON-LD (`Person`, `WebSite`, `BreadcrumbList`) with correct `inLanguage`, same factual content as English.
- The language switcher goes to the **same page in the other language**; the active language is highlighted; no automatic redirects based on browser language (bad for SEO and can trap visitors).
- `sitemap.xml`: add all new URLs with `xhtml:link` alternates for every language; Journal and Gallery stay excluded and `noindex` in all languages.
- **Fonts:** the self-hosted Inter and mono fonts must include **Cyrillic** and **Latin Extended** subsets (and U+02BB). Add `unicode-range` splits, preload only the critical Latin file. Verify glyph coverage (e.g. with `fontTools` if available) — no fallback-font glyphs in headings. Verify the **hero name fits at 320–430px** in Cyrillic (wider letters): adjust the fluid `clamp()` size per language if needed, **no clipping, no horizontal scroll**.
- Check all three languages for text overflow in buttons, nav pill, menu and cards (longer words in RU/UZ).

---

## VERIFICATION & REPORT

Try a real browser again (Playwright Chromium; Chrome `--headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage`; Firefox headless). If it works: screenshots of the homepage + 2 inner pages in each language at 360/390/430/1440, check overflow and console errors, and compare the affordance/tap states. If **no browser works, do not claim visual verification** — say exactly what failed.

Always run the static audits and report results:
- hreflang reciprocity across all 27 pages; canonicals; unique titles/descriptions per page+language; one H1 per page; JSON-LD parse; sitemap vs files; internal link crawl (no 404s); each internal link uses →, each external link uses ↗ + `rel`/`target`.
- No leftover English strings in UZ/RU pages except proper nouns, technology names and URLs.
- `grep` that no `data-sample` block violates the hard limits; list sample sections count per language.

Final report must include: design changes made and why; the affordance audit table; the page table (URL, title, description, H1, canonical) for all languages; the `SAMPLE_CONTENT.md` summary; verification results (or why not); anything unsure.

**Then stop.** Do NOT build `/admin/` or anything else — that is Phase 4.
