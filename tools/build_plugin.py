"""Build the Unraid plugin package and stamp cyberpunk-theme.plg.

    python tools/build_plugin.py <version> <tag>
    python tools/build_plugin.py 2026.11.07 v2.0.0

Writes build/cyberpunk-theme-<version>-noarch-1.txz (a Slackware package that
installs into /usr/local/emhttp/plugins/cyberpunk-theme) and sets the version,
tag and MD5 entities in cyberpunk-theme.plg. Upload the .txz to the GitHub
release named <tag>, then commit the .plg: Unraid reads the .plg from main and
downloads the package from the release.

The fonts (SIL OFL) are downloaded once from github.com/google/fonts into
build/fonts and bundled with their licences. No other dependencies.
"""
import hashlib
import io
import re
import sys
import tarfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
NAME = "cyberpunk-theme"
DEST = f"usr/local/emhttp/plugins/{NAME}"
FONT_BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl"
FONTS = {
    "Rajdhani-Regular.ttf": "rajdhani/Rajdhani-Regular.ttf",
    "Rajdhani-Medium.ttf": "rajdhani/Rajdhani-Medium.ttf",
    "Rajdhani-SemiBold.ttf": "rajdhani/Rajdhani-SemiBold.ttf",
    "Rajdhani-Bold.ttf": "rajdhani/Rajdhani-Bold.ttf",
    "Orbitron-wght.ttf": "orbitron/Orbitron%5Bwght%5D.ttf",
    "OFL-Rajdhani.txt": "rajdhani/OFL.txt",
    "OFL-Orbitron.txt": "orbitron/OFL.txt",
}
TEXT = {".page", ".css", ".md", ".svg", ".txt"}


def fetch_fonts():
    cache = BUILD / "fonts"
    cache.mkdir(parents=True, exist_ok=True)
    for name, path in FONTS.items():
        target = cache / name
        if not target.exists() or target.stat().st_size == 0:
            print(f"downloading {name}")
            with urllib.request.urlopen(f"{FONT_BASE}/{path}", timeout=60) as r:
                target.write_bytes(r.read())
    return cache


def files(font_dir):
    """(path inside the package, source file) for everything the plugin ships."""
    out = [(f"{DEST}/{p.name}", p) for p in sorted((ROOT / "plugin").iterdir()) if p.is_file()]
    out += [(f"{DEST}/palettes/{p.name}", p) for p in sorted((ROOT / "palettes").glob("*.css"))]
    out += [(f"{DEST}/icons/{p.name}", p) for p in sorted((ROOT / "icons").iterdir()) if p.is_file()]
    out += [(f"{DEST}/fonts/{n}", font_dir / n) for n in sorted(FONTS)]
    return out


def build(version):
    # A second build on the same day takes a letter: 2026.11.07a.
    mtime = int(time.mktime(time.strptime(version[:10], "%Y.%m.%d")))
    pkg = BUILD / f"{NAME}-{version}-noarch-1.txz"
    entries = files(fetch_fonts())
    dirs = sorted({str(Path(a).parent).replace("\\", "/") for a, _ in entries} | {"usr", "usr/local", "usr/local/emhttp", "usr/local/emhttp/plugins"})
    with tarfile.open(pkg, "w:xz") as tar:
        for d in dirs:
            info = tarfile.TarInfo(d)
            info.type, info.mode, info.mtime = tarfile.DIRTYPE, 0o755, mtime
            tar.addfile(info)
        for arc, src in entries:
            data = src.read_bytes()
            if src.suffix in TEXT:
                data = data.replace(b"\r\n", b"\n")
            info = tarfile.TarInfo(arc)
            info.size, info.mode, info.mtime = len(data), 0o644, mtime
            tar.addfile(info, io.BytesIO(data))
    return pkg, len(entries)


def stamp(version, tag, md5):
    plg = ROOT / f"{NAME}.plg"
    s = plg.read_text(encoding="utf-8")
    for key, value in (("version", version), ("tag", tag), ("md5", md5)):
        s, n = re.subn(rf'(<!ENTITY {key}\s+")[^"]*(")', rf"\g<1>{value}\g<2>", s)
        if n != 1:
            sys.exit(f"could not set {key} in {plg.name}")
    plg.write_text(s, encoding="utf-8", newline="\n")


def main():
    if len(sys.argv) != 3 or not re.fullmatch(r"\d{4}\.\d{2}\.\d{2}[a-z]?", sys.argv[1]) or not sys.argv[2].startswith("v"):
        sys.exit(__doc__)
    version, tag = sys.argv[1], sys.argv[2]
    pkg, count = build(version)
    md5 = hashlib.md5(pkg.read_bytes()).hexdigest()
    stamp(version, tag, md5)
    print(f"{pkg.relative_to(ROOT)}: {count} files, md5 {md5}")
    print(f"{NAME}.plg stamped: version {version}, tag {tag}")


if __name__ == "__main__":
    main()
