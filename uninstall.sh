#!/bin/bash
# Remove the cyberpunk webGUI theme from the running webGUI and from /boot/config/go.
# Leaves /boot/config/cyberpunk-theme in place; delete it yourself if you want it gone.
#
#   bash /boot/config/cyberpunk-theme/uninstall.sh
rm -rf /usr/local/emhttp/plugins/cyberpunk-theme
if grep -q cyberpunk-theme /boot/config/go; then
  cp /boot/config/go /boot/config/go.bak-cyberpunk-uninstall
  # Drop the block go-snippet.sh added: its marker comment through the install line.
  sed -i '/^# Cyberpunk webGUI theme/,/cyberpunk-theme\/install\.sh/d' /boot/config/go
  bash -n /boot/config/go || { cp /boot/config/go.bak-cyberpunk-uninstall /boot/config/go; echo "go edit failed, restored"; exit 1; }
fi
logger -t cyberpunk-theme "uninstalled"
echo "uninstalled; reload the page. Base theme is unchanged (Settings > Display Settings)."
