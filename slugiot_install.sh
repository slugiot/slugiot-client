#!usr/bin/env bash

# This script assumes that client application code has already been
# installed (at top level) on device along with Linux operating system
# Run with sudo

sudo cp slugiot_startup.h /etc/init.d/slugiot_startup
sudo chown root /etc/init.d/
sudo chmod u+x /etc/init.d/slugiot_startup
sudo update-rc.d slugiot_startup defaults

. /etc/init.d/slugiot_startup start
