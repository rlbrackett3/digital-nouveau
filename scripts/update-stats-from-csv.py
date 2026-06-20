#!/usr/bin/env python3
"""Extract stats from Posts.csv and update Astro frontmatter."""
import csv
import re
from pathlib import Path

CSV_PATH = Path("/root/.hermes/cache/documents/doc_9879131a8257_Posts.csv")
POSTS_DIR = Path("/root/user-files/projects/digital-nouveau/src/content/blog")

# Parse CSV to build slug -> stats mapping
stats_map = {}
with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        slug = row.get('Slug', '').strip()
        if slug:
            stats_map[slug] = {
                'views': row.get('View Count', '0').strip(),
                'comments': row.get('Comment Count', '0').strip(),
                'likes': row.get('Like Count', '0').strip(),
            }

print(f"Loaded stats for {len(stats_map)} posts from CSV")

# Update frontmatter
updated = 0
for md_file in POSTS_DIR.glob("*.md"):
    slug = md_file.stem
    stats = stats_map.get(slug)
    if not stats:
        # Try title matching
        content = md_file.read_text()
        title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip().strip('"').strip("'")
            for s, v in stats_map.items():
                csv_row = [r for r in csv.DictReader(open(CSV_PATH, 'r', encoding='utf-8-sig')) if r.get('Title', '').strip().strip('"').strip("'") == title]
                if csv_row:
                    stats = {'views': csv_row[0]['View Count'].strip(), 'comments': csv_row[0]['Comment Count'].strip(), 'likes': csv_row[0]['Like Count'].strip()}
                    break

    if not stats:
        continue

    content = md_file.read_text()
    lines = content.split('\n')

    # Update or add stats
    def update_line(lines, key, value):
        for i, line in enumerate(lines):
            if line.startswith(f'{key}:'):
                lines[i] = f'{key}: {value}'
                return True
        return False

    changed = False
    for key, val in stats.items():
        if not update_line(lines, key, val):
            # Add before "---" closing
            for i, line in enumerate(lines):
                if line == '---' and i > 0:
                    lines.insert(i, f'{key}: {val}')
                    changed = True
                    break
            else:
                # Try updating existing line
                for j, line in enumerate(lines):
                    if line.startswith(f'{key}:'):
                        lines[j] = f'{key}: {val}'
                        changed = True
                        break

    if changed:
        md_file.write_text('\n'.join(lines))
        updated += 1

print(f"Updated {updated} posts with stats from CSV")