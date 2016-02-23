#!/usr/bin/env python

"""
find answer in database and by search engine
"""
import random
from collections import defaultdict

#penalize too long sentence/ low relavance
def Select(Candidates,history,word2vec_ranking_mode):
    threshold = 50
    answer_list = []
    answer_strings = []

    print "Candidates for select "
    ids =1
    for Candidate in Candidates:
        print "Ids ", ids
        print "weight: ", Candidate[0]
        print "Question: ", Candidate[1]
        print "Answer: ", Candidate[2]
        print "Matched Q or A: ", Candidate[3]
        ids=ids+1
    print "================="
    candidate_range = min(len(Candidates),3)
    for score, question, answer, tag in Candidates:
        if len(answer) > threshold:
            continue
        astring = " ".join(answer)
        if astring.find('--')!=-1 or astring.find(':')!=-1:
            continue
        if astring in answer_strings:
            continue
        answer_strings.append(astring)
        answer_list += [(score, answer, tag)]
    if len(answer_list) > 0:
        #return random.choice(answer_list)
        if word2vec_ranking_mode==1 and history:
            print 'the word2vec_ranking_mode is triggered'
            # based on how similar the previous TickTock utterance to choose
            import gensim
            from sklearn.metrics.pairwise import cosine_similarity
            model = gensim.models.Doc2Vec.load('/tmp/doc2vec_50')
            ticktock_pre = model[history.pop()]
            big_score = -1
            for score, question, answer,tag in Candidates:
                array = model[answer]
                answer_score = cosine_similarity(array,ticktock_pre)
                if big_score < answer_score:
                    answer_chosen = answer
                    big_score = answer_score
            print 'this is the big score'
            print big_score
            return answer_chosen
        else:
            return answer_list[0]
    else:
        return (0, [], '')
def FreqPairMatch(info, database, select=5):
        occur_dict = defaultdict(bool)
        occur_dict.clear()
        info_dict = {}
        for word, pos, weight in info:
                occur_dict[word] = True
                info_dict[word] = (pos, weight)

        Candidate = []
        for idx, utter in database['Q'].items():
                score = 0
                match = 0
                for token in set(utter):
                        if occur_dict[token.lower()]:
                                score += info_dict[token.lower()][1] #weight
                                match += 1
                score = float(score)/(len(utter)+1)* match/(len(info))
                if score > 0:
                        Candidate = UpdateCandidatePair(idx, database, score, Candidate, select, 'Q')

	for idx, utter in database['A'].items():
                score = 0
                for token in utter:
                        if occur_dict[token]:
                                score += info_dict[token][1]    #weight
                score = 0.8*float(score)/(len(utter)+1)* match/len(info)
                if score > 0:
                        Candidate = UpdateCandidatePair(idx, database, score, Candidate, select, 'A')

        if len(Candidate)>0:
                topiclevel = 1
        else:
                topiclevel = -1

        return Candidate, topiclevel

def UpdateCandidatePair(idx, database, score, Candidate, select, tag):
        add = False
        if len(Candidate) < select:
                Candidate += [(score, database['Q'][idx], database['A'][idx], tag)]
                add = True
        else:
                if score > Candidate[select-1][0]:
                        Candidate[select-1] = (score, database['Q'][idx], database['A'][idx], tag)
                        add = True
        if add:
                return sorted(Candidate, key=lambda item:item[0], reverse=True)
        else:
                return Candidate


