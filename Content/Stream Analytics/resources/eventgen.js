///////////////// KEY VARS /////////////////
var sas = "SharedAccessSignature sr=https%3A%2F%2Fstreamanalytics-lab.servicebus.windows.net%2Finputhub&sig=XZGiM%2BOqgpGkWE14w%2FIFwWVFbz4yjKTKsRhz55SjMBU%3D&se=1520964512.624&skn=SendPolicy";
var uri = "https://streamanalytics-lab.servicebus.windows.net/inputhub";
///////////////////////////////////////////

var request = require("request");
uri = uri + "/messages";

var probability = 0.01;     // Probability of fraudulent transaction
var transactions = 0;       // Number of transactions executed
var cardNumber;             // Fraudulent card number

// Simulate a transaction; if successful, function is called
// recursively to simulate additional transactions
send();

function send() {
    var transaction = {
        transactionId: 1000 + transactions++,
        transactionTime: (new Date()).toUTCString(),
        deviceId: 12345 + Math.floor(Math.random() * 88888),
        cardNumber: 123456789 + Math.floor(Math.random() * 888888888),
        amount: Math.ceil((Math.random()) * 20) * 20
    };

    // Occasionally record a card number for later use in generating fraud
    if (Math.random() < probability) {
        cardNumber = transaction.cardNumber;
    }

    // Occasionally generate a fraudulent transaction by reusing a card number
    if (Math.random() < probability && cardNumber != null) {
        transaction.cardNumber = cardNumber;
        cardNumber = null;
    }

    request({
        headers: {
            "Authorization": sas,
            "Content-Type": "application/atom+xml;type=entry;charset=utf-8"
        },
        url: uri,
        method: "POST",
        json: true,
        body: transaction
    }, function (error, response, body) {
        if (error) {
            console.log(error);
        }
        else {
            console.log("[" + transaction.transactionId + "] Event sent (status code: " + response.statusCode + ")");

            if (response.statusCode < 400) {
                send(); // Call recursively if request was successful
            }
            else {
                console.log("*** Event failed with status code " + response.statusCode + " ***");
            }
        }
    });
}