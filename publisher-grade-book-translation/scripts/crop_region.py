#!/usr/bin/env python3
"""Crop figures, tables, formulas, or complex layout regions from page images."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, help="Single source image.")
    parser.add_argument("--bbox", help="Crop box as left,top,right,bottom in pixels.")
    parser.add_argument("--out", type=Path, help="Single output image.")
    parser.add_argument("--padding", type=int, default=0, help="Optional padding in pixels.")
    parser.add_argument("--manifest", type=Path, help="JSON crop manifest with a 'crops' array.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Base path for manifest-relative files.")
    return parser.parse_args()


def parse_bbox(value: str) -> tuple[int, int, int, int]:
    parts = [int(float(part.strip())) for part in value.split(",")]
    if len(parts) != 4:
        raise ValueError("bbox must be left,top,right,bottom")
    left, top, right, bottom = parts
    if right <= left or bottom <= top:
        raise ValueError("bbox right/bottom must be greater than left/top")
    return left, top, right, bottom


def crop_one(source: Path, output: Path, bbox: tuple[int, int, int, int], padding: int) -> dict:
    try:
        from PIL import Image
    except ImportError:
        print("Missing dependency: Pillow. Install with: python -m pip install pillow", file=sys.stderr)
        raise SystemExit(2)

    if not source.exists():
        raise FileNotFoundError(source)

    with Image.open(source) as image:
        left, top, right, bottom = bbox
        left = max(0, left - padding)
        top = max(0, top - padding)
        right = min(image.width, right + padding)
        bottom = min(image.height, bottom + padding)
        output.parent.mkdir(parents=True, exist_ok=True)
        cropped = image.crop((left, top, right, bottom))
        cropped.save(output)
        return {
            "source": str(source),
            "output": str(output),
            "bbox": [left, top, right, bottom],
            "width": cropped.width,
            "height": cropped.height,
        }


def manifest_crops(args: argparse.Namespace) -> list[dict]:
    payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    crops = payload.get("crops", [])
    results = []
    for item in crops:
        source = args.root / item["source"]
        output = args.root / item["output"]
        bbox = tuple(item["bbox"])
        padding = int(item.get("padding", args.padding))
        results.append(crop_one(source, output, bbox, padding))
    return results


def main() -> int:
    args = parse_args()
    if args.manifest:
        results = manifest_crops(args)
    else:
        if not args.image or not args.bbox or not args.out:
            print("Use either --manifest or --image --bbox --out.", file=sys.stderr)
            return 2
        results = [crop_one(args.image, args.out, parse_bbox(args.bbox), args.padding)]

    print(json.dumps({"crops": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
