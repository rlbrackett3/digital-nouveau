#!/usr/bin/env python3
import os, re, json, random

blog_dir = '/root/user-files/projects/digital-nouveau/src/content/blog/'
posts = []
for fname in sorted(os.listdir(blog_dir)):
    if not fname.endswith('.md'):
        continue
    filepath = os.path.join(blog_dir, fname)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    fm_match = re.match(r'---\n(.*?)\n---\n', content, re.DOTALL)
    if not fm_match:
        continue
    fm_text = fm_match.group(1)
    meta = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            meta[key.strip()] = val.strip()
    body_match = re.match(r'---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    body = body_match.group(2)[:1000].strip() if body_match else ''
    posts.append({
        'file': fname,
        'slug': fname.replace('.md', ''),
        'title': meta.get('title', ''),
        'date': meta.get('date', ''),
        'categories': meta.get('categories', ''),
        'tags': meta.get('tags', ''),
        'body': body[:200],
    })

print(f"Total posts with frontmatter: {len(posts)}")
# Pick 20 random posts
random.seed(42)
sample = random.sample(posts, min(20, len(posts)))
print(f"Sample ({len(sample)} posts):")
for p in sample:
    print(f"  {p['slug']} | {p['title']} | {p['date']} | {p['categories']}")
print("---JSON---")
print(json.dumps(sample, indent=2))
