#!/usr/bin/env python3
"""Validate book image assets for obvious production problems."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+", type=Path, help="Images to validate.")
    parser.add_argument("--min-width", type=int, default=80)
    parser.add_argument("--min-height", type=int, default=80)
    parser.add_argument("--blank-stddev", type=float, default=2.0, help="Lower grayscale stddev is treated as blank.")
    parser.add_argument("--json-out", type=Path, help="Optional JSON report path.")
    parser.add_argument("--warn-only", action="store_true", help="Exit 0 even when issues are found.")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_image(path: Path, args: argparse.Namespace) -> dict:
    try:
        from PIL import Image, ImageStat
    except ImportError:
        print("Missing dependency: Pillow. Install with: python -m pip install pillow", file=sys.stderr)
        raise SystemExit(2)

    item = {"path": str(path), "issues": []}
    if not path.exists():
        item["issues"].append("missing")
        return item

    try:
        with Image.open(path) as image:
            item["width"] = image.width
            item["height"] = image.height
            item["mode"] = image.mode
            if image.width < args.min_width or image.height < args.min_height:
                item["issues"].append("too-small")
            gray = image.convert("L")
            stddev = ImageStat.Stat(gray).stddev[0]
            item["gray_stddev"] = round(stddev, 3)
            if stddev < args.blank_stddev:
                item["issues"].append("possibly-blank")
        item["sha256"] = sha256(path)
    except Exception as error:  # noqa: BLE001
        item["issues"].append(f"unreadable:{error}")
    return item


def main() -> int:
    args = parse_args()
    items = [inspect_image(path, args) for path in args.images]
    by_hash = {}
    for item in items:
        digest = item.get("sha256")
        if digest:
            by_hash.setdefault(digest, []).append(item["path"])
    duplicates = [paths for paths in by_hash.values() if len(paths) > 1]
    for paths in duplicates:
        for item in items:
            if item["path"] in paths:
                item["issues"].append("duplicate")

    issue_count = sum(len(item["issues"]) for item in items)
    report = {"image_count": len(items), "issue_count": issue_count, "duplicates": duplicates, "images": items}
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for item in items:
        if item["issues"]:
            print(f"{item['path']}: {', '.join(item['issues'])}")
    print(f"Checked {len(items)} images; issues: {issue_count}")
    return 0 if args.warn_only or issue_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
