package storm.example;

import storm.example.bolt.ParseGpsDataBolt;
import storm.example.bolt.CountryIdBolt;
import storm.example.bolt.RedisCountryCountBolt;
import storm.example.bolt.RedisCoordinatesBolt;
import storm.example.spout.RandomCoordinatesSpout;

import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.tuple.Fields;

import storm.kafka.KafkaConfig;
import storm.kafka.KafkaSpout;
import storm.kafka.SpoutConfig;
import storm.kafka.HostPort;

import java.util.List;
import java.util.ArrayList;


public class KafkaGpsTopology {

    public static void main(String[] args) throws Exception {

        TopologyBuilder builder = new TopologyBuilder();

        String topic = "gps";
        int partitions = 1;
        List<HostPort> hosts = new ArrayList<HostPort>();
        hosts.add(new HostPort("127.0.0.1", 9092));

        List<String> zkHosts = new ArrayList<String>();
        zkHosts.add("127.0.0.1");

        SpoutConfig config = new SpoutConfig(
            new KafkaConfig.StaticHosts(hosts, partitions),
            topic,
            "/kafka",
            "discovery");
        config.zkServers = zkHosts;
        config.zkPort = 2181;
        config.forceStartOffsetTime(-1);

        //builder.setSpout("spout", new RandomCoordinatesSpout());
        builder.setSpout("spout", new KafkaSpout(config));
        builder.setBolt("parser", new ParseGpsDataBolt())
                  .shuffleGrouping("spout");
        builder.setBolt("coordinates", new RedisCoordinatesBolt())
                  .shuffleGrouping("parser");
        builder.setBolt("countryid", new CountryIdBolt())
                  .shuffleGrouping("parser");
        builder.setBolt("countrycount", new RedisCountryCountBolt())
                  .fieldsGrouping("countryid", new Fields("country_id"));

        Config conf = new Config();
        conf.setDebug(true);

        if(args != null && args.length > 0) {
            conf.setNumWorkers(3);
            StormSubmitter.submitTopology(args[0], conf, builder.createTopology());
        } else {
            LocalCluster cluster = new LocalCluster();
            cluster.submitTopology("kafka-gps", conf, builder.createTopology());
        }
    }
}
