#!/bin/bash
# Install the cyberpunk webGUI theme from the flash drive into the running webGUI.
#
# The webGUI lives in RAM, so this has to run at every boot: add go-snippet.sh
# to /boot/config/go once (see README). Safe to re-run at any time.
#
#   bash /boot/config/cyberpunk-theme/install.sh
#
# Turn off without uninstalling: touch /boot/config/cyberpunk-theme/DISABLED
SRC=/boot/config/cyberpunk-theme
DST=/usr/local/emhttp/plugins/cyberpunk-theme
FONT_BASE=https://raw.githubusercontent.com/google/fonts/main/ofl
log() { logger -t cyberpunk-theme "$*"; echo "$*"; }

[ -d "$SRC/plugin" ] || { log "no $SRC/plugin, nothing to install"; exit 0; }

# Palette: PALETTE=<name> in theme.cfg, matching palettes/<name>.css. Default netrunner.
PALETTE=netrunner
[ -f "$SRC/theme.cfg" ] && . "$SRC/theme.cfg"
[ -f "$SRC/palettes/$PALETTE.css" ] || { log "palette '$PALETTE' not found in $SRC/palettes"; exit 1; }

# Fonts (SIL OFL): fetched once into the flash drive, reused at every boot.
# A failed download is not fatal: the theme falls back to the stock fonts.
mkdir -p "$SRC/fonts"
fetch() {
  [ -s "$SRC/fonts/$2" ] && return 0
  curl -fsSL --max-time 30 -o "$SRC/fonts/$2.tmp" "$FONT_BASE/$1" \
    && mv "$SRC/fonts/$2.tmp" "$SRC/fonts/$2" \
    || { rm -f "$SRC/fonts/$2.tmp"; log "font $2 not downloaded, using stock fonts"; }
}
fetch rajdhani/Rajdhani-Regular.ttf  Rajdhani-Regular.ttf
fetch rajdhani/Rajdhani-Medium.ttf   Rajdhani-Medium.ttf
fetch rajdhani/Rajdhani-SemiBold.ttf Rajdhani-SemiBold.ttf
fetch rajdhani/Rajdhani-Bold.ttf     Rajdhani-Bold.ttf
fetch 'orbitron/Orbitron%5Bwght%5D.ttf' Orbitron-wght.ttf

# Build the new copy beside the live one, then swap, so a failed copy never
# leaves a half-installed theme.
tmp="$DST.new"
rm -rf "$tmp"
mkdir -p "$tmp/fonts" "$tmp/icons" || { log "mkdir failed"; exit 1; }
cp "$SRC"/plugin/* "$tmp/" \
  && cp "$SRC/palettes/$PALETTE.css" "$tmp/palette.css" \
  && cp "$SRC"/icons/* "$tmp/icons/" \
  || { log "copy failed, leaving the current install alone"; rm -rf "$tmp"; exit 1; }
cp "$SRC"/fonts/*.ttf "$tmp/fonts/" 2>/dev/null
rm -rf "$DST" && mv "$tmp" "$DST"
log "installed, palette $PALETTE, $(ls "$DST/fonts" | wc -l) fonts"
