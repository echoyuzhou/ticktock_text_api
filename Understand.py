#!/usr/bin/etc python

import nltk

from collections import defaultdict

from gensim import models, corpora

def AddWeight(tag_list, rules, stop_dict,isAlltag, tfidfvalues=None):
	result = []
        #print str(tag_list)
        if not tfidfvalues == None:
            for k in tfidfvalues.keys():
                print k, tfidfvalues[k]
        else:
            print "tfidf is not active"
	for token, pos in tag_list:
		if rules[pos]>0:
                        if not tfidfvalues == None:
                                if token.lower() in tfidfvalues.keys():
                                        result += [(token, pos, rules[pos] * tfidfvalues[token.lower()])]
                                else:
                                        result += [(token, pos, rules[pos])]
                        else:
			        result += [(token, pos, rules[pos])]
		else:
			if pos==".":
                            continue
			if not stop_dict[token]:
				result += [(token.lower(), pos, 1)]

        #for item in result:
         #   print item
	return result


#return [(token, pos_tag, weight)]
def InfoExtractor(utter, resource,isAlltag, history, anaphora,tfidfmodel=None, tfidfdict=None):
        #print "The following is the utter:"
        #print utter
        anaphora_trigger = 0
	rules = resource['rules']
	stop_dict = resource['stop_words']
	tag_list = nltk.pos_tag(nltk.word_tokenize(utter))
        # if there is a pronoun in the last word of the sentence, we will look into previous history of TickTock output
        if not tfidfmodel == None and not tfidfdict == None:
                token = nltk.word_tokenize(utter)
                if anaphora:
                    #print 'we are in infoExtractor in anaphora'
                    #print tag_list[-1][0]
                    #if item[] for item[0] in tag_list in ['him','her','them','it'] and history:
                    noun_list=[]
                    for tag in tag_list:
                        if tag[1] in ['PRP','PRP$'] and (tag[0].lower() not in ['you','i','we', 'my', 'me','yours','our' ]):
                            #print tag
                            if history:
                                TickTock_previous = history[-1]
                                tag_list_previous = nltk.pos_tag(nltk.word_tokenize(TickTock_previous))
                                noun_list = [item for item in tag_list_previous if item[1] in ['NN','NNS','NNP','NNPS']]
                            #print 'this is noun list'
                            #print noun_list
                    if noun_list:
                            #tag_list.append(noun_list[-1])
                            token.append(noun_list[-1][0].lower())
                            anaphora_trigger = 1
                else:
                    print "anaphra triggered, but cannot find a noun to refer to"
#                print 'these are all the token used'
#                print token
                valList = tfidfmodel[tfidfdict.doc2bow(token)]
                #valList = tfidfmodel[tfidfdict.doc2bow(utter.lower().split())] ## talk to Neil about should we use word_tokenize?
#                print "printing valList..."
#                print valList
                resDict = {}
                for tup in valList:
                    key, score = tup
                    dictKey = tfidfdict.get(key)
                    #print dictKey, score
                    if not dictKey == None:
                        resDict[dictKey] = score
                #print 'anaphora trigger'
                #print anaphora_trigger
                return AddWeight(tag_list, rules, stop_dict, isAlltag, resDict), anaphora_trigger
        return AddWeight(tag_list, rules, stop_dict,isAlltag), anaphora_trigger
