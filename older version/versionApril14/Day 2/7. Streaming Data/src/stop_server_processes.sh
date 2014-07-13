#!/bin/bash

ZOOKEEPER_SERVER_STOP=zookeeper-server-stop.sh
KAFKA_SERVER_STOP=kafka-server-stop.sh

which_zk=`which $ZOOKEEPER_SERVER_STOP`
if [ -z "$which_zk" ] ; then
  echo "ERROR: Cannot locate $ZOOKEEPER_SERVER_STOP.  Check your PATH."
  exit 1
fi

which_ks=`which $KAFKA_SERVER_STOP`
if [ -z "$which_ks" ] ; then
  echo "ERROR: Cannot locate $KAFKA_SERVER_STOP.  Check your PATH."
  exit 1
fi

killall redis-server

$KAFKA_SERVER_STOP

sleep 2

$ZOOKEEPER_SERVER_STOP

