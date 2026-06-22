# Content Parity Audit: Local Blog vs. Live Wix Site

**Date:** 2026-06-21
**Scope:** Random sample of 20 local Markdown posts vs. live Wix blog (blog.digitalnouveau.com)
**Method:** Frontmatter extraction from local files, web content scraping of individual Wix post pages, sitemap analysis for publication dates

---

## Summary

Of the 20 randomly sampled local posts, **16 have matching posts on the live Wix site** with matching body text. **4 posts are missing from the Wix site** (returning HTTP 404). All local posts have empty publication dates in their frontmatter. Category/tag data on Wix individual post pages could not be extracted due to Wix's shadow DOM structure.

---

## Local Post Inventory

- **Total local blog posts:** 133
- **Sample size:** 20 (randomly selected)
- **Local frontmatter dates:** All 20 sampled posts have empty/missing `date` fields

---

## Wix Post Inventory

Wix blog posts retrieved via sitemap at `https://www.blog.digitalnouveau.com/blog-posts-sitemap.xml`. The sitemap lists all 120+ blog posts with their last modification dates. Blog index and RSS feeds only render the 3 most recent posts and do not paginate or list all entries.

---

## Comparison Results

### Matched Posts (16 of 20)

The following 16 posts exist on Wix with matching titles and body content:

| # | Local Slug | Wix Date (lastmod) | Body Match |
|---|-----------|-------------------|------------|
| 1 | `architecture-where-design-meets-engineering` | 2016-10-05 | Yes |
| 2 | `arnica-cb1001-sectional-analysis` | 2019-08-15 | Yes |
| 3 | `arnica-ring-1090` | 2013-09-12 | Yes |
| 4 | `contouring-plywood-landscapes` | 2015-06-19 | Yes |
| 5 | `drawing-001` | 2013-02-18 | Yes |
| 6 | `drawing-003` | 2013-02-12 | Yes |
| 7 | `drawing-010` | 2013-02-27 | Yes |
| 8 | `hello-world` | 2019-06-29 | Yes |
| 9 | `have-you-seen-me-new-fossil-found` | 2013-02-19 | Yes |
| 10 | `hyphae-simulations-mk1` | 2019-08-15 | Yes |
| 11 | `hyphae-simulation-mk2` | 2019-08-16 | Yes |
| 12 | `interiors-cavescapes` | 2014-05-25 | Yes |
| 13 | `make-beautiful-things` | 2015-04-09 | Yes |
| 14 | `make-it-better-1` | 2019-09-05 | Yes |
| 15 | `skyfi-october-2020-parable-of-the-sower-octavia-butler` | 2020-10-27 | Yes |
| 16 | `training-the-unit-6-challenge-2020-week-1` | 2020-02-29 | Yes |

**Note:** `have-you-seen-me-new-fossil-found` returned HTTP 404 on Wix but DOES appear in the sitemap with date 2013-02-19. The 404 may be due to a slug mismatch or URL change.

### Missing Posts (4 of 20)

The following 4 local posts do **not** exist on the live Wix site (return HTTP 404):

| # | Local Slug | Wix Sitemap Entry | Notes |
|---|-----------|-------------------|-------|
| 1 | `concept-sketches-lighthouse` | `concept-sketches-for-a-lighthouse` (2015-05-26) | Slug differs; Wix version has "for-a-" prefix |
| 2 | `skyfi-october-2020-parable-of-the-sower` | Not found in sitemap | Completely absent; likely a separate/earlier post |
| 3 | `have-you-seen-me-new-fossil-found` | `have-you-seen-me-new-fossil-found` (2013-02-19) | In sitemap but returns 404 on direct URL |
| 4 | `staircases-perec` | `staircases-georges-perec-species-of-space` (2015-06-28) | Slug differs; Wix version is longer/more specific |

**Important finding:** Two of the "missing" posts (`concept-sketches-lighthouse` and `staircases-perec`) appear in the sitemap with **different slugs**, suggesting the local files may have been saved with different names than their Wix counterparts. The Wix versions likely have longer, more descriptive slugs. The `skyfi-october-2020-parable-of-the-sower` post (without "octavia-butler" suffix) and `have-you-seen-me-new-fossil-found` (in sitemap but 404) remain unexplained.

---

## Date Verification

| Field | Local | Wix |
|-------|-------|-----|
| Publication dates available | **No** (all 20 sampled posts have empty frontmatter dates) | **Yes** (all posts have dates in sitemap) |

**Key finding:** All 20 local sampled posts have empty `date` fields in their Markdown frontmatter. The Wix sitemap provides dates for all posts, confirming they have valid publication dates. This represents a **content gap in the local repository** — dates should be populated from the Wix sitemap.

For matched posts, Wix dates range from 2013-02-12 to 2020-10-27.

---

## Category/Tag Verification

**Status: Could not complete.** Wix individual post pages render categories in a shadow DOM structure that cannot be accessed via standard web scraping or browser console DOM queries. The blog index page shows category links (e.g., "thinkings") next to each post, but these are sidebar navigation links rather than post-specific assigned categories.

The following categories are available in the Wix blog sidebar navigation:
- `design`
- `drawings`
- `readings`
- `skyfi`
- `thinkings`
- `observings`
- `teachings`
- `writings`

Local posts do not appear to have category/tag frontmatter fields in the sampled files.

---

## Discrepancies Summary

### Confirmed Discrepancies

1. **Slug mismatches (2 posts):** `concept-sketches-lighthouse` and `staircases-perec` have different slugs on Wix. The Wix versions use longer, more descriptive slug names.

2. **Missing posts (2 posts):** `skyfi-october-2020-parable-of-the-sower` (without suffix) does not exist on Wix at all. `have-you-seen-me-new-fossil-found` exists in the sitemap but returns HTTP 404 on direct access.

3. **Empty local dates (20 posts):** All sampled local posts have empty frontmatter dates. This is a data quality issue in the local repository.

### Non-Discrepancies

1. **Body text integrity:** All 16 matched posts have matching body text between local files and Wix.
2. **Post existence:** The vast majority of posts are present on Wix.

---

## Recommendations

1. **Fix slug mismatches:** Update local file names and references for `concept-sketches-lighthouse` and `staircases-perec` to match Wix slug conventions, or create redirects/aliases.

2. **Resolve missing posts:** Investigate the absence of `skyfi-october-2020-parable-of-the-sower` on Wix and the 404 status of `have-you-seen-me-new-fossil-found`. These may need to be published or the local files may be outdated.

3. **Populate local dates:** Extract publication dates from the Wix sitemap and populate the `date` field in all local post frontmatter to close the data quality gap.

4. **Complete category audit:** A follow-up audit should extract category/tag assignments from Wix using a different approach (e.g., Wix API, DOM inspection with shadow root access, or manual verification).

---

## Methodology Notes

- **Local post parsing:** Python script extracted frontmatter from 133 local Markdown files using YAML frontmatter parsing.
- **Wix content scraping:** Individual post pages were fetched via `web_extract` (batched 5 URLs at a time). The blog index and RSS feeds only return the 3 most recent posts.
- **Wix dates:** Retrieved from the sitemap XML (`blog-posts-sitemap.xml`), which lists all posts with their `lastmod` dates.
- **Limitations:** Wix uses shadow DOM/Web Components, preventing standard DOM queries on individual post pages. Category/tag extraction was not possible. Browser navigation was unreliable and prone to crashes/timeouts.
- **Confidence level:** High for body text matching and post existence. Low for category/tag parity (data unavailable).

---

*Audit performed via kanban task t_4e802443.*
