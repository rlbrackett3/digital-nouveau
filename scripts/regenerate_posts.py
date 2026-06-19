#!/usr/bin/env python3
"""Regenerate blog posts from Wix CSV export."""
import csv, json, re, html
from pathlib import Path

CSV_PATH = Path("/root/.hermes/cache/documents/doc_9879131a8257_Posts.csv")
OUTPUT_DIR = Path("/root/user-files/projects/digital-nouveau/src/content/blog")

# Category ID to name mapping (from Wix CSV analysis)
CATEGORY_MAP = {
    "5d17ad2306b28c0016c0fb5c": "design",
    "5d17ad910bdf230016d98e95": "drawings",
    "5d17aea198c5cc00160844c0": "readings",
    "5d17ae2709fd900016e34619": "skyfi",
    "5d17adac528d9400e68e4c68": "observings",
    "5d52c93365f8810016f2c9bc": "thinkings",
    "5d52e12bc35e8400177a4d99": "teachings",
    "5f73a3919c98400018a08370": "writings",
}


def parse_rich_content(rich_json_str: str) -> str:
    """Parse Wix rich content JSON into markdown."""
    if not rich_json_str:
        return ""
    try:
        data = json.loads(rich_json_str)
    except json.JSONDecodeError:
        return ""

    lines = []
    for node in data.get("nodes", []):
        ntype = node.get("type", "")

        if ntype == "PARAGRAPH":
            # Extract text from nested text nodes
            texts = []
            for child in node.get("nodes", []):
                if child.get("type") == "TEXT":
                    text = child.get("textData", {}).get("text", "")
                    if text:
                        texts.append(text)
            content = "".join(texts).strip()
            if content:
                lines.append(content)

        elif ntype == "IMAGE":
            img_data = node.get("imageData", {})
            img_src = img_data.get("image", {}).get("src", {}).get("id", "")
            caption = img_data.get("caption", "")
            width = img_data.get("image", {}).get("width", 1200)
            height = img_data.get("image", {}).get("height", 800)

            if img_src:
                # Extract just the hash part
                hash_match = re.search(r'dc9b92_[^#"\s]+', img_src)
                if hash_match:
                    img_filename = hash_match.group()
                    md = f'![{caption}]({img_filename})'
                    lines.append(f"<figure>\n{md}\n{caption and f'<figcaption>{caption}</figcaption>' or ''}\n</figure>")

        elif ntype == "VIDEO":
            video_data = node.get("videoData", {})
            src = video_data.get("video", {}).get("src", {})
            video_url = src.get("url", "") if src else ""
            title = video_data.get("video", {}).get("title", "")

            if video_url:
                # Handle Vimeo embeds
                if "vimeo.com" in video_url:
                    video_id = video_url.split("/")[-1].split("?")[0]
                    lines.append(f'<div class="video-embed"><iframe src="https://player.vimeo.com/video/{video_id}" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe></div>')
                # Handle YouTube embeds
                elif "youtube.com" in video_url or "youtu.be" in video_url:
                    if "youtu.be" in video_url:
                        video_id = video_url.split("/")[-1].split("?")[0]
                    else:
                        match = re.search(r'v=([A-Za-z0-9_-]+)', video_url)
                        video_id = match.group(1) if match else ""
                    if video_id:
                        lines.append(f'<div class="video-embed"><iframe src="https://www.youtube.com/embed/{video_id}" width="640" height="360" frameborder="0" allowfullscreen></iframe></div>')

        elif ntype == "HEADING":
            level = node.get("headingData", {}).get("headingLevel", 2)
            level = min(max(level, 2), 4)  # H2-H4 for content
            texts = []
            for child in node.get("nodes", []):
                if child.get("type") == "TEXT":
                    text = child.get("textData", {}).get("text", "")
                    if text:
                        texts.append(text)
            content = "".join(texts).strip()
            if content:
                lines.append(f"{'#' * level} {content}")

        elif ntype == "BULLETED_LIST":
            list_items = []
            for item in node.get("nodes", []):
                texts = []
                for child in item.get("nodes", []):
                    if child.get("type") == "TEXT":
                        text = child.get("textData", {}).get("text", "")
                        if text:
                            texts.append(text)
                content = "".join(texts).strip()
                if content:
                    list_items.append(f"- {content}")
            if list_items:
                lines.append("\n".join(list_items))

        elif ntype == "NUMBERED_LIST":
            list_items = []
            for i, item in enumerate(node.get("nodes", []), 1):
                texts = []
                for child in item.get("nodes", []):
                    if child.get("type") == "TEXT":
                        text = child.get("textData", {}).get("text", "")
                        if text:
                            texts.append(text)
                content = "".join(texts).strip()
                if content:
                    list_items.append(f"{i}. {content}")
            if list_items:
                lines.append("\n".join(list_items))

    return "\n\n".join(lines)


def process_csv():
    processed = 0

    with open(CSV_PATH, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row.get("Slug", "").strip()
            if not slug:
                continue

            title = row.get("Title", "").strip()
            if not title:
                title = slug.replace("-", " ").title()

            # Published date
            pub_date_str = row.get("Published Date", "").strip()
            pub_date = ""
            if pub_date_str:
                # Convert ISO to YYYY-MM-DD
                match = re.match(r"(\d{4}-\d{2}-\d{2})", pub_date_str)
                if match:
                    pub_date = match.group(1)

            # Categories - parse JSON array of IDs
            cats_str = row.get("Categories", "[]")
            categories = []
            try:
                cat_ids = json.loads(cats_str)
                for cid in cat_ids:
                    name = CATEGORY_MAP.get(str(cid), "")
                    if name:
                        categories.append(name)
            except:
                pass

            # If no categories, check Main Category ID
            if not categories:
                main_cat = row.get("Main Category", "").strip()
                if main_cat:
                    name = CATEGORY_MAP.get(main_cat, "")
                    if name:
                        categories.append(name)

            # Cover image
            cover = row.get("Cover Image", "").strip()
            cover_filename = ""
            if cover:
                hash_match = re.search(r"dc9b92_[^\"#\s]+", cover)
                if hash_match:
                    cover_filename = f"/images/{hash_match.group()}"

            # Stats
            views = int(row.get("View Count", 0) or 0)
            likes = int(row.get("Like Count", 0) or 0)
            comments = int(row.get("Comment Count", 0) or 0)

            # Tags
            tags_str = row.get("Tags", "[]")
            tags = []
            try:
                tags = json.loads(tags_str)
            except:
                tags = []

            # Body content
            rich = row.get("Rich Content", "").strip()
            plain = row.get("Plain Content", "").strip()

            body = parse_rich_content(rich)
            if not body and plain:
                body = html.unescape(plain)

            # Excerpt
            excerpt = row.get("Excerpt", "").strip()
            if excerpt:
                excerpt = html.unescape(excerpt)
            elif body:
                first_para = body.split("\n\n")[0].strip()
                # Strip markdown links/images from excerpt
                first_para = re.sub(r"!\[.*?\]\(.*?\)", "", first_para)
                first_para = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", first_para)
                first_para = re.sub(r"<[^>]+>", "", first_para)
                if first_para:
                    excerpt = first_para[:200]

            # Read time
            read_time = int(row.get("Time To Read", 0) or 0)

            # Build frontmatter
            fm_lines = []
            fm_lines.append("---")
            fm_lines.append(f'title: "{html.escape(title)}"')
            if excerpt:
                fm_lines.append(f'description: "{html.escape(excerpt)}"')
            if pub_date:
                fm_lines.append(f"pubDate: '{pub_date}'")
            # Always include categories (use fallback if empty)
            if categories:
                fm_lines.append(f"categories: {json.dumps(categories)}")
            else:
                fm_lines.append("categories: ['design']")
            if cover_filename:
                fm_lines.append(f'image: "{cover_filename}"')
            if read_time:
                fm_lines.append(f"readTime: {read_time}")
            if tags:
                fm_lines.append(f"tags: {json.dumps(tags)}")
            if views:
                fm_lines.append(f"views: {views}")
            if comments:
                fm_lines.append(f"comments: {comments}")
            if likes:
                fm_lines.append(f"likes: {likes}")
            fm_lines.append("---")
            fm = "\n".join(fm_lines)

            # Write file
            filepath = OUTPUT_DIR / f"{slug}.md"
            content = f"{fm}\n\n{body}\n"
            filepath.write_text(content, encoding="utf-8")
            processed += 1

    print(f"Processed {processed} posts -> {OUTPUT_DIR}")


if __name__ == "__main__":
    process_csv()
