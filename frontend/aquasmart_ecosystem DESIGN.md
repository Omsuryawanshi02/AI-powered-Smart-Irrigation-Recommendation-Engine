---
name: AquaSmart Ecosystem
colors:
  surface: '#faf9f5'
  surface-dim: '#dbdad6'
  surface-bright: '#faf9f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f4f0'
  surface-container: '#efeeea'
  surface-container-high: '#e9e8e4'
  surface-container-highest: '#e3e2df'
  on-surface: '#1b1c1a'
  on-surface-variant: '#414844'
  inverse-surface: '#2f312e'
  inverse-on-surface: '#f2f1ed'
  outline: '#717973'
  outline-variant: '#c1c8c2'
  surface-tint: '#3f6653'
  primary: '#012d1d'
  on-primary: '#ffffff'
  primary-container: '#1b4332'
  on-primary-container: '#86af99'
  inverse-primary: '#a5d0b9'
  secondary: '#79564b'
  on-secondary: '#ffffff'
  secondary-container: '#fed0c1'
  on-secondary-container: '#79574c'
  tertiary: '#002845'
  on-tertiary: '#ffffff'
  tertiary-container: '#003f67'
  on-tertiary-container: '#4cadfd'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c1ecd4'
  primary-fixed-dim: '#a5d0b9'
  on-primary-fixed: '#002114'
  on-primary-fixed-variant: '#274e3d'
  secondary-fixed: '#ffdbcf'
  secondary-fixed-dim: '#e9bdae'
  on-secondary-fixed: '#2d150d'
  on-secondary-fixed-variant: '#5e3f35'
  tertiary-fixed: '#cfe5ff'
  tertiary-fixed-dim: '#99cbff'
  on-tertiary-fixed: '#001d34'
  on-tertiary-fixed-variant: '#004a78'
  background: '#faf9f5'
  on-background: '#1b1c1a'
  surface-variant: '#e3e2df'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  title-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  unit: 8px
  container-padding: 24px
  gutter: 16px
  card-gap: 24px
  section-margin: 48px
---

## Brand & Style

The design system is engineered for the modern agricultural professional, balancing high-performance data analytics with the approachability of a field tool. The brand personality is grounded, intelligent, and nurturing. It avoids the coldness of traditional enterprise software by utilizing a "Warm Modernism" approach—combining structured, data-forward layouts with soft organic shapes and a comforting, earthy color palette.

The visual style prioritizes legibility and clarity for users who may be operating in high-glare outdoor environments. It utilizes large touch targets, high-contrast text, and a sophisticated card-based architecture that feels like a physical dashboard. By focusing on satellite and AI-driven insights rather than hardware, the UI maintains a clean, ethereal quality that emphasizes intelligence over labor.

## Colors

The palette is rooted in the natural lifecycle of farming. **Deep Forest Green** serves as the primary anchor for navigation and primary actions, representing growth and stability. **Earthy Soil Brown** is used for secondary structural elements and grounding information. **Sky Blue** acts as a high-visibility accent for interactive data points, links, and "water-related" metrics.

The background uses a **Warm Off-White**, which reduces eye strain compared to pure white and reinforces the organic nature of the product. For data provenance, a specific "AI Purple" and "Manual Amber" are introduced to clearly distinguish between machine-generated estimates and human-verified entries.

## Typography

This design system utilizes **Inter** exclusively to ensure maximum legibility across all digital touchpoints. The typographic scale is generous, favoring larger sizes to accommodate varying levels of tech-literacy and outdoor usage.

Headlines are bold and tight-set to create a sense of authority. Labels and data points use medium weights to stand out against background cards. For mobile views, display sizes scale down aggressively to maintain information density without sacrificing the "clean" aesthetic.

## Layout & Spacing

The layout follows a **Fluid Grid** system with a heavy emphasis on "Safe Zones." On desktop, a 12-column grid is used with wide 24px gutters to allow the data to breathe. On mobile, a single-column stack is preferred with 16px margins.

Spacing follows an 8px base grid. Content is grouped into logical "Plot Cards" that represent different fields or data sets. Vertical rhythm is strictly enforced to ensure that even data-heavy dashboards remain scannable. Use generous white space between cards to prevent the UI from feeling cluttered or overwhelming.

## Elevation & Depth

Hierarchy is established through **Tonal Layering** and **Ambient Shadows**. The design avoids harsh lines and instead uses soft, diffused shadows to lift cards off the Warm Off-White background.

- **Level 0 (Background):** Warm Off-White (#FDFCF8).
- **Level 1 (Cards):** Pure White (#FFFFFF) with a 24px corner radius and a very soft, large-radius shadow (Blur: 30px, Opacity: 4%, Color: Forest Green).
- **Level 2 (Interactive/Hover):** Increased shadow spread and a subtle 1px border in a lighter tint of the Primary color to indicate focus.
- **Overlays/Modals:** High-blur backdrop filter (10px) to maintain the "clean" SaaS aesthetic while focusing the user's attention.

## Shapes

The shape language is extremely soft and approachable. A **Pill-shaped (Level 3)** roundedness is applied to almost all UI components to evoke a sense of friendliness and safety.

- **Cards:** Minimum 24px corner radius.
- **Buttons:** Fully rounded (pill) ends.
- **Input Fields:** 12px corner radius for a "soft-square" look that remains functional.
- **Data Gauges:** Circular or semi-circular paths with rounded caps on all progress indicators.

## Components

### Data Gauges & Progress
- **Moisture Gauges:** Semi-circular tracks using Sky Blue. The "needle" or indicator should be a soft circle.
- **Growth Progress:** Horizontal bars with a 12px height and pill-shaped caps. Use a gradient of Green to represent progress.

### Cards
- Layouts must include a header section with a clear title and an optional "Data Provenance" badge. Content should be padded by at least 24px on all sides.

### Buttons & Inputs
- **Primary Button:** Deep Forest Green with white text, pill-shaped.
- **Inputs:** Soft-grey backgrounds with a Soil Brown focus state. Labels must always be visible above the field.

### Provenance Badges (AI vs. Manual)
- **AI Estimated:** A soft purple pill tag with a "Sparkle/AI" icon and the text "AI Estimated."
- **Manual Entry:** An amber pill tag with a "Hand/User" icon and the text "Manual Entry."
- These badges must appear in the top right of any data card or next to specific data points to ensure transparency.

### Iconography
- Icons should be "Open Path" style with a 2px stroke weight. 
- Always pair icons with a label (Title-MD or Label-MD) to assist users with lower technical literacy.