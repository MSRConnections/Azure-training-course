package storm.example.bolt;

import backtype.storm.tuple.Tuple;

import org.json.JSONObject;
import org.json.JSONException;

import java.util.Collections;
import java.util.List;
import java.util.HashMap;

public class RedisCountryCountBolt extends RedisBolt {

  private HashMap<String, Integer> counts;

  public RedisCountryCountBolt() {
    // This bolt will publish on the "countrycount" Redis topic
    super("countrycount");

    counts = new HashMap<String, Integer>();
  }


  @Override
  public List<Object> filter(Tuple tuple) {
    if(tuple != null) {
      // Get the count from the map
      String id = tuple.getString(0);
      Integer count = counts.get(id);
      if (count == null) {
        count = 0;
      }

      // Update the count and the count map
      count++;
      counts.put(id, count);

      // Create a JSON object representation of this tuple
      try {
        JSONObject json = new JSONObject();
        json.put("country_id", id);
        json.put("count", count);

        // Publish a string representation of the JSON object
        // to the Redis topic
        publish(json.toString());
      } catch (JSONException e) {
        throw new RuntimeException("Failed to get JSON representation");
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
