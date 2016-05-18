#!usr/bin/env bash

# TODO: Later will add variables for port number, application, and password.

# Fetch internal network ip into variable (more reliable than using just 'hostname -I')
myip=
while IFS=$': \t' read -a line ;do
    [ -z "${line%inet}" ] && ip=${line[${#line[1]}>4?1:2]} &&
        [ "${ip#127.0.0.1}" ] && myip=$ip
  done< <(LANG=C /sbin/ifconfig)

# start web2py with start scheduler command option
python web2py.py -a password -i $myip -p 8080 -K client -X

# TODO: ping port to check webserver running; use awk to see if response (pid), then can start()
# netstat -anp | grep 8080

# Run startup script
curl http://$myip:8080/startup/start.html
