#!/usr/bin/env python3
"""Check internal cross-links within blog posts."""
import os, re, urllib.request, urllib.error

BLOG_DIR = "/root/user-files/projects/digital-nouveau/src/content/blog"
BASE = "http://localhost:4322"

internal_links = set()
broken = []
working = []

for fname in sorted(os.listdir(BLOG_DIR)):
    if not fname.endswith('.md'):
        continue
    slug = fname[:-3]
    fpath = os.path.join(BLOG_DIR, fname)
    with open(fpath) as f:
        content = f.read()
    
    # href="/something" or [text](/something)
    found = re.findall(r'href=[\'"]?(/[^\'"\s>)]+)[\'"\s>)]', content)
    found += re.findall(r'\]\((/[^\s)]+)\)', content)
    
    for link in found:
        link = link.split('#')[0].split('?')[0]
        if link and not link.startswith('http') and not link.startswith('//'):
            internal_links.add((slug, link))

print(f"Found {len(internal_links)} internal cross-links in blog posts\n")

for src, path in sorted(internal_links):
    if path in {p for _, p in broken}:  # skip duplicates already broken
        continue
    url = BASE + path
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=10)
        code = resp.getcode()
        if code >= 400:
            broken.append((src, path, code))
            print(f"  [BROKEN] {code} post='{src}' -> '{path}'")
        else:
            working.append((src, path, code))
    except urllib.error.HTTPError as e:
        broken.append((src, path, e.code))
        print(f"  [BROKEN] {e.code} post='{src}' -> '{path}'")
    except Exception as e:
        broken.append((src, path, str(e)))
        print(f"  [ERROR] {e} post='{src}' -> '{path}'")

print(f"\n{'='*50}")
print(f"Internal cross-links: {len(working)} working, {len(broken)} broken")
if broken:
    print(f"\nBROKEN:")
    for src, path, reason in broken:
        print(f"  [{reason}] '{src}' -> {path}")
else:
    print("No broken internal cross-links found!")