#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pillow",
#     "pyobjc-framework-Cocoa",
# ]
# ///

"""Read an image from the macOS clipboard; save WebP + JPEG in ~/Downloads (same stem)."""

import sys
from datetime import datetime
from io import BytesIO
from pathlib import Path

if sys.platform != "darwin":
    print("clipboard_to_webp.py only runs on macOS.", file=sys.stderr)
    sys.exit(1)

from AppKit import NSPasteboard  # noqa: E402
from PIL import Image  # noqa: E402

# Preferred order: try WebP/JPEG first, then other raster types.
_CLIPBOARD_IMAGE_UTIS = (
    "public.webp",
    "public.jpeg",
    "public.png",
    "public.tiff",
    "com.compuserve.gif",
)

# WebP: embed / repo (smaller).
_WEBP_QUALITY = 84
_WEBP_METHOD = 6

# JPEG: tools that read images (e.g. IDE preview); slightly higher quality for text/UI.
_JPEG_QUALITY = 90


def _clipboard_image_bytes() -> tuple[bytes, str]:
    pb = NSPasteboard.generalPasteboard()
    if pb is None:
        print("Could not access the macOS pasteboard.", file=sys.stderr)
        sys.exit(1)
    for uti in _CLIPBOARD_IMAGE_UTIS:
        data = pb.dataForType_(uti)
        if data is not None and len(data) > 0:
            return bytes(data), uti
    return b"", ""


def _to_rgb(img: Image.Image) -> Image.Image:
    if img.mode in ("RGBA", "LA", "PA"):
        img = img.convert("RGBA")
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.getchannel("A"))
        return bg
    return img.convert("RGB")


def main() -> None:
    raw, uti = _clipboard_image_bytes()
    if not raw:
        print(
            "No image found on the clipboard (copy an image first).",
            file=sys.stderr,
        )
        sys.exit(1)

    downloads = Path.home() / "Downloads"
    downloads.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%H:%M:%S")
    out_webp = downloads / f"{stamp}.webp"
    out_jpeg = downloads / f"{stamp}.jpg"

    img = Image.open(BytesIO(raw))
    img = _to_rgb(img)

    img.save(
        out_webp,
        "WEBP",
        quality=_WEBP_QUALITY,
        method=_WEBP_METHOD,
    )
    img.save(out_jpeg, "JPEG", quality=_JPEG_QUALITY, optimize=True)

    print(f"Saved clipboard image ({uti}) to:")
    print(f"  WebP: {out_webp}")
    print(f"  JPEG: {out_jpeg}")
    print(f"SAVED_PATH_WEBP={out_webp}")
    print(f"SAVED_PATH_JPEG={out_jpeg}")
    # Alias for flows that expect a single "asset" path (the WebP).
    print(f"SAVED_PATH={out_webp}")


if __name__ == "__main__":
    main()
