---
name: AquaSmart
colors:
  surface: '#f9faf2'
  surface-dim: '#d9dbd3'
  surface-bright: '#f9faf2'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4ec'
  surface-container: '#edefe7'
  surface-container-high: '#e8e9e1'
  surface-container-highest: '#e2e3db'
  on-surface: '#1a1c18'
  on-surface-variant: '#414844'
  inverse-surface: '#2f312c'
  inverse-on-surface: '#f0f1e9'
  outline: '#717973'
  outline-variant: '#c1c8c2'
  surface-tint: '#3f6653'
  primary: '#012d1d'
  on-primary: '#ffffff'
  primary-container: '#1b4332'
  on-primary-container: '#86af99'
  inverse-primary: '#a5d0b9'
  secondary: '#2c694e'
  on-secondary: '#ffffff'
  secondary-container: '#aeeecb'
  on-secondary-container: '#316e52'
  tertiary: '#152b1c'
  on-tertiary: '#ffffff'
  tertiary-container: '#2a4131'
  on-tertiary-container: '#93ad98'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c1ecd4'
  primary-fixed-dim: '#a5d0b9'
  on-primary-fixed: '#002114'
  on-primary-fixed-variant: '#274e3d'
  secondary-fixed: '#b1f0ce'
  secondary-fixed-dim: '#95d4b3'
  on-secondary-fixed: '#002114'
  on-secondary-fixed-variant: '#0e5138'
  tertiary-fixed: '#cee9d3'
  tertiary-fixed-dim: '#b3cdb7'
  on-tertiary-fixed: '#092012'
  on-tertiary-fixed-variant: '#354c3b'
  background: '#f9faf2'
  on-background: '#1a1c18'
  surface-variant: '#e2e3db'
typography:
  display-kpi:
    fontFamily: Manrope
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-caps:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-padding-mobile: 16px
  container-padding-desktop: 32px
  gutter: 24px
  card-gap: 20px
---

## Brand & Style

The design system is anchored in a **Corporate Modern** aesthetic with a strong **Minimalist** influence, tailored specifically for the high-stakes environment of precision agriculture. The brand personality is authoritative yet revitalizing, aiming to evoke a sense of "digital growth" and "data-driven stewardship."

The UI should feel like a high-end tool that respects the user's intelligence and time. It prioritizes clarity over decoration, using heavy whitespace to reduce cognitive load for farmers and agronomists managing complex data sets. The emotional response should be one of confidence and calm—shifting the user's perception of irrigation management from a source of stress to a streamlined, professional process. 

Key visual principles:
- **Lush Professionalism:** Utilizing deep greens to signify established expertise and lighter mints to suggest fresh technology.
- **Data Clarity:** Every element serves the readability of field data and AI insights.
- **Modern Utility:** A "Silicon Valley meets the Vineyard" vibe—clean, sharp, and highly functional.

## Colors

The palette is rooted in the natural lifecycle of a crop, moving from deep earth tones to vibrant leaf greens.

- **Primary & Secondary:** `Deep Forest Green` is used for high-level navigation, primary buttons, and heavy branding elements. `Fresh Agricultural Green` serves as the active interaction color.
- **Surfaces:** Use `Light Natural Beige` for the main application background to reduce eye strain compared to pure white. `White` is reserved exclusively for card backgrounds and elevated surfaces.
- **Functional Colors:** These are non-negotiable for safety and efficiency. Green, Amber, Red, and Blue must be used consistently across sensors and charts to indicate soil moisture levels and system health.

## Typography

**Manrope** is the sole typeface for the design system. Its geometric yet slightly condensed nature allows for high information density without sacrificing readability.

- **KPI Values:** Use `display-kpi` for soil moisture percentages or weather degrees. These should be the largest elements on any dashboard.
- **Hierarchy:** Use `label-caps` for section headers above cards to provide clear categorical grouping. 
- **AI Narrative:** AI recommendations should use `body-lg` to ensure they feel like distinct, readable advice rather than just more data.

## Layout & Spacing

This design system utilizes a **12-column fluid grid** for desktop and a **single-column vertical stack** for mobile.

- **The 8px Rule:** All margins and paddings must be multiples of 8px to maintain a rhythmic, professional balance.
- **Responsive Behavior:** On desktop, the sidebar is fixed at 280px. On mobile, navigation moves to a bottom "tab bar" to allow for easy one-handed operation in the field.
- **Card Layouts:** Use a 24px gutter between dashboard widgets. Internal card padding should be a consistent 24px to provide "breathing room" for dense sensor data.

## Elevation & Depth

To achieve a "Fresh & Modern" feel, depth is communicated through **Ambient Shadows** and **Tonal Layers** rather than heavy borders.

- **Level 0 (Background):** `Light Natural Beige` (#F8F9F1).
- **Level 1 (Cards):** `White` (#FFFFFF) with a very soft, diffused shadow: `0px 4px 20px rgba(27, 67, 50, 0.06)`. Note the subtle green tint in the shadow to keep the palette organic.
- **Level 2 (Modals/Popovers):** `White` with a more pronounced shadow: `0px 12px 32px rgba(27, 67, 50, 0.12)`.
- **Interactions:** On hover, cards should subtly lift by increasing the shadow spread and shifting -2px on the Y-axis.

## Shapes

The shape language is defined by **Rounded** corners that mirror the organic curves of nature while maintaining structural integrity.

- **Standard Components:** Buttons and Input fields use `rounded` (8px).
- **Primary Containers:** Stat cards, AI cards, and Chart containers use `rounded-xl` (24px) to create a friendly, accessible "app-like" feel.
- **Status Badges:** Use a fully rounded pill shape (999px) to distinguish them from interactive buttons.

## Components

### Stat Cards
The core of the dashboard. Features a `label-caps` title at the top left, a `display-kpi` value in the center, and a small sparkline or trend indicator at the bottom. Background is always white.

### AI Recommendation Cards
These require high visual priority. Use a `Soft Mint Green` (#D8F3DC) border (2px) or a subtle gradient background to distinguish them from standard sensor cards. Include a prominent "Action" button using the `Deep Forest Green` primary color.

### Buttons
- **Primary:** `Deep Forest Green` background, white text. No border.
- **Secondary:** Transparent background, `Fresh Agricultural Green` border (1.5px) and text.
- **Tertiary:** Text-only for less frequent actions like "View History."

### Status Badges
Used for irrigation status. Backgrounds should be 15% opacity versions of the status colors (Green, Amber, Red) with 100% opacity text of the same hue for maximum legibility and "soft" aesthetic.

### Input Fields
Soft beige background (`#F1F2E9`) with no border in default state. On focus, transition to a `Fresh Agricultural Green` border (2px) and white background.

### Chart Containers
Ensure charts use the system's functional color palette. Grid lines should be faint (`#E5E7EB`) to keep the focus on the data trend.