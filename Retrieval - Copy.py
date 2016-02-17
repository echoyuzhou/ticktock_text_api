#!/usr/bin/env python

"""
find answer in database and by search engine
"""
import random
from collections import defaultdict

#penalize too long sentence/ low relavance
def Select(Candidates):
    threshold = 50
    answer_list = []
    answer_strings = []

    print "Candidates for select ", Candidates

    fileout = open('60question.txt', 'a') ## only for the use of retrieval_question
    for i in range(0, 3):
        fileout.write(' '.join(Candidates[i][1]))
        fileout.write(' '.join(Candidates[i][2])+'\n')
    fileout.write('\n')
    fileout.close
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
        return random.choice(answer_list)
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
                for token in utter:
                        if occur_dict[token]:
                                score += info_dict[token][1]    #weight
                score = float(score)/(len(info)+len(utter))
                if score > 0:
                        Candidate = UpdateCandidatePair(idx, database, score, Candidate, select, 'Q')

	for idx, utter in database['A'].items():
                score = 0
                for token in utter:
                        if occur_dict[token]:
                                score += info_dict[token][1]    #weight
                score = 0.8*float(score)/(len(info)+len(utter))
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

