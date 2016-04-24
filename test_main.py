import test_function
theme = {}
theme['a'] = 'movies'
theme_new = test_function.theme_check(theme)
print 'theme_new:' +theme_new['a'] +'\n'
print 'theme:' + theme['a'] +'\n'
