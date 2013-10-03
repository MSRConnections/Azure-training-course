/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 * 
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package kafka.example;

import kafka.javaapi.producer.ProducerData;
import kafka.producer.ProducerConfig;

import java.util.Random;
import java.util.Properties;


public class KafkaGpsDataProducer
{
  final static String topic = "gps";

  private final kafka.javaapi.producer.Producer<Integer, String> producer;
  private final Properties props;
  private final Random rand;
  private final int delay;

  public KafkaGpsDataProducer(String connection, int delay)
  {
    int sepCount = 0;
    for(int i=0; i<connection.length(); i++) {
      if (connection.charAt(i) == ':') {
        sepCount++;
      }
    }

    props = new Properties();
    props.put("serializer.class", "kafka.serializer.StringEncoder");

    if (sepCount == 2) {
      props.put("broker.list", connection);
    } else {
      props.put("zk.connect", connection);
    }

    // Use random partitioner. Don't need the key type. Just set it to Integer.
    // The message is of type String.
    producer = new kafka.javaapi.producer.Producer<Integer, String>(new ProducerConfig(props));

    rand = new Random();
    this.delay = delay;
  }

  public void run() throws Exception {
    while(true)
    {
      double lat = -90.0 + rand.nextDouble() * 180.0;
      double lon = -180.0 + rand.nextDouble() * 360.0;
      String messageStr = new String(lat + ":" + lon);
      producer.send(new ProducerData<Integer, String>(topic, messageStr));
      System.out.println("Sent: " + messageStr);
      if (delay > 0) {
        Thread.sleep(delay);
      }
    }
  }

  public static void main(String[] args) throws Exception
  {
    if (args.length < 1) {
      System.out.println("Usage: KafkaGpsDataProducer connection_string [delay]");
      System.out.println(" connecton_string may be either a zookeeper conection:");
      System.out.println("    ds-jlinford.cloudapp.net:2181");
      System.out.println(" or a kafka broker connection:");
      System.out.println("    0:ds-jlinford.cloudapp.net:9092");
      System.exit(1);
    }

    String connection = args[0];

    int delay = 500;
    if (args.length > 1) {
      delay = Integer.parseInt(args[1]);
    }

    KafkaGpsDataProducer producer = new KafkaGpsDataProducer(connection, delay);
    producer.run();
  }
}
