# Developing a palette

How to make a new palette, check it, test it on a real server without losing your current setup, take README screenshots that give nothing away, and release it. Every palette in this repo went through these steps.

## 1. How a palette works

A palette is one file, `palettes/<name>.css`, that sets 16 colours on `:root`. `plugin/cyberpunk.css` maps them onto Unraid's own theme variables, so a palette never needs any other CSS.

| Variable | Used for |
|---|---|
| `--cp-pri` | Headings, tile titles, active tab, button outlines, header rule. Also the hover button fill, with `--cp-bg` as its text |
| `--cp-pri-dark` | Darker accent (Unraid's "brand red", jQuery UI button gradient) |
| `--cp-pri-faint` | Very dark tint of the accent |
| `--cp-sec` | Values, links, usage bar fill, dashboard icons, focused inputs |
| `--cp-sec-dim` | Inactive tabs, input borders, scrollbars, checkboxes |
| `--cp-hi` | Highlights (Unraid's light orange status colour) |
| `--cp-faint` | Hairlines, borders, empty bar tracks |
| `--cp-ok` / `--cp-warn` / `--cp-err` | Status: started, warning, error |
| `--cp-bg` | Page background |
| `--cp-panel` / `--cp-panel-alt` | Tiles and tables, alternate rows |
| `--cp-deep` | Header, footer, table headers |
| `--cp-txt` / `--cp-txt-dim` | Body text, secondary text |

Start from the palette closest to what you want: `cp palettes/netrunner.css palettes/<name>.css`. Put a comment at the top saying what the palette is and where its colours come from.

**Design rules that keep it readable:**

- Keep the backgrounds very dark (`--cp-bg`, `--cp-panel` and `--cp-deep` under about 10 % lightness). Tint them towards the palette's hue rather than using neutral grey: that tint is what makes a palette feel like itself.
- `--cp-pri` and `--cp-sec` should be clearly different hues. The dashboard mostly shows `--cp-pri` (titles, active tab) and body text; `--cp-sec` shows up in tab hovers, icons, bars and links.
- `--cp-ok`, `--cp-warn` and `--cp-err` must still read as green, amber and red, whatever the palette.
- If the colours come from a game, film or brand, use only hex values you picked yourself or sampled. Never add logos, fonts, textures or other assets to this repo.

## 2. Check contrast offline

```bash
python tools/check_contrast.py palettes/<name>.css
```

It tests every text colour against every surface (WCAG 2 contrast) and the hover button, and lists anything under 4.5:1. Fix every `FAIL`. A `warning` on `faint` is allowed when the live scan in step 4 passes, because text rarely sits on hairlines or empty bar tracks. Lightening `--cp-sec-dim` or darkening `--cp-faint` slightly usually fixes it.

## 3. Test on a server without losing your setup

Set your current install aside, install your working copy, and put it all back when you are done. From a PC with the repo:

```bash
git archive --format=tar HEAD | ssh root@<server> '
  mv /boot/config/cyberpunk-theme /boot/config/cyberpunk-theme.keep
  mkdir /boot/config/cyberpunk-theme
  tar xf - --no-same-owner -C /boot/config/cyberpunk-theme
  echo PALETTE=<name> > /boot/config/cyberpunk-theme/theme.cfg
  bash /boot/config/cyberpunk-theme/install.sh'
```

Commit first, since `git archive` packs `HEAD`. `--no-same-owner` is needed because the flash drive is FAT32. If the theme was not installed before, skip the `mv` line.

To switch palette while testing (reload the page afterwards with Ctrl+F5):

```bash
ssh root@<server> 'echo PALETTE=<other> > /boot/config/cyberpunk-theme/theme.cfg && bash /boot/config/cyberpunk-theme/install.sh'
```

To put your own install back:

```bash
ssh root@<server> 'rm -rf /boot/config/cyberpunk-theme && mv /boot/config/cyberpunk-theme.keep /boot/config/cyberpunk-theme && bash /boot/config/cyberpunk-theme/install.sh'
```

Only the webGUI's look changes during the test. Nothing else on the server is touched, and `touch /boot/config/cyberpunk-theme/DISABLED` turns the theme off at any time.

## 4. Check contrast on the real pages

Open the webGUI, open the browser console (F12), paste `tools/contrast-scan.js` and press Enter. It lists every visible text under 4.5:1 against the background actually behind it. Run it on Dashboard, Main and Plugins at least, and on Docker, Settings and Tools if you changed more than colours.

Two known exceptions are Unraid's own and stay as they are: the orange "Update Available" badge and the brief "checking..." text on Plugins. Anything else means a colour needs adjusting.

## 5. Take a README screenshot

Screenshots show your server's details, so replace them first:

1. Set the browser window to about 1400 x 720 and open the Dashboard.
2. Edit the `REPLACE` list at the top of `tools/scrub-page.js` with your server name, description, motherboard and BIOS lines, stack names and anything else you see, then paste it into the console. It keeps applying while the dashboard refreshes. It only changes the page in your browser.
3. Read the whole visible page before taking the screenshot: anything not in `REPLACE` is still there. Check the header, the date line under the clock, the Docker and VM tiles, app icons under GPU "Active Apps", and the footer.
4. Move the mouse pointer off the page, take the screenshot and save it as `docs/screenshots/<name>.png`.
5. Open the PNG and look at it before committing. Once it is pushed, it is public.

## 6. Add it to the README

- A row in the palette table at the top: name, accent colour, value colour and highlight.
- A sentence in the paragraph under the table if the palette is inspired by something, saying the colours were picked by eye or from which public source.
- A preview block in **Previews**: `**<name>**` and the image.
- If it is inspired by a game or brand, add the rights holder to the "not affiliated with" line in **Credits and licences**.

## 7. Release

1. Bump the version in the README install lines (the tag in the URL and the extracted folder name).
2. Commit and push.
3. Tag and publish the release:

```bash
git tag -a vX.Y.Z -m "vX.Y.Z: <what changed>"
git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z" --notes "<what changed>"
```

4. Check the install lines from the README work: run steps 1 and 3 of **Install** on a test server, or at least confirm the release archive downloads and contains the new palette.

Use a minor version (`1.2.0` to `1.3.0`) for new palettes and a patch version (`1.2.0` to `1.2.1`) for colour fixes.
