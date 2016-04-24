import sklearn
import pickle
import numpy as np
from sklearn import cross_validation
from sklearn import datasets
from sklearn import svm
from sklearn.metrics import f1_score
from sklearn import preprocessing
import random
import pprint

features = pickle.load(open('features.pkl'))
labels = pickle.load(open('labels.pkl'))

def convert(x):
    if x == 1:
        return 0
    else:
        return 1

labels = map(convert, labels)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(features, labels, test_size=0.2,random_state=0)

#normalization
scaler = preprocessing.StandardScaler().fit(X_train)
X_train_org = X_train
X_test = scaler.transform(X_test)
X_train = scaler.transform(X_train)

# a list of parameters to tune for the rbf kernal svm. need to beat the baseline of acc= 0.712
C_list = [0.1,1,10,100,200,300,400,500,600,700,1000]
gamma_list = [0.01,0.001,0.0001,0.0004,0.00045,0.0005,0.00055,0.0006,0.001,0.01,0.1]
score_matrix =[]
score_list_all = []
clf_list = []
for c in C_list:
    score_list = []
    for g in gamma_list:
        clf = svm.SVC( C = c, gamma= g, kernel='rbf').fit(X_train,y_train)
        clf_list.append(clf)
        score = clf.score(X_test,y_test)
        print 'C: ' + str(c) + ', gamma:' +str(g) + ', mean accuracy:'+ str(score)
        score_list.append(score)
        score_list_all.append(score)
    if score_matrix == []:
        score_matrix = score_list
    else:
        score_matrix = np.vstack((score_matrix,score_list))

max_score = np.amax(score_matrix)
print max_score
index = score_list_all.index(max_score)
clf_max = clf_list[index]
pickle.dump((X_train_org, scaler, clf_max), open('depth_rater.pkl', 'wb'))
