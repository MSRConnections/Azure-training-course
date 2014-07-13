#/bin/sh
#Launch storm topology in a different session:
 
cd $HOME/storm-kafka-demo
java -cp $(lein classpath) storm.example.KafkaCarTopology

