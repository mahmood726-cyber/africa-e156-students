"""
Update group index.html files and root index.html with new paper entries.

Handles:
- Appending new paper cards to group indexes
- Updating PAPER_META and SLUG_TO_ID JavaScript objects
- Updating paper counts in masthead and root index
"""
import re
from html import escape


ROLE_COLORS = ["#1b4f72", "#0e6251", "#4a235a", "#922b21", "#7e5109", "#0b5345", "#566573"]

# Group config: slug -> (color, new_count)
GROUP_CONFIG = {
    "geographic-equity": {"color": "#1b4f72", "group_num": 1},
    "health-disease": {"color": "#922b21", "group_num": 2},
    "governance-justice": {"color": "#7e5109", "group_num": 3},
    "methods-systems": {"color": "#0b5345", "group_num": 4},
}


def _make_paper_card(paper_def, card_num, body):
    """Generate a single paper card HTML block."""
    slug = paper_def["slug"]
    title = escape(paper_def["title"])
    code_slug = slug.replace("_", "-")
    refs = paper_def.get("refs", [])

    # Sentence strip
    strip = '<div class="sent-strip">'
    for c in ROLE_COLORS:
        strip += f'<div class="seg" style="background:{c};" title=""></div>'
    strip += '</div>'

    # References
    refs_html = '<div class="refs"><h4>Suggested References</h4><ol>'
    for r in refs:
        refs_html += f'<li>{escape(r)}</li>'
    refs_html += '</ol></div>'

    body_escaped = escape(body)

    return f"""    <article class="paper-card" id="paper-{card_num}" aria-labelledby="paper-{card_num}-title">
      <div><span class="num" aria-hidden="true">{card_num}</span><h3 id="paper-{card_num}-title">{title}</h3></div>
      {strip}
      <div class="paper-body">{body_escaped}</div>
      <div class="actions">
        <a class="btn btn-primary" href="dashboards/{escape(slug)}.html" target="_blank" rel="noopener noreferrer">View Dashboard</a>
        <a class="btn" href="code/{escape(code_slug)}.py" download>Download Code (.py)</a>
        <button class="btn" type="button" data-slug="{escape(slug)}" onclick="downloadMd('{escape(slug)}', this)">Download Paper (.md)</button>
      </div>
      {refs_html}
      <div class="note-block" role="group" aria-label="Submission metadata for {title}">
          <div class="note-row"><span class="note-key">Type:</span> <span class="note-val">research</span></div>
          <div class="note-row"><span class="note-key">App:</span> <a href="dashboards/{escape(slug)}.html">View dashboard</a></div>
          <div class="note-row"><span class="note-key">Code:</span> <a href="code/{escape(code_slug)}.py" download>{escape(code_slug)}.py</a></div>
          <div class="note-row"><span class="note-key">Data:</span> <span class="note-val">ClinicalTrials.gov API v2</span></div>
          <div class="note-row"><span class="note-key">Date:</span> <span class="note-val">2026-04-07</span></div>
        </div>
    </article>"""


def _make_paper_meta_entry(paper_def):
    """Generate a PAPER_META JS entry for a paper."""
    slug = paper_def["slug"]
    title = paper_def["title"].replace('`', "'").replace('\\', '\\\\')
    code_slug = slug.replace("_", "-")
    refs = paper_def.get("refs", [])

    refs_lines = []
    for i, r in enumerate(refs):
        safe_ref = r.replace('`', "'").replace('\\', '\\\\').replace('\n', ' ')
        refs_lines.append(f"  {i + 1}. {safe_ref}")
    refs_str = '\\\\n'.join(refs_lines)

    return f"""  "{slug}": {{
    title: `{title}`,
    refs: `{refs_str}`,
    dashboard: `dashboards/{slug}.html`,
    code: `code/{code_slug}.py`,
  }}"""


def update_group_index(index_path, new_papers, all_paper_data):
    """Append new paper cards to a group index.html file.

    Parameters
    ----------
    index_path : str
        Path to the group's index.html.
    new_papers : list of dict
        Paper definitions for new papers to add.
    all_paper_data : dict
        Mapping of slug -> {"body": str, "paper_def": dict}.
    """
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    if not new_papers:
        return

    group = new_papers[0]["group"]

    # Find existing paper count by counting paper-card articles
    existing_count = html.count('class="paper-card"')

    # 1. Insert new paper cards before the <script> tag
    #    Find the line with "const SLUG_TO_ID"
    slug_to_id_match = re.search(r'const SLUG_TO_ID\s*=\s*\{', html)
    paper_meta_match = re.search(r'const PAPER_META\s*=\s*\{', html)

    # Find insertion point for cards: just before the rules section or footer
    # We'll insert before the <script> tag
    script_match = re.search(r'\n\s*<script>', html)
    if not script_match:
        print(f"  WARNING: Could not find <script> tag in {index_path}")
        return

    insert_pos = script_match.start()

    # Generate new card HTML
    new_cards_html = "\n"
    for i, paper in enumerate(new_papers):
        card_num = existing_count + i + 1
        slug = paper["slug"]
        body = all_paper_data.get(slug, {}).get("body", "")
        new_cards_html += _make_paper_card(paper, card_num, body) + "\n"

    # Insert cards
    html = html[:insert_pos] + new_cards_html + html[insert_pos:]

    # 2. Update PAPER_META: add new entries before the closing };
    #    Find the last }; of PAPER_META object (before SLUG_TO_ID)
    # Since we modified html, re-find positions
    slug_to_id_match = re.search(r'const SLUG_TO_ID\s*=\s*\{', html)
    if slug_to_id_match:
        # Find the }; just before SLUG_TO_ID
        meta_end = html.rfind('};', 0, slug_to_id_match.start())
        if meta_end > 0:
            new_meta_entries = ""
            for paper in new_papers:
                new_meta_entries += ",\n" + _make_paper_meta_entry(paper)
            html = html[:meta_end] + new_meta_entries + "\n" + html[meta_end:]

    # 3. Update SLUG_TO_ID: add new entries
    slug_to_id_match = re.search(r'(const SLUG_TO_ID\s*=\s*\{)([^}]*)\}', html)
    if slug_to_id_match:
        existing_slug_map = slug_to_id_match.group(2)
        new_slug_entries = ""
        for i, paper in enumerate(new_papers):
            card_num = existing_count + i + 1
            new_slug_entries += f', "{paper["slug"]}": {card_num}'
        updated = slug_to_id_match.group(1) + existing_slug_map + new_slug_entries + "}"
        html = html[:slug_to_id_match.start()] + updated + html[slug_to_id_match.end():]

    # 4. Update paper count in masthead description
    total_papers = existing_count + len(new_papers)
    # Replace "These 20 papers" with new count
    html = re.sub(
        r'These \d+ papers',
        f'These {total_papers} papers',
        html,
        count=1
    )
    # Also update the warning text
    html = re.sub(
        r'Each of the \d+ papers',
        f'Each of the {total_papers} papers',
        html,
        count=1
    )

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Updated {index_path}: {existing_count} -> {total_papers} papers")


def update_root_index(root_path):
    """Update root index.html with new total count (190).

    Parameters
    ----------
    root_path : str
        Path to the root index.html.
    """
    with open(root_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update subtitle: "80 evidence papers" -> "190 evidence papers"
    html = re.sub(
        r'\b80 evidence papers\b',
        '190 evidence papers',
        html
    )

    # 2. Update each group card paper count
    # Geographic Equity: 20 -> 40
    html = re.sub(
        r'(Geographic Equity.*?<div class="paper-count">)\d+ papers',
        r'\g<1>40 papers',
        html,
        flags=re.DOTALL,
        count=1
    )

    # Health & Disease Burden: 20 -> 60
    html = re.sub(
        r'(Health.*?Disease.*?<div class="paper-count">)\d+ papers',
        r'\g<1>60 papers',
        html,
        flags=re.DOTALL,
        count=1
    )

    # Governance, Justice & Sovereignty: 20 -> 45
    html = re.sub(
        r'(Governance.*?Justice.*?<div class="paper-count">)\d+ papers',
        r'\g<1>45 papers',
        html,
        flags=re.DOTALL,
        count=1
    )

    # Methods, Design & Research Systems: 20 -> 45
    html = re.sub(
        r'(Methods.*?Design.*?<div class="paper-count">)\d+ papers',
        r'\g<1>45 papers',
        html,
        flags=re.DOTALL,
        count=1
    )

    # Also update the intro text if present
    html = re.sub(
        r'contains 20 AI-drafted',
        'contains AI-drafted',
        html
    )

    with open(root_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Updated {root_path}: total -> 190 papers")
