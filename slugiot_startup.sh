#!usr/bin/env bash
### BEGIN INIT INFO
# Provides:          web2py
# Required-Start:    $local_fs ram_fs
# Required-Stop:
# Default-Start:     S
# Default-Stop:         0 6
# Short-Description: Starts local web2py server, with scheduler running in background for APP.
### END INIT INFO

PATH="/sbin:/bin:/usr/bin"
PID_FILE=/var/run/web2py.pid
USER=pi
APPDIR=/home/pi/Documents
CMD=$APPDIR/slugiot-client/web2py.py
PYTHON=/usr/bin/python
PORT=8080
PASS=password
APP=client

. /lib/lsb/init-functions

do_start () {
    /sbin/start-stop-daemon --start --chuid $USER -d $APPDIR --background -v --user $USER --pidfile $PID_FILE --make-pidfile --exec $PYTHON --startas $PYTHON -- $CMD -a $PASS -p $PORT -K $APP -i 0.0.0.0 -X
    log_success_msg "Started web2py"
}
do_stop () {
    /sbin/start-stop-daemon --stop -d $APPDIR -v --user $USER --pidfile $PID_FILE --exec $PYTHON --retry 10
    rm $PID_FILE
    log_success_msg "Stopped web2py"
}

# Fetch internal network ip into variable (more reliable than using just 'hostname -I')
pyip=
while IFS=$': \t' read -a line ;do
    [ -z "${line%inet}" ] && ip=${line[${#line[1]}>4?1:2]} &&
        [ "${ip#127.0.0.1}" ] && pyip=$ip
  done< <(LANG=C /sbin/ifconfig)

# Check if webserver up and running and, if so, open web browser to client and
# run startup script from localhost.
nc -z $pyip $PORT; wup=$?;
if [$wup -ne 0]; then
  echo "Connection to $pyip on port $PORT failed"
  exit 1
else
  echo "Connection to client succeeded.  "
  echo "Access client on internal network using http://$pyip:$PORT/"
  echo "Begin call to _start() from localhost..."
  # TODO - need to handle http response code here.  Presently call is rejected.
  curl --ipv4 http://127.0.0.1:$PORT/startup/_start.html
  exit 0
fi
