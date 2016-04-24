import NLG
import sentiment_vader
import random
def rl_test(sent_1,sent_2,sent_3,turn_id,q_table,theme,TemplateLib,TopicLib,Template,init_id,joke_id,more_id):
    action_list = ['switch','end','more','joke','init']
    state = (sent_1,sent_2,sent_3,turn_id)
    q_list =[]
    q_utt =[]
    for action in action_list:
        theme, utt, init_id, joke_id,more_id, engagement_input = NLG.FillTemplate(theme,TemplateLib,TopicLib,Template[action],init_id,joke_id,more_id,0,'','' )
        sent_3 = sentiment_vader.get_sentiment(utt)
        next_state = (sent_1,sent_2,sent_3,turn_id)
        q_list.append(q_table[next_state,action])
        q_utt.append(utt)
        maxQ = max(q_list)
    count = q_list.index(maxQ)
    if count>1:
        best = [i for i in range(len(action_list)) if q_list[i]==maxQ]
        i = random.choice(best)
    else:
        i = q_list.index(maxQ)
    output = q_utt[i]
    action_selected = action_list[i]
    return action_selected,output


