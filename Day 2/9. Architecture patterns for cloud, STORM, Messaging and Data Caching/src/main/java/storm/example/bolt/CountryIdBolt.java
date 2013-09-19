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

import java.io.Serializable;
import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Collection;

public class CountryIdBolt extends BaseBasicBolt {

  private class Feature extends MfFeature implements Serializable {
    private final String id;
    private final MfGeometry geometry;

    // Note: JSONObject is not serializable
    public Feature(String id, MfGeometry geometry, JSONObject unused) {
      this.id = id;
      this.geometry = geometry;
    }

    public String getFeatureId() {
      return id;
    }

    public MfGeometry getMfGeometry() {
      return geometry;
    }

    public void toJSON(JSONWriter builder) throws JSONException {
      throw new RuntimeException("Not Implemented");
    }
  }

  private GeometryFactory geomFactory;
  private MfFeatureCollection countries;

  public CountryIdBolt() throws Exception {
    geomFactory = new GeometryFactory();

    MfGeoJSONReader reader = new MfGeoJSONReader(
        new MfGeoFactory() {
          public MfFeature createFeature(String id, MfGeometry geometry, JSONObject properties) {
            return new Feature(id, geometry, properties);
          }
        });
    String jsonString = IOUtils.toString(getClass().getResourceAsStream("/world-countries.json"));
    countries = (MfFeatureCollection)reader.decode(jsonString);
  }


  @Override
  public void execute(Tuple tuple, BasicOutputCollector collector) {
    String id = null;
    double lat = tuple.getDouble(0);
    double lon = tuple.getDouble(1);
    Point pin = geomFactory.createPoint(new Coordinate(lon, lat));

    for(MfFeature country: countries.getCollection()) {
      Geometry geom = country.getMfGeometry().getInternalGeometry();
      if (geom.contains(pin)) {
        id = country.getFeatureId();
        break;
      }
    }

    if (id != null) {
      // Emit an anchored tuple
      // See: https://github.com/nathanmarz/storm/wiki/Guaranteeing-message-processing
      collector.emit(new Values(id));
    }
    // Bolt extends BaseBasicBolt so tuple is automatically ack'ed
  }

  @Override
  public void declareOutputFields(OutputFieldsDeclarer declarer) {
    declarer.declare(new Fields("country_id"));
  }

}
