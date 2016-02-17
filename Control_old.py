#!/usr/bin/etc python

import Understand
import Retrieval
import random
import sys

#for line in sys.stdin:
#    print line

def Init():
	Tree = ConstructTree()
	Template = ConstructTemplate()
	return Tree, Template


def FindCandidate(database, resource, input_utter, history = []):
        meta_info = Understand.InfoExtractor(input_utter, resource)
        print "Understand"
        print meta_info
        print ""
        Candidates, TopicLevel = Retrieval.FreqPairMatch(meta_info, database)
        relavance, answer, tag = Retrieval.Select(Candidates)
        print "answer from ", tag
        return relavance, answer
#@based on response weight
#def SelectState(relavance, TreeState):
#	branch_idx = TreeState.keys()[0]
#	branch = TreeState[branch_idx]['node']
#	if relavance >= branch['threshold_relavance']:
#		return random.choice(TreeState[branch_idx][True]) #random selection between the tree leaves.
#	else:
#		return random.choice(TreeState[branch_idx][False])

def SelectState(relavance, engagement, TreeState, engaged_list):
	branch_idx = TreeState.keys()[0]
	branch = TreeState[branch_idx]['node']
	if engagement >= branch['threshold_engagement']:
		return random.choice(TreeState[branch_idx][True])
	elif (engagement < branch['threshold_engagement'] ) and (len(engaged_list)==0):
		return random.choice(TreeState[branch_idx][False][0:-1]) #random selection between the tree leaves,expcet the last leave, go back
	else:
		return random.choice(TreeState[branch_idx][False])

def ConstructTree():
        Tree = {}
        branch = {'tag':'criteria', 'name':'relavance', 'threshold_relavance':0.2, 'threshold_engagement':3}
        switch_state = {'tag':'state', 'name':'switch'}
        end_state = {'tag':'state', 'name':'end'}
        init_state = {'tag':'state', 'name':'init'} #initiate things to do
        joke_state = {'tag':'state', 'name':'joke'} #tell a joke
        back_state = {'tag':'state', 'name':'back'} #mention the high engagement point back in history
        continue_state = {'tag':'state', 'name':'continue'}
        expand_state = {'tag':'state', 'name':'expand'}
        Tree[0] = {'node':branch}
        Tree[0][True] = [continue_state, expand_state]
        Tree[0][False] = [switch_state, end_state, init_state, joke_state, back_state] # switch state here means strategy selection selection state.
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
        template['end'] = ['answer', 'template_open']
        template['continue']=['answer']
        template['expand'] = ['answer', 'template_expand']
        template['back'] = ['template_end', 'template_back,topic_back']
        template['joke'] = ['template_joke']
        return template