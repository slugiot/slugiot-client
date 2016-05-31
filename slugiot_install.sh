#!usr/bin/env bash

# This script assumes that client application code has already been
# installed (at top level) on device along with Linux operating system
# Run with sudo

sudo cp slugiot_startup.sh /etc/init.d/slugiot_startup
sudo chown root /etc/init.d/slugiot_startup
sudo chmod u+x /etc/init.d/slugiot_startup
sudo update-rc.d slugiot_startup defaults

sudo cp ramfs.sh /etc/init.d/ramfs
sudo chown root /etc/init.d/ramfs
sudo chmod u+x /etc/init.d/ramfs
sudo update-rc.d ramfs defaults

. /etc/init.d/slugiot_startup start
