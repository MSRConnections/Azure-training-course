package storm.example.bolt;

import backtype.storm.topology.base.BaseBasicBolt;
import backtype.storm.topology.BasicOutputCollector;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;
import backtype.storm.topology.OutputFieldsDeclarer;

import org.mapfish.geo.MfFeature;
import org.mapfish.geo.MfFeatureCollection;
import org.mapfish.geo.MfGeometry;
import org.mapfish.geo.MfGeoFactory;
import org.mapfish.geo.MfGeoJSONReader;

import com.vividsolutions.jts.geom.Geometry;
import com.vividsolutions.jts.geom.GeometryFactory;
import com.vividsolutions.jts.geom.Point;
import com.vividsolutions.jts.geom.Coordinate;

import org.json.JSONObject;
import org.json.JSONWriter;
import org.json.JSONException;

import org.apache.commons.io.IOUtils;
import org.apache.log4j.Logger;

import java.io.Serializable;
import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Collection;

public class ParseCarDataBolt extends BaseBasicBolt {

  private static org.apache.log4j.Logger log = Logger.getLogger(ParseCarDataBolt.class);

  public void execute(Tuple tuple, BasicOutputCollector collector) {
    if (tuple.contains("bytes")) {
      byte[] valueBytes = (byte[])tuple.getValueByField("bytes");
      String valueStr = new String(valueBytes);
      System.out.println("ParseCarDataBolt value : " + valueStr);
      String[] coords = valueStr.split(":");
      try {
    	  int speed = Integer.parseInt(coords[0]);
    	  int rpm = Integer.parseInt(coords[1]);
    	  int temperature = Integer.parseInt(coords[2]);
	  String gear = coords[3];
	  String lat = coords[4];
	  String lon = coords[5];
    	  collector.emit(new Values(speed, rpm, temperature, gear, lat, lon));
      } catch (IndexOutOfBoundsException err) {
        log.error("Expected: <speed>:<rpm>:<temperature>:<gear>, Received: " + valueStr);
      } catch (NumberFormatException err) {
        log.error("Invalid number format: " + valueStr);
      }
    } else {
      log.fatal("Unknown Car data format: field 'bytes' not in tuple");
    }
  }

  public void declareOutputFields(OutputFieldsDeclarer declarer) {
    declarer.declare(new Fields("speed", "rpm","temperature","gear", "lat", "lon"));
  }

}
