import galbackend_online
old_theme = 'movies'
theme = {'100':old_theme}
galbackend_online.InitLogging()
galbackend_online.InitResource('v4')
theme_new, strategy, response,previous_history_new,word2vec = galbackend_online.get_response('switch',1,'test', '100', {'100':['a']},theme)
print theme
