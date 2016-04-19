#!/usr/bin/etc python
import Understand
import Retrieval
import random
import sys
import sentiment
#for line in sys.stdin:
#    print line

def Init():
	Tree = ConstructTree()
	Template = ConstructTemplate()
	return Tree, Template


def FindCandidate(model,database, resource, input_utter, isAlltag, history,anaphora_mode, word2vec_ranking_mode, tfidfmodel=None, tfidfdict=None):
        #print "In Control tfidfmodel: "
        #print tfidfmodel
        #print 'In Control tfidfdict '
        #print tfidfdict
        word2vec = 0
        if not tfidfmodel == None and not tfidfdict == None:
                meta_info, anaphora_trigger = Understand.InfoExtractor(input_utter, resource, isAlltag, history, anaphora_mode, tfidfmodel, tfidfdict)
        else:
                meta_info, anaphora_trigger = Understand.InfoExtractor(input_utter, resource,isAlltag,history,anaphora_mode)
        #print "Understand"
        #print meta_info
        #print ""
        if meta_info.__len__()==0:
                relavance = 0
                answer = 'Can you say something longer.'.split(' ')
        else:
                Candidates, TopicLevel = Retrieval.FreqPairMatch(meta_info, database)
                #print word2vec_ranking_mode
#                print 'history'
#                print history
                #print Candidates
                relavance, answer, tag = Retrieval.Select(Candidates,history,word2vec_ranking_mode,model)
                #print "answer from ", tag
                #print 'Candidates[0][0]'
                #print Candidates[0][0]
                if Candidates:
                    if relavance != Candidates[0][0]:
                        word2vec = 1
        return relavance, answer, anaphora_trigger, word2vec
#@based on response weight
def SelectState_rel_only(policy_mode,str_rule, relavance, user_input, pre_history, TreeState, force_strategy=None):
	branch_idx = TreeState.keys()[0]
	branch = TreeState[branch_idx]['node']
        if not force_strategy == None:
            bool_idx, int_idx = force_strategy
            return TreeState[branch_idx][bool_idx][int_idx]
        if relavance >= branch['threshold_relavance']:
		#print 'we are in the h'
                return TreeState[branch_idx][True][0] # only use the continue, don't expand

	else:
            if policy_mode ==0 or  pre_history==None:
		return random.choice(TreeState[branch_idx][False][0:-1])# don't choose the last leave, go back
	    else:
                #choose this based on the previous utterances' sentiment.
                #curr =[]
                curr_1 = sentiment.get_sentiment(user_input)
                curr_2 = sentiment.get_sentiment(pre_history[-1])
                curr_3 = sentiment.get_sentiment(pre_history[-2])
                if curr_1 not in ['neg','pos','neutral']:
                    curr_1 = 'neg'
                    print user_input
#                print 'this is the previous history'
#                print curr_1
#                print curr_2
#                print curr_3
                strategy = str_rule[(curr_1,curr_2,curr_3)]
                return {'name':strategy}
                #return TreeState[branch_idx][False][2]

def SelectState(relavance, engagement, TreeState, engaged_list):
	branch_idx = TreeState.keys()[0]
	branch = TreeState[branch_idx]['node']
	if engagement >= branch['threshold_engagement']:
		return random.choice(TreeState[branch_idx][True])
	elif (engagement < branch['threshold_engagement'] ) and (len(engaged_list)==0):
		return random.choice(TreeState[branch_idx][False][0:-1]) #random selection between the tree leaves,expcet the last leave, go back
	else:
		return random.choice(TreeState[branch_idx][False])

def SelectState_rel(relavance, engagement, TreeState, engaged_list):
	branch_idx = TreeState.keys()[0]
	branch = TreeState[branch_idx]['node']
	if relavance >= branch['threshold_relavance']:
		return random.choice(TreeState[branch_idx][True])
	elif (relavance < branch['threshold_relavance'] ) and (len(engaged_list)==0):
		return random.choice(TreeState[branch_idx][False][0:-1]) #random selection between the tree leaves,expcet the last leave, go back
	else:
		return random.choice(TreeState[branch_idx][False])
def ConstructTree():
        Tree = {}
        #changed threshold relevance here from 0.2 to 0.12
        branch = {'tag':'criteria', 'name':'relavance', 'threshold_relavance':0.3, 'threshold_engagement':3}
        switch_state = {'tag':'state', 'name':'switch'}
        end_state = {'tag':'state', 'name':'end'}
        init_state = {'tag':'state', 'name':'init'} #initiate things to do
        joke_state = {'tag':'state', 'name':'joke'} #tell a joke
        back_state = {'tag':'state', 'name':'back'} #mention the high engagement point back in history
        continue_state = {'tag':'state', 'name':'continue'}
        expand_state = {'tag':'state', 'name':'expand'}
        more_state = {'tag': 'state', 'name': 'more'}
        Tree[0] = {'node':branch}
        Tree[0][True] = [continue_state, expand_state]
        Tree[0][False] = [switch_state, end_state, init_state, joke_state, more_state, back_state] # switch state here means strategy selection selection state.
        return Tree

#construct a tree based on confidence.
#def ConstructTemplate():
#        template = {}
#        template['switch'] = ['template_end', 'template_new,topic']
#        template['end'] = ['answer', 'template_open']
#        template['continue']=['answer']
#        template['expand'] = ['answer', 'template_expand']
#        return template#

# @zhou construct tree with strategy selection
def ConstructTemplate():
        template = {}
        template['switch'] = ['template_end', 'template_new,topic']
        template['init']= ['template_init']
        template['end'] = [ 'template_end','template_open']
        template['continue']=['answer']
        template['expand'] = ['answer', 'template_expand']
        template['back'] = ['template_end', 'template_back,topic_back']
        template['more'] = ['template_more']
        template['joke'] = ['template_end','template_joke']
        return template
