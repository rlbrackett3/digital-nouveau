#!/usr/bin/env python3
"""Navigate Wix blog pages and extract stats (views/likes/comments) from each visible post."""
import subprocess
import json
import re
import time
from pathlib import Path

WIX_BASE = "https://blog.digitalnouveau.com"
POSTS_DIR = Path("/root/user-files/projects/digital-nouveau/src/content/blog")

def slugify(title):
    """Convert post title to a markdown file slug."""
    slug = title.lower().replace("::", "-").replace("|", "-").strip()
    slug = re.sub(r'[^\w\s-]', '', slug).strip()
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug

def find_post_file(title):
    """Find the matching markdown file by title."""
    slug = slugify(title)
    # Direct match
    for f in POSTS_DIR.glob("*.md"):
        if slug in f.stem or f.stem in slug:
            return f
    # Partial match
    for f in POSTS_DIR.glob("*.md"):
        if any(word in f.stem for word in slug.split('-')[:3]):
            return f
    return None

def main():
    """Navigate Wix pages and extract stats."""
    stats = {}
    
    # Navigate through Wix feed pages
    for page in range(1, 60):
        url = f"{WIX_BASE}/page/{page}" if page > 1 else WIX_BASE
        print(f"\nPage {page}: {url}")
        
        # Use curl to fetch page content
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", "Mozilla/5.0", url],
            capture_output=True, text=True, timeout=10
        )
        
        if "404" in result.stdout[:500] or not result.stdout:
            print("  Page not found, stopping pagination")
            break
        
        # Extract post data from HTML
        # Wix feed shows posts with stats in the HTML
        content = result.stdout
        
        # Find all post blocks with stats
        # Pattern: title + views + comments + likes
        posts = re.findall(r'<h2[^>]*>(.*?)</h2>.*?(\d+)\s*views.*?(\d+)\s*comments.*?(\d+)\s*likes', content, re.DOTALL | re.IGNORECASE)
        
        for title, views, comments, likes in posts:
            title = re.sub(r'<[^>]+>', '', title).strip()
            stats[title] = {"views": views, "comments": comments, "likes": likes}
            print(f"  {title}: {views} views, {comments} comments, {likes} likes")
        
        if not posts:
            print("  No posts found, stopping")
            break
        
        time.sleep(1)  # Rate limit
    
    # Save stats to JSON
    stats_file = Path("/root/user-files/projects/digital-nouveau/stats.json")
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n=== Saved {len(stats)} post stats to stats.json ===")

if __name__ == "__main__":
    main()
