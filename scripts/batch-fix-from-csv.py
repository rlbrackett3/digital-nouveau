#!/usr/bin/env python3
"""
Batch-fix all 111 posts against the Wix CSV dump.
Fixes: dates, stats, categories, images, and title encoding.
"""
import csv
import json
import re
import os
import urllib.request
from pathlib import Path

CSV_PATH = Path("/root/sync/dn_assets/Posts.csv")
POSTS_DIR = Path("/root/user-files/projects/digital-nouveau/src/content/blog")
IMAGES_DIR = Path("/root/user-files/projects/digital-nouveau/public/images")

# Category UUID -> name mapping (verified by cross-referencing local files)
CAT_UUID_MAP = {
    "5d17ad2306b28c0016c0fb5c": "design",
    "5d17ad910bdf230016d98e95": "drawings",
    "5d17adac528d9400e68e4c68": "observings",
    "5d17ae2709fd900016e34619": "skyfi",
    "5d17aea198c5cc00160844c0": "readings",
    "5d52c93365f8810016f2c9bc": "thinkings",
    "5d52e12bc35e8400177a4d99": "teachings",
    "5f73a3919c98400018a08370": "writings",
}

# Fixes for date mismatches from verification
DATE_FIXES = {
    "forming-rivers": "2015-02-25",
    "hyphae-simulation-mk3": "2019-08-18",
    "hyphae-simulations-mk1": "2019-08-15",
    "make-it-better": "2015-09-11",
    "make-things": "2015-10-09",
    "poetry-of-design": "2015-03-25",
    "skyfi-december-2019-ninefox-gambit": "2019-12-24",
}

# Stats fixes
STATS_FIXES = {
    "make-it-better": {"views": 5},
    "skyfi-december-2019-ninefox-gambit": {"views": 12, "likes": 1},
}

WIX_CDN = "https://static.wixstatic.com/media/"

def extract_image_id(cover_field):
    """Extract the image filename from a Wix cover image reference."""
    if not cover_field:
        return None
    # Pattern: wix:image://v1/ID/ID#...
    m = re.search(r'/v1/([^/]+?)(?:~mv2\.[a-z]+(?:~mv2)?\.[a-z]+)', cover_field)
    if m:
        return m.group(1)
    # Simpler: just grab the dc9b92_xxxx pattern
    m2 = re.search(r'(dc9b92_[a-zA-Z0-9]+~mv2\.[a-z]+)', cover_field)
    if m2:
        return m2.group(1)
    return None

def fix_frontmatter_field(content, field, value):
    """Update or add a frontmatter field."""
    # Replace existing
    new_content = re.sub(
        rf'^{re.escape(field)}:.*$',
        f'{field}: {value}',
        content,
        count=1,
        flags=re.MULTILINE
    )
    if new_content != content:
        return new_content
    # Add before closing ---
    new_content = re.sub(
        r'^---\s*$',
        f'{field}: {value}\n---',
        content,
        count=1,
        flags=re.MULTILINE
    )
    return new_content

# Load CSV
with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

# Index by slug
csv_by_slug = {}
for r in rows:
    slug = r.get('Slug', '').strip()
    if slug:
        csv_by_slug[slug] = r

fixed_dates = 0
fixed_stats = 0
fixed_cats = 0
fixed_images = 0
fixed_titles = 0
downloaded = 0

for mdf in sorted(POSTS_DIR.glob("*.md")):
    slug = mdf.stem
    csv_row = csv_by_slug.get(slug)
    if not csv_row:
        continue
    
    content = mdf.read_text(encoding='utf-8')
    changed = False

    # 1. Fix dates
    if slug in DATE_FIXES:
        new_date = DATE_FIXES[slug]
        old = re.search(r'^pubDate:\s*(.+)$', content, re.MULTILINE)
        if old and old.group(1).strip().strip('"').strip("'") != new_date:
            content = re.sub(
                r'^(pubDate:\s*).*$',
                f'pubDate: {new_date}',
                content,
                count=1,
                flags=re.MULTILINE
            )
            fixed_dates += 1
            changed = True

    # 2. Fix stats
    if slug in STATS_FIXES:
        for stat_key, stat_val in STATS_FIXES[slug].items():
            old = re.search(rf'^{stat_key}:\s*(.+)$', content, re.MULTILINE)
            if old:
                old_val = old.group(1).strip()
                if old_val != str(stat_val) and old_val in ('', '0'):
                    content = re.sub(
                        rf'^{stat_key}:.*$',
                        f'{stat_key}: {stat_val}',
                        content,
                        count=1,
                        flags=re.MULTILINE
                    )
                    fixed_stats += 1
                    changed = True

    # 3. Fix categories (if CSV has UUIDs, convert to names)
    csv_cats_str = csv_row.get('Categories', '').strip().strip('"').strip("'")
    if csv_cats_str:
        try:
            csv_uuids = set(json.loads(csv_cats_str.replace('""', '"')))
            csv_names = [CAT_UUID_MAP.get(u, u) for u in csv_uuids]
            csv_names.sort()
            csv_names_str = ', '.join(f'"{n}"' for n in csv_names)
            
            # Check current local categories
            m = re.search(r'^categories:\s*\[(.*?)\]', content, re.MULTILINE | re.DOTALL)
            if m:
                local_cats = set(re.findall(r'"([^"]+)"', m.group(1)))
                if local_cats != set(csv_names):
                    content = re.sub(
                        r'^categories:\s*\[.*?\]',
                        f'categories: [{csv_names_str}]',
                        content,
                        count=1,
                        flags=re.MULTILINE | re.DOTALL
                    )
                    fixed_cats += 1
                    changed = True
        except (json.JSONDecodeError, AttributeError):
            pass

    # 4. Fix cover image
    csv_cover = csv_row.get('Cover Image', '').strip()
    if csv_cover:
        img_id = extract_image_id(csv_cover)
        if img_id:
            img_path = f"/images/{img_id}"
            
            # Check current frontmatter
            m = re.search(r'^image:\s*(.*)$', content, re.MULTILINE)
            current_img = m.group(1).strip().strip('"').strip("'") if m else ""
            
            if not current_img or current_img != img_path:
                # Check if file exists locally
                local_img = IMAGES_DIR / img_id
                if not local_img.exists():
                    # Download from Wix CDN
                    wix_url = f"{WIX_CDN}{img_id}"
                    try:
                        print(f"  Downloading {img_id}...")
                        urllib.request.urlretrieve(wix_url, local_img)
                        downloaded += 1
                    except Exception as e:
                        print(f"  FAILED to download {img_id}: {e}")
                
                if current_img:
                    content = re.sub(
                        r'^image:.*$',
                        f'image: "{img_path}"',
                        content,
                        count=1,
                        flags=re.MULTILINE
                    )
                else:
                    content = fix_frontmatter_field(content, 'image', f'"{img_path}"')
                fixed_images += 1
                changed = True

    # 5. Fix HTML-encoded titles
    if '&#x27;' in content:
        content = content.replace('&#x27;', "'")
        fixed_titles += 1
        changed = True
    if '&amp;' in content:
        content = content.replace('&amp;', '&')
        fixed_titles += 1
        changed = True

    if changed:
        mdf.write_text(content, encoding='utf-8')
        print(f"  Fixed: {slug}")

print(f"\n=== Summary ===")
print(f"  Dates fixed:     {fixed_dates}")
print(f"  Stats fixed:     {fixed_stats}")
print(f"  Categories fixed: {fixed_cats}")
print(f"  Images fixed:     {fixed_images} (downloaded {downloaded} new files)")
print(f"  Titles fixed:     {fixed_titles}")
