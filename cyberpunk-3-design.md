Rebuild this design in your project. Match it exactly: same layout,
typography, color, spacing, radius, shadow, and motion. Do not invent
new visuals.

## design.md

# Cyberpunk 3 — Style Reference
> Cyberpunk: A near-black stage lit as if at night, where depth comes from glow…

**Theme:** dark

A near-black stage lit as if at night, where depth comes from glow and luminance rather than borders or shadows, and surfaces feel like instrumentation floating in void rather than paper or cards. Edges stay flat, hairline, or softly radiant, with panels lifted only one faint tonal step off the canvas, traced rather than boxed. The overall sense is cinematic restraint: vast dark space holding a few precise, glowing focal points. The ground is always near-black, cool or violet-tinted rather than neutral, and color is rationed like signal, not decoration: one or two saturated accent hues (neon, acid, jewel, or electric) are reserved strictly for the single most meaningful value, action, or status. Everything else recedes into grey, charcoal, or off-white, so brightness and hue scarcity are what create hierarchy. A single clean grotesk or mono voice, set tight and cold, with scale and weight (not color or ornament) carrying hierarchy between oversized hero numerals or headlines and small muted labels.

**Ground truth (computed from tokens + reference HTML):** dark theme · page #05080f · ink #e6f4ff · primary #4d9dff · secondary #ff2e88 · applied action color #ff2e88 · display "Geist" · body "Geist". Where the description above conflicts with these values or the Reference HTML, the tokens and HTML are authoritative.

## Tokens: Colors

| Name | Value | Token | Role | Usage | Contrast |
|------|-------|-------|------|-------|----------|
| Canvas | `#05080f` | `--gesso-canvas` | Page background, the floor everything sits on. | Outermost background: body, full-bleed sections. Mirrors Neutral 50. | n/a |
| Surface recessed | `#04060b` | `--gesso-surface-recessed` | Sunken surface below the canvas. | Inset wells: input fields, progress tracks, code blocks. | n/a |
| Surface | `#0c1422` | `--gesso-surface` | Card and panel fill, raised above the canvas. | Cards, panels, sheets, table rows. Mirrors Neutral 100. | n/a |
| Surface elevated | `#333a45` | `--gesso-surface-elevated` | Top elevation tier. | Modals, dropdowns, popovers, tooltips. | n/a |
| Divider | `rgba(255,255,255,0.04)` | `--gesso-divider` | Hairline borders and separators. | 1px rules between rows and sections. Never for text. | n/a |
| Foreground | `#e6f4ff` | `--gesso-fg` | Primary text and high-emphasis icons. | Body copy, headings, primary icons. Mirrors Neutral 900. | AA 4.5:1 on canvas (guaranteed) |
| Foreground muted | `#9aacc4` | `--gesso-fg-muted` | Secondary text. | Captions, metadata, placeholders, disabled labels. Mirrors Neutral 600. | AA 3.0:1 on canvas (guaranteed) |
| Primary | `#4d9dff` | `--gesso-primary` | Brand accent, FILL only (alias: --gesso-accent). | CTA fills, active and selected states, focus rings. 2 to 3 per screen. Do NOT use as text, reach for --gesso-accent-text. | Pair with --gesso-on-accent for the label on top. |
| On primary | `#000000` | `--gesso-on-accent` | Text and icons on a filled primary. | Label color for buttons and chips filled with --gesso-primary. | Contrast-derived against --gesso-primary. |
| Accent (as text) | `#4d9dff` | `--gesso-accent-text` | AA-safe accent for text and icons. | Use THIS for accent-colored links, headings, and icons. Use --gesso-primary for fills. | AA 4.5:1 on canvas (guaranteed). |
| Secondary | `#ff2e88` | `--gesso-secondary` | Supporting brand accent. | Secondary fills, logo discs, supporting highlights. | Pair with on-fill text per --gesso-on-accent. |
| Secondary (as text) | `#ff2e88` | `--gesso-accent-2-text` | AA-safe secondary for text. | Secondary accent used as text or icons. | AA 4.5:1 on canvas (guaranteed). |
| Neutral 50 | `#05080f` | `--gesso-neutral-50` | Page background. | Ramp access by step; prefer the role token above where one exists. | n/a |
| Neutral 100 | `#0c1422` | `--gesso-neutral-100` | Surface. | Ramp access by step; prefer the role token above where one exists. | n/a |
| Neutral 200 | `#242e3f` | `--gesso-neutral-200` | Neutral ramp step. | Ramp access by step; prefer the role token above where one exists. | n/a |
| Neutral 300 | `#3f4b5e` | `--gesso-neutral-300` | Neutral ramp step. | Ramp access by step; prefer the role token above where one exists. | n/a |
| Neutral 400 | `#5c6a7e` | `--gesso-neutral-400` | Neutral ramp step. | Ramp access by step; prefer the role token above where one exists. | n/a |
| Neutral 500 | `#7a8aa0` | `--gesso-neutral-500` | Neutral ramp step. | Ramp access by step; prefer the role token above where one exists. | n/a |
| Neutral 600 | `#9aacc4` | `--gesso-neutral-600` | Muted text and dividers. | Ramp access by step; prefer the role token above where one exists. | AA 3.0:1 on canvas. |
| Neutral 700 | `#b2c4d7` | `--gesso-neutral-700` | Neutral ramp step. | Ramp access by step; prefer the role token above where one exists. | n/a |
| Neutral 800 | `#cbdceb` | `--gesso-neutral-800` | Neutral ramp step. | Ramp access by step; prefer the role token above where one exists. | n/a |
| Neutral 900 | `#e6f4ff` | `--gesso-neutral-900` | Primary text. | Ramp access by step; prefer the role token above where one exists. | AA 4.5:1 on canvas. |
| Neutral 950 | `#e9f5ff` | `--gesso-neutral-950` | Neutral ramp step. | Ramp access by step; prefer the role token above where one exists. | n/a |
| Success | `#16A34A` | `--gesso-success` | Positive signals (gains, completed states). | Meaning only, never decoration. | AA 3.0:1 on canvas, chroma-floored distinct. |
| Warning | `#D97706` | `--gesso-warning` | Caution states. | Meaning only, never decoration. | AA 3.0:1 on canvas, chroma-floored distinct. |
| Error | `#e35151` | `--gesso-error` | Errors, destructive actions, negative signals. | Meaning only, never decoration. | AA 3.0:1 on canvas, chroma-floored distinct. |
| Data 1 | `#9d004e` | `--gesso-data-1` | Categorical data-viz series color. | Charts and series, applied in order. | n/a |
| Data 2 | `#c40063` | `--gesso-data-2` | Categorical data-viz series color. | Charts and series, applied in order. | n/a |
| Data 3 | `#ec0779` | `--gesso-data-3` | Categorical data-viz series color. | Charts and series, applied in order. | n/a |
| Data 4 | `#ff4f92` | `--gesso-data-4` | Categorical data-viz series color. | Charts and series, applied in order. | n/a |
| Data 5 | `#ff8aad` | `--gesso-data-5` | Categorical data-viz series color. | Charts and series, applied in order. | n/a |
| Data 6 | `#ffb6c9` | `--gesso-data-6` | Categorical data-viz series color. | Charts and series, applied in order. | n/a |

## Tokens: Typography

### Geist — Display. Headings, hero copy, large numerical specimens. · `--gesso-font-display`
- **Weights:** 400, 500, 600, 700
- **Line height:** 1.1
- **Letter spacing:** -0.02em
- **Role:** Display. Headings, hero copy, large numerical specimens.

### Geist — Body. Paragraphs, labels, UI chrome. · `--gesso-font-body`
- **Weights:** 400, 500, 600, 700
- **Line height:** 1.5
- **Letter spacing:** 0em
- **Role:** Body. Paragraphs, labels, UI chrome.

### Geist — Mono. Code, numerical tickers, mono-spaced metadata. · `--gesso-font-mono`
- **Weights:** 400, 500, 600, 700
- **Line height:** 1.4
- **Letter spacing:** 0em
- **Role:** Mono. Code, numerical tickers, mono-spaced metadata.

### Type Scale

| Role | Size | Line Height | Letter Spacing | Token |
|------|------|-------------|----------------|-------|
| H1 | 48px | 1.2 | — | `--gesso-text-4xl` |
| H2 | 36px | 1.2 | — | `--gesso-text-3xl` |
| H3 | 28px | 1.2 | — | `--gesso-text-2xl` |
| Body | 16px | 1.5 | — | `--gesso-text-base` |
| Caption | 12px | 1.5 | — | `--gesso-text-xs` |

## Tokens: Spacing & Shapes

**Base unit:** 4px

**Density:** comfortable

### Spacing Scale

| Name | Value | Token |
|------|-------|-------|
| space-1 | 4px | `--gesso-space-1` |
| space-2 | 8px | `--gesso-space-2` |
| space-3 | 12px | `--gesso-space-3` |
| space-4 | 16px | `--gesso-space-4` |
| space-6 | 24px | `--gesso-space-6` |
| space-8 | 32px | `--gesso-space-8` |
| space-12 | 48px | `--gesso-space-12` |
| space-16 | 64px | `--gesso-space-16` |
| space-24 | 96px | `--gesso-space-24` |
| space-32 | 128px | `--gesso-space-32` |

### Border Radius

| Element | Value |
|---------|-------|
| none | 0px |
| sm | 4px |
| md | 8px |
| lg | 16px |
| full | 9999px |

### Shadows

| Name | Value | Token |
|------|-------|-------|
| sm | `0 1px 2px rgba(0,0,0,0.05)` | `--gesso-shadow-sm` |
| md | `0 4px 12px rgba(0,0,0,0.08)` | `--gesso-shadow-md` |
| lg | `0 16px 40px rgba(0,0,0,0.12)` | `--gesso-shadow-lg` |

### Layout

- **Page max-width:** 1280px
- **Section gap:** 80px
- **Container max-width:** 1280px
- **Grid columns:** 12
- **Grid gutter:** 24px
- **Outer margin:** 64px
- **Section padding:** 80px

## Breakpoints

| Name | Min Width |
|------|-----------|
| sm | 640px |
| md | 768px |
| lg | 1024px |
| xl | 1280px |

## Components

### Container
**Role:** Page-level width constraint and 12-column grid wrapper.

Max-width var(--container-max-width) (1280px), centered via margin-inline auto, horizontal padding var(--outer-margin) (64px; drop to 24-32px below the md breakpoint). Vertical rhythm var(--section-padding) (80px) per band. Multi-column regions use display:grid with grid-template-columns: repeat(var(--grid-columns), 1fr) (12) and gap var(--grid-gutter) (24px); children span column ranges (span 6 = half, span 4 = third).

### Navigation Bar
**Role:** Top-anchored primary navigation. One per page.

Full-bleed bar, height 64-72px, inner contents constrained to var(--container-max-width) with var(--outer-margin) inline padding. Logo left, primary links centered or left-grouped, one primary CTA right. Links in --gesso-font-body weight 400, color --gesso-neutral-700 (#3F3F46); hover/active resolve to --gesso-neutral-900 (#e6f4ff). CTA is the Primary Button. Transparent over a hero, then sticky with a --gesso-neutral-50 (#05080f) fill and 1px --gesso-neutral-200 bottom border once scrolled. z-index 100.

### Hero Section
**Role:** Above-the-fold headline band. Sets the first impression.

Fills the upper 55-70% of the viewport with var(--section-padding) vertical breathing room, constrained to the Container. Headline in --gesso-font-display (Geist) at 48px, weight 600, line-height 1.05-1.1, never italic. Subcopy in body font at --gesso-text-lg, color --gesso-neutral-600 (#8fa3bd), max-width ~60ch. Primary + Secondary Button pair beneath. Left-aligned for a marketing scroll, centered for a landing hero.

### Card
**Role:** Container surface for content groupings.

Background --gesso-neutral-50 (#05080f), border 1px solid --gesso-neutral-200 (#E4E4E7), border-radius var(--gesso-radius-md) (8px), padding 24px, --gesso-shadow-sm. Body font for content; display font for any embedded headline. Text fg --gesso-neutral-900 (#e6f4ff). In a grid, cards span 3-6 of the 12 columns.

### Primary Button
**Role:** Highest-emphasis action. Reserved for the main CTA per section.

Background --gesso-primary (#4d9dff), text auto-picked for max contrast (white or near-black), padding 12px 24px, border-radius var(--gesso-radius-md) (8px), font-family --gesso-font-body, font-weight 600. Hover: mix toward --gesso-fg by 10-12%. Use 1-2 per section, never more. The reference screen applies #ff2e88 as its dominant on-screen action color; follow the Reference HTML for color application.

### Secondary Button
**Role:** Supporting action next to a primary CTA.

Background transparent, border 1.5px solid --gesso-primary (#4d9dff), text --gesso-primary, padding 12px 24px (minus 1.5px each axis to compensate for the border), border-radius var(--gesso-radius-md) (8px), body font, weight 600.

### Input
**Role:** Single-line text entry. Default form field.

Background --gesso-neutral-100 (#0c1422), border 1px solid --gesso-neutral-300 (#D4D4D8), border-radius var(--gesso-radius-md) (8px), padding 12px 16px, body font. Focus: border --gesso-primary, ring 3px --gesso-primary at 14% alpha.

### Footer
**Role:** Page-closing navigation and legal. One per page.

Full-bleed block with a top 1px --gesso-neutral-200 (#E4E4E7) divider, var(--section-padding) vertical padding, contents constrained to var(--container-max-width). Multi-column link groups (grid, 2-4 columns): group headings at body weight 600, links --gesso-neutral-600 (#8fa3bd) resolving to --gesso-neutral-900 on hover. Logo and copyright row pinned along the bottom.

### Badge
**Role:** Compact label for status, tags, counts.

Background --gesso-primary (#4d9dff) at 12% alpha, text --gesso-primary, padding 8px 12px, border-radius var(--gesso-radius-full) (9999px), font-size 12px, body font, weight 600, uppercase, letter-spacing 0.04em.

## Do's and Don'ts

### Do

- Keep the canvas true or near-black and build all depth through subtle value steps, hairlines, or soft glow
- Reserve saturated accent color exclusively for one signal: a key value, action, or status
- Let one element, a numeral, headline, or figure, dominate massively oversized against muted supporting content
- Draw charts, dividers, and controls as thin strokes, dotted lines, or flat pills with no gridlines, bevels, or card shadows
- Apply --gesso-primary (#4d9dff) to a maximum of 2-3 elements per screen: a button, a highlight, a badge. Never paint large areas with primary.
- Use --gesso-radius-md (8px) for cards and inputs, --gesso-radius-full for badges and avatars. Inner radii inside a parent: subtract the parent's padding from its radius.

### Don't

- Use more than one or two accent hues, or apply accent color decoratively
- Add drop shadows, gradients, or skeuomorphic depth to surfaces
- Set type in a serif, humanist warm, or display face
- Crowd the layout: leave generous dark space around focal elements
- Don't use Inter as the display font. It's the most overused font in tech. Pick something with character from the fontHints display list.
- Don't use #3B82F6 / indigo-600 as primary unless explicitly briefed. Default blue is the hallmark of a generic SaaS aesthetic.

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 0 | Page | `#05080f` | Default page background. The lightest surface. |
| 1 | Raised | `#0c1422` | Cards, panels, sidebars: anything that sits on top of the page. |
| 2 | Sunken | `#E4E4E7` | Inset surfaces (search bars, code blocks, disabled fields). |
| 3 | Overlay | `#05080f` | Modals and floating panels. Same hue as page; depth comes from --gesso-shadow-lg. |

## Agent Prompt Guide

**Quick Color Reference**

- Primary: #4d9dff
- Secondary: #ff2e88
- Page bg: #05080f
- Body fg: #e6f4ff
- Muted fg: #9aacc4
- Success: #16A34A

**Example Component Prompts**

1. Build a content container. max-width var(--container-max-width) (1280px), margin-inline auto, padding-inline var(--outer-margin) (64px, 24px below md). Wrap every section in it so the page shares one measure.

2. Build a responsive top navigation bar. Full-bleed, height 64-72px, inner row capped at var(--container-max-width) with var(--outer-margin) inline padding. Logo left, links centered (color #3F3F46, hover #e6f4ff), primary CTA right (bg #4d9dff, weight 600). Transparent over the hero, sticky #05080f fill + 1px #E4E4E7 border on scroll. Collapse links to a menu button below 768px.

3. Build a hero band. Constrain to var(--container-max-width) with var(--section-padding) vertical padding. Headline display font (Geist) at 48px weight 700, never italic; subcopy body font (Geist) max-width 60ch color #8fa3bd; primary + secondary CTA row beneath.

4. Build a 12-column responsive grid section. display:grid; grid-template-columns: repeat(12, 1fr); gap var(--grid-gutter) (24px); inside var(--container-max-width) + var(--outer-margin). Cards span 4 columns (3-up) on desktop, span 6 (2-up) at md, span 12 below sm.

5. Build a footer. Full-bleed with a top 1px #E4E4E7 divider, var(--section-padding) vertical padding, contents at var(--container-max-width). 3-4 link-group columns (headings weight 600, links #8fa3bd), logo + copyright row pinned along the bottom.

## Quick Start

### CSS Custom Properties

```css
:root {
  /* Colors */
  --gesso-canvas: #05080f;
  --gesso-surface-recessed: #04060b;
  --gesso-surface: #0c1422;
  --gesso-surface-elevated: #333a45;
  --gesso-divider: rgba(255,255,255,0.04);
  --gesso-fg: #e6f4ff;
  --gesso-fg-muted: #9aacc4;
  --gesso-primary: #4d9dff;
  --gesso-on-accent: #000000;
  --gesso-accent-text: #4d9dff;
  --gesso-secondary: #ff2e88;
  --gesso-accent-2-text: #ff2e88;
  --gesso-neutral-50: #05080f;
  --gesso-neutral-100: #0c1422;
  --gesso-neutral-200: #242e3f;
  --gesso-neutral-300: #3f4b5e;
  --gesso-neutral-400: #5c6a7e;
  --gesso-neutral-500: #7a8aa0;
  --gesso-neutral-600: #9aacc4;
  --gesso-neutral-700: #b2c4d7;
  --gesso-neutral-800: #cbdceb;
  --gesso-neutral-900: #e6f4ff;
  --gesso-neutral-950: #e9f5ff;
  --gesso-success: #16A34A;
  --gesso-warning: #D97706;
  --gesso-error: #e35151;
  --gesso-data-1: #9d004e;
  --gesso-data-2: #c40063;
  --gesso-data-3: #ec0779;
  --gesso-data-4: #ff4f92;
  --gesso-data-5: #ff8aad;
  --gesso-data-6: #ffb6c9;

  /* Typography — Font Families */
  --gesso-font-display: 'Geist', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --gesso-font-body: 'Geist', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --gesso-font-mono: 'Geist', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

  /* Typography — Scale */
  --gesso-text-4xl: 48px;
  --gesso-leading-4xl: 1.2;
  --gesso-text-3xl: 36px;
  --gesso-leading-3xl: 1.2;
  --gesso-text-2xl: 28px;
  --gesso-leading-2xl: 1.2;
  --gesso-text-base: 16px;
  --gesso-leading-base: 1.5;
  --gesso-text-xs: 12px;
  --gesso-leading-xs: 1.5;

  /* Typography — Weights */
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Spacing */
  --spacing-unit: 4px;
  --gesso-space-1: 4px;
  --gesso-space-2: 8px;
  --gesso-space-3: 12px;
  --gesso-space-4: 16px;
  --gesso-space-6: 24px;
  --gesso-space-8: 32px;
  --gesso-space-12: 48px;
  --gesso-space-16: 64px;
  --gesso-space-24: 96px;
  --gesso-space-32: 128px;

  /* Layout */
  --page-max-width: 1280px;
  --container-max-width: 1280px;
  --grid-columns: 12;
  --grid-gutter: 24px;
  --outer-margin: 64px;
  --section-padding: 80px;
  --section-gap: 80px;

  /* Breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;

  /* Border Radius */
  --radius-none: 0px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-full: 9999px;

  /* Shadows */
  --gesso-shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --gesso-shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --gesso-shadow-lg: 0 16px 40px rgba(0,0,0,0.12);

  /* Surfaces */
  --surface-page: #05080f;
  --surface-raised: #0c1422;
  --surface-sunken: #E4E4E7;
  --surface-overlay: #05080f;
}
```

### Tailwind v4

```css
@theme {
  /* Colors */
  --gesso-canvas: #05080f;
  --gesso-surface-recessed: #04060b;
  --gesso-surface: #0c1422;
  --gesso-surface-elevated: #333a45;
  --gesso-divider: rgba(255,255,255,0.04);
  --gesso-fg: #e6f4ff;
  --gesso-fg-muted: #9aacc4;
  --gesso-primary: #4d9dff;
  --gesso-on-accent: #000000;
  --gesso-accent-text: #4d9dff;
  --gesso-secondary: #ff2e88;
  --gesso-accent-2-text: #ff2e88;
  --gesso-neutral-50: #05080f;
  --gesso-neutral-100: #0c1422;
  --gesso-neutral-200: #242e3f;
  --gesso-neutral-300: #3f4b5e;
  --gesso-neutral-400: #5c6a7e;
  --gesso-neutral-500: #7a8aa0;
  --gesso-neutral-600: #9aacc4;
  --gesso-neutral-700: #b2c4d7;
  --gesso-neutral-800: #cbdceb;
  --gesso-neutral-900: #e6f4ff;
  --gesso-neutral-950: #e9f5ff;
  --gesso-success: #16A34A;
  --gesso-warning: #D97706;
  --gesso-error: #e35151;
  --gesso-data-1: #9d004e;
  --gesso-data-2: #c40063;
  --gesso-data-3: #ec0779;
  --gesso-data-4: #ff4f92;
  --gesso-data-5: #ff8aad;
  --gesso-data-6: #ffb6c9;

  /* Typography */
  --gesso-font-display: 'Geist', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --gesso-font-body: 'Geist', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --gesso-font-mono: 'Geist', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

  /* Typography — Scale */
  --gesso-text-4xl: 48px;
  --gesso-leading-4xl: 1.2;
  --gesso-text-3xl: 36px;
  --gesso-leading-3xl: 1.2;
  --gesso-text-2xl: 28px;
  --gesso-leading-2xl: 1.2;
  --gesso-text-base: 16px;
  --gesso-leading-base: 1.5;
  --gesso-text-xs: 12px;
  --gesso-leading-xs: 1.5;

  /* Spacing */
  --gesso-space-1: 4px;
  --gesso-space-2: 8px;
  --gesso-space-3: 12px;
  --gesso-space-4: 16px;
  --gesso-space-6: 24px;
  --gesso-space-8: 32px;
  --gesso-space-12: 48px;
  --gesso-space-16: 64px;
  --gesso-space-24: 96px;
  --gesso-space-32: 128px;

  /* Border Radius */
  --radius-none: 0px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-full: 9999px;

  /* Shadows */
  --gesso-shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --gesso-shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --gesso-shadow-lg: 0 16px 40px rgba(0,0,0,0.12);

  /* Layout */
  --container-max-width: 1280px;
  --grid-columns: 12;
  --grid-gutter: 24px;
  --outer-margin: 64px;
  --section-padding: 80px;

  /* Breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}
```


## Tokens (JSON)

```json
{
  "color": {
    "neutral": {
      "50": "#05080f",
      "100": "#0c1422",
      "200": "#E4E4E7",
      "300": "#D4D4D8",
      "400": "#A1A1AA",
      "500": "#71717A",
      "600": "#8fa3bd",
      "700": "#3F3F46",
      "800": "#27272A",
      "900": "#e6f4ff",
      "950": "#09090B"
    },
    "primary": "#4d9dff",
    "semantic": {
      "error": "#DC2626",
      "success": "#16A34A",
      "warning": "#D97706"
    },
    "secondary": "#ff2e88"
  },
  "motion": {
    "easing": {
      "default": "cubic-bezier(0.2, 0, 0, 1)",
      "emphasis": "cubic-bezier(0.3, 0, 0, 1)"
    },
    "duration": {
      "base": "250ms",
      "fast": "150ms",
      "slow": "400ms"
    }
  },
  "radius": {
    "lg": "16px",
    "md": "8px",
    "sm": "4px",
    "full": "9999px",
    "none": "0"
  },
  "shadow": {
    "lg": "0 16px 40px rgba(0,0,0,0.12)",
    "md": "0 4px 12px rgba(0,0,0,0.08)",
    "sm": "0 1px 2px rgba(0,0,0,0.05)"
  },
  "spacing": {
    "unit": 4,
    "scale": {
      "1": "4px",
      "2": "8px",
      "3": "12px",
      "4": "16px",
      "6": "24px",
      "8": "32px",
      "12": "48px",
      "16": "64px",
      "24": "96px",
      "32": "128px"
    }
  },
  "typeface": {
    "body": "Geist",
    "mono": "Geist",
    "scale": {
      "lg": "18px",
      "sm": "14px",
      "xl": "22px",
      "xs": "12px",
      "2xl": "28px",
      "3xl": "36px",
      "4xl": "48px",
      "base": "16px"
    },
    "display": "Geist",
    "weights": [
      400,
      500,
      600,
      700
    ],
    "bodyWeight": 400,
    "displayWeight": 600
  }
}
```

## Reference HTML

```html
<!DOCTYPE html>
<html lang="ru">
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap"><style id="gesso-link-reset">:where(a){color:inherit;text-decoration:none}</style>
<meta name="gesso-pipeline" content="direct">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CyberStore — Ноутбуки, ПК и комплектующие · Бишкек</title>
<style>
  :root{
    --gesso-canvas:#05080f;
    --gesso-surface:#0c1422;
    --gesso-surface-2:#101c30;
    --gesso-fg:#e6f4ff;
    --gesso-fg-muted:#8fa3bd;
    --gesso-accent:#4d9dff;
    --gesso-on-accent:#04101f;
    --gesso-accent-2:#ff2e88;
    --gesso-divider:#1b3358;
    --font-display:"Satoshi","Hanken Grotesk",sans-serif;
    --font-body:"Hanken Grotesk",sans-serif;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html{background:var(--gesso-canvas)}
  body{
    background:var(--gesso-canvas);
    color:var(--gesso-fg);
    font-family:var(--font-body);
    font-weight:400;
    font-size:15px;
    line-height:1.55;
    -webkit-font-smoothing:antialiased;
    overflow-x:hidden;
  }
  /* circuit board texture */
  body::before{
    content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
    background-image:
      linear-gradient(var(--gesso-divider) 1px,transparent 1px),
      linear-gradient(90deg,var(--gesso-divider) 1px,transparent 1px);
    background-size:64px 64px;
    opacity:.10;
  }
  body::after{
    content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
    background:radial-gradient(900px 500px at 75% -10%,rgba(77,157,255,.14),transparent 60%),
               radial-gradient(700px 400px at 5% 40%,rgba(77,157,255,.06),transparent 60%);
  }
  .wrap{max-width:1280px;margin:0 auto;padding:0 48px;position:relative;z-index:1}
  a{color:inherit;text-decoration:none}
  .ic{width: 16px;height: 16px;display:inline-block;vertical-align:-3px;flex:none}
  .ic-lg{width: 24px;height: 24px}
  .ic-xl{width: 32px;height: 32px}

  /* ============ HEADER ============ */
  header{
    position:sticky;top:0;z-index:50;
    background:rgba(5,8,15,.82);
    backdrop-filter:blur(14px);
    border-bottom:1px solid var(--gesso-divider);
  }
  .nav{display:flex;align-items:center;gap:40px;height:72px}
  .logo{display:flex;align-items:center;gap:12px;font-family:var(--font-display);font-weight:900;font-size:19px;letter-spacing:.06em}
  .logo-mark{
    width:34px;height:34px;border:1px solid var(--gesso-accent);border-radius:8px;
    display:grid;place-items:center;color:var(--gesso-accent);
    box-shadow:0 0 14px rgba(77,157,255,.45),inset 0 0 10px rgba(77,157,255,.18);
  }
  .logo span em{font-style:normal;color:var(--gesso-accent)}
  .nav-links{display:flex;gap:8px;margin-left:16px;flex:1}
  .nav-links a{
    font-family:var(--font-display);font-weight:500;font-size:13.5px;letter-spacing:.1em;text-transform:uppercase;
    color:var(--gesso-fg-muted);padding:9px 16px;border-radius:6px;border:1px solid transparent;
    display:flex;align-items:center;gap:8px;transition:color .15s;
  }
  .nav-links a:hover{color:var(--gesso-fg)}
  .nav-links a.active{
    color:var(--gesso-accent);border-color:var(--gesso-divider);background:var(--gesso-surface);
  }
  .nav-cta{
    display:flex;align-items:center;gap:10px;
    font-family:var(--font-display);font-weight:700;font-size:13px;letter-spacing:.06em;
    color:var(--gesso-on-accent);background:var(--gesso-accent);
    padding:11px 20px;border-radius:8px;
    box-shadow:0 0 20px rgba(77,157,255,.45);
  }
  .nav-hours{font-size:12px;color:var(--gesso-fg-muted);text-align:right;line-height:1.4}
  .nav-hours b{color:var(--gesso-fg);font-weight:500}

  /* ============ HERO ============ */
  .hero{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:64px;align-items:center;padding:88px 0 80px;position:relative}
  .hero-kicker{
    display:inline-flex;align-items:center;gap:10px;
    font-family:var(--font-display);font-weight:500;font-size:12px;letter-spacing:.22em;text-transform:uppercase;
    color:var(--gesso-accent);
    border:1px solid var(--gesso-divider);border-radius:100px;padding:8px 18px;
    background:rgba(77,157,255,.06);
  }
  .pulse{width:7px;height:7px;border-radius:50%;background:var(--gesso-accent);box-shadow:0 0 8px var(--gesso-accent)}
  .hero h1{
    font-family:var(--font-display);font-weight:900;
    font-size:84px;line-height:.94;letter-spacing:-.02em;
    margin:28px 0 24px;
  }
  .hero h1 .glow{
    color:var(--gesso-accent);
    text-shadow:0 0 32px rgba(77,157,255,.65),0 0 80px rgba(77,157,255,.25);
  }
  .hero h1 .dim{color:var(--gesso-fg-muted);display:block;font-weight:500;font-size:26px;letter-spacing:.14em;text-transform:uppercase;margin-top:18px}
  .hero-sub{color:var(--gesso-fg-muted);font-size:17px;max-width:520px}
  .hero-sub b{color:var(--gesso-fg);font-weight:500}
  .hero-actions{display:flex;gap:14px;margin-top:40px;align-items:center;flex-wrap:wrap}
  .btn-primary{
    display:inline-flex;align-items:center;gap:10px;
    font-family:var(--font-display);font-weight:700;font-size:15px;letter-spacing:.03em;
    color:var(--gesso-on-accent);background:var(--gesso-accent);
    padding:16px 30px;border-radius:10px;
    box-shadow:0 0 28px rgba(77,157,255,.5);
    transition:box-shadow .15s;
  }
  .btn-primary:hover{box-shadow:0 0 44px rgba(77,157,255,.75)}
  .btn-ghost{
    display:inline-flex;align-items:center;gap:10px;
    font-family:var(--font-display);font-weight:500;font-size:14px;letter-spacing:.04em;
    color:var(--gesso-fg);border:1px solid var(--gesso-divider);background:var(--gesso-surface);
    padding:15px 26px;border-radius:10px;
  }
  .btn-ghost:hover{border-color:var(--gesso-accent)}
  .hero-stats{display:flex;gap:0;margin-top:56px;border-top:1px solid var(--gesso-divider);padding-top:28px}
  .hero-stat{padding-right:36px;margin-right:36px;border-right:1px solid var(--gesso-divider)}
  .hero-stat:last-child{border-right:none;margin-right:0;padding-right:0}
  .hero-stat .n{font-family:var(--font-display);font-weight:700;font-size:30px;color:var(--gesso-fg)}
  .hero-stat .n em{font-style:normal;color:var(--gesso-accent)}
  .hero-stat .l{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--gesso-fg-muted);margin-top:4px}
  .hero-visual{position:relative}
  .hero-visual .frame{
    position:relative;border:1px solid var(--gesso-divider);border-radius:16px;overflow:hidden;
    background:var(--gesso-surface);
  }
  .hero-visual .frame::after{
    content:"";position:absolute;inset:0;border-radius:16px;pointer-events:none;
    box-shadow:inset 0 0 60px rgba(77,157,255,.12);
  }
  .hero-visual img{width:100%;height:420px;object-fit:cover;display:block;filter:saturate(1.1) contrast(1.05)}
  .hero-tag{
    position:absolute;left:20px;bottom:20px;
    display:flex;align-items:center;gap:10px;
    background:rgba(5,8,15,.85);border:1px solid var(--gesso-accent);border-radius:10px;
    padding:12px 18px;backdrop-filter:blur(8px);
  }
  .hero-tag .t1{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gesso-fg-muted)}
  .hero-tag .t2{font-family:var(--font-display);font-weight:700;font-size:18px;color:var(--gesso-accent)}
  .hero-chip{
    position:absolute;top:-16px;right:-12px;
    background:var(--gesso-surface-2);border:1px solid var(--gesso-divider);border-radius:100px;
    padding:10px 18px;font-family:var(--font-display);font-weight:700;font-size:13px;
    color:var(--gesso-fg);display:flex;align-items:center;gap:8px;
  }
  .hero-chip .ic{color:var(--gesso-accent)}

  /* ============ SECTION HEADS ============ */
  .sec-head{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;margin-bottom:36px}
  .sec-label{font-family:var(--font-display);font-weight:500;font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--gesso-accent);display:flex;align-items:center;gap:12px}
  .sec-label::before{content:"";width:28px;height:1px;background:var(--gesso-accent)}
  .sec-title{font-family:var(--font-display);font-weight:900;font-size:42px;letter-spacing:-.01em;line-height:1.05;margin-top:12px}
  .sec-side{font-size:14px;color:var(--gesso-fg-muted);max-width:320px;text-align:right;line-height:1.6}

  /* ============ FLASH DEALS ============ */
  .deals{padding:24px 0 88px}
  .deals-panel{
    border:1px solid var(--gesso-divider);border-radius:18px;background:var(--gesso-surface);
    padding:36px;position:relative;overflow:hidden;
  }
  .deals-panel::before{
    content:"";position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,var(--gesso-accent),transparent);
    box-shadow:0 0 18px rgba(77,157,255,.6);
  }
  .deals-top{display:flex;align-items:center;justify-content:space-between;gap:24px;margin-bottom:32px;flex-wrap:wrap}
  .deals-live{display:flex;align-items:center;gap:14px}
  .deals-live .badge{
    font-family:var(--font-display);font-weight:700;font-size:11px;letter-spacing:.2em;text-transform:uppercase;
    color:var(--gesso-accent-2);border:1px solid rgba(255,46,136,.45);border-radius:100px;padding:7px 16px;
    box-shadow:0 0 14px rgba(255,46,136,.25);
    display:inline-flex;align-items:center;gap:8px;
  }
  .deals-live .pulse{background:var(--gesso-accent-2);box-shadow:0 0 8px var(--gesso-accent-2)}
  .deals-live h3{font-family:var(--font-display);font-weight:700;font-size:26px;letter-spacing:-.01em}
  .countdown{display:flex;align-items:center;gap:10px}
  .cd-label{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--gesso-fg-muted);margin-right:8px}
  .cd-cell{
    min-width:56px;text-align:center;
    border:1px solid var(--gesso-divider);border-radius:10px;background:var(--gesso-canvas);
    padding:8px 6px 6px;
  }
  .cd-cell .v{font-family:var(--font-display);font-weight:700;font-size:24px;color:var(--gesso-fg);line-height:1}
  .cd-cell .k{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--gesso-fg-muted);margin-top:3px}
  .cd-sep{color:var(--gesso-accent);font-family:var(--font-display);font-weight:700;font-size:22px;align-self:center;padding-bottom:14px}
  .car-controls{display:flex;gap:10px}
  .car-btn{
    width:42px;height:42px;border-radius:10px;border:1px solid var(--gesso-divider);
    background:var(--gesso-canvas);color:var(--gesso-fg);display:grid;place-items:center;
  }
  .car-btn:hover{border-color:var(--gesso-accent);color:var(--gesso-accent)}
  .deal-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
  .deal-card{
    border:1px solid var(--gesso-divider);border-radius:14px;background:var(--gesso-canvas);
    overflow:hidden;display:flex;flex-direction:column;position:relative;
    transition:border-color .15s;
  }
  .deal-card:hover{border-color:rgba(77,157,255,.55);box-shadow:0 0 24px rgba(77,157,255,.15)}
  .deal-img{position:relative}
  .deal-img img{width:100%;height:190px;object-fit:cover;display:block}
  .deal-off{
    position:absolute;top:14px;left:14px;
    font-family:var(--font-display);font-weight:700;font-size:12px;letter-spacing:.06em;
    color:var(--gesso-on-accent);background:var(--gesso-accent);border-radius:6px;padding:5px 10px;
    box-shadow:0 0 16px rgba(77,157,255,.55);
  }
  .deal-body{padding:20px;display:flex;flex-direction:column;gap:8px;flex:1}
  .deal-cat{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--gesso-fg-muted)}
  .deal-name{font-family:var(--font-display);font-weight:700;font-size:17px;line-height:1.3}
  .deal-specs{font-size:12.5px;color:var(--gesso-fg-muted);line-height:1.6}
  .deal-prices{display:flex;align-items:baseline;gap:10px;margin-top:auto;padding-top:14px}
  .deal-prices .now{font-family:var(--font-display);font-weight:700;font-size:24px;color:var(--gesso-accent)}
  .deal-prices .old{font-size:14px;color:var(--gesso-fg-muted);text-decoration:line-through}
  .deal-pay{font-size:12px;color:var(--gesso-fg-muted)}
  .deal-pay b{color:var(--gesso-fg);font-weight:500}
  .deal-buy{
    margin-top:14px;display:flex;align-items:center;justify-content:center;gap:8px;
    border:1px solid var(--gesso-divider);border-radius:9px;padding:11px;
    font-family:var(--font-display);font-weight:700;font-size:13px;letter-spacing:.03em;color:var(--gesso-fg);
  }
  .deal-buy .ic{color:var(--gesso-accent)}
  .deal-buy:hover{border-color:var(--gesso-accent);box-shadow:0 0 14px rgba(77,157,255,.25)}
  .car-dots{display:flex;gap:8px;justify-content:center;margin-top:26px}
  .car-dots i{width:22px;height:3px;border-radius:2px;background:var(--gesso-divider)}
  .car-dots i.on{background:var(--gesso-accent);box-shadow:0 0 8px rgba(77,157,255,.6)}

  /* ============ ADVANTAGES ============ */
  .adv{padding:24px 0 88px}
  .adv-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
  .adv-card{
    border:1px solid var(--gesso-divider);border-radius:16px;background:var(--gesso-surface);
    padding:32px;position:relative;
  }
  .adv-card .tile{
    width:52px;height:52px;border-radius:12px;border:1px solid var(--gesso-divider);
    background:rgba(77,157,255,.08);color:var(--gesso-accent);
    display:grid;place-items:center;margin-bottom:22px;
  }
  .adv-card h4{font-family:var(--font-display);font-weight:700;font-size:20px;margin-bottom:8px}
  .adv-card p{font-size:14px;color:var(--gesso-fg-muted)}
  .adv-card .idx{
    position:absolute;top:26px;right:28px;
    font-family:var(--font-display);font-weight:900;font-size:44px;color:var(--gesso-divider);
    line-height:1;
  }

  /* ============ CREDIT STRIP ============ */
  .credit{padding:24px 0 88px}
  .credit-panel{
    border:1px solid var(--gesso-divider);border-radius:18px;background:var(--gesso-surface);
    display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);overflow:hidden;
  }
  .credit-left{padding:44px;border-right:1px solid var(--gesso-divider)}
  .credit-left h3{font-family:var(--font-display);font-weight:900;font-size:34px;line-height:1.1;margin:14px 0 16px}
  .credit-left h3 em{font-style:normal;color:var(--gesso-accent);text-shadow:0 0 24px rgba(77,157,255,.5)}
  .credit-left p{color:var(--gesso-fg-muted);font-size:14.5px}
  .credit-right{padding:44px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;align-content:center}
  .plan{
    border:1px solid var(--gesso-divider);border-radius:12px;background:var(--gesso-canvas);
    padding:22px 20px;text-align:left;
  }
  .plan .term{font-family:var(--font-display);font-weight:700;font-size:24px;color:var(--gesso-fg)}
  .plan .term em{font-style:normal;color:var(--gesso-accent)}
  .plan .rate{font-size:12px;color:var(--gesso-fg-muted);margin-top:4px}
  .plan .mark{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gesso-accent);margin-top:12px;display:block}

  /* ============ WA BANNER ============ */
  .cta{padding:24px 0 96px}
  .cta-panel{
    border:1px solid rgba(77,157,255,.4);border-radius:18px;
    background:radial-gradient(700px 260px at 85% 50%,rgba(77,157,255,.12),transparent 65%),var(--gesso-surface);
    padding:52px 56px;display:flex;align-items:center;justify-content:space-between;gap:40px;
    box-shadow:0 0 40px rgba(77,157,255,.08);
  }
  .cta-panel h3{font-family:var(--font-display);font-weight:900;font-size:38px;line-height:1.08;letter-spacing:-.01em;margin:12px 0 12px}
  .cta-panel p{color:var(--gesso-fg-muted);font-size:15px;max-width:520px}
  .cta-panel p b{color:var(--gesso-fg);font-weight:500}
  .cta-btn{
    display:inline-flex;align-items:center;gap:12px;flex:none;
    font-family:var(--font-display);font-weight:700;font-size:16px;
    color:var(--gesso-on-accent);background:var(--gesso-accent);
    padding:20px 34px;border-radius:12px;
    box-shadow:0 0 32px rgba(77,157,255,.55);
  }
  .cta-btn:hover{box-shadow:0 0 52px rgba(77,157,255,.8)}
  .cta-btn .ic-lg{width: 24px;height: 24px}

  /* ============ FOOTER ============ */
  footer{border-top:1px solid var(--gesso-divider);padding:52px 0 40px;background:rgba(12,20,34,.5)}
  .foot-grid{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,3fr) minmax(0,3fr) minmax(0,2fr);gap:40px}
  .foot-grid h5{font-family:var(--font-display);font-weight:700;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--gesso-fg);margin-bottom:18px}
  .foot-grid p, .foot-grid a{font-size:13.5px;color:var(--gesso-fg-muted);line-height:1.9;display:block}
  .foot-grid a:hover{color:var(--gesso-accent)}
  .foot-line{display:flex;align-items:center;gap:10px;color:var(--gesso-fg-muted);font-size:13.5px;line-height:1.9}
  .foot-line .ic{color:var(--gesso-accent)}
  .foot-bottom{border-top:1px solid var(--gesso-divider);margin-top:40px;padding-top:24px;display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--gesso-fg-muted)}
  .foot-bottom b{font-family:var(--font-display);letter-spacing:.08em;color:var(--gesso-fg-muted)}
</style>
<style>/* gesso-icon-base v1 */
.ic { display: inline-block; width: 16px; height: 16px; vertical-align: -0.125em; flex-shrink: 0; line-height: 0; }
.ic svg { width: 100%; height: 100%; display: block; }
svg.ic { width: 16px; height: 16px; display: inline-block; vertical-align: -0.125em; flex-shrink: 0; }
.ic[data-icon-style="line"] { stroke-width: var(--ic-stroke, 2); }
.ic[data-icon-style="line"] svg path, .ic[data-icon-style="line"] svg circle, .ic[data-icon-style="line"] svg rect, .ic[data-icon-style="line"] svg line, .ic[data-icon-style="line"] svg polyline, .ic[data-icon-style="line"] svg polygon { stroke-width: inherit; }
.ic-sm { --ic-stroke: 2.25; }
.ic-xs { --ic-stroke: 2.5; }
svg.ic-lg, .ic-lg svg { width: 24px; height: 24px; }
svg.ic-xl, .ic-xl svg { width: 32px; height: 32px; }
svg.ic-2xl, .ic-2xl svg { width: 32px; height: 32px; }
.ic-lg { --ic-stroke: 1.75; }
.ic-xl { --ic-stroke: 1.5; }
.ic-2xl { --ic-stroke: 1.5; }
</style>
<style id="gesso-responsive-shell">html,body{width:100%!important;max-width:100%!important;min-width:0;overflow-x:hidden}@media (max-width:1279.98px){*{min-width:0}h1,h2,h3,h4,h5,h6,p,td,th{min-width:min-content}}@media (min-width:1280px){*{min-width:auto}:where(nav,header){column-gap:24px}:where(nav a,header a){white-space:nowrap}:where(header nav){flex-wrap:wrap}}img,svg,video,canvas,iframe,table{max-width:100%}</style><style id="gesso-mobile-web-layer">.gesso-nav-check,.gesso-nav-burger{display:none}@media (max-width: 480px){nav,nav ul,header ul{flex-wrap:wrap}nav a,header ul a{display:inline-block}table{display:block;overflow-x:auto;min-width:0!important;max-width:100%}[data-gesso-flexwrap]{flex-wrap:wrap}h1,h2,h3{overflow-wrap:break-word}[data-gesso-pinned-height]{height:auto!important;min-height:0!important}.gesso-nav-check{display:block;position:absolute;width:1px;height:1px;margin:0;opacity:0;pointer-events:none}.gesso-nav-check:focus-visible+.gesso-nav-burger{outline:2px solid currentColor;outline-offset:2px}.gesso-nav-burger{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;cursor:pointer;flex-shrink:0;border-radius:8px}.gesso-nav-burger span{display:block;position:relative;width:18px;height:2px;border-radius:1px;background:currentColor}.gesso-nav-burger span::before,.gesso-nav-burger span::after{content:"";position:absolute;left:0;width:18px;height:2px;border-radius:1px;background:currentColor;transition:transform 150ms ease}.gesso-nav-burger span::before{top:-6px}.gesso-nav-burger span::after{top:6px}.gesso-nav-check:checked~.gesso-nav-burger span{background:transparent}.gesso-nav-check:checked~.gesso-nav-burger span::before{transform:translateY(6px) rotate(45deg)}.gesso-nav-check:checked~.gesso-nav-burger span::after{transform:translateY(-6px) rotate(-45deg)}[data-gesso-navlinks]{display:none!important}.gesso-nav-check:checked~[data-gesso-navlinks]{display:flex!important;flex-direction:column;align-items:stretch;flex-basis:100%;min-width:100%;order:99}.wrap{width:100%!important;max-width:100%!important}.nav{flex-wrap:wrap}.logo{flex-wrap:wrap}.nav-links{flex-wrap:wrap}.nav-links a{flex-wrap:wrap}.nav-cta{flex-wrap:wrap}.hero{grid-template-columns:1fr!important}.hero>*{grid-column:1/-1!important;grid-row:auto!important}.hero-kicker{flex-wrap:wrap}.btn-primary{flex-wrap:wrap}.btn-ghost{flex-wrap:wrap}.hero-stats{flex-wrap:wrap}.hero-tag{flex-wrap:wrap}.hero-chip{flex-wrap:wrap}.sec-head{flex-wrap:wrap}.sec-label{flex-wrap:wrap}.deals-live{flex-wrap:wrap}.deals-live .badge{flex-wrap:wrap}.countdown{flex-wrap:wrap}.car-controls{flex-wrap:wrap}.deal-grid{grid-template-columns:1fr!important}.deal-grid>*{grid-column:1/-1!important;grid-row:auto!important}.deal-prices{flex-wrap:wrap}.deal-buy{flex-wrap:wrap}.car-dots{flex-wrap:wrap}.adv-grid{grid-template-columns:1fr!important}.adv-grid>*{grid-column:1/-1!important;grid-row:auto!important}.credit-panel{grid-template-columns:1fr!important}.credit-panel>*{grid-column:1/-1!important;grid-row:auto!important}.credit-right{grid-template-columns:1fr!important}.credit-right>*{grid-column:1/-1!important;grid-row:auto!important}.cta-panel{flex-wrap:wrap}.cta-btn{flex-wrap:wrap}.foot-grid{grid-template-columns:1fr!important}.foot-grid>*{grid-column:1/-1!important;grid-row:auto!important}.foot-line{flex-wrap:wrap}.foot-bottom{flex-wrap:wrap}}@media (prefers-reduced-motion: reduce){.gesso-nav-burger span::before,.gesso-nav-burger span::after{transition:none}}</style><!--gesso-fonts:start--><style id="gesso-font-lock">:root{--gesso-font-display:"Geist", system-ui, -apple-system, sans-serif !important;--gesso-font-body:"Geist", system-ui, -apple-system, sans-serif !important;--gesso-font-mono:"Geist", ui-monospace, "JetBrains Mono", monospace !important;}</style><!--gesso-fonts:end-->
</head>
<body data-brief-role="screen" data-brief-id="screen-root">

<header data-brief-id="header-cyberstore-9-00-22" data-brief-role="header">
  <div class="wrap nav">
    <a class="logo" href="#" data-brief-id="button-cyberstore" data-brief-role="button">
      <span class="logo-mark"><svg data-icon="tabler/cpu" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic ic-lg" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M5 6a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1z"></path><path d="M9 9h6v6H9zm-6 1h2m-2 4h2m5-11v2m4-2v2m7 5h-2m2 4h-2m-5 7v-2m-4 2v-2"></path></g></svg></span>
      <span>CYBER<em>STORE</em></span>
    </a>
    <nav class="nav-links" data-brief-id="nav-top" data-brief-role="nav-top">
      <a class="active" href="#" data-brief-id="button-3" data-brief-role="button"><svg data-icon="tabler/home" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12H3l9-9l9 9h-2M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"></path><path d="M9 21v-6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v6"></path></g></svg>Главная</a>
      <a href="#" data-brief-id="button-4" data-brief-role="button"><svg data-icon="tabler/layout-grid" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M4 5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1zm10 0a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1zM4 15a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1zm10 0a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1z"></path></svg>Каталог</a>
      <a href="#" data-brief-id="button-5" data-brief-role="button"><svg data-icon="tabler/map-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11a3 3 0 1 0 6 0a3 3 0 0 0-6 0"></path><path d="M17.657 16.657L13.414 20.9a2 2 0 0 1-2.827 0l-4.244-4.243a8 8 0 1 1 11.314 0"></path></g></svg>Контакты</a>
    </nav>
    <div class="nav-hours">Ежедневно<br><b>9:00 – 22:00</b></div>
    <a class="nav-cta" href="https://wa.me/996700000000?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5!%20%D0%A5%D0%BE%D1%87%D1%83%20%D0%BE%D1%84%D0%BE%D1%80%D0%BC%D0%B8%D1%82%D1%8C%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%20%D0%B2%20CyberStore" data-brief-id="button-6" data-brief-role="button">
      <svg data-icon="tabler/brand-whatsapp" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m3 21l1.65-3.8a9 9 0 1 1 3.4 2.9z"></path><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0za5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"></path></g></svg>Заказать
    </a>
  </div>
</header>

<section class="wrap hero" data-brief-id="section" data-brief-role="section">
  <div>
    <span class="hero-kicker"><span class="pulse"></span>Бишкек · Айни 31 · Рассрочка 18+</span>
    <h1>
      Твоя техника.<br>
      <span class="glow">Твои правила.</span>
      <span class="dim">Ноутбуки · ПК · Комплектующие</span>
    </h1>
    <p class="hero-sub">
      Официальный магазин электроники в Бишкеке. <b>Рассрочка с банком и без банка — нужен только паспорт.</b> Бесплатная доставка по всему Кыргызстану.
    </p>
    <div class="hero-actions">
      <a class="btn-primary" href="https://wa.me/996700000000?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5!%20%D0%A5%D0%BE%D1%87%D1%83%20%D0%BF%D0%BE%D0%B4%D0%BE%D0%B1%D1%80%D0%B0%D1%82%D1%8C%20%D0%BD%D0%BE%D1%83%D1%82%D0%B1%D1%83%D0%BA%20%D0%B2%20CyberStore" data-brief-id="button-whatsapp" data-brief-role="button">
        <svg data-icon="tabler/brand-whatsapp" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic ic-lg" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m3 21l1.65-3.8a9 9 0 1 1 3.4 2.9z"></path><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0za5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"></path></g></svg>Заказать через WhatsApp
      </a>
      <a class="btn-ghost" href="#" data-brief-id="button-7" data-brief-role="button">
        Смотреть каталог<svg data-icon="tabler/arrow-right" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M5 12h14m-6 6l6-6m-6-6l6 6"></path></svg>
      </a>
    </div>
    <div class="hero-stats">
      <div class="hero-stat" data-brief-id="card-500" data-brief-role="card"><div class="n"><em>500+</em></div><div class="l">Отзывов клиентов</div></div>
      <div class="hero-stat" data-brief-id="card-0-0" data-brief-role="card"><div class="n">0 ₽<em>/0%</em></div><div class="l">Первый взнос по акции</div></div>
      <div class="hero-stat" data-brief-id="card-24-7" data-brief-role="card"><div class="n">24/7</div><div class="l">Приём заказов онлайн</div></div>
      <div class="hero-stat" data-brief-id="card" data-brief-role="card"><div class="n">По КР</div><div class="l">Бесплатная доставка</div></div>
    </div>
  </div>
  <div class="hero-visual">
    <div class="frame" data-brief-id="card-2" data-brief-role="card">
      <img src="https://rpreisbpsxrjwqsfeggf.supabase.co/storage/v1/object/public/direction-images/directions/c1533352-8e8d-4656-ac97-8c295224d7cc/50ba09bb0e04.jpg" data-photo-aspect="hero" alt="Игровой компьютер с неоновой подсветкой" style="max-width:100%" data-stock-provider="pexels" data-stock-page="https://www.pexels.com/photo/black-flat-screen-computer-monitor-and-keyboard-9794458/" data-stock-photographer="Lynde" >
    </div>
    <div class="hero-chip" data-brief-id="card-12" data-brief-role="card"><svg data-icon="tabler/shield-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M11.46 20.846A12 12 0 0 1 3.5 6A12 12 0 0 0 12 3a12 12 0 0 0 8.5 3a12 12 0 0 1-.09 7.06M15 19l2 2l4-4"></path></svg>Гарантия 12 мес</div>
    <div class="hero-tag" data-brief-id="card-42-900-c" data-brief-role="card">
      <div><div class="t1">Хит продаж · этот месяц</div><div class="t2">от 42 900 C</div></div>
    </div>
  </div>
</section>

<section class="wrap deals" data-brief-id="section-2" data-brief-role="section">
  <div class="sec-head">
    <div>
      <div class="sec-label">Flash deals</div>
      <h2 class="sec-title">Горящие предложения</h2>
    </div>
    <p class="sec-side">Цены действуют до конца дня. Количество техники ограничено — бронируйте через WhatsApp в один клик.</p>
  </div>

  <div class="deals-panel">
    <div class="deals-top" data-brief-id="card-3" data-brief-role="card">
      <div class="deals-live" data-brief-id="card-5" data-brief-role="card">
        <span class="badge"><span class="pulse"></span>Live</span>
        <h3>Скидки недели</h3>
      </div>
      <div class="countdown" data-brief-id="card-11-42-18" data-brief-role="card">
        <span class="cd-label">До конца акции</span>
        <div class="cd-cell"><div class="v">11</div><div class="k">час</div></div>
        <span class="cd-sep">:</span>
        <div class="cd-cell"><div class="v">42</div><div class="k">мин</div></div>
        <span class="cd-sep">:</span>
        <div class="cd-cell"><div class="v">18</div><div class="k">сек</div></div>
      </div>
      <div class="car-controls" data-brief-id="card-6" data-brief-role="card">
        <button class="car-btn" aria-label="Назад" data-brief-id="button" data-brief-role="button"><svg data-icon="tabler/chevron-left" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic ic-lg" style="max-width:32px;max-height:32px"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m15 6l-6 6l6 6"></path></svg></button>
        <button class="car-btn" aria-label="Вперёд" data-brief-id="button-2" data-brief-role="button"><svg data-icon="tabler/chevron-right" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic ic-lg" style="max-width:32px;max-height:32px"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m9 6l6 6l-6 6"></path></svg></button>
      </div>
    </div>

    <div class="deal-grid" data-brief-id="card-nova-blade-15-rtx" data-brief-role="card">
      
      <article class="deal-card" data-brief-id="card-nova-blade-15-rtx-2" data-brief-role="card">
        <div class="deal-img">
          <img src="https://rpreisbpsxrjwqsfeggf.supabase.co/storage/v1/object/public/direction-images/directions/c1533352-8e8d-4656-ac97-8c295224d7cc/1eb6375303a1.jpg" data-photo-aspect="card" alt="Игровой ноутбук" style="max-width:100%" data-stock-provider="pexels" data-stock-page="https://www.pexels.com/photo/colorful-backlit-gaming-keyboard-close-up-32285847/" data-stock-photographer="Willfried Wende" >
          <span class="deal-off">−22%</span>
        </div>
        <div class="deal-body">
          <span class="deal-cat">Ноутбук · Игровой</span>
          <h4 class="deal-name">NOVA Blade 15 · RTX 4060</h4>
          <p class="deal-specs">Ryzen 7 7840HS · 16 ГБ DDR5 · 512 ГБ SSD · 144 Гц IPS</p>
          <div class="deal-prices"><span class="now">58 900 C</span><span class="old">75 500 C</span></div>
          <p class="deal-pay">Рассрочка: <b>4 908 C / мес</b> · 12 мес</p>
          <a class="deal-buy" href="https://wa.me/996700000000?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5!%20%D0%A5%D0%BE%D1%87%D1%83%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%3A%20NOVA%20Blade%2015%20RTX%204060%20%D0%B7%D0%B0%2058%20900%20C%20(%D1%81%D0%BA%D0%B8%D0%B4%D0%BA%D0%B0%20Flash%20Deal%20%E2%88%9222%25)" data-brief-id="button-8" data-brief-role="button">
            <svg data-icon="tabler/brand-whatsapp" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m3 21l1.65-3.8a9 9 0 1 1 3.4 2.9z"></path><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0za5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"></path></g></svg>Быстрый заказ
          </a>
        </div>
      </article>
      
      <article class="deal-card" data-brief-id="card-cyber-core-rtx-4070" data-brief-role="card">
        <div class="deal-img">
          <img src="https://rpreisbpsxrjwqsfeggf.supabase.co/storage/v1/object/public/direction-images/directions/c1533352-8e8d-4656-ac97-8c295224d7cc/2eb9093c3617.jpg" data-photo-aspect="card" alt="Игровой ПК" style="max-width:100%" data-stock-provider="pexels" data-stock-page="https://www.pexels.com/photo/black-computer-motherboard-159235/" data-stock-photographer="Pixabay" >
          <span class="deal-off">−15%</span>
        </div>
        <div class="deal-body">
          <span class="deal-cat">ПК · Сборка</span>
          <h4 class="deal-name">CYBER Core · RTX 4070</h4>
          <p class="deal-specs">i5-13400F · 32 ГБ DDR5 · 1 ТБ NVMe · 650W Bronze</p>
          <div class="deal-prices"><span class="now">84 500 C</span><span class="old">99 400 C</span></div>
          <p class="deal-pay">Рассрочка: <b>7 041 C / мес</b> · 12 мес</p>
          <a class="deal-buy" href="https://wa.me/996700000000?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5!%20%D0%A5%D0%BE%D1%87%D1%83%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%3A%20CYBER%20Core%20RTX%204070%20%D0%B7%D0%B0%2084%20500%20C%20(%D1%81%D0%BA%D0%B8%D0%B4%D0%BA%D0%B0%20Flash%20Deal%20%E2%88%9215%25)" data-brief-id="button-9" data-brief-role="button">
            <svg data-icon="tabler/brand-whatsapp" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m3 21l1.65-3.8a9 9 0 1 1 3.4 2.9z"></path><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0za5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"></path></g></svg>Быстрый заказ
          </a>
        </div>
      </article>
      
      <article class="deal-card" data-brief-id="card-gpu-vector-x-rtx" data-brief-role="card">
        <div class="deal-img">
          <img src="https://rpreisbpsxrjwqsfeggf.supabase.co/storage/v1/object/public/direction-images/directions/c1533352-8e8d-4656-ac97-8c295224d7cc/0ffafbb8ebbe.jpg" data-photo-aspect="card" alt="Видеокарта" style="max-width:100%" data-stock-provider="pexels" data-stock-page="https://www.pexels.com/photo/close-up-of-computer-part-6704947/" data-stock-photographer="Sergei Starostin" >
          <span class="deal-off">−18%</span>
        </div>
        <div class="deal-body">
          <span class="deal-cat">Комплектующие</span>
          <h4 class="deal-name">GPU Vector X · RTX 4060 Ti</h4>
          <p class="deal-specs">8 ГБ GDDR6 · 2 вентилятора · PCIe 4.0 · б/у гарантия</p>
          <div class="deal-prices"><span class="now">31 200 C</span><span class="old">38 000 C</span></div>
          <p class="deal-pay">Рассрочка: <b>2 600 C / мес</b> · 12 мес</p>
          <a class="deal-buy" href="https://wa.me/996700000000?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5!%20%D0%A5%D0%BE%D1%87%D1%83%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%3A%20GPU%20Vector%20X%20RTX%204060%20Ti%20%D0%B7%D0%B0%2031%20200%20C%20(%D1%81%D0%BA%D0%B8%D0%B4%D0%BA%D0%B0%20Flash%20Deal%20%E2%88%9218%25)" data-brief-id="button-10" data-brief-role="button">
            <svg data-icon="tabler/brand-whatsapp" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m3 21l1.65-3.8a9 9 0 1 1 3.4 2.9z"></path><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0za5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"></path></g></svg>Быстрый заказ
          </a>
        </div>
      </article>
    </div>

    <div class="car-dots" data-brief-id="card-4" data-brief-role="card"><i class="on"></i><i></i><i></i></div>
  </div>
</section>

<section class="wrap adv" data-brief-id="section-3" data-brief-role="section">
  <div class="sec-head">
    <div>
      <div class="sec-label">Почему мы</div>
      <h2 class="sec-title">Система работает на вас</h2>
    </div>
    <p class="sec-side">Каждый заказ проходит проверку, тестирование и упаковку перед отправкой в любой регион Кыргызстана.</p>
  </div>
  <div class="adv-grid">
    <div class="adv-card" data-brief-id="card-7" data-brief-role="card">
      <span class="idx">01</span>
      <div class="tile"><svg data-icon="tabler/bolt" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic ic-xl" style="max-width:32px;max-height:32px"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M13 3v7h6l-8 11v-7H5z"></path></svg></div>
      <h4>Быстро</h4>
      <p>Доставка по Бишкеку — в день заказа. По Кыргызстану — 1–3 дня, бесплатно. Отправка в день подтверждения.</p>
    </div>
    <div class="adv-card" data-brief-id="card-8" data-brief-role="card">
      <span class="idx">02</span>
      <div class="tile"><svg data-icon="tabler/shield-lock" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic ic-xl" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a12 12 0 0 0 8.5 3A12 12 0 0 1 12 21A12 12 0 0 1 3.5 6A12 12 0 0 0 12 3"></path><path d="M11 11a1 1 0 1 0 2 0a1 1 0 1 0-2 0m1 1v2.5"></path></g></svg></div>
      <h4>Надёжно</h4>
      <p>Официальная гарантия 12 месяцев, проверка техники при получении. Рассрочка с банком и без банка — 18+, только паспорт.</p>
    </div>
    <div class="adv-card" data-brief-id="card-24-7-2" data-brief-role="card">
      <span class="idx">03</span>
      <div class="tile"><svg data-icon="tabler/clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic ic-xl" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0-18 0"></path><path d="M12 7v5l3 3"></path></g></svg></div>
      <h4>Онлайн 24/7</h4>
      <p>Принимаем заказы круглосуточно через WhatsApp. Консультация и подбор конфигурации — ежедневно с 9:00 до 22:00.</p>
    </div>
  </div>
</section>

<section class="wrap credit" data-brief-id="section-4" data-brief-role="section">
  <div class="credit-panel">
    <div class="credit-left">
      <div class="sec-label">Рассрочка</div>
      <h3>Паспорт —<br>и техника <em>твоя</em></h3>
      <p>Оформляем рассрочку с банком и без банка. Первый взнос — от 0%, решение по заявке за 15 минут прямо в магазине или онлайн.</p>
    </div>
    <div class="credit-right">
      <div class="plan" data-brief-id="card-6-0" data-brief-role="card">
        <div class="term">6 <em>мес</em></div>
        <div class="rate">без переплаты</div>
        <span class="mark">0% в месяц</span>
      </div>
      <div class="plan" data-brief-id="card-12-2" data-brief-role="card">
        <div class="term">12 <em>мес</em></div>
        <div class="rate">минимальный платёж</div>
        <span class="mark">от 2% в месяц</span>
      </div>
      <div class="plan" data-brief-id="card-24" data-brief-role="card">
        <div class="term">24 <em>мес</em></div>
        <div class="rate">максимальный срок</div>
        <span class="mark">нужен только паспорт</span>
      </div>
    </div>
  </div>
</section>

<section class="wrap cta" data-brief-id="section-5" data-brief-role="section">
  <div class="cta-panel">
    <div>
      <div class="sec-label">Direct</div>
      <h3>Нашли свой ПК?<br>Забирайте в рассрочку.</h3>
      <p>Нажмите кнопку — откроется <b>WhatsApp с готовым сообщением</b>: выбранная модель, цена и срок рассрочки уже в тексте. Останется только отправить.</p>
    </div>
    <a class="cta-btn" href="https://wa.me/996700000000?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5!%20%D0%A5%D0%BE%D1%87%D1%83%20%D0%BE%D1%84%D0%BE%D1%80%D0%BC%D0%B8%D1%82%D1%8C%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%20%D0%B2%20CyberStore%20(%D0%90%D0%B9%D0%BD%D0%B8%2031%2C%20%D0%91%D0%B8%D1%88%D0%BA%D0%B5%D0%BA)" data-brief-id="button-whatsapp-2" data-brief-role="button">
      <svg data-icon="tabler/brand-whatsapp" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic ic-lg" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m3 21l1.65-3.8a9 9 0 1 1 3.4 2.9z"></path><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0za5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"></path></g></svg>Написать в WhatsApp
    </a>
  </div>
</section>

<footer data-brief-id="footer" data-brief-role="footer">
  <div class="wrap foot-grid">
    <div data-brief-id="card-cyberstore-500-18" data-brief-role="card">
      <a class="logo" href="#" style="margin-bottom:16px" data-brief-id="button-cyberstore-2" data-brief-role="button">
        <span class="logo-mark"><svg data-icon="tabler/cpu" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic ic-lg" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M5 6a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1z"></path><path d="M9 9h6v6H9zm-6 1h2m-2 4h2m5-11v2m4-2v2m7 5h-2m2 4h-2m-5 7v-2m-4 2v-2"></path></g></svg></span>
        <span>CYBER<em>STORE</em></span>
      </a>
      <p style="margin-top:14px;max-width:300px">Магазин ноутбуков, ПК и комплектующих в Бишкеке. 500+ отзывов, рассрочка 18+, бесплатная доставка по КР.</p>
    </div>
    <div data-brief-id="card-9" data-brief-role="card">
      <h5>Магазин</h5>
      <a href="#" data-brief-id="button-11" data-brief-role="button">Главная</a>
      <a href="#" data-brief-id="button-12" data-brief-role="button">Каталог</a>
      <a href="#" data-brief-id="button-13" data-brief-role="button">Контакты</a>
      <a href="#" data-brief-id="button-flash" data-brief-role="button">Flash-скидки</a>
    </div>
    <div data-brief-id="card-10" data-brief-role="card">
      <h5>Контакты</h5>
      <div class="foot-line"><svg data-icon="tabler/map-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11a3 3 0 1 0 6 0a3 3 0 0 0-6 0"></path><path d="M17.657 16.657L13.414 20.9a2 2 0 0 1-2.827 0l-4.244-4.243a8 8 0 1 1 11.314 0"></path></g></svg>Бишкек, ул. Айни 31</div>
      <div class="foot-line"><svg data-icon="tabler/clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0-18 0"></path><path d="M12 7v5l3 3"></path></g></svg>9:00 – 22:00, без выходных</div>
      <div class="foot-line"><svg data-icon="tabler/brand-whatsapp" viewBox="0 0 24 24" fill="none" stroke="currentColor" data-icon-style="line" class="ic" style="max-width:32px;max-height:32px"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m3 21l1.65-3.8a9 9 0 1 1 3.4 2.9z"></path><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0za5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"></path></g></svg>+996 700 000 000</div>
    </div>
    <div data-brief-id="card-11" data-brief-role="card">
      <h5>Доставка</h5>
      <p>По Бишкеку — в день заказа.<br>По Кыргызстану — 1–3 дня.<br>Бесплатно при любом заказе.</p>
    </div>
  </div>
  <div class="wrap foot-bottom">
    <span>© 2024 CyberStore · Бишкек</span>
    <b>НЕОН · СИГНАЛ · СКОРОСТЬ</b>
  </div>
</footer>

</body>
</html>
```

Use the tokens as CSS variables. Treat the reference HTML as the visual
source of truth; adapt structure to your framework, but do not deviate
from the visual system.
