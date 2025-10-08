# Golf Guy Platform – Development Plan

## 1) Executive Summary
A production-grade, content-first golf travel platform for Swedish golfers, built as a modern React + FastAPI + MongoDB application. The MVP will prioritize:
- Content CMS for Destinations and Articles (with sample seed data: 10 destinations, 5 articles)
- High-converting homepage (hero carousel, featured destinations, editorial strip, trust signals)
- Inquiry flow that logs to an Admin Dashboard (status management, notes, export)
- Mocked Instagram feed (latest 3 posts) with graceful fallback
- English default language with a ready framework for Swedish (sv-SE) expansion
- Demo auto-login buttons for Client and Admin (easily removable, no heavy coupling)

This foundation emphasizes premium UI aligned to the provided design guidelines (fairway greens, gold accents, Playfair Display + Karla fonts), SEO readiness, performance budgets, and scalability for Phase 2+ features (Year’s List, testimonials, analytics, i18n, automation).

## 2) Objectives
- Business
  - Increase qualified inquiries from destination pages and homepage
  - Establish trust: partner badges, testimonials, professional editorial content
  - Empower non-technical staff to manage content end-to-end via Admin CMS
- Technical
  - Ship a reliable, fast MVP with clean APIs and clear data models
  - Enforce SEO & performance foundations (sitemap, robots, structured data, lazy images)
  - Establish scalable patterns for rotations, i18n, analytics, and future AI

## 3) UI/UX Design Guidelines (Applied)
- Color & Tokens (from design_guidelines.md)
  - Primary (actions) → fairway green hsl(151 45% 30%)
  - Accent (premium hints) → gold hsl(45 42% 56%)
  - Neutrals per tokens; avoid raw hex primaries; use tokenized colors only
  - Gradients: allowed only in hero/section backgrounds; <20% viewport; no saturated stacks
- Typography
  - Headings: Playfair Display; Body/UI: Karla; Admin headings: Chivo
  - Semantic scale: clear hierarchy (h1–h6), 70ch max measure for long reads
- Components (Shadcn/UI only) & Patterns
  - Cards for destinations and articles, HeroCarousel, GalleryCarousel, StickyEnquiryDrawer
  - Forms via shadcn Form + Input/Select/Textarea + Sonner toasts
  - Icons: lucide-react
- States & Testability
  - Every interactive element has hover, focus-visible, active, disabled states
  - Every interactive or critical info element includes data-testid (kebab-case)
- Accessibility & Responsiveness
  - WCAG 2.1 AA: contrast/scrims on imagery; keyboard nav; ARIA labels
  - Mobile-first layout; 44x44px touch targets; sticky mobile enquiry button
- Explicit mapping
  - Per design guidelines, using fairway green for primary buttons and CTAs; gold for ratings, price tags, and accents; gradients restricted to hero only

## 4) Implementation Steps (Phased)

### Phase 1: Core MVP (In Progress)
- Backend (FastAPI, MongoDB)
  - Define models (UUID IDs, timezone-aware datetimes): Destination, Article, HeroCarousel, Testimonial, Partner, Inquiry, Settings
  - CRUD endpoints under /api/*; Pydantic response models; CORS; bind 0.0.0.0:8001
  - Inquiry endpoints: create, list, update status, add notes, CSV export
  - Mock Instagram endpoint: /api/instagram/latest → returns 3 cached mock posts
  - Rotation service (request-time): compute if hero/articles rotation due (every 10 days) and update featured flags lazily on first read of day
- Frontend (React + Shadcn + Tailwind)
  - Global theme tokens: update index.css with design tokens; load Google Fonts
  - Layout: Header with navigation + language toggle (EN default); Footer with trust links
  - Homepage: 6-slide HeroCarousel, featured destinations grid, editorial strip, trust bar, CTA band
  - Destinations: listing (filters sheet on mobile), detail page (gallery, quick facts, CTA)
  - Articles: listing + detail with categories, related destinations
  - Partners & About: static content pages
  - Contact/Inquiry: multi-step form with validation; logs to admin; Sonner toasts
  - Admin Dashboard: tabs (Content, Articles, Destinations, Inquiries), tables, inline create/edit forms, status management, CSV export
  - Demo Buttons: “Demo Client” and “Demo Admin” – auto-login by setting a demo flag/token in localStorage; routes guard reads the flag (clean removable)
  - Mock Instagram strip with fallback UI
- Seed Data
  - 10 destinations (name, slug, country/region, descriptions, SEK price_from/to, images, highlights)
  - 5 articles (title, slug, category, publish_date, featured flags, destination links)
  - 6 hero slides (title, subtitle, image, cta)
  - 3 partners (Eastern DGolf + charity partner(s))
- SEO Foundations
  - sitemap.xml and robots.txt via backend
  - SPA meta tags scaffold (react-helmet-async planned), alt text, canonical patterns
- Performance
  - Lazy-load images, image aspect ratios, skeletons for data fetches

### Phase 2: SEO, Performance & Trust Enhancements (Planned)
- Add react-helmet-async for per-route SEO fields
- Structured Data: Article, Breadcrumb, Organization
- Lighthouse mobile target ≥90; bundle trimming; image compression pipeline
- Trust content: testimonials CRUD and display; partner badges refinement

### Phase 3: Advanced Content & Rotation (Planned)
- Year’s List: ranking and votes by year, import/export
- Rotation scheduler refinement: background-friendly approach (on-demand threshold checks)
- More filters (budget, region, nights, golfers), saved views for admin

### Phase 4: Internationalization (Planned)
- i18n structure already in place (copy keys); English default; add Swedish (sv-SE) strings and date/price formats; per-locale SEO fields

### Phase 5: Analytics & Reporting (Planned)
- Event tracking: hero interactions, destination views, inquiry conversions, outbound links
- Admin charts: bookings per week, top destinations, channel split

### Phase 6: Production Hardening (Planned)
- Rate limiting for inquiry API; secure headers; GDPR data retention policy; backup/export strategy; monitoring and logs

## 5) Technical Details
- Backend
  - Environment: MONGO_URL from env; server binds 0.0.0.0:8001; all routes prefixed with /api
  - Data model basics (all IDs as UUID strings; timestamps with timezone.utc):
    - Destination: id, name, slug, country, region, short_desc, long_desc, price_from, price_to, currency="SEK", images[], highlights[], seo{title, description, canonical}
    - Article: id, title, slug, content, category, publish_date, featured_until, destination_ids[], seo{}
    - HeroCarousel: id, title, subtitle, image, destination_id?, cta_text, cta_url, rotation_days=10, order
    - Testimonial: id, name, rating(1–5), content, destination_id?, published
    - Partner: id, name, type, logo, description, url
    - Inquiry: id, name, email, phone?, destination_id?, dates?, group_size?, budget?, status{new,in_progress,responded,closed}, notes[], created_at
    - Settings: key, value
  - Patterns
    - Pydantic models for request/response
    - Rotation: on read of /api/featured or /api/hero, if now ≥ next_rotation_at, toggle/advance featured set and persist next_rotation_at
    - Simple per-IP rate limit in-memory for inquiries (MVP); escalates to DB cache later
- Frontend
  - Use process.env.REACT_APP_BACKEND_URL + "/api" for all API calls
  - State: minimal React state + hooks; avoid global store until needed
  - Components: Shadcn UI only for inputs, selects, calendar, dialog, toast; lucide-react icons
  - Language: EN default; simple i18n wrapper to enable Swedish later; header toggle present (text/resources primarily in EN for MVP)
  - Demo Auth: localStorage demo flags; route guards show Admin Dashboard when admin flag set; easily removable
- SEO
  - sitemap.xml (backend route), robots.txt (backend), canonical URL pattern `/destinations/{slug}`, `/articles/{slug}`
- Accessibility
  - ARIA labels on logos, form fields associations, keyboard nav on carousels/dialogs; focus-visible rings

## 6) Next Actions
- Backend
  1) Scaffold models and endpoints for Destination, Article, Inquiry, HeroCarousel, Partner, Settings
  2) Implement mock /api/instagram/latest and rotation-on-read logic
  3) Seed DB with sample data endpoints/fixtures
- Frontend
  4) Apply design tokens in index.css; load Google Fonts (Playfair, Karla, Chivo)
  5) Build base layout (Header with language toggle, Demo buttons; Footer)
  6) Implement Homepage (hero, featured destinations, editorial strip, trust bar)
  7) Destinations list/detail + Articles list/detail
  8) Inquiry multi-step form; Admin Dashboard (tabs + tables + status updates + CSV export)
  9) Mock Instagram component using /api/instagram/latest with fallback skeletons
- QA/SEO/Perf
  10) Add sitemap.xml & robots.txt; alt text; canonical meta; initial Lighthouse pass

## 7) Success Criteria
- Functional
  - End-to-end flow: browse → view destination → submit inquiry → visible in Admin → status updated → CSV export works
  - Mock Instagram displays 3 posts with fallback
  - Demo Client/Admin buttons work and are easily removable
- UX & Performance
  - Mobile-first layout; skeletons for loading; sticky enquiry CTA
  - Lighthouse mobile ≥90; TTFB <2s home; images lazy-loaded; CLS <0.1
- SEO
  - sitemap.xml + robots.txt served; canonical URLs; alt text; basic structured data
- Admin Autonomy
  - Staff can add/edit/publish destinations and articles without dev help; 10 sample destinations + 5 articles in place
- Future-Ready
  - i18n scaffolding present; rotation scheduler pattern in place; analytics-ready events planned
