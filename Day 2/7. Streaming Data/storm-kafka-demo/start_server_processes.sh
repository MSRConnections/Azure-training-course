#!/bin/bash

ZOOKEEPER_SERVER_START=zookeeper-server-start.sh
KAFKA_SERVER_START=kafka-server-start.sh
REDIS_SERVER_START=/usr/bin/redis-server

ZK_LOG=$HOME/zookeeper-server.log
KS_LOG=$HOME/kafka-server.log
RS_LOG=$HOME/redis-server.log

which_zk=`which $ZOOKEEPER_SERVER_START`
if [ -z "$which_zk" ] ; then
  echo "ERROR: Cannot locate $ZOOKEEPER_SERVER_START.  Check your PATH."
  exit 1
fi

which_ks=`which $KAFKA_SERVER_START`
if [ -z "$which_ks" ] ; then
  echo "ERROR: Cannot locate $KAFKA_SERVER_START.  Check your PATH."
  exit 1
fi

if [ ! -x "$REDIS_SERVER_START" ] ; then
  echo "ERROR: Cannot execute $REDIS_SERVER_START.  Check Redis installation."
  exit 1
fi

KAFKA_HOME=$(readlink -f $(dirname $which_zk)/..)
if [ -z "$KAFKA_HOME" ] ; then
  echo "ERROR: Cannot determine Kafka installation location."
fi

$which_zk "$KAFKA_HOME/config/zookeeper.properties" > "$ZK_LOG" 2>&1 &
echo "Logging Zookeeper output to $ZK_LOG"

sleep 2

$which_ks "$KAFKA_HOME/config/server.properties" > "$KS_LOG" 2>&1 &
echo "Logging Kafka server output to $KS_LOG"

sleep 2

$REDIS_SERVER_START > "$RS_LOG" 2>&1 &
echo "Logging redis server output to $RS_LOG"

