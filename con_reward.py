import readall
import nltk
def con_reward(conv):
# this can be updated, with different overall metric for conversation. such as user_reported engagement, conversational depth. information gain.
#this version, we name it conversation information gain, which is the number of unique words.
    word_set = []
    for utt in conv:
        word_set = word_set+nltk.word_tokenize(utt)
    word_set = list(set(word_set))
    return len(word_set)


