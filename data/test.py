#!/usr/bin/env python

# 
# routines for running the out-of-lab testing
# 
# usage: > python test.py
# 

from sys import argv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
import numpy as np
import preprocess
import math

# steering the decision biased towards touching or no touching
bias = 0

# optimized parameters for t ranging from 0.6 to 1.5:
# 
# {'bootstrap': False, 'max_depth': 300, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 4, 'n_estimators': 200}
# {'bootstrap': False, 'max_depth': 200, 'max_features': 'log2', 'min_samples_leaf': 2, 'min_samples_split': 5, 'n_estimators': 250}
# {'bootstrap': False, 'max_depth': 150, 'max_features': 'log2', 'min_samples_leaf': 4, 'min_samples_split': 5, 'n_estimators': 150}
# {'bootstrap': False, 'max_depth': 300, 'max_features': 'log2', 'min_samples_leaf': 2, 'min_samples_split': 3, 'n_estimators': 100}
# {'bootstrap': False, 'max_depth': 350, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 3, 'n_estimators': 250}
# {'bootstrap': False, 'max_depth': 200, 'max_features': 'log2', 'min_samples_leaf': 2, 'min_samples_split': 3, 'n_estimators': 150}
# {'bootstrap': False, 'max_depth': 150, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 150}
# {'bootstrap': False, 'max_depth': 150, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 300}
# {'bootstrap': False, 'max_depth': 300, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 3, 'n_estimators': 200}
# {'bootstrap': False, 'max_depth': 200, 'max_features': 'log2', 'min_samples_leaf': 4, 'min_samples_split': 4, 'n_estimators': 100}
# {'bootstrap': False, 'max_depth': 150, 'max_features': 'log2', 'min_samples_leaf': 2, 'min_samples_split': 3, 'n_estimators': 300}

# onsets where inference starts
onsets = [
    1.0, 1.1, 1.2, 1.3, 1.4, 1.5
    ]
# baseline:
# onsets = [1.1]

# training sets to be tested
training_sets = [
    'm_onset_1.0.csv', 'm_onset_1.1.csv',  'm_onset_1.2.csv',  'm_onset_1.3.csv', 'm_onset_1.4.csv', 'm_onset_1.5.csv'
    ]
# baseline:
# training_sets = ['m_onset_1.1.csv']

# to store models created for each training set
model_sets = []

# data sets for testing
raw_testing_sets = ['p_all2.csv']

# random forest models
rfs = [
    # RandomForestClassifier(n_estimators=250, min_samples_split=5, min_samples_leaf=2, max_features='log2', max_depth=200, bootstrap=False),
    # RandomForestClassifier(n_estimators=150, min_samples_split=5, min_samples_leaf=4, max_features='log2', max_depth=150, bootstrap=False),
    # RandomForestClassifier(n_estimators=100, min_samples_split=3, min_samples_leaf=2, max_features='log2', max_depth=300, bootstrap=False),
    # RandomForestClassifier(n_estimators=250, min_samples_split=3, min_samples_leaf=1, max_features='log2', max_depth=350, bootstrap=False),
    RandomForestClassifier(n_estimators=150, min_samples_split=3, min_samples_leaf=2, max_features='log2', max_depth=200, bootstrap=False),
    RandomForestClassifier(n_estimators=150, min_samples_split=2, min_samples_leaf=1, max_features='log2', max_depth=150, bootstrap=False),
    RandomForestClassifier(n_estimators=300, min_samples_split=2, min_samples_leaf=1, max_features='log2', max_depth=150, bootstrap=False),
    RandomForestClassifier(n_estimators=200, min_samples_split=3, min_samples_leaf=1, max_features='log2', max_depth=300, bootstrap=False),
    RandomForestClassifier(n_estimators=100, min_samples_split=4, min_samples_leaf=4, max_features='log2', max_depth=200, bootstrap=False),
    RandomForestClassifier(n_estimators=300, min_samples_split=3, min_samples_leaf=2, max_features='log2', max_depth=150, bootstrap=False)
]

# the routine to run the testing procedure
def do_test(testing_sets):
    test_results = []
    onset_perfs = []

    # 
    # train the model
    # 
    for i in range(0, len(training_sets)):
        # separate into features (x) and labels (y)
        data_set = training_sets[i]
        trainfile = open(data_set, 'r')
        trainlines = trainfile.readlines()
        trainlines.pop(0)
        xtrain = []
        ytrain = []

        for datastr in trainlines:
            idxLastSep = datastr.rindex(',')
            labelstr = datastr[idxLastSep+1:len(datastr)-1]
            datastr = datastr[0: idxLastSep]
            dataline = list(map(float, datastr.split(',')))

            xtrain.append(dataline)
            ytrain.append(labelstr)

        print('# of features:', len(xtrain[0]))

        print('training model ...')

        # compute f1 score
        rf = rfs[i]
        rf.fit(xtrain, ytrain)
        scoring = ['precision_macro', 'recall_macro']
        scores = cross_validate(rf, xtrain, ytrain, scoring=scoring)
        pre = scores['test_precision_macro'].mean()
        rec = scores['test_recall_macro'].mean()
        f1 = 2 * pre * rec / (pre+rec)
        print("f1 score: %0.4f" % (f1))

        onset_perfs.append(f1)
        model_sets.append(rf)

    # 
    # segmenting testing data: 
    # - xtest_toutches: [ [x, x ... x], [x, x ... x] ... ]
    #   each subset corresponds to a face touching action 
    # - xtest_nontouches: [x, x, x ... x]
    #   all nontouches are mixed
    # 
    for testing_set in testing_sets:
        testing_file = open(testing_set, 'r')
        datalines = testing_file.readlines()

        xtest_touches = []
        xtest_nontouches = []
        xtouch = []
        
        for datastr in datalines:
            idxLastSep = datastr.rindex(',')
            labelstr = datastr[idxLastSep+1:].strip()
            if labelstr == 'Touching':
                xtouch.append(datastr)
            elif labelstr == 'No Touching':
                # store the last chunk of face touching data
                if len(xtouch) > 0:
                    xtest_touches.append(xtouch)
                    xtouch = []
                xtest_nontouches.append(datastr)
        # last patch
        if len(xtouch) > 0:
            xtest_touches.append(xtouch)

        # 
        # testing
        # 

        # assign weight to each model with different time windows based on their f1 perf.
        alpha = 10
        onset_weights = [math.exp(alpha * (x-onset_perfs[0])) for x in onset_perfs]
        print(onset_weights)
        
        onset_detections = [] # tally when decision are made (at each time point e.g., 1.0, ... 1.5)
        test_result = []

        # testing true positives
        ntp = 0
        for xtouch in xtest_touches:
            for datastr in xtouch:
                vote = 0
                for i in range(0, len(onsets)):
                    datains = preprocess.do_preprocess(datastr, onsets[i])
                    if datains == None:
                        continue
                    prediction = model_sets[i].predict([datains])
                    if prediction[0] == 'Touching':
                        vote += onset_weights[i]
                    elif prediction[0] == 'No Touching':
                        vote -= onset_weights[i]

                    # calculating a projected vote to see if subsequent time points can be skipped
                    proj_vote = vote
                    for k in range(i+1, len(onsets)):
                        proj_vote -= onset_weights[k]

                    if proj_vote > bias:
                        break

                if vote > bias:
                    while i >= len(onset_detections):
                        onset_detections.append(0)
                    onset_detections[i] += 1
                    ntp += 1
                    break
            
        test_result.append(ntp)
        print("true positive rate: %.04f (%2d/%2d)" % (ntp/len(xtest_touches), ntp, len(xtest_touches)))
        print(onset_detections)
        test_result.extend(onset_detections)
        
        # testing false positives
        nfp = 0
        infer_rate = 4
        wind_size = 1.5
        nskip = infer_rate * wind_size  # how many samples in a time window
        cntr_skip = 0
        cntr_progress = 0

        for datastr in xtest_nontouches:
            # after detecting a face touching, skip the next time window 
            # (can't have two touches in one time window)
            if cntr_skip > 0:
                cntr_skip -= 1
                continue
            
            vote = 0
            for i in range(0, len(onsets)):
                datains = preprocess.do_preprocess(datastr, onsets[i])
                if datains == None:
                    continue
                prediction = model_sets[i].predict([datains])
                if prediction[0] == 'Touching':
                    vote += onset_weights[i]
                elif prediction[0] == 'No Touching':
                    vote -= onset_weights[i]

                # calculating a projected vote to see if subsequent time points can be skipped
                proj_vote = vote
                for k in range(i+1, len(onsets)):
                    proj_vote += onset_weights[k]

                if proj_vote < bias:
                    break

            if vote > bias:
                nfp += 1
                cntr_skip = nskip
            
            cntr_progress += 1
            print("%3d%%" % int(cntr_progress * 100 / len(xtest_nontouches)), end='\r')

        test_result.append(nfp)
        print("false positive rate: %.04f (%2d/%2d)" % (nfp/len(xtest_nontouches), nfp, len(xtest_nontouches)))

        test_results.append(test_result)

    return test_results

if __name__ == "__main__":
    
    do_test(raw_testing_sets)