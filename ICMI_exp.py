import scipy.io
import numpy as np
from sklearn import svm
from sklearn import cross_validation
import sys
from scipy import stats
def get_confusion_matrix(predicted,label):
    label = np.array(label)
    label_unique = np.unique(label)
    dim = len(label_unique)
    conf_matrix = np.zeros((dim,dim))
    index = 0
    for predict_i in predicted:
        conf_matrix [label[index]-1,predict_i-1] = conf_matrix [label[index],predict_i] +1
        index = index+1
    return conf_matrix
def SVR_cross_val(data,label):
    #C_list = [1,10,0.1,0.05,0.001,0.0001]
    #epsilon_list = [0.1,0.15,0.2,0.3]
    label = np.array(label)/5.0
    #print label
    C_list = [1]
    epsilon_list = [0.2]
    score_list = []
#    for C_value in C_list:
#        for epsilon_value in epsilon_list:
    clf = svm.SVR()
    scores = cross_validation.cross_val_score(clf,data,label,cv=5, scoring = 'mean_squared_error')
            #score_list.append(-scores.mean())
        #print scores
            #print ("C: %0.2f, epsilon: %0.2f, Mean_squred_error: %0.2f (+/- %0.2f)" %(C_value,epsilon_value,-scores.mean(), scores.std() * 2))
            #print ('\n')
        #predicted = cross_validation.cross_val_predict(clf,data,label,cv=5)
        #construct a confusion matrix
        #conf_matrix = get_confusion_matrix(predicted,label)
        #print conf_matrix
    #score_min = min(score_list)
    #print ("The best mse: %0.2f"%(score_min))
    return np.sqrt(-scores.mean())

def SVM_binary(data,label):
    label = label>3
    print len(np.where(label==0)[0])
    print len(label)
    clf = svm.SVC(class_weight = 'balanced')
    scores = cross_validation.cross_val_score(clf,data,label,cv=5)
    predicted = cross_validation.cross_val_predict(clf,data,label,cv=5)
    accuracy = 1-float(sum((np.array(predicted) -np.array(label))))/len(label)
    print accuracy
    print scores.mean()
    return scores.mean()
def main():
    data_mat = scipy.io.loadmat('ICMI_data')
    data = np.array(data_mat['data_org'])
    #print data[:,1]
    #sys.exit()
    label = np.ravel(np.array(data_mat['label_org']))
    model_dim ={'all':range(12),'vision':[0,1,2,3],'audio':[4,5],'lexical':[6,12],'turn_taking':[7,8,9,10,11,13]}
    #print 'overall best mse'+'\n'
    #all_mse = SVR_cross_val(data,label)
    for model in model_dim.keys():
        print model
        data_new = data[:,model_dim[model]]
        accuray_new = SVM_binary(data_new,label)
        print accuray_new
        mse_new = SVR_cross_val(data_new,label)
        print mse_new

if __name__ == "__main__":
    main()



