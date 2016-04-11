import sklearn
import pickle
import numpy as np
from sklearn import cross_validation
from sklearn import datasets
from sklearn import svm
iris = datasets.load_iris()
#print iris
#print type(iris)
sent = pickle.load(open('sent.pkl'))
print sent
#X_train, X_test, y_train, y_test = cross_validation.train_test_split(iris.data,iris.target, test_size=0.4,random_state=0)
# make the labels into 0 and 1 to make it easier
target = sent['target'] ==3
X_train, X_test, y_train, y_test = cross_validation.train_test_split(sent['data'],target, test_size=0.2,random_state=0)
print (X_train.shape,y_train.shape)
print (X_test.shape,y_test.shape)
clf = svm.SVC(kernel='linear',C=1).fit(X_train,y_train)
score = clf.score(X_test,y_test)
print score
#print type(iris.target[0])
#print iris.target
