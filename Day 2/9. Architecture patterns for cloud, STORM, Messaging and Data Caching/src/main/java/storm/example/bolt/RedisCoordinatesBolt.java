package storm.example.bolt;

import backtype.storm.tuple.Tuple;

import org.json.JSONObject;
import org.json.JSONException;

import java.util.List;
import java.util.Collections;


public class RedisCoordinatesBolt extends RedisBolt {

  public RedisCoordinatesBolt() {
    // This bolt will publish on the "coordinates" Redis topic
    super("coordinates");
  }

  @Override
  public List<Object> filter(Tuple tuple) {
    if(tuple != null) {

      try {
        // Build a JSON object representation of these coordinates
        JSONObject json = new JSONObject();
        json.put("lat", tuple.getDouble(0));
        json.put("lon", tuple.getDouble(1));

        // Publish a string representation of the JSON object
        // to the Redis topic
        publish(json.toString());
      } catch (JSONException e) {
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

}
