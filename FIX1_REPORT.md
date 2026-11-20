# FIX1 — Static audit report

## Underline rules

| Scope | Remaining rule | Audit result |
|---|---|---|
| All anchors/states | `a, a:hover, a:focus, a:active, a:visited { text-decoration: none; }` | One `text-decoration` declaration remains in the CSS tree. |
| Paragraph prose links | `p a, .prose a` use a 2px ember-gradient background underline | This is the only underline-style appearance; no `border-bottom` or `text-underline` link hacks remain. |

`grep -R "text-decoration" css` returns only the global reset in `css/fix1.css`.

## Header structure and language stability

| Language | Routes | Header structure/classes | Header geometry |
|---|---:|---|---|
| EN | 9 | Identical signature | Fixed 3-column logo / language / menu grid |
| UZ | 9 | Identical signature | Same dimensions and cell positions as EN |
| RU | 9 | Identical signature | Same dimensions and cell positions as EN |

Static comparison found one header DOM/class signature and one menu-language-switcher signature across all 27 routes. The wordmark remains `AZIZBEK ABBOSOV`. Each language has a 44×44px cell, identical font metrics and reserved border width; active state changes only its fill. The language links and active marker vary by route. Accessible labels remain localized.

## Link and card layout

Rows, social links, project actions and project cards use normal-flow grid columns for text and arrows. The arrow column is reserved separately, with a 48px gradient chip. Profile handles sit directly below their platform names. Link captions state the action. At 320–430px the row grids use `minmax(0,1fr)` plus a fixed arrow column, `min-width:0`, and wrapping text; project titles and long localized headings can wrap instead of running beneath an arrow. Contact-row inner width leaves room for the full 44px icon, 48px arrow and the profile handle. Desktop columns retain the same separation. Non-link information cards do not gain arrow chips or hover/press styling.

## Absolute and fixed positioning inventory

| Selector(s) | Purpose | Why text remains clear |
|---|---|---|
| `header` / `.site-header` (`fixed`) | Top navigation pill | Fixed 60px pill; hero/inner hero top padding reserves space below it. |
| `canvas#space`, `.vignette`, `.grain` (`fixed`) | Background starfield, vignette and texture | Decorative layers; vignette/grain ignore pointer input and do not contain text. |
| `.menu-overlay` (`fixed`) | Full-screen menu surface | Modal UI shown on open; its own links and controls occupy the surface. |
| `.menu-close` (`absolute`) | Close control at the overlay top edge | 44px target; overlay reserves at least 86px above menu content. |
| `.orb`, `.ring` (`absolute`) | Hero light and ring decoration | Hero copy is positioned above them (`.hero-in`, z-index 3). |
| `.stage .label` (`absolute`) | Journey stage label | Pinned to top-left, apart from the centered chapter card. |
| `.stage .count` (`absolute`) | Outlined chapter counter | Pointer-inert, z-index 0 behind cards (z-index 1); capped at 150px on desktop. |
| `.card3d` (`absolute`) | Scroll-positioned journey card | The card contains its own text; other row arrows are not positioned over it. |
| `.opens-new-tab` (`absolute`) | Visually hidden new-tab explanation | 1px clipped accessibility text; it is not painted over visible copy. |
| `.pc::before` (`absolute`) | Project-card glow | Pointer-inert, clipped by the card, behind card content at z-index 0. |
| `.timeline-list::before`, `.timeline-node` (`absolute`) | Timeline rail and nodes | Rail occupies the padded left gutter; card/year content starts to its right. |
| `.footer-social a::after` (`absolute`) | Compact external-link badge | Badge sits above/right of the icon; its adjusted top keeps it clear of the centered SVG glyph. |

All link-row, contact-row, menu-row and project-action arrows are in grid flow; none use absolute positioning.

## Desktop type caps (1024px and wider)

| Text | Maximum |
|---|---:|
| Homepage H1 | 170px |
| Inner-page H1 | 120px |
| Section H2 | 96px |
| Journey year | 120px |
| Journey card title | 40px |
| Chapter counter | 150px |
| Statement paragraph | 64px |
| Marquee | 40px |
| Project-card title | 34px |
| Social/link-row title | 32px |

Mobile clamp minimums are unchanged. Long Uzbek/Russian headings use wrapping and `overflow-wrap:anywhere`; grid text columns have `min-width:0`, and arrows retain their own column through desktop widths.

## Footer and sprite audit — all 27 routes

| Page | Four profile URLs | Shared sprite references |
|---|---|---|
| `/about/` | PASS | PASS |
| `/developer/` | PASS | PASS |
| `/education/` | PASS | PASS |
| `/experience/` | PASS | PASS |
| `/future/` | PASS | PASS |
| `/gallery/` | PASS | PASS |
| `/` | PASS | PASS |
| `/journal/` | PASS | PASS |
| `/ru/about/` | PASS | PASS |
| `/ru/developer/` | PASS | PASS |
| `/ru/education/` | PASS | PASS |
| `/ru/experience/` | PASS | PASS |
| `/ru/future/` | PASS | PASS |
| `/ru/gallery/` | PASS | PASS |
| `/ru/` | PASS | PASS |
| `/ru/journal/` | PASS | PASS |
| `/ru/timeline/` | PASS | PASS |
| `/timeline/` | PASS | PASS |
| `/uz/about/` | PASS | PASS |
| `/uz/developer/` | PASS | PASS |
| `/uz/education/` | PASS | PASS |
| `/uz/experience/` | PASS | PASS |
| `/uz/future/` | PASS | PASS |
| `/uz/gallery/` | PASS | PASS |
| `/uz/` | PASS | PASS |
| `/uz/journal/` | PASS | PASS |
| `/uz/timeline/` | PASS | PASS |

The external sprite at `assets/icons/sprite.svg` contains `github`, `linkedin`, `telegram`, and `instagram`. The 27 route pages and all three 404 documents use valid same-origin `use` references; no page depends on an inline-only sprite. The footer uses the same four URLs in the same order on every route.

## Other static checks

- 27 route pages and 3 404 documents parsed without duplicate attributes or mismatched HTML tags.
- One H1 per route; all route JSON-LD blocks parse.
- All same-origin hrefs resolve to a static file or route index; all language switchers preserve the current route.
- Every `_blank` link has `rel="noopener noreferrer"`.
- CSS brace counts balance; one global `text-decoration` declaration remains.
- Draft markers remain at 41 per language.
