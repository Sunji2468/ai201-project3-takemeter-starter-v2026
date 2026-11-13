"""Collect unlabeled Ask HN comments with source provenance; no model calls."""

import csv
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
API = "https://hacker-news.firebaseio.com/v0/"


def fetch(path):
    with urlopen(API + path + ".json", timeout=30) as response:
        return json.load(response)


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "br", "pre"):
            self.parts.append("\n\n")
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))

    def handle_endtag(self, tag):
        if tag == "a" and self.links:
            href = self.links.pop()
            # Retain full URLs even when the rendered link text is shortened.
            if href:
                self.parts.append(f" ({href})")

    def handle_data(self, data):
        self.parts.append(data)


def plain(html):
    parser = PlainText()
    parser.feed(html)
    return re.sub(r"\n{3,}", "\n\n", "".join(parser.parts)).strip()


def main():
    output = ROOT / "data" / "hn_unlabeled.csv"
    existing = []
    if output.exists():
        with output.open(newline="", encoding="utf-8") as handle:
            existing = list(csv.DictReader(handle))
    retrieved = datetime.now(timezone.utc).isoformat()
    ids = fetch("askstories")
    with ThreadPoolExecutor(max_workers=6) as pool:
        stories = list(pool.map(lambda item: fetch(f"item/{item}"), ids))
        candidates = []
        for story in stories:
            if not story or story.get("dead") or story.get("deleted"):
                continue
            if not story.get("title", "").lower().startswith("ask hn:"):
                continue
            for item in story.get("kids", [])[:60]:
                candidates.append((item, story))
        comments = list(pool.map(lambda pair: fetch(f"item/{pair[0]}"), candidates))
    rows = existing[:]
    seen = {" ".join(row["text"].split()).casefold() for row in existing}
    for (_, story), comment in zip(candidates, comments):
        if not comment or comment.get("dead") or comment.get("deleted"):
            continue
        text = plain(comment.get("text", ""))
        key = " ".join(text.split()).casefold()
        if not text or key in seen:
            continue
        seen.add(key)
        rows.append({
            "id": comment["id"], "text": text, "label": "", "note": "",
            "source_url": f'https://news.ycombinator.com/item?id={comment["id"]}',
            "thread_id": story["id"], "thread_title": story["title"],
            "retrieved_at_utc": retrieved, "original_html": comment["text"],
        })
    if not rows:
        raise SystemExit("No comments returned; no files written.")
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    # Spread the reading sample over threads instead of reading one thread first.
    groups = {}
    for row in rows:
        groups.setdefault(row["thread_id"], []).append(row)
    sample = []
    for position in range(60):
        for group in groups.values():
            if position < len(group) and len(sample) < 40:
                sample.append(group[position])
    lines = ["# Ask HN reading sample", "", "Unlabeled real comments for the initial reading exercise. Read the whole comment", "and its source context before proposing labels. No training has run.", ""]
    for number, row in enumerate(sample, 1):
        lines.extend([f'## {number}. {row["thread_title"]}', "", f'Source: {row["source_url"]}', "", row["text"], ""])
    (ROOT / "data" / "reading_sample.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Collected {len(rows)} unique comments from {len(groups)} threads.")
    print(f"Reading sample: {len(sample)} comments. All labels remain blank.")


if __name__ == "__main__":
    main()
