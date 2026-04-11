#!/usr/bin/env python3
"""
Patch published group pages to use static paper downloads and emit matching markdown files.
"""

from __future__ import annotations

import re
import shutil
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GITHUB_PAGES = "https://mahmood726-cyber.github.io/africa-e156-students"
GITHUB_REPO = "https://github.com/mahmood726-cyber/africa-e156-students"
GROUPS = (
    "geographic-equity",
    "health-disease",
    "governance-justice",
    "methods-systems",
)

ARTICLE_RE = re.compile(r"<article class=\"paper-card\".*?</article>", re.S)
BUTTON_RE = re.compile(
    r"<button class=\"btn\" type=\"button\" data-slug=\"([^\"]+)\" "
    r"onclick=\"downloadMd\('[^']+', this\)\">Download Paper \(\.md\)</button>"
)
TITLE_RE = re.compile(r"<h3[^>]*>(.*?)</h3>", re.S)
BODY_RE = re.compile(r"<div class=\"paper-body\">(.*?)</div>", re.S)
APP_RE = re.compile(
    r"<div class=\"note-row\"><span class=\"note-key\">App:</span> "
    r"<a href=\"([^\"]+)\">[^<]+</a></div>"
)
CODE_RE = re.compile(
    r"<div class=\"note-row\"><span class=\"note-key\">Code:</span> "
    r"<a href=\"([^\"]+)\"[^>]*>[^<]+</a></div>"
)
DATE_RE = re.compile(
    r"<div class=\"note-row\"><span class=\"note-key\">Date:</span> "
    r"<span class=\"note-val\">(.*?)</span></div>"
)
REFS_BLOCK_RE = re.compile(r"<div class=\"refs\">.*?<ol>(.*?)</ol></div>", re.S)
REF_ITEM_RE = re.compile(r"<li>(.*?)</li>", re.S)
APP_ROW_RE = re.compile(
    r"(<div class=\"note-row\"><span class=\"note-key\">App:</span> "
    r"<a href=\"[^\"]+\">[^<]+</a></div>)"
)
TAG_RE = re.compile(r"<[^>]+>")


def strip_tags(text: str) -> str:
    return unescape(TAG_RE.sub("", text)).strip()


def extract_required(pattern: re.Pattern[str], text: str, label: str) -> str:
    match = pattern.search(text)
    if not match:
        raise ValueError(f"Missing {label}")
    return match.group(1)


def build_markdown(group_id: str, slug: str, article_html: str) -> str:
    title = strip_tags(extract_required(TITLE_RE, article_html, "title"))
    body = strip_tags(extract_required(BODY_RE, article_html, "body"))
    app_rel = extract_required(APP_RE, article_html, "app link")
    code_rel = extract_required(CODE_RE, article_html, "code link")
    date = strip_tags(extract_required(DATE_RE, article_html, "date"))

    refs_match = REFS_BLOCK_RE.search(article_html)
    refs = []
    if refs_match:
        refs = [strip_tags(item) for item in REF_ITEM_RE.findall(refs_match.group(1))]

    app_url = f"{GITHUB_PAGES}/{group_id}/{app_rel}"
    code_url = f"{GITHUB_REPO}/blob/master/{group_id}/{code_rel}"

    md = f"# {title}\n\n{body}\n\n"
    if refs:
        md += "## References\n\n"
        md += "\n".join(f"{idx}. {ref}" for idx, ref in enumerate(refs, 1))
        md += "\n\n"
    md += "## Note Block\n\n"
    md += "- Type: research\n"
    md += f"- App: {app_url}\n"
    md += f"- Code: {code_url}\n"
    md += "- Data: ClinicalTrials.gov API v2\n"
    md += f"- Date: {date}\n"
    return md


def rewrite_article(article_html: str) -> str:
    button_match = BUTTON_RE.search(article_html)
    if not button_match:
        return article_html

    slug = button_match.group(1)
    article_html = BUTTON_RE.sub(
        f'<a class="btn" href="papers/{slug}.md" download>Download Paper (.md)</a>',
        article_html,
        count=1,
    )

    if 'note-key">Paper:' not in article_html:
        paper_row = (
            f'\\1\n          <div class="note-row"><span class="note-key">Paper:</span> '
            f'<a href="papers/{slug}.md" download>{slug}.md</a></div>'
        )
        article_html = APP_ROW_RE.sub(paper_row, article_html, count=1)

    return article_html


def sync_group(group_id: str) -> int:
    page_path = ROOT / group_id / "index.html"
    page_text = page_path.read_text(encoding="utf-8")
    paper_dir = ROOT / group_id / "papers"
    shutil.rmtree(paper_dir, ignore_errors=True)
    paper_dir.mkdir(parents=True, exist_ok=True)

    articles = ARTICLE_RE.findall(page_text)
    if not articles:
        raise ValueError(f"No paper cards found in {page_path}")

    updated_page = page_text
    written = 0

    for article in articles:
        slug = extract_required(BUTTON_RE, article, "paper button slug")
        md_path = paper_dir / f"{slug}.md"
        md_path.write_text(build_markdown(group_id, slug, article), encoding="utf-8")
        updated_page = updated_page.replace(article, rewrite_article(article), 1)
        written += 1

    page_path.write_text(updated_page, encoding="utf-8")
    return written


def main() -> None:
    total = 0
    for group_id in GROUPS:
        written = sync_group(group_id)
        total += written
        print(f"{group_id}: {written} papers")
    print(f"Total papers written: {total}")


if __name__ == "__main__":
    main()
