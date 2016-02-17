"""example of Python client calling Knowledge Graph Search API."""
import fileinput
import json
import urllib
#api_key = open('api_key.txt').read()
def NE_disp(name_entity_list):
    api_key = 'AIzaSyA_MGutOdKJTwhq0iVn7TBPfOYJbrDcfG8'
    response_disp_list =[]
    for item in name_entity_list:
	#query = 'Football'
	query = item
        print query
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
	disp = response['itemListElement'][0]['result']['description']
        response_disp_list.append(disp)
        print response['itemListElement'][0]['result']['detailedDescription']['articleBody']
    return response_disp_list
#for element in response['itemListElement']:
 # print element['result']['name'] + ' (' + str(element['resultScore']) + ')'
