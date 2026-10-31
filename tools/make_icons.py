"""Turn your own logo into the theme's header mark and status favicons.

Optional: without these files the theme uses icons/logo.svg and keeps
Unraid's stock favicon.

Input: a PNG whose shape is defined by its alpha channel (white or any
colour on transparent works best; square or close to it).
Output, written next to this repo's icons/ folder:
  logo.png             white mask, 256 px (the CSS tints it)
  fav-green-on.png     64 px, array started
  fav-red-on.png       64 px, array stopped
  fav-yellow-on.png    64 px, array in transition

Usage: python tools/make_icons.py path/to/your-logo.png
Needs Pillow (pip install Pillow).
"""
import sys
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "icons"
STATUS = {
    "fav-green-on.png": (0x1D, 0xED, 0x83),
    "fav-red-on.png": (0xFF, 0x61, 0x59),
    "fav-yellow-on.png": (0xFF, 0xD7, 0x41),
}


def tinted(mask: Image.Image, rgb, size: int) -> Image.Image:
    m = mask.copy()
    m.thumbnail((size, size), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    solid = Image.new("RGBA", m.size, rgb + (255,))
    solid.putalpha(m.split()[3])
    canvas.paste(solid, ((size - m.width) // 2, (size - m.height) // 2), solid)
    return canvas


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    mask = Image.open(sys.argv[1]).convert("RGBA")
    OUT.mkdir(exist_ok=True)
    tinted(mask, (255, 255, 255), 256).save(OUT / "logo.png", optimize=True)
    for name, rgb in STATUS.items():
        tinted(mask, rgb, 64).save(OUT / name, optimize=True)
    print("wrote logo.png and 3 favicons to", OUT)


if __name__ == "__main__":
    main()
