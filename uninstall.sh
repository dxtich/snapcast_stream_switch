#!/usr/bin/env sh
install_dir=$(dirname "$0")

sudo systemctl stop snapcontrol.service
sudo systemctl disable snapcontrol.service
sudo systemctl daemon-reload

sudo rm -f /etc/systemd/system/snapcontrol.service
sudo rm -f /usr/local/lib/snapcontrol.py
