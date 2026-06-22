#!/usr/bin/env python3
"""Audit all blog post frontmatter for normalization issues."""
import os, re, glob

BLOG_DIR = "/root/user-files/projects/digital-nouveau/src/content/blog"
md_files = sorted(glob.glob(os.path.join(BLOG_DIR, "*.md")))

# Known Wix categories (from blog.digitalnouveau.com)
WIX_CATEGORIES = {
    "design", "skyfi", "readings", "thinkings", "jewelry", 
    "process", "workshops", "teaching", "collaboration", 
    "exhibitions", "residencies", "publications", "writing",
    "photography", "drawing", "sculpture", "digital",
    "architecture", "environmental", "performance", "video"
}

issues = {"doubled_images": [], "bad_pubdate": [], "unknown_categories": [], "empty_images": [], "image_paths": []}

for fpath in md_files:
    fname = os.path.basename(fpath)
    slug = fname.replace(".md", "")
    
    with open(fpath) as f:
        content = f.read()
    
    # Extract frontmatter
    fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not fm_match:
        issues["empty_images"].append((slug, "no frontmatter found"))
        continue
    
    fm = fm_match.group(1)
    
    # Check image field
    img_match = re.search(r'^image:\s*(.+)$', fm, re.MULTILINE)
    if img_match:
        img_val = img_match.group(1).strip()
        issues["image_paths"].append((slug, img_val))
        
        # Check for doubled path: /images/images/
        if re.search(r'^["\']?/images/images/', img_val):
            issues["doubled_images"].append((slug, img_val))
        
        # Check for double slash in path
        if '//' in img_val and not img_val.startswith('http'):
            issues["doubled_images"].append((slug, f"doubled slash: {img_val}"))
    
    # Check empty/blank image
    img_empty = re.search(r'^image:\s*["\']{0,2}["\']{0,2}\s*$', fm, re.MULTILINE)
    if img_empty:
        issues["empty_images"].append((slug, "image is empty string"))
    
    # Check pubDate format
    date_match = re.search(r"^pubDate:\s*'([^']+)'", fm, re.MULTILINE)
    if date_match:
        date_val = date_match.group(1)
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_val):
            issues["bad_pubdate"].append((slug, date_val))
    
    # Check categories
    cat_match = re.search(r'^categories:\s*\[(.+?)\]', fm, re.MULTILINE)
    if cat_match:
        cats_str = cat_match.group(1)
        cats = [c.strip().strip('"').strip("'") for c in cats_str.split(',')]
        for cat in cats:
            if cat and cat not in WIX_CATEGORIES:
                issues["unknown_categories"].append((slug, cat))

# Print results
print(f"{'='*60}")
print(f"SCAN COMPLETE: {len(md_files)} posts scanned")
print(f"{'='*60}")

if issues["doubled_images"]:
    print(f"\nDOUBLED IMAGE PATHS: {len(issues['doubled_images'])}")
    for slug, val in issues["doubled_images"]:
        print(f"  {slug}: {val}")
else:
    print("\nDOUBLED IMAGE PATHS: None found")

if issues["empty_images"]:
    print(f"\nEMPTY IMAGE FIELDS: {len(issues['empty_images'])}")
    for slug, val in issues["empty_images"]:
        print(f"  {slug}: {val}")
else:
    print("\nEMPTY IMAGE FIELDS: None found")

if issues["bad_pubdate"]:
    print(f"\nBAD PUBDATE FORMAT: {len(issues['bad_pubdate'])}")
    for slug, val in issues["bad_pubdate"]:
        print(f"  {slug}: {val}")
else:
    print("\nBAD PUBDATE FORMAT: None found")

if issues["unknown_categories"]:
    print(f"\nUNKNOWN CATEGORIES: {len(issues['unknown_categories'])}")
    for slug, cat in issues["unknown_categories"]:
        print(f"  {slug}: '{cat}'")
else:
    print("\nUNKNOWN CATEGORIES: None found")

# Also print all unique categories found
all_cats = set()
for fpath in md_files:
    with open(fpath) as f:
        content = f.read()
    fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        cat_match = re.search(r'^categories:\s*\[(.+?)\]', fm, re.MULTILINE)
        if cat_match:
            cats_str = cat_match.group(1)
            cats = [c.strip().strip('"').strip("'") for c in cats_str.split(',')]
            all_cats.update(cats)

print(f"\nALL CATEGORIES FOUND: {sorted(all_cats)}")
print(f"{'='*60}")
