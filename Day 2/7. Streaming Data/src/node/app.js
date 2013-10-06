var express = require('express')
  , redis = require('redis');

var app = express()
  , http = require('http')
  , server = http.createServer(app)
  , io = require('socket.io').listen(server);

var topics = redis.createClient();
topics.subscribe("countrycount");
topics.subscribe("coordinates");

var static_dirs = [ 'js', 'css', 'img', 'data' ];
for (var i=0; i<static_dirs.length; i++) {
  var static_path = '/' + static_dirs[i];
  app.use(static_path, express.static(__dirname + static_path));
}

var port = process.env.PORT || 80;
server.listen(port, function() {
  console.log("Listening on port " + port);
});

app.get('/', function (req, res) {
  res.sendfile(__dirname + '/index.html');
});

app.get('/kafka-gps-client-0.0.1-SNAPSHOT-standalone.jar', function (req, res) {
  res.download(__dirname + '/kafka-gps-client-0.0.1-SNAPSHOT-standalone.jar');
});

io.sockets.on('connection', function (socket) {
  topics.on('message', function(channel, message) {
    socket.emit(channel, message);
  });
});

