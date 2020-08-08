#!/usr/bin/env sh
install_dir=$(dirname "$0")

cp -f "$install_dir"/snapcontrol.service /etc/systemd/system/
chown root:root /etc/systemd/system/snapcontrol.service
chmod 644 /etc/systemd/system/snapcontrol.service

cp -f "$install_dir"/snapcontrol.py /usr/local/bin/snapcontrol
chown root:root /usr/local/bin/snapcontrol
chmod 644 /usr/local/bin/snapcontrol
systemctl daemon-reload
systemctl enable snapcontrol.service