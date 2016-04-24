import readall
import nltk
import sklearn
from sklearn import preprocessing
import numpy as np
import pickle
import data_prepare_breakdown
import readall
import gensim
import depth_rater_features
def con_reward(conv,dic):
# this can be updated, with different overall metric for conversation. such as user_reported engagement, conversational depth. information gain.
#this version, we name it conversation information gain, which is the number of unique words.
    #pickle.dump((conv,dic),open('conv_test.pkl','w'))
    word_set = []
    X_train, scaler,clf = pickle.load(open('breakdown_detector.pkl'))
    utt_vec = []
    length_vec =[]
    model = gensim.models.Word2Vec.load('/tmp/word2vec_100_break')
    x_depth, scaler_depth,clf_depth = pickle.load(open('depth_rater.pkl'))
    id = 0
    utt_pre = []
    length_pre = 0
    for utt in conv:
        tokens = nltk.word_tokenize(utt)
        word_set = word_set+tokens
    word_set = list(set(word_set))
    info_gain = len(word_set)
    sent, length = data_prepare_breakdown.extract_word2vec_length({'junk':conv},dic)
    data_test = np.hstack((sent['data'],length['data']))
    data_test = scaler.transform(data_test)
    value = clf.predict(data_test)
    app_value = sum(value)*20
    print 'app_value: '+ str(app_value)
    feature_list = []
    turns =[]
    for key in conv["Turns"]:
        turns.append(conv["Turns"][key])
    feature_list.append(depth_rater_features.extract_features(turns))
    feature_test = scaler_depth.transform(feature_list)
    depth_value = clf_depth.predict(feature_test)
    print 'depth_value: ' + str(depth_value[0])
    return app_value, depth_value[0], len(word_set)


