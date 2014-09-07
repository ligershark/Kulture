
function GetPackagesStartWith(startsWith,host,port){
	// curl 'http://www.nuget.org/api/v2/Packages?&includePrerelease=true&$filter=startswith%28Id,%20%27Microsoft%27%29%20eq%20true'
	host = host || 'www.myget.org';
	port = port || 80;

	host = host.toLowerCase();

	path = '/api/v2/Packages?includePrerelease=true&$select=Id,Version&$filter=startswith%28Id,%20%27'+startsWith+'%27%29%20eq%20true';

	if(host.localeCompare('www.myget.org')==0){
		path = '/F/aspnetmaster' + path	
	}
	console.log('host: '+host);
	console.log('path: '+path);

	var options = {
		host: host,
		port: port,
		path: path,
		headers: {
          accept: 'application/json'
      }
	}

	var http = require('http');
	var req = http.get(options, function(resp){
	  resp.setEncoding('utf8');
	  resp.on('data', function(chunk){
	    console.log(chunk);
	  });
	})

	req.on("error", function(e){
	  console.log("Got error: " + e.message);
	});


	req.end();	
}

function GetAllPackageNames(host,port,uriPrefix,callback){
	var request = require('request');
	uriPrefix = uriPrefix || 'http://www.nuget.org/api/v2/'
	
	var uri = uriPrefix+'Packages()?$select=Id&includePrerelease=true';
	var options = {
		uri : uri,
		method : "GET",
		timeout : 1000,
		headers: {
          accept: 'application/json'
      }
	};

	var allPackageNames = [];
	var respHasNextLink = false;
	var nextLink = uri;
	var counter = 0;
	var sleep = require('sleep');
	var underscore = require('underscore');
	var maxNumErrors = 100;
	var numErrors = 0;

	var continueGettingPkgNames = function(uri,callback){
		counter++;
		options.uri = uri;
		var cReq = request(options,function(cError,cResponse,cBody){
			if(cResponse != null){
				cResponse.setEncoding('utf8');
			}

			if(cError){
				if(numErrors++ > maxNumErrors){
					console.error('too many errors, stopping.');
					console.log('making pkg names unique: '+allPackageNames.length);
					allPackageNames = underscore.uniq(allPackageNames);
					console.log('finished: '+allPackageNames.length);
					console.log('uri: '+uri);
				}
				else{
					console.error('************************* ERROR ******************************');
					console.error(cError);
					// sleep to slow down the number of requests for a bit
					sleep.sleep(1);
					continueGettingPkgNames(uri,callback);
				}
			}
			else if(cBody!=null){
				var cJsonBody = JSON.parse(cBody);
				var cNames = GetPackageNamesFromJson(cBody);
				for(var i=0;i<cNames.length;i++){
					var cPkgName = cNames[i];
					allPackageNames.push(cPkgName);
				}

				if(counter % 25 == 0){
					console.log(allPackageNames.length);
				}
				var cNextLink = GetJsonResponseNextLink(cJsonBody);

				if(cNextLink != null){
					continueGettingPkgNames(cNextLink,callback);
				}
				else{
					console.log('making pkg names unique: '+allPackageNames.length);
					allPackageNames = underscore.uniq(allPackageNames);
					console.log('finished: '+allPackageNames.length);
					callback(allPackageNames);
				}

			}
			else{
				console.log('******body is null');
			}
		}).end();
	};

	continueGettingPkgNames(uri,callback);
}

function GetJsonResponseNextLink(jsonObj){
	var nextLink = null;
	if(jsonObj['d'].__next){
		nextLink = jsonObj['d'].__next
	}

	return nextLink;
}

function GetPackageNamesFromJson(response){
	var util = require('util');
	var underscore = require('underscore');
	var jsonObj = JSON.parse(response);
	var results = jsonObj['d'].results;	
	var numResults = results.length;
	var pkgNames = [];

	for(var i = 0; i<numResults;i++){
		name = jsonObj['d'].results[i]['Id'];
		if(pkgNames.indexOf(name)<=0){
			pkgNames.push(name);	
		}
	}
	if(pkgNames == null || pkgNames.length<=0){
		console.log('empty pkg names for: '+response);
	}
	return underscore.uniq(pkgNames);
}

var fs = require('fs');
var outputFilename = '~/temp/package-names.txt';

GetAllPackageNames(null,null,'http://www.myget.org/F/aspnetmaster/api/v2/',function(allNamesMyGet){
	console.log('completed download from myget, now starting nuget download.');

	GetAllPackageNames(null,null,'http://www.nuget.org/api/v2/',function(allNamesNuGet){
		namesToWrite = []
		namesToWrite.push(allNamesNuGet)
		namesToWrite.push(allNamesMyGet)
		
		var wstream = fs.createWriteStream(outputFilename);
		for(var i = 0;i<allNamesMyGet.length;i++){
			wstream.write(allNamesMyGet[i]);
			wstream.write('\n');
		}
		for(var i = 0;i<allNamesNuGet.length;i++){
			wstream.write(allNamesNuGet[i]);
			wstream.write('\n');
		}
	});
});