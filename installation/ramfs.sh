#! /bin/sh
### BEGIN INIT INFO
# Provides:          ram_fs
# Required-Start:    $local_fs
# Required-Stop:
# Default-Start:     S
# Default-Stop:         0 6
# Short-Description: Prepares RAM file system for cam.
### END INIT INFO

PATH=/sbin:/bin

. /lib/lsb/init-functions

do_start () {
    mkdir -p /ramfs
    mount -o size=200M -t tmpfs none /ramfs
    echo "Started ramfs"
}
do_stop () {
    umount /ramfs
}

case "$1" in
  start)
        do_start
        ;;
  restart|reload|force-reload)
        do_stop || echo 1
        do_start
        ;;
  stop|status)
        # No-op
        ;;
  *)
        echo "Usage: $0 start|stop" >&2
        exit 3
        ;;
esac
