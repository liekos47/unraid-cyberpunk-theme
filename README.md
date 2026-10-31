# Unraid cyberpunk theme

A dark, neon webGUI theme for Unraid 7.x: near-black navy panels, angular cut corners, Rajdhani and Orbitron type, and two palettes.

| Palette | Headings and accents | Values and links |
|---|---|---|
| `netrunner` (default) | red `#FF6159` | cyan `#5EF6FF` |
| `relic` | acid yellow `#F1FF5E` | electric blue `#6DA1FF` |

Run one palette per server and you can tell your boxes apart at a glance.

## How it works

Unraid evaluates every plugin page marked `Menu="Buttons"` in the `<head>` of every webGUI page, right after its own theme stylesheet. This theme is one such page (`plugin/CyberpunkTheme.page`) that adds three stylesheets. **No Unraid file is modified.** The stock themes are built on CSS variables, so the theme mostly remaps those variables, plus a few rules for shapes and for colours that Unraid or its plugins set directly.

- Works on any base theme. `black` is recommended (Settings > Display Settings).
- The array-state favicon keeps its meaning (green started, red stopped, yellow in transition) if you supply your own logo (see below).
- Text contrast was checked at 4.5:1 or better on Dashboard, Main, Shares, Users, Settings, Plugins, Docker, VMs, Tools and Syslog, on the black and white bases. Exceptions left stock: Unraid's orange "Update Available" badge and the brief "checking..." text on the Plugins page.
- Tested on Unraid 7.3.3. A later Unraid release can change the page markup; the fallback is always the stock theme, never a broken page.

## Install

From a shell on the server (Tools > Terminal, or SSH):

```bash
# 1. Put the files on the flash drive
mkdir -p /boot/config/cyberpunk-theme
cd /tmp && curl -fsSL https://github.com/<you>/<repo>/archive/refs/heads/main.tar.gz | tar xz
cp -r /tmp/<repo>-main/* /boot/config/cyberpunk-theme/

# 2. Optional: pick the palette (default netrunner)
echo 'PALETTE=relic' > /boot/config/cyberpunk-theme/theme.cfg

# 3. Install now (downloads the two OFL fonts once from github.com/google/fonts)
bash /boot/config/cyberpunk-theme/install.sh

# 4. Reinstall at every boot (the webGUI lives in RAM)
grep -q cyberpunk-theme /boot/config/go || cat /boot/config/cyberpunk-theme/go-snippet.sh >> /boot/config/go
```

Reload the webGUI (Ctrl+F5).

## Your own logo

The header shows `icons/logo.svg`, an original placeholder mark tinted with the palette. To use your own:

```bash
python tools/make_icons.py my-logo.png     # on any PC with Pillow
```

That writes `icons/logo.png` (header mark) and `icons/fav-{green,red,yellow}-on.png` (array-state favicons). Copy them to `/boot/config/cyberpunk-theme/icons/` and re-run `install.sh`. Any PNG whose shape is in its alpha channel works.

Only use artwork you have the right to use.

## Turn off, uninstall

- Off until you remove the file, no reboot: `touch /boot/config/cyberpunk-theme/DISABLED`
- Uninstall (removes the live copy and the `go` lines, keeps the flash folder): `bash /boot/config/cyberpunk-theme/uninstall.sh`

## Add a palette

Copy `palettes/netrunner.css` to `palettes/<name>.css`, change the `--cp-*` colours, set `PALETTE=<name>` in `theme.cfg` and re-run `install.sh`. Check that body text (`--cp-txt`) and dim text (`--cp-sec-dim`) stay readable on `--cp-panel` and `--cp-deep`.

## Credits and licences

- Code: MIT, see `LICENSE`.
- Fonts: [Rajdhani](https://github.com/google/fonts/tree/main/ofl/rajdhani) (Indian Type Foundry) and [Orbitron](https://github.com/google/fonts/tree/main/ofl/orbitron) (Matt McInerney), SIL Open Font License 1.1. They are not in this repository: `install.sh` downloads them.
- A fan-made theme inspired by the look of cyberpunk games. Not affiliated with or endorsed by CD PROJEKT RED or Lime Technology. No game assets are included.
