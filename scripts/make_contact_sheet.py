#!/usr/bin/env python3
"""Create a contact sheet for quick manual review of cropped images."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+", type=Path, help="Images to include. Shell globs are OK.")
    parser.add_argument("--out", type=Path, default=Path("review/contact-sheet.png"), help="Output sheet path.")
    parser.add_argument("--cols", type=int, default=4, help="Number of columns.")
    parser.add_argument("--thumb-width", type=int, default=360, help="Thumbnail width.")
    parser.add_argument("--label-height", type=int, default=34, help="Space for filename labels.")
    parser.add_argument("--background", default="white", help="Background color.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Missing dependency: Pillow. Install with: python -m pip install pillow", file=sys.stderr)
        return 2

    images = [path for path in args.images if path.exists()]
    missing = [str(path) for path in args.images if not path.exists()]
    if missing:
        print("Missing images:", *missing, sep="\n- ", file=sys.stderr)
    if not images:
        print("No existing images to include.", file=sys.stderr)
        return 2

    thumbs = []
    max_cell_height = 0
    for path in images:
        with Image.open(path) as image:
            image = image.convert("RGB")
            ratio = args.thumb_width / image.width
            thumb_height = max(1, int(image.height * ratio))
            thumb = image.resize((args.thumb_width, thumb_height))
            thumbs.append((path, thumb))
            max_cell_height = max(max_cell_height, thumb_height + args.label_height)

    cols = max(1, args.cols)
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * args.thumb_width, rows * max_cell_height), args.background)
    draw = ImageDraw.Draw(sheet)

    for index, (path, thumb) in enumerate(thumbs):
        col = index % cols
        row = index // cols
        x = col * args.thumb_width
        y = row * max_cell_height
        sheet.paste(thumb, (x, y))
        label = path.name[:60]
        draw.text((x + 6, y + thumb.height + 6), label, fill="black")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
