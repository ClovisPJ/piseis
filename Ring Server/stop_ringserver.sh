#!/bin/sh

HOME=./

# announce script
echo "Stopping ringserver:"

# stop ringserver
if [ -f "${HOME}/log/ringserver.pid" ] ; then
    pid=`cat ${HOME}/log/ringserver.pid`
    echo "Stopping ringserver [$pid]..."
    kill $pid
    rm -f ${HOME}/log/ringserver.pid
fi
sleep 1

echo "ringserver stopped."
echo ""
exit 1

