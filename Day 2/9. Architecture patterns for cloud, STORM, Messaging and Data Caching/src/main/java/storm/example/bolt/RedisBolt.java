package storm.example.bolt;

import java.util.List;
import java.util.Map;

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

/**
 * This abstract bolt class will help publishing the bolt processing into
 * a redis pubsub channel
 * @author arcturus@ardeenelinfierno.com
 *
 */
public abstract class RedisBolt extends BaseRichBolt {
    
    protected String channel;
    protected String configChannel;
    protected OutputCollector collector;
    protected Tuple currentTuple;
    protected Logger log;
    protected JedisPool pool;
    protected ConfigListenerThread configListenerThread;

    public interface OnDynamicConfigurationListener {
        public void onConfigurationChange(String conf);
    }

    public RedisBolt(String channel) {
        this.channel = channel;
        configChannel = "config_update_" + channel;
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

    public abstract List<Object> filter(Tuple tuple);

    public void publish(String msg) {
        Jedis jedis = pool.getResource();
        jedis.publish(channel, msg);
        pool.returnResource(jedis);
    }

    protected void setupNonSerializableAttributes() {

    }

    /**
     * Will create a new thread (carefull, if you specify a multiplicity of 3
     * for this bolt, you will create 3 new threads). That will listen to a 
     * redis pubsub channel, when ever a message is sent to that channel,
     * will read the key with the specific name in the message and pass it to the
     * onConfiguration function.
     */
    protected void setupDynamicConfiguration(final OnDynamicConfigurationListener listener) {
        configListenerThread = new ConfigListenerThread(listener);
        configListenerThread.start();
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
