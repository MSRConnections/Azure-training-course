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
import java.util.LinkedList;
import java.util.List;
import kafka.javaapi.producer.ProducerData;
import kafka.producer.ProducerConfig;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.Properties;
import java.util.StringTokenizer;
import java.util.Random;
import java.util.Properties;
import java.util.Dictionary;
import java.util.Hashtable;
import java.util.List;
import java.util.ArrayList;

public class KafkaCarDataProducer
{
  final static String topic = "car";

  private final kafka.javaapi.producer.Producer<Integer, String> producer;
  private final Properties props;
  private final Random rand;
  private final int delay;

  public KafkaCarDataProducer(String connection, int delay)
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
	      String home = System.getProperty("user.home");
	      File csv = new File(home + "/storm-kafka-demo/testdata.csv"); // CSV..
	      BufferedReader br = new BufferedReader(new FileReader(csv));

	      String line = "";
	      int testCount = 0;
	      List messages = new LinkedList();
	      while ((line = br.readLine()) != null) { 
	          StringTokenizer st = new StringTokenizer(line, ",");
	          //index 4 speed, 9 rpm, 10 temperature, 11 gear, 13 14 latitude longitude,
	          int currentCount = 0;
	          String messageStr = "";
	          while (st.hasMoreTokens()) {               
	              if(currentCount==0)
	              {
	              	  messageStr += st.nextToken() + ":";                  	
	              }
	              else if(currentCount==1)
	              {
	              	  messageStr +=  st.nextToken() + ":";                  	
	              }
	              else if(currentCount==2)
	              {
	              	  messageStr +=  st.nextToken() + ":";                  	
	              }
	              else if(currentCount==3)
	              {
	              	  messageStr += st.nextToken() + ":";                  	
	              }
		      else if(currentCount==4)
                      {
                          messageStr += st.nextToken() + ":";
                      }
                      else if(currentCount==5)
                      {
                          messageStr += st.nextToken();
                      }
	              else
	              {
	              	st.nextToken();
	              }
	              
	              currentCount++;
	          } 
	          producer.send(new ProducerData<Integer, String>(topic, messageStr));
		  messages.add(messageStr);
	          System.out.println("Sent: " + messageStr);
	          if (delay > 0) 
	          {
	              Thread.sleep(delay);
	          }
	      } 
	      br.close();
	      int currentCount2=0;
	      while(true)
	      {
                  producer.send(new ProducerData<Integer, String>(topic, messages.get(currentCount2).toString()));
                  System.out.println("Sent2: " + messages.get(currentCount2));
                  if (delay > 0)
                  {
                      Thread.sleep(delay);
                  }
				  if(currentCount2==messages.size()-1)
				  {
					  currentCount2=0;
				  }
				  else
				  { 
					  currentCount2++;
				  }
	      }
  }

  public static void main(String[] args) throws Exception
  {
    if (args.length < 1) {
      System.out.println("Usage: KafkaCarDataProducer connection_string [delay]");
      System.out.println(" connecton_string may be either a zookeeper conection:");
      System.out.println("    ds-jlinford.cloudapp.net:2181");
      System.out.println(" or a kafka broker connection:");
      System.out.println("    0:ds-jlinford.cloudapp.net:9092");
      System.exit(1);
    }

    String connection = args[0];

    int delay = 1000;
    if (args.length > 1) {
      delay = Integer.parseInt(args[1]);
    }

    KafkaCarDataProducer producer = new KafkaCarDataProducer(connection, delay);
    producer.run();
  }
}
