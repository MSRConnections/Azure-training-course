var util = require('util');
var crypto = require('crypto');

function SignatureGenerator()
{
	var self = this;

	return {
		generateServiceBusSignature: function(url, sharedAccessKeyName, sharedAccessKey, expiry) {
			var expiryEpoch = expiry instanceof Date ? expiry.getTime() : expiry;
			var data = util.format('%s\n%s', encodeURIComponent(url), expiryEpoch);

			var algorithm = crypto.createHmac('sha256', sharedAccessKey);
			algorithm.update(data);

			var signature = algorithm.digest('base64');

			var token = util.format(
				'SharedAccessSignature sr=%s&sig=%s&se=%s&skn=%s',
				encodeURIComponent(url),
				encodeURIComponent(signature),
				encodeURIComponent(expiryEpoch),
				encodeURIComponent(sharedAccessKeyName)
				);

			return token;
		}
	};
}

module.exports = new SignatureGenerator();
