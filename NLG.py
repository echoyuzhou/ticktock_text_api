#!/usr/bin/env python

import random
#import galbackend_cnn
def GenerateResponsePair(TopicLevel, Candidates, refine_strategy=-1):
        if TopicLevel==-1: #off topic
                output = 'Ok. Tell me more about yourself.'
        else:
		select = random.choice(Candidates)
		pair = [select[1], select[2]]
                output = [" ".join(pair[0]), " ".join(pair[1])]

        return output

def FillTemplate(theme, TemplateLib, TopicLib, template, init_id, joke_id,more_id, engaged_input, answer=[],output=[]):
    #global topic_id,init_id,joke_id,more_
    sent_list = []
    for item in template:
        for unit in item.split(','):
            #print 'this is the unit' +unit
            if unit == 'oov' or unit =='name_entity' or unit =='short_answer' or unit =='not_repeat':
                sent_list.append(output)
            elif unit == 'answer':
                output = ' '.join(answer)
                punc_list = [".",",","?","'","!"]
                for punc in punc_list:
                    if punc in output:
                        output = output.replace(' '+punc,punc)
                sent_list.append(output)
            elif unit == 'template_back' and len(engaged_input)<1:
                continue
            elif unit == 'topic_back':
                if len(engaged_input)>0:
                    sent_list.append(engaged_input[0])
                    sent_list.append('do you want to talk more about that?')
                    engaged_input.pop(0)
                else:
                    unit = random.choice(['joke','init','switch'])
            elif unit == 'topic':
		#print topic_id
                topic_list  = [topic for topic in TopicLib if topic != theme]
                #print topic_list
                #print 'theme' +theme +'\n'
                theme = random.choice(topic_list)
                sent_list.append(theme)
            elif unit == 'template_init':
                #print TemplateLib['template_init']
# here we use initiation that is attached to certain topic.
		init_index = init_id %len(TemplateLib['template_init'][theme])
                sent_list.append(TemplateLib['template_init'][theme][init_index])
		init_id = init_id + 1
	    elif unit == 'template_joke':
# we use joke that is attached to certain topic.
                #print 'The theme is ' + theme
		#print TemplateLib['template_joke']
                joke_index = joke_id%len(TemplateLib['template_joke'][theme])
		sent_list.append(TemplateLib['template_joke'][theme][joke_index])
		joke_id = joke_id + 1
            elif unit == 'template_more':
                more_index = more_id%len(TemplateLib['template_more'])
                sent_list.append(TemplateLib['template_more'][more_index])
                more_id = more_id + 1
	    else:
		sent_list.append(random.choice(TemplateLib[unit]))
    #pr
    return theme, ' '.join(sent_list), init_id, joke_id, more_id, engaged_input
