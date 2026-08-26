# Frontend Architecture & Design System Documentation

**Project:** Personalized Career Recommendation Platform for Classes 7–12  
**Framework:** Flask 3.0+ & Jinja2 Templates, Bootstrap 5.3, Chart.js 4.4, Vanilla CSS Design System  
**Theme:** Light Mode & Dark Mode with LocalStorage Persistence & Zero Gradients

---

## 1. Design System & Philosophy
The frontend is engineered as a clean, accessible, flat-design educational guidance system. It eliminates all visual clutter, excessive animations, and gradient fills in favor of structured typography, solid brand colors, and clear data visualization.

---

## 2. Color Palette (CSS Custom Properties)

| Role | Light Mode Hex | Dark Mode Hex | Usage |
| :--- | :--- | :--- | :--- |
| **Primary** | `#1B2CC1` | `#7692FF` | Main brand, primary buttons, active states, key metrics |
| **Secondary** | `#7692FF` | `#98ACFF` | Supporting accents, secondary buttons |
| **Page Background** | `#F8FAFC` | `#0F172A` | Base viewport background |
| **Surface Card** | `#FFFFFF` | `#1E293B` | Main content cards, modals, table bodies |
| **Subtle Surface** | `#F1F5F9` | `#334155` | Secondary callouts, table headers, score pills |
| **Text Main** | `#111827` | `#F8FAFC` | Headings and primary body copy |
| **Text Secondary**| `#4B5563` | `#CBD5E1` | Subtext, labels, metadata descriptions |
| **Text Muted** | `#6B7280` | `#94A3B8` | Footnotes, captions, disabled hints |
| **Border** | `#E5E7EB` | `#334155` | Card dividers, table borders, input outlines |
| **Success** | `#15803D` | `#22C55E` | Match confirmation, completed status |
| **Warning** | `#B45309` | `#F59E0B` | In-progress badges, skipped questions notice |
| **Danger / Error**| `#B91C1C` | `#EF4444` | Validation errors, destructive actions |
| **Info** | `#2563EB` | `#3B82F6` | Informational callouts, learning matches |

*Strict Rule:* **Zero Gradients.** All backgrounds, buttons, borders, and text use solid flat colors.

---

## 3. Typography Hierarchy
- **Font Family:** `Inter`, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif.
- **H1 / Display:** 2.25rem – 2.75rem (Font weight: 700)
- **H2:** 1.75rem – 2.00rem (Font weight: 700)
- **H3 / H4:** 1.25rem – 1.50rem (Font weight: 700)
- **Body:** 1.00rem (16px, line-height: 1.5)
- **Small / Meta:** 0.875rem (14px)

---

## 4. Theme System (Light / Dark Mode)
- **Immediate Initialization:** Inline execution in `<head>` queries `localStorage.getItem('app_theme')` and `window.matchMedia('(prefers-color-scheme: dark)')` to prevent any flash of unstyled content.
- **Toggle Mechanism:** Navbar theme toggle button switches `data-theme="light"` and `data-theme="dark"` on `<html>`.
- **Dynamic Event Broadcasting:** Dispatches `themechange` event across `window` so Chart.js instances automatically redraw gridlines and labels with optimal contrast.

---

## 5. Reusable Component Library

| Component | CSS Selector | Description |
| :--- | :--- | :--- |
| **Primary Button** | `.btn-primary-custom` | Solid primary background with focus ring |
| **Secondary Button** | `.btn-secondary-custom` | Solid secondary background |
| **Outline Button** | `.btn-outline-custom` | Transparent background with border and hover state |
| **Content Card** | `.card-custom` | Solid background, subtle border, gentle shadow |
| **Subtle Card** | `.card-subtle` | Subdued surface for inner callouts and score boxes |
| **Top Pick Card** | `.card-top-pick` | Prominent 4px solid left border for #1 recommendation |
| **Badges** | `.badge-custom.*` | Pill-free rectangular badges with subtle padding |
| **Progress Bar** | `.progress-container-custom` | Horizontal progress indicator with solid fill |
| **Form Inputs** | `.form-control-custom` | Theme-aware text, select, and number inputs |
| **Rating Grid** | `.rating-grid-custom` | 5-column rating buttons with descriptive levels |
| **Table** | `.table-custom` | Theme-aware responsive table with clean borders |

---

## 6. Page Structure & Architecture

1. **`index.html` (Landing Page):**
   - Solid flat hero with clear CTA.
   - 4-step "How It Works" process.
   - 19-dimensional assessment overview.
   - Career catalogue preview with live stats.
   - Transparent XGBoost model notice.

2. **`dashboard.html` (Student Dashboard):**
   - Assessment progress status banner.
   - Top 3 career recommendation cards.
   - Quick action shortcuts to Career Explorer and Profile.

3. **`instructions.html` & `assessment.html` (Questionnaire UX):**
   - Grade-tailored questions for Classes 7–12.
   - Multi-step questionnaire with real-time autosave indicators (`✓ Progress saved`).
   - Friendly non-technical prompt language.
   - Descriptive 1–5 rating controls.

4. **`review.html` (Pre-Submission Checklist):**
   - Summary check of all questions (Answered vs Skipped).
   - Confirmation modal with progressive loading overlay.

5. **`results.html` (Career Recommendations):**
   - **Top 1 Primary Match Hero Card** with compatibility score, domain, and description.
   - **4 Profile Match Components:** Ability (8-D), Interest (10-D), Academic, Learning.
   - **Interactive Visualizations:** Cognitive Radar Chart & Disciplinary Bar Chart.
   - **Why This Career Matches You:** Matched strengths and growth areas.
   - **Top Ranked Recommendations Table:** Full ranking across 1,206 career candidates.
   - **5-Stage Educational Milestones Accordion:** Progressive career roadmap.
   - **Transparent Model Metrics:** Distinct separation of 80.99% classification accuracy from 96.18% Hit@1 recommendation ranking.

6. **`career_explorer.html` & `career_details.html` (Career Browsing):**
   - Live search keyword filter.
   - Domain, subdomain, and cluster dropdowns.
   - Responsive career cards and pagination.
   - Detailed degree requirements, essential skills, and school subjects.

---

## 7. Accessibility & Performance
- **WCAG 2.1 AA Contrast:** All text pairings exceed the 4.5:1 minimum contrast ratio.
- **Focus Rings:** Distinct `:focus-visible` styling for full keyboard navigation.
- **Reduced Motion:** Adheres to `prefers-reduced-motion: reduce` by disabling smooth transitions.
- **Zero Heavy Assets:** Pure SVG icons (Bootstrap Icons) and Chart.js vector canvases.
