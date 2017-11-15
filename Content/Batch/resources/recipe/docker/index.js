var azure = require('azure-storage');
var fs = require('fs');
var child_process = require('child_process');
var path = require('path');

var connStr = process.env.AZ_STORE_CONN_STR

var fileService = azure.createFileService(connStr);

fileService.createShareIfNotExists('myfileshare', function(error, result, response) {
	if (!error) {
		
		var processFile = function(){
			fileService.listFilesAndDirectoriesSegmented('myfileshare', 'textfiles', null, function(error, result, response){
				//console.log(result.entries.files);
				if (result.entries.files.length > 0){
					var fileName = result.entries.files[0].name;
					console.log("Processing: " + fileName);
					var writable = fs.createWriteStream(fileName);
					fileService.createReadStream('myfileshare', 'textfiles', fileName, function(){
						fileService.deleteFileIfExists('myfileshare', 'textfiles', fileName, function(){
							var fileBaseName = path.basename(fileName, '.txt');
							var cmd = 'espeak --stdout -f "' + fileName + '" > "' + fileBaseName + '.wav"'
							console.log(cmd);
							console.log(child_process.execSync(cmd));
							var cmd = 'oggenc -q 6 "'  + fileBaseName + '.wav" -o "'  + fileBaseName + '.ogg"'
							console.log(cmd);
							console.log(child_process.execSync(cmd));
							fileService.createFileFromLocalFile('myfileshare', '', fileBaseName + '.ogg', fileBaseName + '.ogg', function(error, result, response){
								console.log(result);
								processFile();
							})
						})
					}).pipe(writable);
				}
			})			
		}
		processFile();
	}
});