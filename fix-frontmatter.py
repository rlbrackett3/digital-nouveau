#!/usr/bin/env python3
"""Fix frontmatter in all 57 blog posts: descriptions, dates, titles, and add images."""
import json, re, os

MAP_PATH = "/root/user-files/projects/digital-nouveau/blog-image-mapping.json"
with open(MAP_PATH) as f:
    image_map = json.load(f)

BLOG_DIR = "/root/user-files/projects/digital-nouveau/src/content/blog"
files = sorted(os.listdir(BLOG_DIR))
print(f"Total blog files: {len(files)}")

MONTH_MAP = {
    'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
    'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
    'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
}

# Map slug -> expected first letter of title (inferred from slug)
SLUG_FIRST_LETTER = {
    '200-million-years-ago': '2',
    'a-mindful-drawing-practice': 'A',
    'adrift': 'A',
    'aesthetic-tuning-colony': 'A',
    'architecture-of-2020': 'T',
    'cholla-cactus-wood': 'C',
    'cocooning-ring-prototypes': 'C',
    'comics-architectural-narratives': 'C',
    'comics-beyond-fiction': 'C',
    'concept-sketches-lighthouse': 'C',
    'design-and-digital-design-2020': 'D',
    'design-digital-design-fa20-crit-02': 'T',
    'drawing-018-veins': 'D',
    'drawing-020-laminar-erosion': 'D',
    'drawing-021-summer-camp': 'D',
    'drawing-022-swelling-bud': 'D',
    'forming-rivers': 'F',
    'hyphae-mk2': 'H',
    'hyphae-mk3': 'H',
    'hyphae-simulation-mk2': 'H',
    'hyphae-simulation-mk3': 'H',
    'hyphae-simulations-mk1': 'H',
    'inspiring-june-flowers': 'I',
    'keep-it-simple-stu': 'K',
    'landforms-craggs': 'L',
    'learning-to-design-home': 'L',
    'make-beautiful-things': 'M',
    'make-things': 'M',
    'motervation': 'M',
    'not-quite-micro-worlds': 'N',
    'organisms': 'O',
    'out-there': 'O',
    'poetry-of-design': 'P',
    'pratt-final-review-design-1-fa2014': 'P',
    'representational-analysis': 'R',
    'rock-dwellers': 'R',
    'self-portraits-in-the-time-of-distance': 'S',
    'skyfi-april-2019': 'S',
    'skyfi-april-2020-agency': 'S',
    'skyfi-december-2019': 'S',
    'skyfi-july-2019': 'S',
    'skyfi-june-2020': 'S',
    'skyfi-november-2019': 'S',
    'skyfi-october-2020-parable-of-the-sower': 'S',
    'skyfi-september-2019': 'S',
    'staircases-perec': 'S',
    'suspended': 'S',
    'technocrafting-digital-hand': 'T',
    'the-computer-connection': 'T',
    'the-onnit-6-challenge-recap': 'T',
    'the-owl': 'T',
    'thick-space': 'T',
    'travel-documents': 'T',
    'traveller-emergence': 'T',
    'within-the-pixels': 'W',
}

stats = {'fixed_descriptions': 0, 'fixed_dates': 0, 'added_images': 0, 'fixed_titles': 0, 'skipped': 0}

for fname in files:
    if not fname.endswith('.md'):
        continue
    slug = fname.replace('.md', '')
    fpath = os.path.join(BLOG_DIR, fname)

    with open(fpath) as f:
        content = f.read()
    original = content

    # --- Fix description: strip the ": '..." prefix ---
    # Pattern matches: description: ": 'Some text." -> description: "Some text."
    desc_pattern = re.compile(
        r'^(description:\s*)"(: \'?)(.+?)"$', re.MULTILINE
    )
    m = desc_pattern.search(content)
    if m:
        desc_text = m.group(3)
        fixed_desc = f'{m.group(1)}"{desc_text}"'
        content = content[:m.start()] + fixed_desc + content[m.end():]
        stats['fixed_descriptions'] += 1
        print(f"  {slug}: fixed description ({desc_text[:60]}...)")

    # --- Fix titles: restore missing first character ---
    title_match = re.search(r'^title:\s*"(.+?)"', content, re.MULTILINE)
    if title_match:
        current_title = title_match.group(1)
        expected_first = SLUG_FIRST_LETTER.get(slug, '')

        if expected_first:
            first_char = current_title[0] if current_title else ''

            if current_title.startswith(' ') and expected_first != ' ':
                fixed_title = expected_first + current_title.lstrip()
                content = (content[:title_match.start(1)] + fixed_title +
                           content[title_match.end(1):])
                stats['fixed_titles'] += 1
                print(f"  {slug}: title fixed (lead space) → '{fixed_title}'")

            elif (first_char != expected_first and first_char.islower()
                  and len(current_title) > 1 and current_title[1:2].isupper()):
                fixed_title = expected_first + current_title[1:]
                content = (content[:title_match.start(1)] + fixed_title +
                           content[title_match.end(1):])
                stats['fixed_titles'] += 1
                print(f"  {slug}: title fixed (missing '{expected_first}') → '{fixed_title}'")

            elif slug == '200-million-years-ago' and current_title.startswith('00'):
                fixed_title = '200' + current_title[2:]
                content = (content[:title_match.start(1)] + fixed_title +
                           content[title_match.end(1):])
                stats['fixed_titles'] += 1
                print(f"  {slug}: title fixed → '{fixed_title}'")

            elif slug == 'adrift' and 'rifting' in current_title:
                fixed_title = 'Adrift'
                content = (content[:title_match.start(1)] + fixed_title +
                           content[title_match.end(1):])
                stats['fixed_titles'] += 1
                print(f"  {slug}: title fixed → '{fixed_title}'")

            elif slug == 'organisms' and current_title.startswith('RGANISMS'):
                fixed_title = 'O' + current_title
                content = (content[:title_match.start(1)] + fixed_title +
                           content[title_match.end(1):])
                stats['fixed_titles'] += 1
                print(f"  {slug}: title fixed (missing O) → '{fixed_title}'")

            elif slug == 'thick-space' and current_title.startswith('HICK'):
                fixed_title = 'T' + current_title
                content = (content[:title_match.start(1)] + fixed_title +
                           content[title_match.end(1):])
                stats['fixed_titles'] += 1
                print(f"  {slug}: title fixed (missing T) → '{fixed_title}'")

    # --- Fix pubDate: convert month-only formats to ISO ---
    date_match = re.search(
        r"^pubDate:\s*'(\w{3})\s+(\d{4})'", content, re.MULTILINE
    )
    if date_match:
        month_str = date_match.group(1).lower()
        year_str = date_match.group(2)
        month_num = MONTH_MAP.get(month_str)
        if month_num:
            new_date = f"{year_str}-{month_num}-01"
            content = (content[:date_match.start()] +
                       f"pubDate: '{new_date}'" +
                       content[date_match.end():])
            stats['fixed_dates'] += 1
            print(f"  {slug}: date fixed → '{new_date}'")

    # --- Add image field from mapping ---
    images = image_map.get(slug, [])
    if images:
        if not re.search(r'^image:', content, re.MULTILINE):
            first_image = images[0]
            # Insert image line right after categories line
            cat_match = re.search(r'^categories:.*$', content, re.MULTILINE)
            if cat_match:
                image_line = f"\nimage: \"/images/{first_image}\""
                content = (content[:cat_match.end()] + image_line +
                           content[cat_match.end():])
                stats['added_images'] += 1
                print(f"  {slug}: added image /images/{first_image}")

    if content != original:
        with open(fpath, 'w') as f:
            f.write(content)
    else:
        stats['skipped'] += 1

print(f"\n{'='*50}")
print(f"Descriptions fixed: {stats['fixed_descriptions']}")
print(f"Dates fixed:        {stats['fixed_dates']}")
print(f"Images added:       {stats['added_images']}")
print(f"Titles fixed:       {stats['fixed_titles']}")
print(f"Skipped (no change): {stats['skipped']}")
print(f"{'='*50}")