#!/usr/bin/env python3
"""Fix missing image references in blog posts.

1. Add /images/ prefix to markdown images that use relative paths.
2. Strip truly missing figure images.
3. Strip truly missing markdown images.
"""
import os
import re
import json
from pathlib import Path

BASE_DIR = Path("/root/user-files/projects/digital-nouveau")
PUBLIC_IMAGES = BASE_DIR / "public" / "images"
BLOG_DIR = BASE_DIR / "src" / "content" / "blog"

# Get all existing image filenames
existing = set(PUBLIC_IMAGES.iterdir())
existing_names = {f.name for f in existing}

# Regex to strip Wix dimension suffix: _d_WxH_s_N -> .ext
DIM_SUFFIX = re.compile(r'_d_\d+_\d+_s_\d+\.')

# Collect all unique image references from current state
figure_refs = set()  # from <img src="/images/dc9b92_...">
md_refs = set()      # from ![alt](/images/dc9b92_...) or ![alt](dc9b92_...)

for md_file in BLOG_DIR.glob("*.md"):
    content = md_file.read_text()
    # Figure images
    for m in re.finditer(r'src="/images/dc9b92_[^"]*"', content):
        img = m.group().removeprefix('src="').removesuffix('"')
        figure_refs.add(img)
    # Markdown images (with or without /images/ prefix)
    for m in re.finditer(r'\]\((dc9b92_[^)]+)\)', content):
        img = m.group(1)
        if not img.startswith('/images/'):
            img = f'/images/{img}'
        md_refs.add(img)

all_refs = figure_refs | md_refs

# Normalize to filename
def to_filename(ref):
    if ref.startswith('/images/'):
        return ref[len('/images/'):]
    return ref

# Classify
found = []
missing_with_base = []  # (original_ref, base_ref)
truly_missing = []

for ref in all_refs:
    fname = to_filename(ref)
    if fname in existing_names:
        found.append(ref)
    else:
        base_fname = DIM_SUFFIX.sub('.', fname)
        if base_fname in existing_names:
            missing_with_base.append((ref, f'/images/{base_fname}'))
        else:
            truly_missing.append(ref)

print(f"Total unique refs: {len(all_refs)}")
print(f"Found: {len(found)}")
print(f"Missing with base: {len(missing_with_base)}")
print(f"Truly missing: {len(truly_missing)}")

# Build replacement map for base versions
replacements = {}
for orig, base in missing_with_base:
    replacements[orig] = base

# Apply fixes
fixed_count = 0
for md_file in BLOG_DIR.glob("*.md"):
    content = md_file.read_text()
    new_content = content

    # 1. Add /images/ prefix to relative markdown images
    new_content = re.sub(r'\]\((dc9b92_[^)]+)\)', r'](/images/\1)', new_content)

    # 2. Replace missing images that have base versions
    for orig, base in replacements.items():
        new_content = new_content.replace(orig, base)

    # 3. Strip truly missing figure images
    for img in truly_missing:
        escaped = re.escape(img)
        pattern = rf'<figure>\s*<img src="{escaped}"[^>]*/?>\s*\n*</figure>'
        new_content = re.sub(pattern, '', new_content, flags=re.DOTALL)
        pattern2 = rf'<figure>\s*<img src="{escaped}"[^>]*/?>\s*\n*</figure>\s*\n'
        new_content = re.sub(pattern2, '', new_content, flags=re.DOTALL)

    # 4. Strip truly missing markdown images
    for img in truly_missing:
        escaped = re.escape(img)
        pattern = rf'!\[[^\]]*\]\({escaped}\)'
        new_content = re.sub(pattern, '', new_content)
        new_content = re.sub(r'\n{3,}', '\n\n', new_content)

    if new_content != content:
        md_file.write_text(new_content)
        fixed_count += 1

print(f"\nFixed {fixed_count} files")

# Verify
remaining = 0
for md_file in BLOG_DIR.glob("*.md"):
    content = md_file.read_text()
    for img in truly_missing:
        if img in content:
            remaining += 1

print(f"Remaining broken refs: {remaining}")
if remaining > 0:
    for md_file in BLOG_DIR.glob("*.md"):
        content = md_file.read_text()
        for img in truly_missing:
            if img in content:
                print(f"  STILL IN {md_file.name}: {img}")
