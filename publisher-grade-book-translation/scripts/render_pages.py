#!/usr/bin/env python3
"""Render PDF pages to PNG images for visual-first book translation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Source PDF path.")
    parser.add_argument("--out", type=Path, default=Path("pages/page-images"), help="Output image directory.")
    parser.add_argument("--dpi", type=int, default=180, help="Render DPI. 180-220 is usually enough.")
    parser.add_argument("--prefix", default="page", help="Output filename prefix.")
    parser.add_argument("--first", type=int, default=1, help="First 1-based page to render.")
    parser.add_argument("--last", type=int, help="Last 1-based page to render.")
    parser.add_argument("--manifest", type=Path, help="Optional JSON manifest output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("Missing dependency: PyMuPDF. Install with: python -m pip install pymupdf", file=sys.stderr)
        return 2

    if not args.pdf.exists():
        print(f"PDF not found: {args.pdf}", file=sys.stderr)
        return 2

    args.out.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(args.pdf)
    page_count = len(doc)
    first = max(1, args.first)
    last = min(page_count, args.last or page_count)
    if first > last:
        print(f"Invalid page range: {first}-{last}", file=sys.stderr)
        return 2

    matrix = fitz.Matrix(args.dpi / 72, args.dpi / 72)
    entries = []
    for page_number in range(first, last + 1):
        page = doc[page_number - 1]
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        image_path = args.out / f"{args.prefix}-{page_number:04d}.png"
        pix.save(str(image_path))
        entries.append(
            {
                "page": page_number,
                "image": str(image_path),
                "width": pix.width,
                "height": pix.height,
                "dpi": args.dpi,
            }
        )

    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        payload = {"source": str(args.pdf), "page_count": page_count, "rendered_pages": entries}
        args.manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Rendered {len(entries)} pages to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
