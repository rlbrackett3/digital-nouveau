#!/usr/bin/env python3
"""Check which empty-image posts have mapping entries."""
import json, re, os, glob

BLOG_DIR = "/root/user-files/projects/digital-nouveau/src/content/blog"
MAP_PATH = "/root/user-files/projects/digital-nouveau/blog-image-mapping.json"

with open(MAP_PATH) as f:
    image_map = json.load(f)

md_files = sorted(glob.glob(os.path.join(BLOG_DIR, "*.md")))

# Find posts with empty images
empty_posts = []
for fpath in md_files:
    fname = os.path.basename(fpath)
    slug = fname.replace(".md", "")
    with open(fpath) as f:
        content = f.read()
    fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        img_empty = re.search(r'^image:\s*["\']{0,2}["\']{0,2}\s*$', fm, re.MULTILINE)
        if img_empty:
            has_mapping = slug in image_map
            mapping_count = len(image_map.get(slug, []))
            empty_posts.append((slug, has_mapping, mapping_count))

print(f"Posts with empty image field: {len(empty_posts)}")
print()

with_mapping = [p for p in empty_posts if p[1]]
without_mapping = [p for p in empty_posts if not p[1]]

print(f"With mapping entry: {len(with_mapping)}")
for slug, _, count in with_mapping:
    print(f"  {slug}: {count} images in map")

print(f"\nWITHOUT mapping entry: {len(without_mapping)}")
for slug, _, _ in without_mapping:
    print(f"  {slug}")
