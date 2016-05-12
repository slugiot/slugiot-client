#!usr/bin/env bash

# start python with option to also start scheduler
sudo python web2py.py -a password -K client -X

# Run startup script
(sleep 10; python sudo ./applications/client/controllers/startup.py)&

