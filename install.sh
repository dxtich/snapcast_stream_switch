#!/bin/sh
install_dir=$(dirname "$0")

sudo cp -f "$install_dir"/snapcontrol.service /etc/systemd/system/
sudo chown root:root /etc/systemd/system/snapcontrol.service
sudo chmod 644 /etc/systemd/system/snapcontrol.service

sudo cp -f "$install_dir"/snapcontrol.py /usr/local/lib/snapcontrol.py
sudo chown root:root /usr/local/lib/snapcontrol.py
sudo chmod 644 /usr/local/lib/snapcontrol.py
sudo systemctl daemon-reload
sudo systemctl enable snapcontrol.service