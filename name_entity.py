# this is to detect the name entity of a sentence, the return value [['New York'],[Pittsburgh]]
import nltk
#import fileinput
import json
import urllib
def find_NE(t,name_entity): # only return the first NE found, will ignore the rest
    try:
        t.label()
    except AttributeError:
        #print t
        return None
    else:
        # now we know that t.node is defined
        if t.label() == 'NE':
         #   print 'this is the NE'
         #   print [item[0] for item in t]
            name_entity.append( [item[0] for item in t])
        else:
            for child in t:
                find_NE(child,name_entity)
    return name_entity
def name_entity_detection(user_input):
        sent_token = nltk.word_tokenize(user_input)
        sent_postag = nltk.pos_tag(sent_token)
        sent_tree = nltk.ne_chunk(sent_postag,binary=True)
        #print sent_tree
        ne = find_NE(sent_tree,[])
        #print 'this is the name entity'
        #print ne
        if ne:
         #   print ne[0][0]
         #   print sent_token[0]
            if ne[0][0]==sent_token[0]:
          #      print 'it is the first word'
                return []
            else:
          #      print 'this is return the list'
                return ne

def NE_kb(name_entity_list):
    api_key = 'AIzaSyA_MGutOdKJTwhq0iVn7TBPfOYJbrDcfG8'
    response_disp_list =[]
    for item in name_entity_list:
	#query = 'Football'
	query = item
        #print query
	service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
	params = {
    	'query': query,
    	'limit': 10,
    	'indent': True,
    	'key': api_key,
	}
	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())
	#print response
        try:
            disp = response['itemListElement'][0]['result']['description']
            response_disp_list.append(disp)
        except:
            response_disp_list =[]
        #print response['itemListElement'][0]['result']['detailedDescription']['articleBody']
    return response_disp_list
#
def name_entity_generation(name_entity_list, response_disp_list):
# we only talk about the first name entity
    response = response_disp_list[0]
    name = name_entity_list[0]
    #if type(name) is 'list':
    name_al = ' '.join(name)
    output = 'Are you talking about '+ name_al + ', the ' +response
    return output

