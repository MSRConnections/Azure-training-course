var url = 'https://tessel-atg.servicebus.windows.net/tessel-atg-tenant1/publishers/tessel-atg-tenant1-device1/messages';
console.log('url: %s', url);

var sharedAccessKeyName = 'tessel-atg-tenant1-policy1';
console.log('sharedAccessKeyName: %s', sharedAccessKeyName);

var sharedAccessKey = '54TnnQr9GH37TZzQziLOVsDCgxC6outsbWuNhFKMP7E=';
console.log('sharedAccessKey: %s', sharedAccessKey);

var expiry = new Date(1454612852);
console.log('expiry: %s', expiry);

var sas = require('../index');
console.log(sas);

var signature = sas.generateServiceBusSignature(url, sharedAccessKeyName, sharedAccessKey, expiry);
console.log('signature: %s', signature);
