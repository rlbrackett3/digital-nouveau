#!/usr/bin/env python3
"""Normalize frontmatter across all 133 blog posts in digital-nouveau.

Fixes:
1. Empty image fields: populated from blog-image-mapping.json first,
   then from body image references, then skipped.
2. Body image references stripped of /images/ prefix → clean filenames.
3. Validates pubDate format (YYYY-MM-DD) — skip if OK.
4. Validates categories against Wix taxonomy — skip if OK.
"""
import re, os, json, glob

BLOG_DIR = "/root/user-files/projects/digital-nouveau/src/content/blog"
MAPPING_FILE = "/root/user-files/projects/digital-nouveau/blog-image-mapping.json"
WIX_CATEGORIES = {"design", "drawings", "readings", "skyfi", "thinkings", "observings", "teachings", "writings"}

# Load blog-image-mapping.json
with open(MAPPING_FILE) as f:
    image_mapping = json.load(f)

# Track stats
stats = {"fixed_image": 0, "skipped_no_image": 0, "skipped_no_change": 0, "bad_date": 0, "bad_category": 0, "total": 0}

def extract_first_body_image(content):
    """Extract the first valid image reference from post body, return filename only.
    Handles both markdown ![alt](url) and HTML <img src="url"> formats.
    """
    # HTML img tags — priority (more common in these posts)
    img_tags = re.findall(r'<img\s+src="(.*?)"', content)
    for ref in img_tags:
        if ref.startswith("/images/"):
            return ref[len("/images/"):]
        if not ref.startswith("http"):
            return ref

    # Markdown images: ![alt](filename) — exclude external URLs
    body_images = re.findall(r'!\[.*?\]\((?!https?://)([^)]+)\)', content)
    for ref in body_images:
        if ref.startswith("/images/"):
            return ref[len("/images/"):]
        if not ref.startswith("http"):
            return ref

    return None

def process_post(filepath, filename):
    """Process a single blog post. Returns (was_changed, reason)."""
    with open(filepath) as f:
        content = f.read()

    # Extract frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not fm_match:
        return False, "no frontmatter"

    fm_text = fm_match.group(1)
    rest = content[fm_match.end():]

    # Check pubDate format
    date_match = re.search(r'^pubDate:\s*(.+)$', fm_text, re.MULTILINE)
    if date_match:
        date_str = date_match.group(1).strip().strip('"\'')
        if not re.match(r'^\d{4}-\d{2}-\d{2}', date_str):
            stats["bad_date"] += 1
            return False, f"bad date: {date_str}"

    # Check categories
    cat_match = re.search(r'^categories:\s*\[(.+?)\]', fm_text, re.MULTILINE)
    if cat_match:
        cats_str = cat_match.group(1)
        cats = [c.strip().strip('"\'') for c in cats_str.split(',')]
        for cat in cats:
            if cat not in WIX_CATEGORIES:
                stats["bad_category"] += 1
                return False, f"bad category: {cat}"

    # Check image field
    image_match = re.search(r'^image:\s*(.+)$', fm_text, re.MULTILINE)
    if not image_match:
        return False, "no image field at all"

    current_image = image_match.group(1).strip().strip('"\'')
    slug = filename.replace('.md', '')

    if current_image:
        # Has an image — check if it's valid (not doubled path)
        if current_image.startswith("/images/images/"):
            # Doubled path fix
            new_image = "/images/" + current_image[len("/images/images/"):]
            content = content[:image_match.start(1)] + new_image + content[image_match.end(1):]
            with open(filepath, 'w') as f:
                f.write(content)
            return True, f"doubled path fixed → {new_image}"
        return False, "already has image"

    # Empty image field — try to fill
    # Priority 1: blog-image-mapping.json
    if slug in image_mapping and image_mapping[slug]:
        new_image = image_mapping[slug][0]
        content = content[:image_match.start(1)] + new_image + content[image_match.end(1):]
        with open(filepath, 'w') as f:
            f.write(content)
        return True, f"filled from mapping → {new_image}"

    # Priority 2: body image references
    first_body_img = extract_first_body_image(rest)
    if first_body_img:
        content = content[:image_match.start(1)] + first_body_img + content[image_match.end(1):]
        with open(filepath, 'w') as f:
            f.write(content)
        return True, f"filled from body → {first_body_img}"

    # No image found anywhere
    stats["skipped_no_image"] += 1
    return False, f"no image source for {slug}"

# Main loop
for md_file in sorted(glob.glob(os.path.join(BLOG_DIR, "*.md"))):
    filename = os.path.basename(md_file)
    stats["total"] += 1
    changed, reason = process_post(md_file, filename)
    if changed:
        stats["fixed_image"] += 1
        print(f"  FIXED: {filename}: {reason}")
    else:
        if reason != "no image field at all":
            pass  # silent for unchanged

# Print summary
print(f"\n{'='*60}")
print(f"Normalization complete:")
print(f"  Total posts scanned:  {stats['total']}")
print(f"  Image fields filled:  {stats['fixed_image']}")
print(f"  Skipped (no source):  {stats['skipped_no_image']}")
print(f"  Already OK:           {stats['skipped_no_change'] + stats['total'] - stats['fixed_image'] - stats['skipped_no_image']}")
print(f"  Bad dates:            {stats['bad_date']}")
print(f"  Bad categories:       {stats['bad_category']}")
print(f"{'='*60}")
