# DESIGN.md — Blacklink early access

> The door to a private room, not a website. One page, one purpose: a serious builder requests access.
> Hierarchy comes from luminance, weight and space. Never hue.

Source of truth for brand values: `BLACKLINK_MASTER_BRIEF.md` §2 (app repo, read-only).
Scope: `index.html` only. The legal pages (`privacy.html`, `terms.html`) are built separately by `tools/build-legal.py`.

## 1. Atmosphere

**Style**: strict monochrome, dark, still.
**Keywords**: private, cold, tactical, hairline, heavy type, presence, one gesture.
**Feel**: an unlit private room. One soft light, nothing else moving.

**No background shapes.** The user has twice rejected drawn background elements (an oval table with seat rings, then a round table with ten seats). The background is light, vignette and grain only. Do not add rings, circles, tables or other line art.

**Ambient layer** (all `aria-hidden`, `pointer-events: none`, behind content):
1. `.light` — a very large, very low-opacity radial light that drifts on a 50s loop; on desktop with a fine pointer it also eases ~4% toward the cursor.
2. `.vignette` — radial falloff so every edge reaches pure black.
3. `.grain` — static film grain: a 160px SVG `feTurbulence` tile as a data URI, opacity 0.06.

**Dependencies**: none. CSS plus ~3 KB of vanilla JS for UI states (measured with comments and whitespace removed; ~1.3 KB gzipped). No build step.

## 2. Colour tokens

The §2.2 ladder, values unchanged. No accent; the inverse white button is the only emphasis.

```css
--bg: #000000;  --bg-elevated: #0a0a0a;  --surface: #141414;  --surface-hover: #1c1c1c;
--border: #262626;  --border-strong: #3f3f3f;
--text: #ffffff;  --text-secondary: #a3a3a3;  --text-muted: #767676;
--text-hint: #8a8a8a;   /* added: input placeholder grey, 5.3:1 on --surface (muted is 4.05:1 there) */
--inverse-bg: #ffffff;  --inverse-text: #000000;
--bg-rgb: 0, 0, 0;  --text-rgb: 255, 255, 255;
```

Rules: every colour is a token reference; only `:root` contains hex. White at low alpha (`rgba(var(--text-rgb), a)`) is used for hairlines, light and grain. Meaningful text is `--text-secondary` or brighter; `--text-muted` is for meta only (App Store, footer, consent line — 4.69:1 on black).

## 3. Typography

Self-hosted, declared inline in `index.html` (no render-blocking stylesheet); Archivo Black and Inter are preloaded. `Inter-400/500/600.woff2` are the same variable file, so it is declared once with `font-weight: 400 600` and downloads once.

| Role | Font | Size | Colour |
|---|---|---|---|
| Wordmark (headline) | Archivo Black, uppercase, 0.1em | clamp(30px, 6.6vw, 50px) | `--text` with a permanent `--glow-soft` halo |
| Tagline | Inter 500 | clamp(16px, 0.9vw + 12px, 20px) | `--text-secondary` |
| Pitch (supporting line) | Inter 400 | clamp(14px, 0.4vw + 13px, 16px), max 40ch | `--text-secondary` |
| COMING SOON | Archivo Black, uppercase, two lines | clamp(34px, 7.4vw, 60px) | `--text-secondary` (quieter than the headline; set `--text` to restore its old weight) |
| App Store | Inter 500, uppercase, 0.14em | 12px | `--text-muted` |
| Invite "Be first in the room." | Inter 500 | 15px | `--text` |
| Input | Inter 400 | 16px (iOS never zooms) | `--text` |
| Button | Inter 600, uppercase, 0.12em | 13px | `--inverse-text` |
| Note / consent / footer | Inter 400 | 13 / 13 / 12px | error / muted / muted |

Hierarchy: logo → headline → form; everything else quieter.

## 4. Components and states

**Field** (`.fieldwrap` > `input.field` + `.hint`): 56px tall, `--surface`, 1px `--border`, radius 12px. A real `<label>` (visually hidden), `type=email`, `inputmode=email`, `autocomplete=email`. The visible "your@email.com" is a decorative `.hint` that eases up 4px on focus and disappears once typing starts. Focus: border to `--text-muted` plus a soft 1px outer ring (`.fieldwrap::after`, opacity only). Error: `aria-invalid="true"` brightens the border to `--text-secondary`; a single 4px horizontal nudge.

**Button** (`#submit`): white pill, 56px. Hover (hover-capable devices only): lifts 1px and one slow inner sheen. Press: scale 0.985. Desktop fine pointer: magnetic, drifts at most 4px toward the cursor. Sending: label fades, a 1px line slides along the base, `disabled` + `aria-busy`.

**States, in place, no layout jump.** The form block and the confirmation share one CSS grid cell (`.stage`), so the reserved height is the taller of the two from first paint and never changes.
- **Idle** — form visible; the confirmation is `visibility: hidden` and `inert`.
- **Sending** — as above.
- **Error** — plain-language message in `#note` (`role=status`, `aria-live=polite`; reserved line height). Typed text is never cleared. Messages: "Enter a valid email address." / "Something went wrong. Try again."
- **Success** — form block fades and rises 8px and becomes `inert`; "You're on the list." then "We'll be in touch when your invite is ready." then the share line fade in (250 / 450 / 650ms); focus moves to the confirmation heading (`tabindex=-1`).

**Share line**: "joinblacklink.com" is a button that copies `https://joinblacklink.com` and swaps to "Copied" for 1.6s (both labels share a grid cell, so no width jump). A visually hidden live region announces "Link copied".

**Reveals** (`.rv`, max two): "War rooms" and "Live presence" carry a dotted underline (drawn as a dotted bottom border because Safari ignores text decoration on buttons). Hover, keyboard focus or tap shows one line beneath the supporting line; blur or a second tap hides it. Texts live in one reserved line (two on narrow screens), linked by `aria-describedby`.

**Presence cue**: a 6px white dot before the consent line ("Early access opens in waves. …"), pulsing opacity/scale on a 4s period. Honest wording only: nothing about rooms being open or people being present.

**Logo**: the PNG is untouched. It is served as display-sized WebP copies (`logoB-480.webp`, `logoB-840.webp`) with a transparent background: white with alpha taken from brightness, which matches the PNG within 0.33/255 over black and has no box edge over the ambient layer in any browser. `logoB.png` remains the fallback. Nothing sits behind the logo; the entrance sweep is masked to the logo shape.

## 5. Layout

Single centred column, `--col: 520px`; the capture block is 440px. Body uses `100dvh` and `env(safe-area-inset-*)`. Spacing scale: 4 / 8 / 12 / 16 / `--s5` clamp(20px, 2.6vh, 28px) / `--s6` clamp(24px, 3.6vh, 40px). The page fits one screen at 768×1024, 1440×900 and larger desktops; phones scroll slightly.

Tap targets are at least 44px: the field and button are 56px; the reveals, the copy button and the consent link extend their hit area with a pseudo-element; footer links get 44px rows on coarse pointers.

## 6. Depth

Flat. Hairline borders and the ambient light only. No shadows or backdrop blur. Two glows, both requested by the user: the BLACKLINK wordmark glows permanently with the softer `--glow-soft`, and COMING SOON fades into `--glow` on a loop (§7). The user tried a stronger wordmark glow and reverted it. The only filter is the logo's one-time 3px entrance blur.

## 7. Motion

Every timing is a CSS variable in `:root` (`--t-*`), with one easing: `--ease: cubic-bezier(0.2, 0.8, 0.2, 1)`. Only `transform` and `opacity` animate, plus the logo's entrance blur.

**Entrance, once per session** (start times):

| t | What |
|---|---|
| 0ms | pure black |
| 150ms | grain, vignette and light fade in (1200ms) |
| 300ms | logo rises 12px, fades in and sharpens from a 3px blur (900ms) |
| 700ms | headline (wordmark + tagline) settles (800ms) |
| 820ms | supporting line, same motion |
| 1500ms | COMING SOON + App Store (600ms) |
| 1800ms | invite line, form, consent and footer (400ms) |
| 2600ms | one specular sweep across the logo (1200ms), never repeated |

Everything has landed by 2.2s. Logo and headline start at 1% opacity rather than 0, which is still black to the eye; browsers skip fully transparent paints when timing Largest Contentful Paint, and without this Lighthouse reports no LCP at all.

**COMING SOON glow** (requested by the user): the text rests in `--text-secondary` grey; a white copy on top (`.soon-glow`, `aria-hidden`, soft white `text-shadow`) fades 0 → 1 → 0 on a `--t-glow` 5s ease-in-out loop that starts once the entrance has landed. Only its opacity animates.

After the entrance, only the drifting light, the presence dot and the COMING SOON glow move. `will-change` is applied during the entrance only (`html.entering`, removed at 2.8s).

**Repeat visit in the same session** (`sessionStorage` key `bl-seen`, read by a tiny head script before first paint): `html.quick` replaces the whole entrance with a 400ms fade (`--t-quick`).

**Reduced motion** (`prefers-reduced-motion: reduce`): one 200ms opacity fade (`--t-reduced`) replaces everything. No drift, no sweep, no glow loop, no magnetic button, no pulse, no nudge; the sending line is static; the success state still swaps in place.

## 8. Do's and Don'ts

### Do
- Keep all copy verbatim: wordmark, tagline, supporting line, COMING SOON (two lines), App Store, "Be first in the room.", REQUEST ACCESS, the waves line, the confirmation lines, the share line, the footer.
- Keep the signup logic untouched: Brevo form endpoint + Supabase `join_waitlist` RPC in parallel, field names, validation, honeypot, mailto fallback. UI states wrap around it through `ui.fail()` and `ui.done()` only.
- Keep every motion value in the `--t-*` variables.

### Don't
- ❌ No hue anywhere: no accent, no coloured focus ring, no red error text.
- ❌ No new sections, nav, testimonials, feature lists, counters or scroll-driven animation.
- ❌ No rings, circles, tables or line art in the background.
- ❌ No fake social proof: no member numbers, no "online now", no claim that rooms are live.
- ❌ No libraries and no build step.
- ❌ No layout-affecting animation; no shadows or backdrop blur; no glow beyond the wordmark and the COMING SOON loop.
- ❌ No hover-only behaviour without a tap and keyboard equivalent.
- ❌ Don't edit `logoB.png`; regenerate the WebP copies from it if it ever changes.
- ❌ Never reference files outside this folder.

## 9. Responsive

| Width | Behaviour |
|---|---|
| < 480px | Form stacks (field above button, both full width). Reveal line reserves two lines. |
| ≥ 480px | Field and button on one row. |
| ≥ 600px | Reveal line reserves one line. |
| Landscape ≤ 500px tall | Compact steps: smaller logo and COMING SOON; page scrolls. |

Logo width is `min(400px, 60vw, 38vh)`, so short screens shrink the logo before anything else. Checked at 375, 390, 768 and 1440px wide, in iOS Safari (iPhone 16 Pro simulator: no input zoom, field and button stay above the keyboard, safe areas respected), with keyboard-only navigation, and under reduced motion.
