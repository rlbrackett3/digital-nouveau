# Content Audit: Wix vs Staging

**Date:** 2026-06-28
**Task:** t_4325c8a3 — Audit content completeness between Wix (blog.digitalnouveau.com) and staging (digital-nouveau.getforge.io)

---

## 1. Post Counts

| Source | Total Posts | Posts with Images |
|--------|-------------|-------------------|
| Wix    | 111         | 97                |
| Staging| 133         | 26                |
| Delta  | +22         | -71               |

## 2. Post Migration Status

### 2.1 Posts Migrated (111/111) — ✅ PASS
All 111 Wix blog posts are present on staging. No posts were lost during migration.

### 2.2 Posts Added Post-Migration (22)
The following 22 posts exist on staging but have no Wix equivalent (added after migration):

- 200-million-years-ago
- a-butterfly-for-hope
- architecture-where-design-meets-engineering
- arnica-cb1001-sectional-analysis
- arnica-ring-1090
- arnica-softly
- arterial-spray-or-coffee-ricocheting-off-a-door-and-onto-a-wall
- body-transforms-laminar-cloud-folly-2014
- bones-flowers-arnica-cufflink-prototypes
- brrrrrraaaaaaiiiiiiiinnnnnsssss
- cholla-cactus-wood-joshua-tree-national-park
- cocooning-luna-moth-ring
- cocooning-ring-prototypes
- concept-sketches-for-a-lighthouse
- contouring-plywood-landscapes
- demon-seed
- dn-studios-application
- drawing-001
- drawing-002
- drawing-003
- drawing-004

*(Note: The staging listing showed 22 "staging-only" posts. Review these slugs to confirm they are legitimately new content and not Wix posts that were renamed/slugged differently during migration.)*

## 3. Image Audit — ❌ CRITICAL

### 3.1 Summary
- **Wix has images for 97 posts** (out of 111 total)
- **Staging has images for only 26 posts**
- **71 posts have images on Wix but are missing images on staging**

### 3.2 Affected Posts (first 30 of 71)
The following posts have images on Wix but are missing images on staging:

1. 200-million-years-ago
2. a-butterfly-for-hope
3. architecture-where-design-meets-engineering
4. arnica-cb1001-sectional-analysis
5. arnica-ring-1090
6. arnica-softly
7. arterial-spray-or-coffee-ricocheting-off-a-door-and-onto-a-wall
8. body-transforms-laminar-cloud-folly-2014
9. bones-flowers-arnica-cufflink-prototypes
10. brrrrrraaaaaaiiiiiiiinnnnnsssss
11. cholla-cactus-wood-joshua-tree-national-park
12. cocooning-luna-moth-ring
13. cocooning-ring-prototypes
14. concept-sketches-for-a-lighthouse
15. contouring-plywood-landscapes
16. demon-seed
17. dn-studios-application
18. drawing-001
19. drawing-002
20. drawing-003
21. drawing-004
22. drawing-005
23. drawing-006
24. drawing-007
25. drawing-008
26. drawing-009
27. drawing-010
28. drawing-011
29. drawing-012
30. drawing-013

*(Full list of 71 posts in attached data.)*

### 3.3 Root Cause
Images referenced in Wix posts use Wix static hosting URLs (e.g. `https://static.wixstatic.com/media/...`). These URLs likely broke during migration to staging and were stripped from the markdown content, or the image files were not copied over.

### 3.4 Recommended Fix
1. For each of the 71 affected posts, extract the Wix image URLs from the sitemap
2. Download the images from Wix static hosting
3. Copy images into staging's `/src/content/blog/` directory or an images asset directory
4. Update the markdown frontmatter or body content to reference the local image paths

## 4. Date Discrepancies

Most posts on staging have dates offset by **+1 day** compared to Wix.

| Post | Wix Date | Staging Date | Delta |
|------|----------|--------------|-------|
| 200-million-years-ago | 2013-06-04 | Jun 3, 2013 | -1 day |
| a-butterfly-for-hope | 2014-02-13 | Feb 12, 2014 | -1 day |
| a-mindful-drawing-practice | 2021-04-12 | Jan 14, 2024 | **+3 years** |
| a-texas-thistle | 2019-08-20 | Aug 19, 2019 | -1 day |
| adrift | 2019-09-18 | Sep 17, 2019 | -1 day |
| aesthetic-tuning-colony | 2019-10-15 | Oct 14, 2019 | -1 day |
| architecture-where-design-meets-engineering | 2016-10-05 | Oct 4, 2016 | -1 day |
| arnica-cb1001-sectional-analysis | 2019-08-15 | Oct 8, 2013 | **+7 years** |
| arnica-ring-1090 | 2013-09-12 | Sep 11, 2013 | -1 day |
| arnica-softly | 2015-03-24 | Mar 23, 2015 | -1 day |

### Pattern Analysis
- **~90% of posts** show a consistent +1 day offset (likely timezone conversion issue, e.g. UTC vs Eastern time)
- **2 outliers** show massive date discrepancies:
  - `a-mindful-drawing-practice`: Wix=2021-04-12, Staging=2024-01-14 (+3 years)
  - `arnica-cb1001-sectional-analysis`: Wix=2019-08-15, Staging=2013-10-08 (+7 years)
  These likely have manually set dates that differ from the original Wix publish dates.

### Recommended Fix
1. Fix the timezone conversion for the bulk of posts (apply -1 day offset consistently)
2. Manually review and correct the 2 outlier posts

## 5. Portfolio / Projects

### 5.1 Wix Portfolio
- **6 project pages found** in sitemap:
  1. subterranean-infestations
  2. fflourish
  3. ardn
  4. project-name-03
  5. project-name-02
  6. project-name-01
- Portfolio page at `/portfolio` returns **404**
- Portfolio at `/Projects` (capital P) renders as a JavaScript SPA (no server-side content)

### 5.2 Staging Portfolio
- URL: `/portfolio/index.html`
- Status: **200 OK** (rendered)
- Content: **Placeholder only** — 4 generic sections with no actual project data:
  1. Architecture & Design (generic description)
  2. Fabrication & Making (generic description)
  3. Research & Development (generic description)
  4. Teaching & Pedagogy (generic description)

### 5.3 Finding
**All 6 Wix project pages are missing from staging.** The staging portfolio is a generic placeholder, not a data-driven page populated from the project content files.

### 5.4 Recommended Fix
- Check if project .md files exist in `/src/content/` or similar directory on staging
- If they exist, update the portfolio page template to dynamically list projects
- If they don't exist, the project content needs to be migrated from Wix

## 6. Category / Feed Structure

### 6.1 Wix Categories (9 total)
From the blog feed navigation:
1. everything
2. design
3. drawings
4. readings
5. skyfi
6. thinkings
7. observings
8. teachings
9. writings

### 6.2 Staging Categories (8 of 9)
| Category | Status |
|----------|--------|
| design | 200 OK |
| drawings | 200 OK |
| readings | 200 OK |
| skyfi | 200 OK |
| thinkings | 200 OK |
| observings | 200 OK |
| teachings | 200 OK |
| writings | 200 OK |
| everything | **404 Not Found** |

### 6.3 Category Pages Content
**Critical: Staging category pages return 200 OK but contain 0 post links.** The category pages render but do not list any posts. The homepage also has 0 post links.

### 6.4 Wix Category Pages
URLs at `/post-category/<category>` all return **404 Not Found**. Wix blog categories appear to be client-side filters only (no separate page URLs).

### 6.5 Skyfi Page
- Wix: Available at `/skyfi-a-reading-list` (from pages sitemap)
- Staging: Available at `/skyfi-a-reading-list/index.html` (from navigation)

## 7. Overall Assessment

### Severity Summary

| Issue | Severity | Count |
|-------|----------|-------|
| Missing images | 🔴 CRITICAL | 71 posts |
| Portfolio not populated | 🟡 HIGH | 6 projects missing |
| Category pages don't list posts | 🟡 HIGH | 8 pages |
| Date discrepancies | 🟢 LOW | ~111 posts |
| Homepage doesn't list posts | 🟡 HIGH | 1 page |
| "everything" category 404 | 🟢 LOW | 1 page |

### Positive Findings
- All 111 Wix posts migrated to staging with no deletions
- All 8 category pages exist (except "everything")
- The site structure and navigation match Wix

### Action Items

1. **URGENT: Fix 71 missing images** — Download images from Wix static hosting and update post markdown files
2. **HIGH: Populate portfolio page** — Migrate 6 Wix projects and update portfolio template
3. **HIGH: Fix category pages** — Update category page templates to dynamically list posts
4. **HIGH: Fix homepage** — Ensure homepage lists recent posts
5. **LOW: Fix "everything" category** — Create or remove the "everything" navigation item
6. **LOW: Fix date offsets** — Apply timezone correction to normalize dates

## 8. Data Sources

- Wix blog sitemap: `https://www.blog.digitalnouveau.com/blog-posts-sitemap.xml`
- Wix pages sitemap: `https://www.blog.digitalnouveau.com/pages-sitemap.xml`
- Wix Projects sitemap: `https://www.blog.digitalnouveau.com/dynamic-Projects_p_60def5ff_e9fe_42df_a927_f56d70ff45a3_0_5000-sitemap.xml`
- Staging homepage: `https://digital-nouveau.getforge.io/`
- Staging parsed post data: `/tmp/staging_posts.json` (133 posts)
- Comparison data: `/tmp/wix_staging_comparison.json`
- Wix sitemap dump: `/tmp/wix_blog_sitemap.xml` (738 lines, 111 posts)
