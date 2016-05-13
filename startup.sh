#!usr/bin/env bash

# start web2py with start scheduler command option
sudo python web2py.py -a '<recycle>' -i 127.0.0.1 -p 8000 -K client -X

# Run startup script (which first requires scheduler to be run)
(sleep 10; python sudo ./applications/client/controllers/startup.py)&

