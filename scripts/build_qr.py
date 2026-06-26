#!/usr/bin/env python3
"""Generate a QR-code PNG that links to the deployed explainer site.

Keeps the page self-contained (no view-time calls to an external QR API).
Drop the output in docs/ and point the template's {{QR_IMG}} at it.

Usage:
    python3 build_qr.py <url> <output.png> [--fg "#1d2128"] [--scale 10]

Requires the `qrcode` package (pulls in Pillow):
    python3 -m pip install "qrcode[pil]"
"""
import argparse
import os
import sys

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_M
except ImportError:
    sys.exit('qrcode is required: python3 -m pip install "qrcode[pil]"')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", help="URL the QR code should open, e.g. https://owner.github.io/repo/")
    ap.add_argument("output", help="output PNG path, e.g. docs/qr.png")
    ap.add_argument("--fg", default="#1d2128", help="foreground (module) color")
    ap.add_argument("--bg", default="#ffffff", help="background color")
    ap.add_argument("--scale", type=int, default=10, help="pixels per module (box_size)")
    args = ap.parse_args()

    qr = qrcode.QRCode(border=2, box_size=args.scale, error_correction=ERROR_CORRECT_M)
    qr.add_data(args.url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=args.fg, back_color=args.bg)

    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    img.save(args.output)
    print(f"Wrote {args.output} -> {args.url}")


if __name__ == "__main__":
    main()
