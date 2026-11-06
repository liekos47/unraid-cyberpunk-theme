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

Start from the palette closest to what you want: `cp palettes/netrunner.css palettes/<name>.css`. The first line names its place in the settings page list, then a comment says what the palette is and where its colours come from:

```css
/* @group Mass Effect @desc title blue, HUD teal, renegade orange */
```

`@group` is the heading it is listed under (the settings page orders Cyberpunk 2077, Cyberpunk: Edgerunners, Neon and Mass Effect first, then any other group alphabetically; a file without the line goes under Custom) and `@desc` is the short description after its name.

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

Build the plugin package from your working copy and install it from local files, so nothing is downloaded from GitHub:

```bash
python tools/build_plugin.py 2026.11.07 v2.0.0     # any version and tag while testing
ssh root@<server> 'mkdir -p /boot/config/plugins/cyberpunk-theme'
scp build/cyberpunk-theme-2026.11.07-noarch-1.txz root@<server>:/boot/config/plugins/cyberpunk-theme/
scp cyberpunk-theme.plg root@<server>:/tmp/
ssh root@<server> 'plugin install /tmp/cyberpunk-theme.plg'
```

The plugin finds the package already on the flash drive with the right MD5 and installs it. Pick your palette in Settings > User Utilities > Cyberpunk Theme; the dropdown previews it without saving.

- If you already run the plugin, this installs over it and keeps your saved choice. Put your release back afterwards with Plugins > Install Plugin and the normal URL.
- If you run a manual install, set it aside first: `mv /boot/config/cyberpunk-theme /boot/config/cyberpunk-theme.keep` and `rm -rf /usr/local/emhttp/plugins/cyberpunk-theme`. Afterwards `plugin remove cyberpunk-theme.plg`, move the folder back and run its `install.sh`.
- To test a boot without rebooting: `removepkg cyberpunk-theme-<version>-noarch-1`, `rm -rf /var/log/plugins/cyberpunk-theme.plg /usr/local/emhttp/plugins/cyberpunk-theme`, then `plugin install` again. That is the state Unraid starts from.

To try a palette file alone on a running install, copy it to `/usr/local/emhttp/plugins/cyberpunk-theme/palettes/` and reload the settings page: it appears in the list straight away (until the next boot).

Only the webGUI's look changes during the test. Nothing else on the server is touched, and `touch /boot/config/plugins/cyberpunk-theme/DISABLED` turns the theme off at any time, settings page included.

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

The plugin has two parts: `cyberpunk-theme.plg` on `main`, which every server checks for updates, and the package `cyberpunk-theme-<version>-noarch-1.txz`, attached to a GitHub release. The `.plg` names the release tag and the package's MD5, so the two must go out together.

1. Pick the plugin version, the release date as `YYYY.MM.DD` (a second release on the same day adds a number: `2026.11.07.1`; not a letter, which Unraid's package tool ranks below the plain date and then skips), and the release tag: a minor version (`2.0.0` to `2.1.0`) for new palettes or features, a patch version (`2.0.0` to `2.0.1`) for colour fixes.
2. Add an entry at the top of `<CHANGES>` in `cyberpunk-theme.plg` (`###<version> (<tag>)` and a few lines). Unraid shows it on the Plugins page.
3. Build. This writes the package to `build/` and stamps the version, tag and MD5 into the `.plg`:

```bash
python tools/build_plugin.py 2026.11.07 v2.0.0
```

4. Bump the tag in the README's manual install lines (the URL and the extracted folder name).
5. Commit, push, then publish the release with the package straight away. Between the push and the upload, a server that checks for updates finds a package that is not there yet and simply reports an error; the next check works.

```bash
git push origin main
git tag -a vX.Y.Z -m "vX.Y.Z: <what changed>"
git push origin vX.Y.Z
gh release create vX.Y.Z build/cyberpunk-theme-<version>-noarch-1.txz --title "vX.Y.Z" --notes "<what changed>"
```

6. Check it: download the `.plg` from the raw URL and the package from the release, and compare the MD5 with the one in the `.plg`. Then install from the URL on a test server (Plugins > Install Plugin), or on a server that already runs it, check for updates on the Plugins page.
