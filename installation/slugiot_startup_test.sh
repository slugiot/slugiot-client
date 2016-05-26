#!/usr/bin/env bash

# This script starts web2py on the client in test mode (i.e., not from the system startup script).
# This is handy for testing.
# Give this command in the parent dir of slugiot-client and slugiot-server.

PATH="/sbin:/bin:/usr/bin"
PID_FILE=/var/run/web2py.pid
USER=pi
CMD=slugiot-client/web2py.py
PYTHON=/usr/bin/python
PORT=8080
PASS=password
APP=client

# TODO - Remove -e flag when done testing.  Better: allow to run this script with debug option.
do_start () {
    $PYTHON -- $CMD -e -a $PASS -p $PORT -K $APP -i 0.0.0.0 -X
    echo "Started web2py!"
}

do_stop () {
    /usr/bin/pkill -9 -f "python web2py"
    echo "Stopped web2py"
}

do_startup(){
    # Fetch internal network ip into variable
    pyip=
    while IFS=$': \t' read -a line ;do
        [ -z "${line%inet}" ] && ip=${line[${#line[1]}>4?1:2]} &&
            [ "${ip#127.0.0.1}" ] && pyip=$ip
      done< <(LANG=C /sbin/ifconfig)

    # Check if webserver up and running and, if so, open web browser to client and
    # run startup script from localhost.
    nc -z $pyip $PORT; wup=$?;
    if [ $wup -ne 0 ]; then
      echo "Connection to $pyip on port $PORT failed"
      exit 1
    else
      echo "Connection to client succeeded.  Begin call to _startup() from localhost..."
      httpUrl="http://127.0.0.1:$PORT/startup/_startup.html"
      rep=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n' $httpUrl)
      status=$?
      if [ $status -ne 0 && $rep -ne 200 ]; then
        echo "Failed to startup $APP completely; http_status = $rep.  Check it!!!"
      else
        # TODO - Final checks per _startup() controller.  E.g., sqlite3 util check scheduler created.
        echo "Completed startup of $APP with http_status = $rep "
      fi
      echo "Access admin area using http://$pyip:$PORT/ "
    fi
}


case "$1" in
  start)
        do_start
        sleep 10
        do_startup
        ;;
  stop)
        do_stop
        ;;
  *)
        echo "Usage: $0 start|stop" >&2
        exit 3
        ;;
esac
