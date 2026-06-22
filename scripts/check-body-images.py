#!/usr/bin/env python3
"""Check body image references for the 37 unmapped empty-image posts."""
import re, os, glob

BLOG_DIR = "/root/user-files/projects/digital-nouveau/src/content/blog"
UNMAPPED = [
    "a-butterfly-for-hope", "a-texas-thistle", "architecture-where-design-meets-engineering",
    "arnica-softly", "arterial-spray-or-coffee-ricocheting-off-a-door-and-onto-a-wall",
    "brrrrrraaaaaaiiiiiiiinnnnnsssss", "cholla-cactus-wood-joshua-tree-national-park",
    "demon-seed", "drawing-001", "drawing-002", "drawing-003", "drawing-004",
    "drawing-005", "drawing-006", "drawing-007", "drawing-008", "drawing-009",
    "drawing-010", "drawing-011", "drawing-012", "drawing-013", "drawing-014",
    "drawing-015", "drawing-016", "drawing-017", "drawing-019",
    "drawing-021-summer-camp-landscapes", "fun-with-the-scanner",
    "journey-through-america-s-southwest", "make-it-better-1",
    "on-a-trip-to-the-rose-garden", "patterns-arnica-cb1001",
    "proto-flower", "savoring-complexity",
    "sterling-luna-moth-transformation-le-dweez-de-luna",
    "thick-space-mapping-ambiguous-territories", "tictoc-a-gnarly-clock",
]

# Extract image references from post bodies
for slug in UNMAPPED:
    fpath = os.path.join(BLOG_DIR, f"{slug}.md")
    if not os.path.exists(fpath):
        print(f"{slug}: FILE MISSING")
        continue
    
    with open(fpath) as f:
        content = f.read()
    
    # Look for figure/image references in the body (not frontmatter)
    # Pattern: ![alt](filename) or <img src="filename">
    body_images = re.findall(r'!\[.*?\]\((.*?)\)', content)
    img_src = re.findall(r'<img\s+src="(.*?)"', content)
    
    all_refs = body_images + img_src
    
    if all_refs:
        print(f"{slug}: {len(all_refs)} body image refs")
        for ref in all_refs[:3]:
            print(f"  - {ref}")
    else:
        print(f"{slug}: no body image refs")
