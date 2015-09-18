# Shared Access Signature Generator for Node.js

This package allows you to easily generate a Shared Access Signature for use in REST API calls to Microsoft Azure services. Currently the package generates signatures that are suitable for use with Azure Service Bus (includng Event Hubs).

## Why?

If you are working with Azure you might be wondering why this package exists given that there are already some Node.js packages. My reasoning is that I was working with some smaller embedded platforms which didn't support some of the packages that Microsoft's own package relied on, so this way I can have tighter control of the dependencies and a very simple package.

## Usage

Using the package is easy. Just download and install it via NPM.

```sh
npm install shared-access-signature
```

Once the package is downloaded and installed you can call it by requiring in the ```shared-access-signature``` package and calling the ```generateServiceBusSignature(url, sharedAccessKeyName, sharedAccessKey, expirty)``` method.

```js
var sas = require('shared-access-signature');

var url = 'https://namespace.servicebus.windows.net/hubname/publishers/devicename/messages';
var sharedAccessKeyName = 'sample-key';
var sharedAccessKey = 'S4lxDeOkdGFgi7xbIVdBakWpxDaPitKsGFUPFxZKT14=';
var currentDate = new Date();
var expiry = currentDate.getTime() + 3600;

var sas = require('shared-access-signature');
var signature = sas.generateServiceBusSignature(url, sharedAccessKeyName, sharedAccessKey, expiry);
console.log(signature);
```

The expiry parameter can also take a Date object which is helpful, I recommend checking out the awesome [momentjs](http://momentjs.com/) library to deal with dates and quickly generate Date objects projected into the future.

```js
...
var moment = require('moment');
var expiry = moment().add(1, 'day').toDate();
var signature = sas.generateServiceBusSignature(url, sharedAccessKeyName, sharedAccessKey, expiry);
```

## Contributions
If you find any bugs or would like to see a feature fork the code and submit a pull request, otherwise raise and issue.
