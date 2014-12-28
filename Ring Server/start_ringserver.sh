#!/bin/sh

WORKING_DIR=.

if [ ! -e "${WORKING_DIR}/log" ]; then
	mkdir ${WORKING_DIR}/log
fi

# stop ringserver
./stop_ringserver.sh

# start ringserver
echo "Starting ringserver..."
LOGFILE=${WORKING_DIR}/log/ringserver.log
nohup ./ringserver ring.conf 1> ${LOGFILE} 2>&1 &
PID=$!
echo ${PID} > ${WORKING_DIR}/log/ringserver.pid
echo "   ringserver pid=${PID}, logfile=${LOGFILE}"
sleep 1
