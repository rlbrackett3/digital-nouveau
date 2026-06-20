# Digital Nouveau - Verification Plan

## Gates (ordered fast → rigorous)

### Gate 1: Build
- **Command:** `npm run build`
- **Pass:** Exit 0, 146 pages built, 0 errors
- **Fail:** Any build error

### Gate 2: Background
- **Check:** `curl -s http://localhost:4322/ | grep -q "neural-bg"`
- **Visual:** Neural pattern visible behind content at 15% opacity
- **Pass:** Background renders on all pages

### Gate 3: Text Readability
- **Check:** Body text color is `rgb(28, 235, 244)` NOT white/gray
- **Visual:** All text readable on mobile (Tailscale `100.114.36.84:4322`)
- **Pass:** User confirms text is legible on phone

### Gate 4: Link Colors
- **Check:** All `<a>` elements have `color: rgb(28, 235, 244)`
- **Command:** `curl -s http://localhost:4322/ | grep -c "#0000ee"` returns 0
- **Pass:** No blue links, all cyan

### Gate 5: Typography
- **Check:** Font-family includes `DM Sans` or `brandon-grot`
- **Visual:** Titles render at 28px, body at 14px
- **Pass:** Font stack loads from Google Fonts or local

### Gate 6: Header Structure
- **Check:** Title "Digital Nouveau ~" present
- **Check:** Taglines present
- **Check:** Utility nav (feed/portfolio/skyfi) present
- **Check:** Main nav categories present (9 items)
- **Pass:** Header matches Wix screenshot

### Gate 7: Blog Card Structure
- **Check:** Image → meta (author/date) → title → social → stats order
- **Visual:** Card border is 1px cyan
- **Pass:** First post card matches Wix screenshot

### Gate 8: Recent Posts Grid
- **Check:** 3-column grid CSS (`grid-template-columns: repeat(3, 1fr)`)
- **Check:** 3+ recent post cards rendered
- **Pass:** Grid matches Wix screenshot

### Gate 9: Footer
- **Check:** Newsletter form present (name + email + submit)
- **Check:** "follow along" heading present
- **Pass:** Footer matches Wix screenshot

### Gate 10: Content Count
- **Check:** 111 posts in `src/content/blog/`
- **Command:** `ls src/content/blog/*.md | wc -l` returns 111
- **Pass:** All posts rendered in `/blog/` archive

### Gate 11: SkyFi Page
- **Check:** 4-column book list layout
- **Check:** "Currently Reading" section present
- **Pass:** SkyFi page matches Wix screenshot

### Gate 12: Mobile Readability
- **User check:** Open `100.114.36.84:4322` on phone
- **Pass:** User confirms everything is readable

## Automation

Gates 1, 4, 10 can be automated in CI:
```bash
#!/bin/bash
# verify.sh
npm run build && echo "Gate 1 PASS" || exit 1
curl -s http://localhost:4322/ | grep -c "#0000ee" | grep -q "^0$" && echo "Gate 4 PASS" || exit 1
ls src/content/blog/*.md | wc -l | grep -q "111" && echo "Gate 10 PASS" || exit 1
```

## Manual Gates

Gates 2-3, 5-9, 11-12 require visual comparison against Wix screenshots.

## Gate Results

| Gate | Status | Notes |
|------|--------|-------|
| 1. Build | ✅ PASS | 146 pages, 0 errors |
| 2. Background | ✅ PASS | Neural bg visible, opacity 0.15 |
| 3. Text Readability | ✅ PASS | Cyan #1cebf4 on #000000 |
| 4. Link Colors | ✅ PASS | All links cyan #1cebf4 |
| 5. Typography | ✅ PASS | DM Sans Light 300, 14px body |
| 6. Header | ✅ PASS | Title/taglines left, nav right |
| 7. Blog Cards | ⬜ TODO | |
| 8. Recent Posts | ⬜ TODO | |
| 9. Footer | ⬜ TODO | |
| 10. Content | ⬜ TODO | |
| 11. SkyFi | ⬜ TODO | |
| 12. Mobile | ⬜ TODO | Final user approval |
