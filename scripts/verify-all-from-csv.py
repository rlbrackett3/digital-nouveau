#!/usr/bin/env python3
"""
Cross-reference every post in the Wix CSV dump against our local markdown files.
Reports: missing posts, content length mismatch, image differences, stat/date drifts.
"""
import csv
import json
import re
from pathlib import Path

CSV_PATH = Path("/root/sync/dn_assets/Posts.csv")
POSTS_DIR = Path("/root/user-files/projects/digital-nouveau/src/content/blog")

def extract_text_from_rich(rich):
    """Extract all plain text from Wix's rich content JSON (node-based format)."""
    if not rich:
        return ""
    texts = []
    def walk(nodes):
        if isinstance(nodes, dict):
            nodes = [nodes]
        for n in nodes:
            if not isinstance(n, dict):
                continue
            t = n.get("type", "")
            if t == "TEXT" and "textData" in n:
                texts.append(n["textData"].get("text", ""))
            if "nodes" in n:
                walk(n["nodes"])
    try:
        data = json.loads(rich)
        walk(data.get("nodes", []))
    except (json.JSONDecodeError, AttributeError):
        pass
    return "\n".join(texts)

def extract_images_from_rich(rich):
    """Extract image src IDs from Wix rich content."""
    images = []
    def walk(nodes):
        if isinstance(nodes, dict):
            nodes = [nodes]
        for n in nodes:
            if not isinstance(n, dict):
                continue
            if n.get("type") == "IMAGE" and "imageData" in n:
                src = n["imageData"].get("image", {}).get("src", {}).get("id", "")
                if src:
                    images.append(src)
            if "nodes" in n:
                walk(n["nodes"])
    try:
        data = json.loads(rich)
        walk(data.get("nodes", []))
    except (json.JSONDecodeError, AttributeError):
        pass
    return images

def parse_cover_image(cover):
    """Extract the image filename from Wix cover image reference."""
    if not cover:
        return ""
    m = re.search(r'([\w]+~mv2\.\w+)', cover)
    if m:
        return m.group(1)
    return cover

def read_frontmatter(content):
    """Read YAML frontmatter from markdown into a dict."""
    fm = {}
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return fm
    for line in m.group(1).split('\n'):
        line = line.strip()
        if ':' in line:
            key, _, val = line.partition(':')
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm

def get_body(content):
    """Get body text (after frontmatter)."""
    m = re.match(r'^---\s*\n.*?\n---\s*\n(.*)', content, re.DOTALL)
    if m:
        return m.group(1).strip()
    return content.strip()

def strip_html(text):
    """Remove HTML tags for comparison."""
    return re.sub(r'<[^>]+>', '', text).strip()

def normalize(text):
    """Normalize whitespace for comparison."""
    return re.sub(r'\s+', ' ', text).strip()

# Load CSV
rows = []
with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print(f"Loaded {len(rows)} posts from CSV\n")

# Build slug index from CSV
csv_by_slug = {}
csv_by_title = {}
for r in rows:
    slug = r.get('Slug', '').strip()
    title = r.get('Title', '').strip().strip('"').strip("'")
    if slug:
        csv_by_slug[slug] = r
    if title:
        csv_by_title[title.lower()] = r

# Get local files
local_files = sorted(POSTS_DIR.glob("*.md"))

# Results
issues = []
matched = 0
missing_images = []
content_mismatches = []
stat_diffs = []
date_diffs = []
category_diffs = []
title_diffs = []

for mdf in local_files:
    slug = mdf.stem
    content = mdf.read_text(encoding='utf-8')
    fm = read_frontmatter(content)
    body = get_body(content)
    body_plain = normalize(strip_html(body))
    local_title = fm.get('title', '').strip().strip('"').strip("'")

    # Find CSV match
    csv_row = csv_by_slug.get(slug)
    if not csv_row:
        # Try title match
        csv_row = csv_by_title.get(local_title.lower())
    if not csv_row:
        issues.append(f"⚠ NO CSV MATCH: {slug} (title='{local_title}')")
        continue

    matched += 1
    csv_title = csv_row.get('Title', '').strip().strip('"').strip("'")
    csv_plain = normalize(csv_row.get('Plain Content', '').strip())
    csv_rich = csv_row.get('Rich Content', '')
    csv_rich_text = normalize(extract_text_from_rich(csv_rich))
    csv_cover = parse_cover_image(csv_row.get('Cover Image', ''))

    # --- Title ---
    n_local = normalize(local_title.lower())
    n_csv = normalize(csv_title.lower())
    if n_local != n_csv and n_local not in n_csv and n_csv not in n_local:
        title_diffs.append(f"  TITLE: local='{local_title}' vs csv='{csv_title}'")

    # --- Body content ---
    # Compare our plain body vs CSV plain content (most reliable)
    csv_body_for_compare = csv_rich_text if len(csv_rich_text) > len(csv_plain) else csv_plain
    
    # Normalize both for comparison
    loc = body_plain[:500]  # first 500 chars
    csvc = normalize(csv_body_for_compare)[:500]
    
    if len(loc) < 20 and len(csvc) > 100:
        content_mismatches.append(f"  BODY: local={len(body_plain)}chars vs csv={len(csv_body_for_compare)}chars — possible missing content")
    elif abs(len(body_plain) - len(csv_body_for_compare)) > 200 and len(csv_body_for_compare) > 100:
        # Check if local has video embed (which would be stripped in comparison)
        has_video = '<iframe' in body or '<div class="video-embed"' in body
        if not has_video or len(body_plain) < len(csv_body_for_compare) * 0.5:
            content_mismatches.append(f"  BODY SIZE: local={len(body_plain)}chars vs csv={len(csv_body_for_compare)}chars — {slug}")

    # --- Cover image ---
    local_img = fm.get('image', '')
    if csv_cover and (not local_img or csv_cover not in local_img):
        if local_img != csv_cover:
            missing_images.append(f"  IMAGE: local='{local_img}' vs csv='{csv_cover}' — {slug}")

    # --- Stats ---
    for stat_key, csv_field in [('views', 'View Count'), ('likes', 'Like Count'), ('comments', 'Comment Count')]:
        csv_val = csv_row.get(csv_field, '').strip()
        local_val = fm.get(stat_key, '').strip()
        if csv_val and csv_val != '0' and local_val != csv_val:
            stat_diffs.append(f"  STAT {stat_key}: local={local_val} vs csv={csv_val} — {slug}")

    # --- Date ---
    csv_date = csv_row.get('Published Date', '').strip()
    local_date = fm.get('pubDate', '').strip().strip('"').strip("'")
    if csv_date and local_date:
        # Normalize: csv might be 2015-05-26T16:44:15Z, local might be '2015-05-26' or 2015-05-26
        csv_d = csv_date[:10]
        local_d = local_date[:10]
        if csv_d != local_d:
            date_diffs.append(f"  DATE: local={local_date} vs csv={csv_date[:10]} — {slug}")

    # --- Categories ---
    csv_cats = csv_row.get('Categories', '').strip().strip('"').strip("'")
    local_cats = fm.get('categories', '').strip()
    if csv_cats and local_cats:
        try:
            csv_cat_list = set(json.loads(csv_cats.replace('""', '"')))
            local_cat_list = set(re.findall(r'["\']?(\w+)["\']?', local_cats))
            # Category mapping: Wix uses different names sometimes
            mapping = {'projects': 'design', 'thoughts': 'thinkings'}
            csv_mapped = set(mapping.get(c, c) for c in csv_cat_list)
            if csv_mapped and not csv_mapped.intersection(local_cat_list):
                category_diffs.append(f"  CATS: local={local_cat_list} vs csv={csv_cat_list} — {slug}")
        except (json.JSONDecodeError, AttributeError):
            pass

# --- Report ---
print(f"Matched: {matched}/{len(local_files)} posts\n")

if title_diffs:
    print(f"=== TITLE MISMATCHES ({len(title_diffs)}) ===")
    for d in title_diffs[:15]:
        print(d)
    if len(title_diffs) > 15:
        print(f"  ... and {len(title_diffs)-15} more")

if content_mismatches:
    print(f"\n=== CONTENT ISSUES ({len(content_mismatches)}) ===")
    for d in content_mismatches[:25]:
        print(d)
    if len(content_mismatches) > 25:
        print(f"  ... and {len(content_mismatches)-25} more")

if missing_images:
    print(f"\n=== COVER IMAGE DIFFERENCES ({len(missing_images)}) ===")
    for d in missing_images[:20]:
        print(d)
    if len(missing_images) > 20:
        print(f"  ... and {len(missing_images)-20} more")

if stat_diffs:
    print(f"\n=== STAT DIFFERENCES ({len(stat_diffs)}) ===")
    for d in stat_diffs[:20]:
        print(d)
    if len(stat_diffs) > 20:
        print(f"  ... and {len(stat_diffs)-20} more")

if date_diffs:
    print(f"\n=== DATE DIFFERENCES ({len(date_diffs)}) ===")
    for d in date_diffs[:15]:
        print(d)
    if len(date_diffs) > 15:
        print(f"  ... and {len(date_diffs)-15} more")

if category_diffs:
    print(f"\n=== CATEGORY DIFFERENCES ({len(category_diffs)}) ===")
    for d in category_diffs[:10]:
        print(d)
    if len(category_diffs) > 10:
        print(f"  ... and {len(category_diffs)-10} more")

if issues:
    print(f"\n=== UNMATCHED POSTS ({len(issues)}) ===")
    for d in issues:
        print(d)

print(f"\n--- Summary ---")
print(f"  Total local posts:  {len(local_files)}")
print(f"  CSV rows:           {len(rows)}")
print(f"  Matched:            {matched}")
print(f"  Content issues:     {len(content_mismatches)}")
print(f"  Cover image diffs:  {len(missing_images)}")
print(f"  Stat diffs:         {len(stat_diffs)}")
print(f"  Date diffs:         {len(date_diffs)}")
print(f"  Category diffs:     {len(category_diffs)}")
