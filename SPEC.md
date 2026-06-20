# Digital Nouveau — Wix to Astro Clone

**Status:** Phase 1 :: Spec Authoring
**Location:** `/root/user-files/projects/digital-nouveau/`
**Dev server:** `100.114.36.84:4322`

## Goal

Clone the Wix blog (blog.digitalnouveau.com) as an Astro static site with visual fidelity. Text, layout, colors, graphics match. Platform for future growth. All 111 posts from Posts.csv rendered.

## Requirements

### Typography
- Primary font: Brandon Grotesque Light (if user provides) OR closest free match: DM Sans 300 / Space Grotesk
- Body: 14px, line-height 1.5
- Titles: 28px, light weight
- Nav links: 14px

### Colors
- Background: `#000000` pure black
- Text: `#1ceb f4` cyan
- Links: `#1ceb f4` cyan (NOT blue)
- Borders: `rgba(28, 235, 244, 0.2)`
- Muted: `rgba(28, 235, 244, 0.6)`

### Background
- Neural network pattern image, fixed position, opacity 0.15
- Downloaded from Wix CDN to `public/neural-bg.png`

### Header
- Left: "Digital Nouveau ~" title + taglines
- Right: feed / portfolio / skyfi utility nav
- Below: horizontal nav bar (everything, design, drawings, readings, skyfi, thinkings, observings, teachings, writings)
- Thin cyan border separating nav from content

### Blog Post Cards
- Image full-width at top
- Meta row: author avatar + "~rooks /l" | date + read time
- Title: 28px cyan
- Social buttons: Facebook, X, LinkedIn, Copy link
- Stats: views | comments | likes with icons
- Card border: 1px cyan

### Home Page
- Featured post (full card)
- "RECENT POSTS" heading
- 3-column grid of post thumbnails
- Comments section (avatar + textarea + submit)
- Footer: newsletter form (name/email inputs + subscribe button)

### SkyFi Page
- 4-column book list layout
- "Currently Reading" section
- Underlined book titles as links

### Content
- 111 posts from Posts.csv
- Images from Wix CDN in `public/images/`
- Frontmatter: title, date, excerpt, readTime, image, category

## Non-Goals
- Video hosting (deferred)
- GetForge deployment (paused until approval)
- New features beyond Wix clone

## Success Criteria
1. Neural background visible on all pages
2. All text readable (cyan on black)
3. Font renders as Brandon Grotesque or DM Sans Light
4. Link colors are cyan `#1ceb f4`
5. Header matches Wix screenshot
6. Blog cards match Wix screenshot
7. Recent posts in 3-column grid
8. Footer newsletter styled correctly
9. All 111 posts accessible
10. SkyFi page matches Wix
11. Build passes 0 errors, 146 pages
