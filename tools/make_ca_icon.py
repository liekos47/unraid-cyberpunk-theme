"""Draw icon.png, the 256 px icon Community Apps shows for the plugin.

    python tools/make_ca_icon.py

The mark is icons/logo.svg (drawn here from the same coordinates, so no SVG
renderer is needed), in netrunner red with a cyan trace, on a dark tile.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
S = 1024                 # drawn at 4x, scaled down to 256 for smooth edges
U = S / 64 * 0.78        # logo.svg units (0-64) to pixels, with a margin
OFF = (S - 64 * U) / 2

BG, EDGE = (14, 14, 23, 255), (40, 40, 64, 255)
RED, CYAN = (255, 97, 89, 255), (94, 246, 255, 255)

OUTER = [(32, 2), (58, 17), (58, 39), (44, 55), (32, 62), (6, 47), (6, 17)]
INNER = [(32, 9), (12, 20.5), (12, 43.5), (32, 55), (40, 50.4), (52, 36.5), (52, 20.5)]
TRACE = [(20, 24), (34, 24), (40, 30), (44, 30), (44, 34), (38, 34), (32, 28), (20, 28)]
BARS = [[(20, 38), (30, 38), (30, 42), (20, 42)], [(34, 38), (44, 38), (44, 42), (34, 42)]]


def px(points):
    return [(OFF + x * U, OFF + y * U) for x, y in points]


def mark(colour_hex, colour_trace):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.polygon(px(OUTER), fill=colour_hex)
    d.polygon(px(INNER), fill=(0, 0, 0, 0))
    d.polygon(px(TRACE), fill=colour_trace)
    for bar in BARS:
        d.polygon(px(bar), fill=colour_trace)
    return layer


def main():
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((8, 8, S - 8, S - 8), radius=150, fill=BG, outline=EDGE, width=12)
    glow = mark(RED, CYAN).filter(ImageFilter.GaussianBlur(28))
    img = Image.alpha_composite(img, glow)
    img = Image.alpha_composite(img, glow)
    img = Image.alpha_composite(img, mark(RED, CYAN))
    out = ROOT / "icon.png"
    img.resize((256, 256), Image.LANCZOS).save(out, optimize=True)
    print(f"{out.name}: 256x256")


if __name__ == "__main__":
    main()
