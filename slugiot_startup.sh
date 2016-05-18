#!usr/bin/env bash

# TODO - start webserver as daemon like luca's RPi bootcamp script

SERVER=example.com
PORT=8080
PASS=password

# Fetch internal network ip into variable (more reliable than using just 'hostname -I')
myip=
while IFS=$': \t' read -a line ;do
    [ -z "${line%inet}" ] && ip=${line[${#line[1]}>4?1:2]} &&
        [ "${ip#127.0.0.1}" ] && myip=$ip
  done< <(LANG=C /sbin/ifconfig)

# start web2py with start scheduler command option
python web2py.py -a $PASS -i $myip -p $PORT -K client -X

# Check if webserver up and running and, if so, run startup script
nc -z $myip $PORT; wup=$?;
if [$wup -ne 0]; then
  echo "Connection to $myip on port $PORT failed"
  exit 1
else    # TODO - need to handle http response code here
  echo "Connection to $myip on port $PORT succeeded.  Call to _start()."
  curl --ipv4 http://$myip:$PORT/startup/_start.html
  exit 0
fi
