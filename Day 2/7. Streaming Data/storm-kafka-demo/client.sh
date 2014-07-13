#/bin/sh
#Launch kafka client:
 
cd $HOME/storm-kafka-demo/kafka-car-client
java -cp $(lein classpath) kafka.example.KafkaCarDataProducer localhost

