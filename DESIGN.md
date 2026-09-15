# DESIGN.md — Blacklink coming-soon

> A secret members' club meets a tactical command room. Hierarchy comes from luminance, weight and space. Never hue.

Source of truth: `BLACKLINK_MASTER_BRIEF.md` §2 (app repo, read-only). Where this file and §2 disagree, §2 wins.
Scope: the single page `index.html` in this folder. No other pages.

## 1. Visual Theme & Atmosphere

**Style**: Dark Editorial, strict monochrome
**Keywords**: exclusive, cold, tactical, still, heavy type, hairline, negative space, presence
**Tone**: restrained and confident — NOT neon, NOT glassy, NOT playful, NOT "startup gradient"
**Feel**: a black table in an unlit room. One lamp. Someone has just sat down.

**Interaction Tier**: L1 (精致静态) — deliberately, not L2. The page is one viewport with no scroll narrative, so scroll reveals, parallax and nav-scroll states have nothing to act on. This is a documented deviation from the skill's Landing Page baseline (see §8).
**Dependencies**: CSS only. No GSAP, no Lenis, no WebGL, no canvas library.

## 2. Color Palette & Roles

The palette is the §2.2 luminance ladder, unchanged. There is no accent. The primary CTA is inverse (white on black) and that inversion is the only "emphasis colour" on the page.

```css
:root {
  /* Backgrounds */
  --bg: #000000;              /* page */
  --bg-elevated: #0a0a0a;     /* ambient layer floor (background art never brighter than --surface) */
  --surface: #141414;         /* input, confirmation card */
  --surface-hover: #1c1c1c;   /* pressed/hover surface */

  /* Borders */
  --border: #262626;          /* hairlines, card and input borders */
  --border-strong: #3f3f3f;   /* focused input, active ring */

  /* Text */
  --text: #ffffff;            /* wordmark, COMING SOON, confirmation headline */
  --text-secondary: #a3a3a3;  /* tagline, pitch, error note — ~8.3:1 on black */
  --text-muted: #525252;      /* App Store label, footer, placeholder — meta only; ~2.9:1, never for copy that carries meaning */

  /* Inverse (primary CTA) */
  --inverse-bg: #ffffff;
  --inverse-text: #000000;

  /* Accent — intentionally none */
  --accent: var(--text);      /* alias only; there is no hue anywhere */

  /* RGB helpers for rgba() */
  --bg-rgb: 0, 0, 0;
  --text-rgb: 255, 255, 255;
  --border-rgb: 38, 38, 38;

  /* Semantic — expressed by copy and luminance, not colour */
  --success: var(--text);
  --error: var(--text-secondary);
  --warning: var(--text-secondary);

  color-scheme: dark;
}
```

**Color Rules:**
- Every colour in `index.html` is a `var(--…)` reference. Zero hard-coded hex outside `:root`.
- Meaningful text never uses `--text-muted`. It fails AA on black; use it only where losing the text loses nothing.
- No hue. No gradients that introduce hue. A luminance-only gradient (black → #0a0a0a) is allowed for the ambient layer floor and nowhere else.
- Ambient/background art is capped at `--border` (#262626) brightness. Content always out-luminates the background.
- Error and success states are communicated by wording, never by red/green.

## 3. Typography Rules

**Font Stack:**
```css
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;500;600&display=swap');
/* Fallbacks: "Archivo Black","Arial Black",Impact,sans-serif  |  "Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif */
```

| Role | Font | Size | Weight | Line Height | Letter Spacing | Case |
|------|------|------|--------|-------------|----------------|------|
| Display — COMING SOON | Archivo Black | clamp(40px, 13vw, 84px) | 400 | 0.95 | 0.04em | UPPER |
| Wordmark — BLACKLINK | Archivo Black | clamp(26px, 7vw, 32px) | 400 | 1.0 | 0.1em | UPPER |
| Tagline | Inter | 17px | 500 | 1.5 | 0 | sentence |
| Body / pitch | Inter | 15px | 400 | 1.5 | 0 | sentence — `--text-secondary` |
| Label — App Store, button | Inter | 13px | 500 / 600 | 1 | 0.12em | UPPER |
| Caption — footer | Inter | 12px | 400 | 1.5 | 0 | sentence — `--text-muted` |
| Error note | Inter | 12px | 400 | 1.5 | 0 | sentence — `--error` (= secondary) |
| Input | Inter | 16px | 400 | 1 | 0 | — |

**Typography Rules:**
- Display and wordmark are always uppercase with tracking; body is never uppercase except labels.
- Archivo Black is used at weight 400 only (it has one weight). Never fake-bold it.
- Display size deliberately exceeds the app's 32px scale because the web viewport is larger; the ratio between display, title and body is preserved.
- The wordmark is a lockup, not a headline: it stays at or under 32px so COMING SOON is the page's only display-size statement.
- Contrast rule: anything the reader must understand (tagline, pitch, error text) sits at `--text-secondary` or brighter (≥ 4.5:1). `--text-muted` is reserved for meta the page still works without (App Store label, footer, placeholder).
- **NEVER use**: Anton (brief alternative, not chosen), Space Grotesk, Playfair, any serif, any mono, system default sans for display.

**Text Decoration** (per `text-decoration-rules.md`, style = 极简克制 column):
- Display h1: no gradient, no glow, no text-shadow.
- Wordmark: none.
- Body: none. Links: luminance change only, no underline animation.

## 4. Component Stylings

### Primary button (white pill)
```css
.btn {
  height: 48px; padding: 0 24px;
  font: 600 13px/1 var(--font-body); letter-spacing: .12em; text-transform: uppercase;
  color: var(--inverse-text); background: var(--inverse-bg);
  border: 0; border-radius: 999px; cursor: pointer;
  transition: opacity 150ms ease-out, transform 150ms ease-out;
}
.btn:hover        { opacity: .9; }
.btn:active       { transform: scale(.98); }
.btn:focus-visible{ outline: 2px solid var(--text); outline-offset: 3px; }
.btn[disabled]    { opacity: .6; cursor: default; transform: none; }
```

### Input
```css
.field {
  height: 48px; padding: 0 16px;
  font: 400 16px/1 var(--font-body); color: var(--text);
  background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
  transition: border-color 150ms ease-out;
}
.field::placeholder { color: var(--text-muted); }
.field:hover        { border-color: var(--border-strong); }
.field:focus        { border-color: var(--border-strong); outline: none; }
.field:user-invalid { border-color: var(--border-strong); }
.field[disabled]    { opacity: .6; }
```

### Confirmation card ("You're on the list.")
```css
.done { padding: 20px 24px; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; }
.done .headline { font: 600 17px/1.5 var(--font-body); color: var(--text); }
.done .sub      { font: 400 13px/1.5 var(--font-body); color: var(--text-muted); }
/* Static. No hover (not interactive). Enters with the shared 220ms fade-up. */
```

### Links (footer only)
```css
a { color: var(--text-muted); text-decoration: none; transition: color 150ms ease-out; }
a:hover, a:focus-visible { color: var(--text-secondary); outline: none; }
a:focus-visible { outline: 1px solid var(--border-strong); outline-offset: 2px; }
```

### Navigation
None. A coming-soon page has nowhere to navigate. Do not add one.

### Tags / Badges
None on this page. If ever needed: 12px Inter 500, uppercase, `--text-muted` on `--surface`, 1px `--border`, radius 999.

## 5. Layout Principles

**Container:**
- Content column max width: 560px, centered.
- Capture (form) max width: 400px.
- Page padding: 20px sides on phone, safe-area aware; 24px top / 20px bottom on phone, 32px top / 24px bottom on desktop.
- `main` inner padding: 32px vertical on phone, 16px on desktop, so the composition also fits a 1280×900 desktop without scrolling.

**Spacing Scale** (§2.4): 4 / 8 / 12 / 16 / 24 / 32, plus 48 / 56 / 72 for the vertical rhythm between the three content groups (brand, display, capture).
- Logo → wordmark: 24 (phone) / 32 (desktop)
- Wordmark → tagline: 16 / 20
- Tagline → pitch: 8
- Pitch → COMING SOON: 56 / 72
- COMING SOON → App Store: 12
- App Store → capture: 48 / 56

**Grid:**
```css
body { min-height: 100dvh; display: flex; flex-direction: column; }
main { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.ambient { position: fixed; inset: 0; z-index: 0; pointer-events: none; }  /* background layer */
main, footer { position: relative; z-index: 1; }
```

## 6. Depth & Elevation

| Level | Treatment | Use |
|-------|-----------|-----|
| Ambient | `--bg` floor, art capped at `--border` luminance | background layer behind everything |
| Flat | `--bg`, no border | page, text |
| Hairline | 1px `--border` on `--surface` | input, confirmation card |
| Focused | 1px `--border-strong` | focused input |
| Inverse | `--inverse-bg` | primary CTA only |

No box-shadows anywhere. No glow. Depth is a two-step luminance ladder, nothing more.

## 7. Animation & Interaction

**Motion Philosophy**: §2.4 verbatim — 150–250ms, ease-out, opacity and small translate only. Nothing bouncy. Nothing continuous in the foreground.
**Tier**: L1

### Dependencies
None.

### Entrance Animation
```css
.fade-up { opacity: 0; transform: translateY(8px); animation: fade-up 220ms cubic-bezier(.16,1,.3,1) forwards; }
@keyframes fade-up { to { opacity: 1; transform: none; } }
/* One block, one animation. No per-element stagger. */
```

### Scroll Behavior
None. The page does not scroll on a phone ≥ 667px tall; where it does, nothing is tied to scroll.

### Hover & Focus States
As specified per component in §4. Every interactive element (input, button, footer link) has hover + focus-visible.

### Special Effects — ambient background layer ("The Table")
The one addition beyond the current page. Derived from the war room (§3, §4), not from a generic effect library.

- A fixed, full-viewport layer behind the content draws the war-room table as hairline geometry: one oval table outline and the 10 seat rings at the exact §4 seat coordinates (percentages of the layer).
- Rendered as inline SVG (viewBox 100×62), `vector-effect: non-scaling-stroke` on every shape so the line is exactly 1px at any scale, stroke colour `--surface` (#141414) at rest — present but barely there. On phones the SVG is drawn at 130vw and offset slightly below centre (translate -50%, -44%) so the table sits under the display line and no seat ring touches the pitch copy; on desktop it is capped at 1200px and centred.
- **Presence beat**: on a slow cadence (one event every 5–9s, randomised), a single seat ring brightens from `--surface` to `--border` (#262626) over **200ms ease-out**, holds, then returns over **200ms ease-out** after ~4s. At most one seat lit at a time. Reads as "someone just sat down at the table" — live presence, which is the product's first pillar.
- Every visible change is a discrete 200ms ease-out opacity step. There is no continuous tween, no drift, no rotation, no particles. Between beats the layer is perfectly still. This is how a background concept stays inside §2.4.
- Cap: the lit ring never exceeds `--border` luminance, so it can never compete with `--text-muted` copy.
- Implementation: CSS transition on `stroke` / `opacity` toggled by a tiny `setInterval` (~30 lines). Idle-safe: paused when `document.hidden`.

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  .fade-up { animation: none; opacity: 1; transform: none; }
  .btn, .field, a { transition: none; }
  .ambient .seat { transition: none; }   /* JS also skips the presence beat entirely */
}
```

## 8. Do's and Don'ts

### Do
- Use only the §2.2 tokens. If a colour is not in `:root`, it does not exist.
- Keep the existing copy verbatim: wordmark, tagline, pitch, COMING SOON, App Store, GET NOTIFIED, "You're on the list.", footer.
- Keep the existing email capture behaviour (endpoint constant → JSON POST; fallback → mailto + localStorage; honeypot; inline validation).
- Let the background be felt, not seen: if a first-time viewer notices the table before the wordmark, it is too bright.
- Keep every transition between 150 and 250ms with ease-out.
- Design phone-first at 375×667; desktop is the same composition with more air.
- Keep the page one viewport tall on phones from 375×667 up: viewports ≤ 720px tall on phone widths use the compact rhythm in §9.
- Ship a single self-contained `index.html` plus local image assets. No build step.

### Don't
- ❌ No hue anywhere — no accent, no coloured gradient, no coloured focus ring, no red error text.
- ❌ No glow, text-shadow, box-shadow, backdrop-filter or blur.
- ❌ No continuous ambient motion — no drifting, rotating, breathing, marquee, particles, smoke, aurora, silk, WebGL.
- ❌ No per-character / split-text / scramble / typewriter text animation on any heading.
- ❌ No magnetic buttons, cursor followers, click sparks or 3D tilt.
- ❌ No scroll-driven anything. No sticky nav, no parallax, no pin.
- ❌ No external JS libraries (GSAP, Lenis, Three.js, vue-bits ports).
- ❌ No emoji, no icon library, no stock imagery. The logo is the only image.
- ❌ No new copy, sections, feature lists, social proof or "3 wow moments". This is a coming-soon page, not a launch site.
- ❌ Never reference files outside this folder.

## 9. Responsive Behavior

**Breakpoints:** orientation decides the composition; width and height decide the scale.
| Name | Condition | Key Changes |
|------|-----------|-------------|
| Phone portrait | portrait, < 480px | One centred column. Form stacks (input above button); logo 240px; spacing at the smaller step. Unchanged reference layout. |
| Portrait, wider | portrait, 480–767px | Same column; form goes inline (input + pill on one row) |
| Tablet portrait | portrait, ≥ 768px | Same column scaled up: logo min(52vw, 440px), wordmark to 40px, display to 120px (capped by 12vh), form 480px / 52px controls |
| Landscape / desktop | landscape, ≥ 768px wide and > 500px tall | **Same single centred column**, scaled. Container min(960px, 84vw). Every size is `min(width-based, height-based)` so the column fills the screen but fits the viewport at 1366×768, 1440×900, 1920×1080 without scrolling. |
| Phone landscape | landscape, ≤ 500px tall | Same column with compact steps (logo 200px, display 40–56px). Scrolls: a 375px-tall viewport cannot hold the composition. |

**Landscape scale (all `clamp(min, min(vw, vh), max)`):**
- Logo width min(36vw, 38vh, 480px). Wordmark 28–44px via min(3vw, 4.4vh). Tagline 17–22px. Pitch 15–19px, max 44ch.
- COMING SOON 72–128px via min(8vw, 11vh): always the largest element, roughly 3× the wordmark.
- Controls 48–56px tall via 6vh; capture up to min(560px, 46vw).
- Gaps scale with vh (logo→wordmark 20–32px, pitch→display 32–64px, store→capture 28–48px) so short viewports compress rhythm before type.
- The table stays centred behind the display line, width min(100vw, 1200px).

**Touch Targets:** input and button are 48px tall (≥ 44px). Full-width on phone.
**Collapsing Strategy:** one centred column at every size and orientation. Only the scale, the form direction and the spacing steps change. Nothing is hidden.
**Short phones (≤ 720px tall, < 768px wide):** logo 180px, top padding 16, main padding 8, display and capture gaps 32, note min-height 0. Same composition, smaller steps, so a 375×667 phone still shows everything without scrolling.
**Ambient layer:** SVG uses `preserveAspectRatio="xMidYMid meet"` with an explicit width (130vw on phone, min(100vw, 1200px) on desktop) so seat percentages hold at any aspect ratio and the table always frames rather than crowds the content. Decoration never overlaps copy: on phones the table is offset below centre.

```css
@media (min-width: 480px) { form { flex-direction: row; } }
@media (min-width: 768px) and (orientation: portrait) { /* scaled single column, see table */ }
@media (orientation: landscape) and (min-width: 768px) {
  main { max-width: min(960px, 84vw); }
  .logo { width: min(36vw, 38vh, 480px); }
  .wordmark { font-size: clamp(28px, min(3vw, 4.4vh), 44px); }
  .soon { font-size: clamp(72px, min(8vw, 11vh), 128px); }
}
```
