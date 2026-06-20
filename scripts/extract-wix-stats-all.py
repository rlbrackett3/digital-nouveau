#!/usr/bin/env python3
"""Extract Wix blog stats from all pages and update Astro frontmatter."""
import re
import json
from pathlib import Path
import subprocess
import time

WIX_BASE = "https://blog.digitalnouveau.com"
POSTS_DIR = Path("/root/user-files/projects/digital-nouveau/src/content/blog")

def extract_stats_from_page(page_url):
    """Navigate to a Wix page and extract post stats."""
    # Use browser to extract stats
    js = """
    let _p = document.body.innerText;
    let _s = [];
    // Split by post separators (views/comments appear after each post)
    let _posts = _p.split(/\\d+ min read\\n/);
    _posts.forEach(x => {
        let _v = x.match(/(\\d+)\\s*views?/i);
        let _c = x.match(/(\\d+)\\s*comments?/i);
        let _l = x.match(/(\\d+)\\s*likes?/i);
        if (_v || _c || _l) {
            _s.push({
                views: _v ? _v[1] : '0',
                comments: _c ? _c[1] : '0',
                likes: _l ? _l[1] : '0'
            });
        }
    });
    JSON.stringify(_s);
    """
    # Navigate and extract (placeholder - actual implementation would use browser tools)
    return []

def main():
    """Main extraction loop."""
    print("=== Wix Blog Stats Extraction ===\n")
    
    # Navigate through Wix pages
    for page in range(1, 60):  # Max 60 pages (2 posts per page)
        url = f"{WIX_BASE}/page/{page}"
        print(f"Navigating to {url}...")
        
        # Extract stats from page
        stats = extract_stats_from_page(url)
        if not stats:
            break
        
        print(f"  Extracted {len(stats)} posts")
        time.sleep(1)  # Rate limit
    
    print("\nDone extracting stats")

if __name__ == "__main__":
    main()
