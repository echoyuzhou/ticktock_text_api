import galbackend_online
import sentiment
galbackend_online.InitLogging()
galbackend_online.InitResource('v4')
while True:
    user_id = 'a'
    history = {user_id : ['aa','bb']}
    theme = {user_id: 'movies'}
    theme, strategy,utt,previous_history, word2vec = galbackend_online.get_response('joke',1,'joke_joke',user_id,history,theme)
    print utt
    sent = sentiment.get_sentiment(utt)
    print sent
    if sent not in ['pos','neg','neutral']:
        break
