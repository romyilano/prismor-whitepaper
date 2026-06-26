#!/usr/bin/env python3
"""Bundle an explainer into a single downloadable PDF.

Full structure (the explainer "reader's packet"):
  1. Cover page reproducing the website masthead (title, standfirst, credit).
  2. The comic panels, one per page (panels_dir/page-1.png …).
  3. Two recall worksheets — a "whiteboard" page (sketch what you remember, from
     memory) and a "discussion & avenues" mind-map page (filled in by hand). The
     point: can the reader rebuild it from memory, and what did they actually learn?
  4. If a source document is supplied, a divider page then the full source
     (paper / spec / whitepaper) appended at the back.

The cover + comic + worksheet pages are rendered with headless Chrome (for real
typography), then merged with the source PDF using pypdf.

If Chrome or pypdf isn't available, falls back to a panels-only PDF via Pillow
(no cover / worksheets / source) so you still get something.

Usage:
    pip install pypdf            # plus a local Google Chrome / Chromium
    python3 build_pdf.py --panels docs/panels --out docs/<slug>.pdf \
        --title "Measuring What Matters" \
        --standfirst "A confident benchmark score can measure almost nothing." \
        --source paper.pdf            # local source PDF to append
    python3 build_pdf.py --panels docs/panels --out docs/<slug>.pdf \
        --source-url https://arxiv.org/pdf/2511.04703   # download + append
    python3 build_pdf.py --panels docs/panels --out docs/<slug>.pdf --no-worksheets
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    return None


def page_num(path: str) -> int:
    m = re.search(r"(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else 0


def panel_files(panels_dir: Path) -> list[str]:
    return sorted(
        (f for ext in ("png", "jpg", "jpeg", "webp")
         for f in glob.glob(os.path.join(str(panels_dir), f"page-*.{ext}"))),
        key=page_num,
    )


def worksheets_html() -> str:
    """Two by-hand recall worksheets — placed after the comic, before the source."""
    return """
  <section class="worksheet">
    <p class="kicker">Worksheet &middot; One of Two</p>
    <h2>From memory, <em>the whiteboard</em></h2>
    <p class="ws-lede">Close the comic &mdash; don't peek. Sketch out what you recollect and understand,
       as if you were standing at a whiteboard explaining it to a colleague. Boxes, arrows, a few words.</p>
    <div class="ws-board"><span class="ws-hint">your whiteboard</span></div>
    <p class="ws-foot">Whatever stays blank is the part worth re-reading. Recall first, re-read second.</p>
  </section>
  <section class="worksheet">
    <p class="kicker">Worksheet &middot; Two of Two</p>
    <h2>Discussion &amp; <em>avenues</em></h2>
    <p class="ws-lede">Mind-map this by hand &mdash; on your tablet if you have one, or a physical whiteboard.
       The questions matter more than the answers: what did you actually learn, and where would you take it next?</p>
    <div class="ws-grid">
      <div class="ws-cell"><p class="num">01</p><h3>What did I actually learn?</h3></div>
      <div class="ws-cell"><p class="num">02</p><h3>What's still fuzzy?</h3></div>
      <div class="ws-cell"><p class="num">03</p><h3>Avenues to explore next</h3></div>
      <div class="ws-cell"><p class="num">04</p><h3>Who would I ask? What would I test?</h3></div>
    </div>
  </section>"""


def front_html(panels: list[str], cfg: dict, with_worksheets: bool, with_source: bool) -> str:
    plates = "".join(
        f'<section class="plate"><img src="{Path(p).resolve().as_uri()}"></section>'
        for p in panels
    )
    worksheets = worksheets_html() if with_worksheets else ""
    divider = ""
    if with_source:
        divider = f"""
  <section class="divider">
    <h2>{cfg['source_heading']}</h2>
    <p>{cfg['source_note']}</p>
  </section>"""
    byline = "".join(f"<span>{b}</span>" for b in cfg["byline"])
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500&display=swap" rel="stylesheet">
<style>
  :root {{ --paper:#e6e9e4; --ink:#1d2128; --muted:#6c7178; --spot:#3c5d72; --line:#1d2128; }}
  @page {{ size: 8.5in 11in; margin: 0; }}
  * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{ background: var(--paper); color: var(--ink); font-family: "Newsreader", Georgia, serif; }}
  a {{ color: var(--spot); text-decoration: none; }}
  section {{ width: 8.5in; height: 11in; overflow: hidden; }}
  section + section {{ page-break-before: always; }}
  .kicker {{ text-transform: uppercase; letter-spacing: 0.3em; font-size: 0.8rem; font-weight: 600;
             color: var(--spot); margin: 0 0 30px; }}
  .cover {{ padding: 1.1in 1.05in; display: flex; flex-direction: column; justify-content: center; }}
  .cover h1 {{ font-family: "Fraunces", serif; font-weight: 500; font-size: 4.6rem; line-height: 0.98;
               letter-spacing: -0.025em; margin: 0; }}
  .cover h1 em {{ font-style: italic; color: var(--spot); }}
  .standfirst {{ font-family: "Fraunces", serif; font-size: 1.7rem; color: var(--muted); font-style: italic;
                 line-height: 1.3; max-width: 22em; margin: 34px 0 0; }}
  .byline {{ font-size: 0.74rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted);
             margin-top: 40px; border-top: 1.5px solid var(--line); padding-top: 14px;
             display: flex; gap: 28px; flex-wrap: wrap; }}
  .credit {{ font-size: 0.74rem; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted);
             margin: 14px 0 0; }}
  .plate {{ display: flex; align-items: center; justify-content: center; padding: 0.5in; }}
  .plate img {{ max-width: 7.5in; max-height: 10in; width: auto; height: auto; object-fit: contain;
                border: 1.5px solid var(--line); box-shadow: 8px 8px 0 rgba(29,33,40,0.10); }}
  .divider {{ padding: 1.3in 1.05in; display: flex; flex-direction: column; justify-content: center; }}
  .divider h2 {{ font-family: "Fraunces", serif; font-weight: 500; font-size: 3.2rem; margin: 0;
                 letter-spacing: -0.02em; }}
  .divider p {{ font-size: 1.1rem; color: var(--muted); max-width: 26em; line-height: 1.5; margin: 24px 0 0; }}
  .worksheet {{ padding: 0.85in 1.05in 0.75in; display: flex; flex-direction: column; }}
  .worksheet .kicker {{ margin: 0 0 16px; }}
  .worksheet h2 {{ font-family: "Fraunces", serif; font-weight: 500; font-size: 2.9rem;
                   letter-spacing: -0.02em; margin: 0; line-height: 1.0; }}
  .worksheet h2 em {{ font-style: italic; color: var(--spot); }}
  .ws-lede {{ font-family: "Fraunces", serif; font-size: 1.22rem; font-style: italic; color: var(--muted);
              line-height: 1.4; max-width: 30em; margin: 16px 0 20px; }}
  .ws-board {{ flex: 1; border: 1.6px solid var(--line); border-radius: 3px; position: relative;
               box-shadow: 8px 8px 0 rgba(29,33,40,0.08);
               background-image: radial-gradient(rgba(29,33,40,0.12) 1.1px, transparent 1.1px);
               background-size: 24px 24px; background-position: 14px 14px; }}
  .ws-hint {{ position: absolute; bottom: 12px; right: 16px; font-size: 0.7rem; letter-spacing: 0.2em;
              text-transform: uppercase; color: var(--muted); }}
  .ws-foot {{ font-size: 0.82rem; color: var(--muted); margin: 14px 0 0; font-style: italic; }}
  .ws-grid {{ flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 16px; }}
  .ws-cell {{ border: 1.4px solid var(--line); border-radius: 3px; padding: 14px 16px 16px;
              display: flex; flex-direction: column;
              background-image: radial-gradient(rgba(29,33,40,0.09) 1px, transparent 1px);
              background-size: 22px 22px; background-position: 11px 44px; }}
  .ws-cell .num {{ font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase;
                   color: var(--spot); margin: 0 0 5px; }}
  .ws-cell h3 {{ font-family: "Fraunces", serif; font-weight: 500; font-size: 1.12rem; margin: 0;
                 color: var(--ink); line-height: 1.15; }}
</style></head><body>
  <section class="cover">
    <p class="kicker">{cfg['kicker']}</p>
    <h1>{cfg['title_html']}</h1>
    <p class="standfirst">{cfg['standfirst']}</p>
    <div class="byline">{byline}</div>
    <p class="credit">{cfg['credit']}</p>
  </section>
  {plates}{worksheets}{divider}
</body></html>"""


def render_front_pdf(chrome: str, html: str, work: Path) -> Path:
    html_path = work / "front.html"
    html_path.write_text(html, encoding="utf-8")
    front_pdf = work / "front.pdf"
    subprocess.run(
        [
            chrome, "--headless=new", "--disable-gpu",
            "--no-pdf-header-footer", "--allow-file-access-from-files",
            "--virtual-time-budget=15000",
            f"--print-to-pdf={front_pdf}", html_path.as_uri(),
        ],
        check=True, capture_output=True,
    )
    if not front_pdf.exists():
        sys.exit("Chrome did not produce the front PDF.")
    return front_pdf


def get_source_pdf(work: Path, supplied: str | None, url: str | None) -> Path | None:
    if supplied:
        return Path(supplied)
    if not url:
        return None
    dest = work / "source.pdf"
    req = urllib.request.Request(url, headers={"User-Agent": "explainer-site-generator/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
            f.write(r.read())
    except urllib.error.URLError as exc:
        # Fall back to system curl (OS trust store) when urllib's SSL verification
        # fails — common on freshly-built Pythons lacking a configured CA bundle.
        print(f"urllib download failed ({exc.reason}); falling back to curl ...", file=sys.stderr)
        subprocess.run(
            ["curl", "-fsSL", "-A", "explainer-site-generator/1.0", url, "-o", str(dest)],
            check=True,
        )
    return dest


def pillow_fallback(panels: list[str], out: str, res: float) -> int:
    try:
        from PIL import Image
    except ImportError:
        sys.exit("No Chrome and no Pillow. Install one: `pip install pillow` (panels-only) "
                 "or install Google Chrome + `pip install pypdf` for the full packet.")
    print("WARNING: Chrome not found — building panels-only PDF (no cover/worksheets/source).",
          file=sys.stderr)
    imgs = [Image.open(f).convert("RGB") for f in panels]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    imgs[0].save(out, save_all=True, append_images=imgs[1:], resolution=res)
    print(f"Wrote {out} — {len(imgs)} pages (panels only).")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--panels", default="docs/panels", help="dir with page-*.png (default: docs/panels)")
    ap.add_argument("--out", default="docs/explainer.pdf", help="output PDF path")
    ap.add_argument("--title", default="An Explainer", help="cover title (use *stars* for the italic spot color)")
    ap.add_argument("--standfirst", default="", help="cover standfirst / dek")
    ap.add_argument("--kicker", default="An Explainer, in Six Pages", help="cover kicker line")
    ap.add_argument("--byline", action="append", default=[], help="cover byline chip, repeatable")
    ap.add_argument("--credit", default="", help="cover credit line (HTML allowed)")
    ap.add_argument("--source", help="local source PDF to append at the back (paper/spec/whitepaper)")
    ap.add_argument("--source-url", help="download a source PDF and append it at the back")
    ap.add_argument("--source-heading", default="The source, in full",
                    help="divider heading before the appended source")
    ap.add_argument("--source-note", default="What follows is the complete source document this explainer covers.",
                    help="divider note before the appended source")
    ap.add_argument("--no-worksheets", action="store_true", help="omit the two recall worksheets")
    ap.add_argument("--res", type=float, default=150.0, help="Pillow-fallback resolution (dpi)")
    args = ap.parse_args()

    panels = panel_files(Path(args.panels))
    if not panels:
        sys.exit(f"No page-*.png found in {args.panels}")

    # *stars* -> italic spot <em>
    title_html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", args.title)
    cfg = {
        "kicker": args.kicker,
        "title_html": title_html,
        "standfirst": args.standfirst,
        "byline": args.byline,
        "credit": args.credit,
        "source_heading": args.source_heading,
        "source_note": args.source_note,
    }

    chrome = find_chrome()
    if not chrome:
        return pillow_fallback(panels, args.out, args.res)

    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        sys.exit("pypdf is required for the full packet: `pip install pypdf` "
                 "(or omit Chrome to fall back to a panels-only PDF).")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        source_pdf = get_source_pdf(work, args.source, args.source_url)
        html = front_html(panels, cfg, not args.no_worksheets, source_pdf is not None)
        front_pdf = render_front_pdf(chrome, html, work)

        writer = PdfWriter()
        readers = [PdfReader(str(front_pdf))]
        if source_pdf is not None:
            readers.append(PdfReader(str(source_pdf)))
        for reader in readers:
            for page in reader.pages:
                writer.add_page(page)
        with open(out_path, "wb") as f:
            writer.write(f)

        n = len(PdfReader(str(out_path)).pages)
    extras = [] if args.no_worksheets else ["2 worksheets"]
    if source_pdf is not None:
        extras.append("source appended")
    tail = (" — " + ", ".join(extras)) if extras else ""
    print(f"Wrote {out_path} ({n} pages){tail}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
