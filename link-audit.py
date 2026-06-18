#!/usr/bin/env python3
"""Comprehensive link audit for Digital Nouveau site."""

import urllib.request
import urllib.error
import re
import time
import sys

BASE = "http://localhost:4322"
visited = set()
broken = []
working = []

# All expected paths from the codebase analysis
NAV_PATHS = ["/", "/blog", "/about", "/portfolio", "/skyfi-a-reading-list"]

CATEGORIES = ["design", "drawings", "readings", "skyfi", "thinkings", "observings", "teachings", "writings"]
CATEGORY_PATHS = [f"/category/{c}" for c in CATEGORIES]

BLOG_SLUGS = [
    "200-million-years-ago", "a-mindful-drawing-practice", "adrift",
    "aesthetic-tuning-colony", "cholla-cactus-wood", "cocooning-ring-prototypes",
    "comics-architectural-narratives", "comics-beyond-fiction",
    "concept-sketches-lighthouse", "drawing-018-veins", "drawing-020-laminar-erosion",
    "drawing-021-summer-camp", "drawing-022-swelling-bud", "forming-rivers",
    "hyphae-simulation-mk2", "hyphae-simulation-mk3", "hyphae-simulations-mk1",
    "inspiring-june-flowers", "journey-southwest", "keep-it-simple-stu",
    "landforms-craggs", "learning-to-design-home", "make-beautiful-things",
    "make-it-better", "make-things", "motervation", "not-quite-micro-worlds",
    "organisms", "out-there", "poetry-of-design", "pratt-final-review-design-1-fa2014",
    "representational-analysis", "rock-dwellers", "self-portraits-in-the-time-of-distance",
    "skyfi-april-2019", "skyfi-april-2020-agency", "skyfi-december-2019",
    "skyfi-july-2019", "skyfi-june-2020", "skyfi-november-2019",
    "skyfi-october-2020-parable-of-the-sower", "skyfi-september-2019",
    "staircases-perec", "suspended", "technocrafting-digital-hand",
    "the-computer-connection", "the-onnit-6-challenge-recap", "the-owl",
    "thick-space", "travel-documents", "traveller-emergence", "within-the-pixels",
]
BLOG_PATHS = [f"/blog/{slug}" for slug in BLOG_SLUGS]

def check_url(path, label=""):
    url = BASE + path
    if path in visited:
        return
    visited.add(path)
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=10)
        code = resp.getcode()
        final_url = resp.geturl()
        if code >= 400:
            broken.append((path, code))
            print(f"  [BROKEN] {code} {path}")
        else:
            print(f"  [OK] {code} {path}")
            working.append((path, code))
            if final_url.rstrip('/') != url.rstrip('/'):
                print(f"    -> redirects to {final_url}")
        return code
    except urllib.error.HTTPError as e:
        broken.append((path, e.code))
        print(f"  [BROKEN] {e.code} {path}")
        return e.code
    except Exception as e:
        broken.append((path, str(e)))
        print(f"  [ERROR] {e} {path}")
        return None

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

# === NAV PAGES ===
print_section("NAV PAGES")
for p in NAV_PATHS:
    check_url(p)

# === CATEGORY PAGES ===
print_section("CATEGORY PAGES")
for p in CATEGORY_PATHS:
    check_url(p)

# === BLOG POSTS ===
print_section("BLOG POSTS")
for p in BLOG_PATHS:
    check_url(p)

# === BLOG LISTING VERIFICATION ===
print_section("BLOG LISTING: LINK COUNT VERIFICATION")
try:
    resp = urllib.request.urlopen(BASE + "/blog", timeout=10)
    html = resp.read().decode('utf-8')
    blog_links = re.findall(r'href="/blog/([^"\'/]+)"', html)
    print(f"  Blog listing page contains {len(blog_links)} post links")
    
    # Check which slugs are present vs missing
    listing_slugs = set(blog_links)
    expected_slugs = set(BLOG_SLUGS)
    missing = expected_slugs - listing_slugs
    extra = listing_slugs - expected_slugs
    
    if missing:
        print(f"  WARNING: {len(missing)} post(s) not linked from listing:")
        for m in sorted(missing):
            print(f"    - /blog/{m}")
    else:
        print(f"  All {len(expected_slugs)} posts are linked from the listing page.")
    
    if extra:
        print(f"  EXTRA slugs found in listing (not in our expected list): {extra}")
except Exception as e:
    print(f"  ERROR fetching blog listing: {e}")

# === HOME PAGE CATEGORY NAV VERIFICATION ===
print_section("HOME PAGE: CATEGORY NAV LINKS")
try:
    resp = urllib.request.urlopen(BASE + "/", timeout=10)
    html = resp.read().decode('utf-8')
    category_nav_links = re.findall(r'href="/category/([^"\'/]+)"', html)
    print(f"  Home page has {len(set(category_nav_links))} unique category nav links")
    missing_cats = [c for c in CATEGORIES if c not in category_nav_links]
    if missing_cats:
        print(f"  WARNING: categories missing from homepage nav: {missing_cats}")
    else:
        print(f"  All 8 categories present in homepage nav.")
except Exception as e:
    print(f"  ERROR fetching homepage: {e}")

# === SUMMARY ===
print_section("FINAL SUMMARY")
print(f"  Total URLs checked: {len(visited)}")
print(f"  Working: {len(working)}")
print(f"  Broken:  {len(broken)}")

if broken:
    print(f"\n  *** {len(broken)} BROKEN LINK(S) FOUND ***")
    for path, reason in broken:
        print(f"    - {path}: {reason}")
    sys.exit(1)
else:
    print(f"\n  No broken links found!")
    sys.exit(0)