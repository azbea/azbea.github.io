# CODEX — PHASE 2: ENGLISH INNER PAGES (abbosov.com)

Phase 1 (English homepage) is done. Now build the **English inner pages**.

Re-read before starting: `CODEX_PROMPT.md` (project rules, design lock, SEO, content rules — all still apply), `MASTER_PROJECT_PROMPT.md`, `design-reference/index.html`, and your own Phase 1 code. This prompt adds to them; on conflict, `CODEX_PROMPT.md` wins.

## 0. Rules that do not change

- Design is LOCKED. Inner pages use **only the existing components and tokens** from the homepage (starfield canvas, glass nav pill, mono labels, huge uppercase Inter Display headings with ember-gradient `em`, `card3d` glass cards, `pc` project cards, language pills, social rows, grain, vignette, footer, full-screen menu). **Do not invent new visual styles.** If a new layout is needed (e.g. timeline), build it from the same tokens, borders, radii, glass and mono labels.
- Mobile first (360 / 375 / 390 / 414 first, then 768+). No horizontal overflow, 44px touch targets, `100svh`.
- Plain HTML/CSS/vanilla JS. No build step, no external requests, no new dependencies.
- Facts only (section 5 of `CODEX_PROMPT.md`). No invented memories, dates, employers, numbers, awards, or photos. Unknown details = clearly marked placeholders.
- English only in this phase. Language switcher: do not output links/hreflang to `/uz/` or `/ru/` pages that do not exist yet.
- SEO is priority #1: every page unique title + description, one H1, canonical, OG/Twitter, JSON-LD, breadcrumbs, internal links, in-HTML content (no JS-injected text).

## 1. Shared pieces (build once, reuse)

1. **Shared header/menu/footer markup** used identically on every page (copy the homepage's). The nav pill and the full-screen menu list: Home, About, Education, Experience, Developer, Timeline, Journal, Gallery, Future + social links. Mark the current page (`aria-current="page"`, ember highlight).
2. **Inner-page hero** (compact, ~60–70svh): mono tag/label → giant H1 in the display font with the gradient on the last word → one-line lead. Subtle orb glow and one ring only (lighter than the homepage). Scroll-driven fade/Z-move like the homepage hero but gentler.
3. **Breadcrumbs** (`Home / Page`) in mono style, with `BreadcrumbList` JSON-LD.
4. **Section reveal** animation: elements fade/rise/tilt slightly in 3D on scroll using the same easing as the project cards. Reduced-motion → no animation. No-JS → everything visible.
5. **Next-page link row** at the bottom of each page ("Next: Education →") in the big social-row style, plus the contact section (reuse from the homepage).
6. **Vertical timeline component** (used on Education and Timeline pages): a thin `--line` vertical rail, ember dot nodes that glow as they enter view, year in the big gradient display type, glass card per entry. Mobile layout is single column, rail on the left. Desktop may alternate/offset but must stay calm and editorial.
7. **Placeholder component**: dashed `--line` border glass box with a mono label and text like `[Add a personal memory about this period.]`. Visually obvious as "to be filled", styled consistently, easy to find/replace (class `.ph`).
8. Update the homepage so every link and button points to real pages: "Explore my story" → `/about/`, "Discover my work" → `/developer/`, project cards → their live sites (`target="_blank" rel="noopener noreferrer"`), the journey section gets a link to `/timeline/`, plus internal contextual links to `/education/`, `/experience/`, `/future/`.

## 2. Pages (each = `<slug>/index.html`, absolute-root-relative internal links)

For each: title, description (≤155 chars), H1, structure. Use these SEO titles/descriptions (adjust wording only if clearly better, keep the name in each).

### `/about/`
- Title: `About Azizbek Abbosov — Biography & Personal Story`
- Description: `The personal story of Azizbek Abbosov: growing up in Chust, Uzbekistan, studying in South Korea, exploring technology and building what comes next.`
- H1: `The story of Azizbek Abbosov` (gradient on "Abbosov").
- Editorial biography in 10 chapters (numbered `01…10` in the big outlined counter style), each: short heading, 2–4 sentences of mature, natural prose built **only from known facts**, then a `.ph` placeholder for a personal memory where appropriate.
  1. Where it began — Chust, Uzbekistan
  2. Early education (Secondary School No. 3, 2014–2023)
  3. Learning and academic development (Polytechnic No. 2, graduated with honors)
  4. Discovering aviation
  5. Studying in South Korea (KAU, Aviation Management, first academic year, then academic leave; about three years living in Korea)
  6. New academic and professional directions (TSUE Banking, online)
  7. Exploring technology
  8. Teaching and communication (English teacher at an education center in Tashkent; IELTS Academic 7.0)
  9. International ambitions
  10. The road ahead
- Include a facts strip (glass card): born 19 June 2007 · Chust, Uzbekistan · Languages (Uzbek native, English advanced/IELTS 7.0, Russian fluent, Tajik high, Korean beginner). No other personal data.
- Do not state he is a pilot, a KAU graduate, or a TSUE graduate. Aviation is an interest/academic background only.

### `/education/`
- Title: `Education — Azizbek Abbosov`
- Description: `Educational background of Azizbek Abbosov: school and polytechnic in Chust, Aviation Management at Korea Aerospace University, and Banking at TSUE.`
- H1: `Education of Azizbek Abbosov`.
- Vertical timeline, exactly these four entries (newest information accurate, no implied completion):
  - **2014–2023** — Secondary School No. 3, Chust, Uzbekistan. School education completed in 2023.
  - **2023–2025** — Chust District Polytechnic No. 2, Chust, Uzbekistan. Graduated with honors (red diploma).
  - **2025** — Korea Aerospace University (KAU), South Korea. Aviation Management (Pilot Program). Completed the first academic year (two semesters); subsequently on academic leave. Status chip: `Academic leave`.
  - **2025 – present** — Tashkent State University of Economics (TSUE), Uzbekistan. Banking, online format with some offline exams. Status chip: `In progress`.
- Beneath: a "Languages & certification" row: IELTS Academic 7.0; language pills.
- Each entry has an optional image slot (placeholder) and a `.ph` for memories.

### `/experience/`
- Title: `Experience — Azizbek Abbosov`
- Description: `Professional and international experience of Azizbek Abbosov: teaching English in Tashkent and living, studying and adapting abroad in South Korea.`
- H1: `Experience of Azizbek Abbosov`.
- Two glass-card blocks: **Teaching English** (education center in Tashkent; worked with learners at different levels; prepared and delivered English grammar explanations; employer/dates = placeholders) and **International experience** (about three years in South Korea; adapting to a new environment, academic life, working with international students; no invented places/events). Plus a "Technology" teaser card linking to `/developer/`.

### `/developer/`
- Title: `Azizbek Abbosov — Software Development & Projects`
- Description: `Software projects by Azizbek Abbosov: BekeDu.uz, ShokMarket.uz, FaslMarket.uz and an education-center management platform in development.`
- H1: `Software by Azizbek Abbosov`.
- Four `pc` project cards: BekeDu.uz ("Done for good learning."), ShokMarket.uz, FaslMarket.uz (all with external links) and **Education-center management platform — In development** (no link; list the planned modules: platform admin, center owner/admin, teachers, students, attendance, homework, grades, schedules, financial records, payment tracking). Each card has fields for role, technologies, status, screenshot slot, live link, optional repo link — unknowns as `.ph`. No metrics, revenue, users or ownership claims.
- "Technologies he has worked with or explored" grouped (Frontend / Backend / Databases / Tools) as chips. **Do not rank or label expertise levels.**
- JSON-LD: `CollectionPage` or `ItemList` of the projects as `SoftwareApplication`/`WebSite` items **without** invented properties.
- This page also targets "Azizbek Abbosov developer" — use that wording naturally once in the lead, not repeatedly.

### `/timeline/`
- Title: `Timeline — Azizbek Abbosov`
- Description: `A chronological timeline of Azizbek Abbosov's journey from Chust, Uzbekistan through school, polytechnic, South Korea and beyond.`
- H1: `The journey of Azizbek Abbosov`.
- Vertical timeline with **only confirmed** entries, no invented months: 2007 born (19 June, Chust); 2014 began secondary school; 2023 completed school, began polytechnic; 2025 graduated polytechnic with honors; 2025 began Aviation Management at KAU; 2025 began Banking at TSUE; later: academic leave from KAU (no date). Order carefully; undated items are labelled "Date to be confirmed" in a `.ph` style rather than guessed. Data lives in `data/timeline.json` and the page HTML is generated from the same content by hand (no runtime fetch needed for SEO).

### `/journal/`
- Title: `Journal — Azizbek Abbosov`
- Description: `Reflections, notes and writing by Azizbek Abbosov. New entries coming soon.`
- H1: `Journal`. Designed empty state: glass card "First entries are on the way." + mono label. **No fake articles.** Include the reusable article template in `/data/templates/` (not published) ready for future posts, with `Article` JSON-LD scaffold.

### `/gallery/`
- Title: `Gallery — Azizbek Abbosov`
- Description: `A visual archive of moments, places and projects from the journey of Azizbek Abbosov. Photographs coming soon.`
- H1: `Gallery`. A responsive grid of designed placeholder tiles (dark glass, faint ember glow, mono label `PHOTO — COMING SOON`), ready to swap for real images (`<figure>` + `<figcaption>` + `loading="lazy"` + width/height + alt). **No stock photos, no generated "memories".**

### `/future/`
- Title: `Future — Azizbek Abbosov`
- Description: `What's next for Azizbek Abbosov: aviation, international education, software, entrepreneurship and building useful digital products.`
- H1: `What's next`. Big statement paragraph + glass cards for: Aviation, International education, Technology & software, Entrepreneurship, Opportunities in the US and internationally. Phrase everything as **interest/ambition**, never as achieved ("hopes to", "is exploring", "is interested in").

## 3. SEO work in this phase

- Update `sitemap.xml` with all new URLs (`lastmod`, no hreflang alternates for non-existent languages). Keep `robots.txt` valid.
- Every page: canonical (`https://abbosov.com/<slug>/`), OG/Twitter (reuse the OG image; `og:type=website`; `profile` stays on home), Person `sameAs` kept consistent, `BreadcrumbList`.
- Homepage + inner pages interlink with descriptive anchor text including the name where natural (e.g. "Azizbek Abbosov's education").
- Add `ProfilePage`-style `mainEntity` (Person) on `/about/` with the same accurate facts as the homepage. `alumniOf` only Chust District Polytechnic No. 2. Never KAU/TSUE.
- No duplicate titles/descriptions across pages. No thin pages: the journal/gallery empty states stay `index` for now but with unique intro text; if you judge they are too thin to index, set `noindex` on those two **and tell me** (recommended: noindex until they have real content, and keep them out of the sitemap until then — do that).

## 4. Verification — do this properly this time

Phase 1 verification was skipped because the browser would not start. **Try harder and report honestly:**

1. Start a local server (`python3 -m http.server 8000`; if denied, use `npx serve` or Node's built-in `http`; if all denied, say exactly what was denied).
2. For a headless browser try, in order: Playwright Chromium; `chromium`/`google-chrome` with `--headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage`; Firefox headless. Save error output if each fails.
3. If a browser works: screenshot **every page** at 360, 390, 430, 768, 1440 px (top, middle, bottom). Check no horizontal scroll at 320–430, no console errors, menu opens/closes with Esc/focus trap, nav `aria-current`, all internal links resolve (crawl them), reduced-motion and no-JS rendering. Compare the homepage against `design-reference/index.html` and fix any visual drift. Run Lighthouse mobile if possible and report scores.
4. If **no** browser can run, do a static audit (link crawl, HTML validity, unique titles/descriptions, one H1 per page, JSON-LD parse, sitemap vs. files) and say plainly that visual verification was not possible. **Do not claim things are verified when they are not.**

## 5. Deliverables and stop

- All pages above, shared components, updated homepage links, updated `sitemap.xml`, `data/*.json` for timeline/education/projects, README updated (new pages, how to add a page, how to fill placeholders).
- Final report: what's done; the verification results (or exactly why not); a table of every page with title/description/H1/canonical; list of placeholders the owner must fill; anything you changed on the homepage; anything you were unsure about.
- **Then stop.** Do NOT start Uzbek/Russian, admin, or anything else. Phase 3 (UZ + RU translations) comes next.
