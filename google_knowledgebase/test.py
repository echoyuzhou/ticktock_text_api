"""example of Python client calling Knowledge Graph Search API."""
import fileinput
import json
import urllib

api_key = open('api_key.txt').read()
for line in fileinput.input():
    	pass
	#query = 'Football'
	query = line
	service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
	params = {
    	'query': query,
    	'limit': 10,
    	'indent': True,
    	'key': api_key,
	}
	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())
	print response
	print response['itemListElement'][0]['result']['description']
	print response['itemListElement'][0]['result']['detailedDescription']['articleBody']

#for element in response['itemListElement']:
 # print element['result']['name'] + ' (' + str(element['resultScore']) + ')'
