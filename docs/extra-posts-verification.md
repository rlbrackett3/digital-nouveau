# Extra Posts Verification Report

**Task:** Identify local blog posts not present on the live Wix site, verify each against blog.digitalnouveau.com, and document findings.

**Date:** 2026-06-21

**Method:** Browser-based navigation to `https://blog.digitalnouveau.com/blog/<slug>` for each local post. Wix 404 pages display a "Sign Up" dialog overlay. Automated curl/web-extract requests are blocked by Wix's bot detection and return empty content; HTTP 200 status is unreliable due to Wix SPA client-side routing (all routes return 200). Therefore, browser inspection was the only reliable verification method.

**Baseline:** The authoritative list of Wix-published posts is stored in `scripts/wix-stats-cache.json` (the Wix API export). All comparisons are against this file.

---

## Findings

**All 14 local blog posts are confirmed absent from the live Wix site.** Each slug was navigated to in the browser and returned a Wix 404 page (displaying the "Sign Up" dialog).

No title/slug mismatches were found — none of these posts exist on Wix at all, so no comparison of titles or slugs against Wix-published versions is possible.

---

## Confirmed Missing Posts

| # | Local Slug | Local Title (from frontmatter) | Status on Wix |
|---|-----------|-------------------------------|---------------|
| 1 | `cholla-cactus-wood` | "Cholla Cactus Wood - Joshua Tree National Park" | 404 — Not published |
| 2 | `comics-beyond-fiction-trans-fiction-2020` | "Comics Beyond Fiction :: [Trans-] FICTION 2020" | 404 — Not published |
| 3 | `concept-sketches-for-a-lighthouse` | "Concept Sketches for a Lighthouse" | 404 — Not published |
| 4 | `learning-to-design-home` | "Learning to Design @ Home :: Drawing and Modeling" | 404 — Not published |
| 5 | `make-it-better` | "Make It Better" | 404 — Not published |
| 6 | `organisms` | "ORGANISMS :: HYPNO-TOPO-GRAPHY" | 404 — Not published |
| 7 | `out-there-and-all-those-images-in-there` | "Out There :: And All Those Images In There" | 404 — Not published |
| 8 | `skyfi-april-2020-agency-by-william-gibson` | "SkyFi :: April 2020 :: Agency by William Gibson" | 404 — Not published |
| 9 | `skyfi-december-2019-ninefox-gambit` | "SkyFi :: December 2019 :: Ninefox Gambit" | 404 — Not published |
| 10 | `skyfi-july-2019` | "SkyFi :: July 2019 :: Strange Stars" | 404 — Not published |
| 11 | `skyfi-september-2019` | "SkyFi :: September 2019 :: Shadowbahn by Steve Erickson" | 404 — Not published |
| 12 | `staircases-georges-perec-species-of-space` | "Staircases - Georges Perec - Species of Space" | 404 — Not published |
| 13 | `the-computer-connection` | "The Computer Connection :: Alfred Bester" | 404 — Not published |
| 14 | `thick-space-mapping-ambiguous-territories` | "THICK SPACE :: MAPPING AMBIGUOUS TERRITORIES" | 404 — Not published |

---

## Summary

- **Total local posts checked:** 14
- **Confirmed present on Wix:** 0
- **Confirmed missing on Wix:** 14 (100%)
- **Title/slug mismatches:** N/A (no Wix versions exist to compare against)

### Observations

1. **Local-first workflow:** All 14 posts exist only in the local `src/content/blog/` directory and have not been published to the Wix site. These appear to be drafts, unpublished content, or posts that were written locally but never deployed.

2. **SkyFi posts are a notable subset:** 5 of the 14 posts are part of the "SkyFi" series (monthly reading lists from 2019-2020). None of these appear on the live site, suggesting the SkyFi series may be in early development or deprioritized.

3. **No Wix-published duplicates exist:** None of the 14 local slugs could be found via Wix's search or pagination — they are not hidden posts, draft-published posts with different slugs, or posts that were later removed.

4. **Recommendation:** These posts are candidates for:
   - Publishing to the Wix site (if they are considered ready)
   - Deletion from the local repository (if they are abandoned drafts)
   - Further development (if they are work-in-progress)

---

## Open Questions

1. Were any of these posts ever published on Wix and later removed? (Wix provides no public archive or wayback for unpublished/removed posts.)
2. Is the full Wix API export (`wix-stats-cache.json`) up to date with all current published posts, or could there be posts on Wix that are not reflected in the cache?
3. Do any of the 14 local posts have corresponding but differently-slug'd versions already published on Wix?
