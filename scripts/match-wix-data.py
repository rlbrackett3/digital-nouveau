#!/usr/bin/env python3
"""
Wix Data Match Report
Compares current Astro frontmatter against Wix source data for:
- pubDate (from Wix HTML JSON)
- views, likes, comments (from wix-stats-cache.json)
- title match verification
"""
import json
import re
import os
from pathlib import Path

BASE = "/root/user-files/projects/digital-nouveau"
BLOG_DIR = Path(f"{BASE}/src/content/blog")
CACHE_FILE = f"{BASE}/scripts/wix-stats-cache.json"
SOURCE_HTML = f"{BASE}/references/wix-home.html"

def extract_wix_posts_from_html():
    """Parse the Wix feed JSON to get firstPublishedDate + slug."""
    html = ""
    for src in [f"{BASE}/references/wix-home.html", f"{BASE}/references/wix-source.html"]:
        with open(src) as f:
            html += f.read()
    
    result = {}
    
    # Try: backslash-escaped JSON: firstPublishedDate\":\"ISO_DATE\",...,slug\":\"SLUG\"
    for m in re.finditer(r'firstPublishedDate\\(?:"|u0022)\s*:\s*\\(?:"|u0022)([^\\]+)', html):
        date = m.group(1)
        # Find the nearest slug
        context = html[m.end():m.end()+500]
        sm = re.search(r'slug\\(?:"|u0022)\s*:\s*\\(?:"|u0022)([^\\"]+)', context)
        if sm and sm.group(1) not in ['robertbrackett3', 'robertbrackett']:
            slug = sm.group(1)
            if slug not in result:
                result[slug] = {'firstPublishedDate': date}
    
    # Try unescaped: "firstPublishedDate":"ISO_DATE"
    if not result:
        posts = re.findall(r'"firstPublishedDate"\s*:\s*"([^"]+)"[^}]+"slug"\s*:\s*"([^"]+)"', html)
        for date, slug in posts:
            if slug not in result:
                result[slug] = {'firstPublishedDate': date}
    
    print(f"Extracted {len(result)} posts from Wix HTML source")
    return result

def load_cache():
    """Load the wix-stats-cache.json."""
    with open(CACHE_FILE) as f:
        return json.load(f)

def load_markdown_frontmatter():
    """Load all markdown frontmatter files."""
    posts = {}
    for f in sorted(BLOG_DIR.glob("*.md")):
        slug = f.stem
        content = f.read_text()
        fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            posts[slug] = {'error': 'no frontmatter'}
            continue
        
        fm_text = fm_match.group(1)
        fm = {}
        for line in fm_text.split('\n'):
            line = line.strip()
            if ':' in line:
                key, _, val = line.partition(':')
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                fm[key] = val
        
        posts[slug] = fm
    
    return posts

def main():
    wix_dates = extract_wix_posts_from_html()
    cache = load_cache()
    posts = load_markdown_frontmatter()
    
    print(f"\n{'='*80}")
    print(f"WIX DATA MATCH REPORT")
    print(f"{'='*80}\n")
    print(f"Total markdown posts: {len(posts)}")
    print(f"Wix cache entries: {len(cache)}")
    print(f"Wix HTML posts with dates: {len(wix_dates)}\n")
    
    stats_matched = 0
    stats_mismatch = 0
    stats_no_cache = 0
    stats_diffs = []
    
    dates_matched = 0
    dates_no_html = 0
    dates_diffs = []
    
    for slug, fm in sorted(posts.items()):
        if 'error' in fm:
            continue
        
        title = fm.get('title', '(no title)')
        
        # === Stats comparison ===
        cache_entry = None
        cache_title = None
        for c_title, c_val in cache.items():
            if c_val.get('file') and Path(c_val['file']).stem == slug:
                cache_entry = c_val
                cache_title = c_title
                break
        
        if cache_entry:
            mismatches = []
            for field in ['views', 'likes', 'comments']:
                wix_val = int(cache_entry.get(field, 0))
                cur_val = int(fm.get(field, 0))
                if wix_val != cur_val:
                    mismatches.append(f"{field}: Wix={wix_val} Cur={cur_val}")
            if mismatches:
                stats_mismatch += 1
                stats_diffs.append(f"  {slug}: {'; '.join(mismatches)}")
            stats_matched += 1
        else:
            stats_no_cache += 1
            stats_diffs.append(f"  MISS-cache: {slug} — title '{title}'")
        
        # === Date comparison ===
        if slug in wix_dates:
            wix_date = wix_dates[slug]['firstPublishedDate'][:10]
            cur_date = fm.get('pubDate', '').strip("'")
            if cur_date != wix_date:
                dates_diffs.append(f"  {slug}: Wix={wix_date} vs Cur={cur_date}")
            dates_matched += 1
        else:
            dates_no_html += 1

    print(f"{'='*80}")
    print(f"STATS (views/likes/comments)")
    print(f"{'='*80}")
    print(f"  OK (matched):         {stats_matched - stats_mismatch}")
    print(f"  NEED UPDATE:         {stats_mismatch}")
    print(f"  Not in cache:        {stats_no_cache}")
    print()
    if stats_diffs:
        for d in stats_diffs:
            print(d)
        print()
    
    print(f"{'='*80}")
    print(f"DATES (pubDate)")
    print(f"{'='*80}")
    print(f"  OK (matched):        {dates_matched - len(dates_diffs)}")
    print(f"  NEED UPDATE:         {len(dates_diffs)}")
    print(f"  No Wix date source:  {dates_no_html}")
    print()
    if dates_diffs:
        print("  Date mismatches:")
        for d in dates_diffs:
            print(d)
        print()
    
    print(f"{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"  Total posts:          {len(posts)}")
    print(f"  Stats OK:             {stats_matched - stats_mismatch}")
    print(f"  Stats need update:    {stats_mismatch}")
    print(f"  Dates OK:             {dates_matched - len(dates_diffs)}")
    print(f"  Dates need update:    {len(dates_diffs)}")
    print(f"  Dates need scraping:  {dates_no_html}")
    
    # Save report to file
    report_path = f"{BASE}/docs/wix-data-discrepancy-report.txt"
    with open(report_path, 'w') as f:
        f.write(f"WIX DATA DISCREPANCY REPORT\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"Generated: {__import__('datetime').datetime.now().isoformat()}\n")
        f.write(f"Posts requiring stats updates: {stats_mismatch}\n")
        f.write(f"Posts requiring date updates: {len(dates_diffs)}\n")
        f.write(f"Posts with no Wix date data: {dates_no_html}\n\n")
        
        f.write("--- STATS UPDATES NEEDED ---\n")
        for d in stats_diffs:
            f.write(f"{d}\n")
        
        f.write("\n--- DATE UPDATES NEEDED ---\n")
        for d in dates_diffs:
            f.write(f"{d}\n")
    
    print(f"\nReport saved to: {report_path}")

if __name__ == '__main__':
    main()