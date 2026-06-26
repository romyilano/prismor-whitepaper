#!/usr/bin/env python3
"""
build_prompts_page.py — render an internal "prompt review" website for a manga project.

The explainer pipeline writes one self-contained image prompt per page into
`page-01.md … page-06.md` (everything after the `Image Prompt:` marker). Before spending
tokens/credits generating art, it is useful to see ALL prompts on one page so a human can
read them side by side and rewrite them. This script collects the prompts and writes a
single `prompts.html` in the same editorial house style.

This is a REVIEW surface, not an editor: the source of truth is the `.md` files. Edit those,
then re-run this script (and re-run generate_panels.py once you're happy).

Usage:
    python3 build_prompts_page.py <manga-project-dir> [--out prompts.html] [--title "..."]

Example:
    python3 build_prompts_page.py documentation/explainer-src/manga/reverse-engineering
"""
import argparse
import html
import sys
from pathlib import Path

PROMPT_MARKER = "Image Prompt:"


def extract_prompt(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    idx = text.find(PROMPT_MARKER)
    if idx == -1:
        return ""  # no prompt yet — surfaced as a warning in the page
    return text[idx + len(PROMPT_MARKER):].strip()


def extract_title(md_path: Path) -> str:
    for line in md_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return md_path.stem


def page_files(pages_dir: Path):
    out = []
    for p in sorted(pages_dir.glob("page-*.md")):
        try:
            n = int(p.stem.split("-")[1])
        except (IndexError, ValueError):
            continue
        out.append((n, p))
    return out


PAGE_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} — prompt review</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet" />
<style>
  :root {{ --paper:#e6e9e4; --panel:#f0f2ed; --ink:#1d2128; --muted:#6c7178; --spot:#3c5d72; --hair:#cdd1c9; --line:#1d2128; }}
  * {{ box-sizing: border-box; }}
  html {{ font-size: 19px; -webkit-font-smoothing: antialiased; }}
  body {{ margin:0; background: radial-gradient(circle at 1px 1px, rgba(29,33,40,0.04) 1px, transparent 0) 0 0 / 4px 4px, var(--paper); color: var(--ink); font-family: "Newsreader", Georgia, serif; line-height: 1.5; }}
  .strip {{ max-width: 880px; margin: 0 auto; padding: 0 28px 120px; }}
  a {{ color: var(--spot); }}
  .intbar {{ background: var(--ink); color: var(--paper); text-transform: uppercase; letter-spacing: 0.22em; font-size: 0.6rem; font-weight: 600; text-align: center; padding: 9px 16px; }}
  header.mast {{ padding: 64px 0 18px; border-bottom: 1.5px solid var(--line); }}
  .kicker {{ text-transform: uppercase; letter-spacing: 0.3em; font-size: 0.72rem; font-weight: 600; color: var(--spot); margin: 0 0 10px; }}
  h1 {{ font-family: "Fraunces", serif; font-weight: 500; font-size: clamp(2.4rem, 6vw, 3.8rem); line-height: 1.0; letter-spacing: -0.02em; margin: 0; }}
  h1 em {{ font-style: italic; color: var(--spot); }}
  .standfirst {{ font-family: "Fraunces", serif; font-style: italic; color: var(--muted); font-size: 1.3rem; margin: 18px 0 0; max-width: 34em; }}
  .gate {{ margin: 26px 0 0; border: 1.5px solid var(--line); background: var(--panel); padding: 16px 18px; font-size: 0.95rem; }}
  .gate b {{ color: var(--spot); }}
  .gate code {{ font-family: ui-monospace, Menlo, monospace; font-size: 0.85em; background: #fff; padding: 1px 5px; border: 1px solid var(--hair); }}
  .card {{ margin: 48px 0 0; }}
  .card-no {{ text-transform: uppercase; letter-spacing: 0.2em; font-size: 0.7rem; font-weight: 600; color: var(--spot); margin: 0 0 4px; }}
  .card h2 {{ font-family: "Fraunces", serif; font-weight: 500; font-style: italic; font-size: 1.7rem; line-height: 1.1; letter-spacing: -0.02em; margin: 0 0 6px; }}
  .meta {{ font-size: 0.78rem; color: var(--muted); margin: 0 0 12px; }}
  .meta b {{ color: var(--ink); font-weight: 600; }}
  .promptwrap {{ position: relative; }}
  .copybtn {{ position: absolute; top: 10px; right: 10px; text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.62rem; font-weight: 600; padding: 6px 12px; border: 1.5px solid var(--line); background: var(--paper); color: var(--ink); cursor: pointer; font-family: inherit; }}
  .copybtn:hover {{ background: var(--spot); color: var(--paper); border-color: var(--spot); }}
  pre.prompt {{ margin: 0; background: #fff; border: 1.5px solid var(--line); box-shadow: 5px 5px 0 rgba(29,33,40,0.08); padding: 20px 22px; white-space: pre-wrap; word-wrap: break-word; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.82rem; line-height: 1.55; }}
  .missing {{ color: #9a3b2f; font-style: italic; }}
  .toc {{ margin: 22px 0 0; font-size: 0.92rem; columns: 2; column-gap: 32px; }}
  .toc a {{ display: block; padding: 3px 0; }}
  footer {{ margin-top: 64px; border-top: 1.5px solid var(--line); padding-top: 20px; font-size: 0.7rem; letter-spacing: 0.04em; color: var(--muted); text-transform: uppercase; }}
</style>
</head>
<body>
<div class="intbar">Internal — prompt review · edit the page-0N.md files, then regenerate</div>
<div class="strip">
  <header class="mast">
    <p class="kicker">Prompt Review — Before Generation</p>
    <h1>The <em>script</em>, before the art.</h1>
    <p class="standfirst">Every image prompt for this explainer, on one page. Read them, rewrite them, then generate. This is the stopgap between the storyboard and the credits.</p>
    <div class="gate">
      <b>How to use this.</b> The source of truth is the <code>page-0N.md</code> files in this folder —
      edit the text after each <code>Image Prompt:</code> marker. Re-run <code>build_prompts_page.py</code>
      to refresh this view. When the prompts read right, generate with
      <code>generate_panels.py --page N --force</code>. Copy buttons are for pasting into an image model by hand.
    </div>
    <nav class="toc">{toc}</nav>
  </header>
  {cards}
  <footer>{footer}</footer>
</div>
<script>
  document.querySelectorAll('.copybtn').forEach(function (b) {{
    b.addEventListener('click', function () {{
      var pre = b.parentElement.querySelector('pre.prompt');
      navigator.clipboard.writeText(pre.innerText).then(function () {{
        var t = b.textContent; b.textContent = 'Copied'; setTimeout(function () {{ b.textContent = t; }}, 1200);
      }});
    }});
  }});
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir", help="manga project dir containing page-0N.md")
    ap.add_argument("--out", default=None, help="output html (default: <project_dir>/prompts.html)")
    ap.add_argument("--title", default=None, help="display title (default: dir name)")
    args = ap.parse_args()

    proj = Path(args.project_dir)
    if not proj.is_dir():
        sys.exit(f"not a directory: {proj}")
    pages = page_files(proj)
    if not pages:
        sys.exit(f"no page-0N.md files in {proj}")

    title = args.title or proj.name.replace("-", " ")
    out = Path(args.out) if args.out else proj / "prompts.html"

    toc_items, cards = [], []
    for n, p in pages:
        ptitle = extract_title(p)
        prompt = extract_prompt(p)
        anchor = f"page-{n}"
        toc_items.append(f'<a href="#{anchor}">Page {n} — {html.escape(ptitle.split("—")[-1].strip())}</a>')
        if prompt:
            chars = len(prompt)
            body = (
                f'<div class="promptwrap"><button class="copybtn">Copy</button>'
                f'<pre class="prompt">{html.escape(prompt)}</pre></div>'
            )
            meta = f'<p class="meta"><b>{chars}</b> chars · source: <b>{html.escape(p.name)}</b></p>'
        else:
            body = '<p class="missing">No <code>Image Prompt:</code> marker found in this file yet.</p>'
            meta = f'<p class="meta">source: <b>{html.escape(p.name)}</b></p>'
        cards.append(
            f'<section class="card" id="{anchor}">'
            f'<p class="card-no">Page {n}</p>'
            f'<h2>{html.escape(ptitle)}</h2>{meta}{body}</section>'
        )

    footer = f"{len(pages)} prompts · {html.escape(proj.name)} · review surface — not the source of truth"
    out.write_text(
        PAGE_TMPL.format(
            title=html.escape(title),
            toc="\n".join(toc_items),
            cards="\n".join(cards),
            footer=footer,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {out} ({len(pages)} prompts)")


if __name__ == "__main__":
    main()
