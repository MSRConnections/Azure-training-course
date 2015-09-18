var sas = require('shared-access-signature');

ask("Azure Event Hub URL", function (url) {
    ask("Policy name", function (policy) {
        ask("Policy key", function (key) {
            var expiry = new Date(new Date().getTime() + 10 * 24 * 60 * 60 * 1000); // 10 days hence
            var signature = sas.generateServiceBusSignature(url, policy, key, expiry);
            console.log("");
            console.log(signature);
            console.log("");
            process.exit();
        });
    });
});

function ask(question, callback) {
    var stdin = process.stdin
    var stdout = process.stdout;

    stdin.resume();
    stdout.write(question + ": ");

    stdin.once('data', function(data) {
        data = data.toString().trim();
 
        if (data.length > 0) {
            callback(data);
        } else {
            ask(question, callback);
        }
    });
}
