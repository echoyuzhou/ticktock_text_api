from nltk.sentiment import vader
def get_sentiment(response):
    processed_response = response.replace('"','')
    if vader.negated(processed_response):
        sentiment = 'neg'
        return 'neg'
    sent = vader.SentimentIntensityAnalyzer()
    score = sent.polarity_scores(processed_response)
    sent_list = ['neg','neutral','pos']
    neg = score['neg']
    neutral = score['neu']
    pos = score['pos']
    sent_score = [neg,neutral,pos]
    big_score = max(sent_score)
    index = sent_score.index(big_score)
    sentiment = sent_list[index]
    return sentiment
