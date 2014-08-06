package storm.example.bolt;
import com.microsoft.windowsazure.services.core.storage.*;
import com.microsoft.windowsazure.services.table.client.*;
import com.microsoft.windowsazure.services.table.client.TableQuery.*;
import java.util.Calendar;
import org.json.JSONObject;
import org.json.JSONException;

import java.util.List;
import java.util.Map;
import java.util.Collections;

import org.apache.log4j.Logger;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;
import redis.clients.jedis.JedisPubSub;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;


public class RedisCarBolt extends BaseRichBolt {

	public String channel;
    public String configChannel;
    public OutputCollector collector;
    public Tuple currentTuple;
    public Logger log;
    public JedisPool pool;
    public ConfigListenerThread configListenerThread;
    
    public interface OnDynamicConfigurationListener {
        public void onConfigurationChange(String conf);
    }
    
	public class CarInfo extends TableServiceEntity
	{
		public CarInfo(String lastName, String firstName) {
	        this.partitionKey = lastName;
	        this.rowKey = firstName;
	    }

	    public CarInfo() { }

	    int rpm;
	    int speed;
	    int temp;
	    String gear;
	    String lat;
	    String lon;

	    public int getRPM() {
	        return this.rpm;
	    }
	    
	    public int getSpeed() {
	        return this.speed;
	    }
	    
	    public int getTemp() {
	        return this.temp;
	    }
	    
	    public String getGear() {
	        return this.gear;
	    }
	    
	    public String getLat() {
	        return this.lat;
	    }
	    
	    public String getLon() {
	        return this.lon;
	    }

	    
	    public void setRPM(int rpm) {
	        this.rpm = rpm;
	    }

	    public void setSpeed(int speed) {
	        this.speed = speed;
	    }

	    public void setTemp(int temp) {
	        this.temp = temp;
	    }
	    
	    public void setGear(String gear) {
	        this.gear = gear;
	    }

	    public void setLat(String lat) {
	        this.lat = lat;
	    }

	    public void setLon(String lon) {
	        this.lon = lon;
	    }	
	}
	public final String storageConnectionString = 
		    "DefaultEndpointsProtocol=http;" + 
		    "AccountName=[Storage Account Name];" + 
		    "AccountKey=[Storage Account Key]";

  public RedisCarBolt() {
    this.channel = "coordinates";
    configChannel = "config_update_" + "coordinates";
  }

  public void setupNonSerializableAttributes() {

  }

  /**
   * Will create a new thread (carefull, if you specify a multiplicity of 3
   * for this bolt, you will create 3 new threads). That will listen to a 
   * redis pubsub channel, when ever a message is sent to that channel,
   * will read the key with the specific name in the message and pass it to the
   * onConfiguration function.
   */
  public void setupDynamicConfiguration(final OnDynamicConfigurationListener listener) {
      configListenerThread = new ConfigListenerThread(listener);
      configListenerThread.start();
  }
  
  @Override
  public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
      this.collector = collector;
      pool = new JedisPool(new JedisPoolConfig(), "localhost");
      log = Logger.getLogger(getClass().getName());
      setupNonSerializableAttributes();
  }

  @Override
  public void execute(Tuple tuple) {
      currentTuple = tuple;
      List<Object> result = filter(tuple);
      if(result != null) {
          for(Object obj: result) {
              collector.emit(tuple, new Values(obj));
          }
          collector.ack(tuple);
      }
  }

  @Override
  public void cleanup() {
      if(pool != null) {
          pool.destroy();
      }

      if(configListenerThread != null) {
          configListenerThread.end();
      }
  }

  @Override
  public void declareOutputFields(OutputFieldsDeclarer declarer) {
      declarer.declare(new Fields(channel));
  }
  
  public void publish(String msg) {
      Jedis jedis = pool.getResource();
      jedis.publish(channel, msg);
      pool.returnResource(jedis);
  }
  
  public List<Object> filter(Tuple tuple) {
    if(tuple != null) {	
      try {
        JSONObject json = new JSONObject();
        json.put("speed", tuple.getInteger(0));
        json.put("rpm", tuple.getInteger(1));
        json.put("temperature", tuple.getInteger(2));
        json.put("gear", tuple.getString(3));
        json.put("lat", tuple.getString(5));
        json.put("lon", tuple.getString(4));
        // Publish a string representation of the JSON object
        // to the Redis topic
		CloudStorageAccount storageAccount =
    		    CloudStorageAccount.parse(storageConnectionString);

    		// Create the table client.
    		CloudTableClient tableClient = storageAccount.createCloudTableClient();

    		// Create the table if it doesn't exist.
    		String tableName = "carinfo";
    		CloudTable table = tableClient.getTableReference("carinfo");
    		table.createIfNotExist();
    		Calendar ca = Calendar.getInstance();
    		System.out.println(ca.getTimeInMillis());
    		Thread.sleep(100);
    		
    		CarInfo car1 = new CarInfo("car1", String.valueOf(ca.getTimeInMillis()));
    		car1.setSpeed(tuple.getInteger(0));
    		car1.setRPM(tuple.getInteger(1));
    		car1.setTemp(tuple.getInteger(2));
    		car1.setGear(tuple.getString(3));
    		car1.setLat(tuple.getString(4));
    		car1.setLon(tuple.getString(5));

    		// Create an operation to add the new customer to the people table.
    		TableOperation insertCarInfo = TableOperation.insert(car1);

    		// Submit the operation to the table service.
    		tableClient.execute(tableName, insertCarInfo);
        System.out.println("Filter: " + json.toString());
        publish(json.toString());
      } catch (Exception e) {
        throw new RuntimeException("Failed to get JSON representation.");
      }

      // Acknowledge this tuple by returning an empty list.
      // The list is empty because we don't need to emit any fields.
      //
      // IMPORTANT: Returning null will cause the tuple to not
      // be acknowledged (see RedisBolt.java).
      // Every processed tuple must be acked or failed. Storm uses 
      // memory to track each tuple, so if you don't ack/fail every 
      // tuple, the task will eventually run out of memory.
      return Collections.emptyList();
    }
    return null;
  }

  private class ConfigListenerThread extends Thread {
      
      //Use it's own pool, is in a different thread.
      final Jedis jedis = new Jedis("localhost");
      private OnDynamicConfigurationListener listener;
      
      public ConfigListenerThread(OnDynamicConfigurationListener l) {
          listener = l;
      }
      
      @Override
      public void run() {
          jedis.subscribe(new JedisPubSub() {
              
              @Override
              public void onUnsubscribe(String arg0, int arg1) {
                  // TODO Auto-generated method stub
                  
              }
              
              @Override
              public void onSubscribe(String arg0, int arg1) {
                  // TODO Auto-generated method stub
                  
              }
              
              @Override
              public void onPUnsubscribe(String arg0, int arg1) {
                  // TODO Auto-generated method stub
                  
              }
              
              @Override
              public void onPSubscribe(String arg0, int arg1) {
                  // TODO Auto-generated method stub
                  
              }
              
              @Override
              public void onPMessage(String arg0, String arg1, String arg2) {
                  // TODO Auto-generated method stub
                  
              }
              
              @Override
              public void onMessage(String channel, String message) {
                  if(message == null) {
                      return;
                  }
                  
                  Jedis readConfigJedis = pool.getResource();
                  String config = readConfigJedis.get(message);
                  if(config == null) {
                      log.warn("Could not find any configuration with key " + message);
                      return;
                  }
                  pool.returnResource(readConfigJedis);
                  
                  listener.onConfigurationChange(config);
              }
          }, configChannel);
      }
      
      public void end() {
          if(jedis != null) {
              jedis.quit();
          }
      }
  }
}
