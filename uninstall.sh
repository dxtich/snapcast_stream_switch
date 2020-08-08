#!/usr/bin/env sh
install_dir=$(dirname "$0")

systemctl stop snapcontrol.service
systemctl disable snapcontrol.service
systemctl daemon-reload

rm -f /etc/systemd/system/snapcontrol.service
rm -f /usr/local/bin/snapcontrol
