#!/usr/bin/etc python

import nltk

from collections import defaultdict

from gensim import models, corpora

def AddWeight(tag_list, rules, stop_dict,isAlltag, tfidfvalues=None):
	result = []
        print str(tag_list)
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

        for item in result:
            print item
	return result


#return [(token, pos_tag, weight)]
def InfoExtractor(utter, resource,isAlltag, history, tfidfmodel=None, tfidfdict=None):
        print "The following is the utter:"
        print utter
	rules = resource['rules']
	stop_dict = resource['stop_words']
	tag_list = nltk.pos_tag(nltk.word_tokenize(utter))
        # if there is a pronoun in the last word of the sentence, we will look into previous history of TickTock output
        if tag_list[-1][0]in ['him','her','them','it']:
            if history:
                print "anaphra triggered"
                TickTock_previous = history.pop()
                tag_list_previous = nltk.pos_tag(nltk.word_tokenize(TickTock_previous))
                noun_list = [item for item in tag_list_previous if item[1] in ['NN','NNS','NNP','NNPS']]
                if noun_list:
                    tag_list.append(noun_list[-1])
                    print "anaphra triggered, but cannot find a noun to refer to"

        if not tfidfmodel == None and not tfidfdict == None:
                valList = tfidfmodel[tfidfdict.doc2bow(utter.lower().split())]
                print "printing valList..."
                print valList
                resDict = {}
                for tup in valList:
                    key, score = tup
                    dictKey = tfidfdict.get(key)
                    print dictKey, score
                    if not dictKey == None:
                        resDict[dictKey] = score
                return AddWeight(tag_list, rules, stop_dict, isAlltag, resDict)
	return AddWeight(tag_list, rules, stop_dict,isAlltag)

