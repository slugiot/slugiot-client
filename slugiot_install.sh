#!usr/bin/env bash

# This script assumes that client application code has already been
# installed (at top level) on device along with Linux operating system
# Run with sudo

sudo cp slugiot_startup.sh /etc/init.d

sudo chmod +x /etc/init.d/slugiot_startup.sh

. /etc/init.d/slugiot_startup.sh
