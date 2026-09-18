#!/usr/bin/env python3
"""Regenerate the served WebP for every screenshot under src/pages/.

Screenshots are kept as PNG — lossless, so they can be re-encoded any number of
times without decay — and served as WebP, which is around 90% smaller at this
quality with no visible difference on screenshot material. build-blog.py skips
a .png whose .webp sibling exists, so the PNGs stay in the repo and are never
published.

Run after adding or replacing a screenshot, then run build-blog.py:

    python3 tools/webp.py
    python3 tools/build-blog.py

Only rewrites a .webp that is missing or older than its .png, so it is cheap to
run every time. Pass --force to re-encode everything (e.g. after changing
QUALITY).
"""
import sys
from pathlib import Path

from PIL import Image

QUALITY = 82  # verified against the originals at 1:1; text stays crisp
ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"


def main() -> int:
    force = "--force" in sys.argv
    if not PAGES.exists():
        print(f"no {PAGES}", file=sys.stderr)
        return 1

    before = after = 0
    written = skipped = 0
    for png in sorted(PAGES.glob("*/*.png")):
        webp = png.with_suffix(".webp")
        if not force and webp.exists() and webp.stat().st_mtime >= png.stat().st_mtime:
            skipped += 1
            continue
        # method=6 is the slowest, densest setting; alpha is preserved.
        Image.open(png).save(webp, "WEBP", quality=QUALITY, method=6)
        b, a = png.stat().st_size, webp.stat().st_size
        before += b
        after += a
        written += 1
        print(f"  {png.parent.name}/{png.name:<26} {b/1024:6.0f}KB → {a/1024:5.0f}KB  ({100*(1-a/b):3.0f}% smaller)")

    if written:
        print(f"\n{written} written, {before/1024:.0f}KB → {after/1024:.0f}KB "
              f"({100*(1-after/before):.0f}% smaller)")
    if skipped:
        print(f"{skipped} already current (--force to re-encode)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
