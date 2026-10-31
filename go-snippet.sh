
# Cyberpunk webGUI theme. /usr/local/emhttp is in RAM, so the theme is
# reinstalled from the flash drive at every boot. Turn it off without a reboot:
# touch /boot/config/cyberpunk-theme/DISABLED
[ -f /boot/config/cyberpunk-theme/install.sh ] && bash /boot/config/cyberpunk-theme/install.sh >/dev/null 2>&1
