"""Offline contrast check for palette files.

Checks every text colour of a palette against every surface it can sit on,
using the WCAG 2 formula, and the hover button (background colour on the
accent). Anything under 4.5:1 is listed. No dependencies.

`faint` (hairlines, empty bar tracks) rarely has text on it, so a pair
under 4.5:1 there is a warning, not a failure: confirm it with the live scan
(tools/contrast-scan.js) instead.

    python tools/check_contrast.py palettes/*.css

Exit code 1 if any palette fails (a pair under 4.5:1 on any surface but faint).
"""
import re
import sys

TEXT = ["txt", "txt-dim", "sec-dim", "pri", "sec", "hi", "ok", "warn", "err"]
SURFACES = ["bg", "panel", "panel-alt", "deep", "faint"]
MIN = 4.5


def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def main(paths):
    failed = False
    for path in paths:
        with open(path, encoding="utf-8") as f:
            colours = dict(re.findall(r"--cp-([\w-]+):\s*(#[0-9A-Fa-f]{6})", f.read()))
        missing = [k for k in TEXT + SURFACES if k not in colours]
        if missing:
            print(f"{path}: missing {', '.join(missing)}")
            failed = True
            continue
        low = [(ratio(colours[t], colours[s]), t, s) for t in TEXT for s in SURFACES]
        worst = min(low)
        low = [x for x in low if x[0] < MIN]
        button = ratio(colours["bg"], colours["pri"])
        if button < MIN:
            low.append((button, "bg", "pri (hover button)"))
        fails = [x for x in low if x[2] != "faint"]
        status = "FAIL" if fails else ("warn" if low else "ok")
        print(f"{status:4} {path}: worst {worst[0]:.2f} ({worst[1]} on {worst[2]}), hover button {button:.2f}")
        for r, t, s in sorted(low):
            print(f"     {r:.2f}  {t} on {s}{'' if s != 'faint' else '  (warning)'}")
        failed |= bool(fails)
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
