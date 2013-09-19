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

public class ParseGpsDataBolt extends BaseBasicBolt {

  private static org.apache.log4j.Logger log = Logger.getLogger(ParseGpsDataBolt.class);

  private double convertCoord(String coordStr, double min, double max) {
    double coord = Double.parseDouble(coordStr);
    if (coord < min) {
      double bad = coord;
      coord = coord % min;
      log.warn("Invalid coordinate "+bad+" corrected to "+coord);
    } else if (coord > max) {
      double bad = coord;
      coord = coord % max;
      log.warn("Invalid coordinate "+bad+" corrected to "+coord);
    }
    return coord;
  }

  @Override
  public void execute(Tuple tuple, BasicOutputCollector collector) {
    if (tuple.contains("bytes")) {
      byte[] valueBytes = (byte[])tuple.getValueByField("bytes");
      String valueStr = new String(valueBytes);
      String[] coords = valueStr.split(":");
      try {
        double lat = convertCoord(coords[0], -90, 90);
        double lon = convertCoord(coords[1], -180, 180);
        collector.emit(new Values(lat, lon));
      } catch (IndexOutOfBoundsException err) {
        log.error("Expected: <lat>:<lon>, Received: " + valueStr);
      } catch (NumberFormatException err) {
        log.error("Invalid number format: " + valueStr);
      }
    } else {
      log.fatal("Unknown GPS data format: field 'bytes' not in tuple");
    }
  }

  @Override
  public void declareOutputFields(OutputFieldsDeclarer declarer) {
    declarer.declare(new Fields("lat", "lon"));
  }

}
