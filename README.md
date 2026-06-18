# Digital Nouveau Blog

Migration of blog.digitalnouveau.com from Wix to static Astro hosting on GetForge.

## Stack

- **Framework:** Astro 5.x (static output)
- **Content:** Markdown with frontmatter (title, description, pubDate, categories)
- **Hosting:** GetForge (CloudFront CDN)
- **Source:** Wix SPA (blog.digitalnouveau.com)

## Structure

```
src/
├── content/blog/     # 57 extracted posts (.md)
├── pages/            # File-based routing
├── components/       # SiteLayout, Header, Footer
├── layouts/          # BlogPost layout
├── styles/           # global.css (dark theme)
└── utils/            # posts.ts
```

## Commands

```bash
npm run dev      # Local dev server
npm run build    # Static build to dist/
npm run preview  # Preview built site
```

## Content

- 57 blog posts extracted from Wix (2013-2020)
- 8 categories: design, drawings, readings, skyfi, thinkings, observings, teachings, writings
- Cross-category tagging supported
- SkyFi reading list: separate page with ~100 books

## Remaining Work

- [ ] Extract remaining ~15 posts from Wix
- [ ] Download Wix post images
- [ ] Deploy to GetForge
- [ ] DNS verification
- [ ] Visual styling polish
