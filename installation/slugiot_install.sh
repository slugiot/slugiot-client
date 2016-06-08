#!usr/bin/env bash

# This script assumes that client application code has already been
# installed (at top level) on device along with Linux operating system
# Run with sudo

sudo update-rc.d slugiot_startup remove
sudo update-rc.d ramfs remove

cd /home/pi/slugiot-client/installation
sudo cp slugiot_startup.sh /etc/init.d/slugiot_startup
sudo chown root /etc/init.d/slugiot_startup
sudo chmod u+x /etc/init.d/slugiot_startup
sudo update-rc.d -f slugiot_startup defaults

sudo cp ramfs.sh /etc/init.d/ramfs
sudo chown root /etc/init.d/ramfs
sudo chmod u+x /etc/init.d/ramfs
sudo update-rc.d -f ramfs defaults

# Manually start them instead of reboot
sudo sh /etc/init.d/ramfs restart
sleep 1
sudo sh /etc/init.d/slugiot_startup restart

# Check status of services
sudo service ramfs status -l
sudo service slugiot_startup status -l
