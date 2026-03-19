#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

"""Copy a WebP (or any image file) into the current working directory with a safe stem."""

import re
import shutil
import sys
from pathlib import Path


def safe_stem(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80] if s else "image"


def main() -> None:
    if len(sys.argv) < 3:
        print(
            "Usage: image_to_workspace.py <source.webp> <descriptive-name-stem>",
            file=sys.stderr,
        )
        sys.exit(1)

    src = Path(sys.argv[1]).expanduser().resolve()
    stem = safe_stem(sys.argv[2])

    if not src.is_file():
        print(f"Not a file: {src}", file=sys.stderr)
        sys.exit(1)

    dest_dir = Path.cwd().resolve()
    dest = dest_dir / f"{stem}.webp"
    if dest.exists():
        n = 2
        while True:
            dest = dest_dir / f"{stem}-{n}.webp"
            if not dest.exists():
                break
            n += 1

    shutil.copy2(src, dest)
    print(f"Copied to: {dest}")


if __name__ == "__main__":
    main()
