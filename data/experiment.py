#!/usr/bin/env python

# 
#  the main script to run the experiments
# 
#   1. cross-validation
#   2. f1 score (as a function of time window)
#   3. out-of-lab testing
# 
#  usage: > python experiment.py
# 

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
import subprocess
import test

SKIP1 = True    # skip the cross-validation
SKIP2 = True    # skip the f1 score
SKIP3 = False   # skip the out-of-lab testing

# no. of repetitions for part 1, 2 and 3
NREP1 = 5   
NREP2 = 5
NREP3 = 1

# file of training data corresponding to sensor data up to the point t (0.1s <= t <= 1.5s)
onsets = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
onset_files = [
    'm_onset_0.1.csv', 'm_onset_0.2.csv', 'm_onset_0.3.csv',  'm_onset_0.4.csv', 'm_onset_0.5.csv',
    'm_onset_0.6.csv', 'm_onset_0.7.csv', 'm_onset_0.8.csv',  'm_onset_0.9.csv', 'm_onset_1.0.csv',
    'm_onset_1.1.csv', 'm_onset_1.2.csv', 'm_onset_1.3.csv',  'm_onset_1.4.csv', 'm_onset_1.5.csv'
]

testing_files = ['p1_all.csv', 'p2_all.csv', 'p3_all.csv']

# for part 1: training data sorted into three sets
touch_v_general = 'm_04221701_touch_v_general.csv'
touch_v_nearmiss = 'm_04221701_touch_v_nearmiss.csv'
touch_v_nearmuss_v_general = 'm_04241449_touch_nearmiss_notouch.csv'

# unpack a file of data into instances of features (x) and labels (y)
def unpack(fn):
    datafile = open(fn, 'r')
    datalines = datafile.readlines()
    datalines.pop(0) # remove the first line of attribute names

    x = []
    y = []
    for datastr in datalines:
        idxLastSep = datastr.rindex(',')
        labelstr = datastr[idxLastSep+1:len(datastr)-1]
        datastr = datastr[0: idxLastSep]
        dataline = list(map(float, datastr.split(',')))

        x.append(dataline)
        y.append(labelstr)
    
    return x, y

if __name__ == "__main__":
    #
    # 1. cross-validation
    #
    if SKIP1==False:
        print('############### validation ... ')
        print('TvG mean, TvG std, TvN mean, TvN std')
        for n in range(0, NREP1):
            xtg, ytg = unpack(touch_v_general)
            xtn, ytn = unpack(touch_v_nearmiss)
            rf = RandomForestClassifier()
            rf.fit(xtg, ytg)
            scores_tg = cross_val_score(rf, xtg, ytg, cv=10)
            rf.fit(xtn, ytn)
            scores_tn = cross_val_score(rf, xtn, ytn, cv=10)
            print("%0.4f, %0.4f, %0.4f, %0.4f" % (scores_tg.mean(), scores_tg.std(), scores_tn.mean(), scores_tn.std()))
    else:
        print('############### skipped validation ... ')

    print('')

    # 
    # 2. f1 scores
    # 
    if SKIP2==False:
        print('############### onset f1 score ... ')
        print('0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5')

        for n in range(0, NREP2):
            rf = RandomForestClassifier(n_estimators=100, min_samples_split=6, min_samples_leaf=1, max_features='auto', max_depth=550, bootstrap=False)
            for onset_file in onset_files:
                x, y = unpack(onset_file)
                rf.fit(x, y)
                scoring = ['precision_macro', 'recall_macro']
                scores = cross_validate(rf, x, y, scoring=scoring)
                pre = scores['test_precision_macro'].mean()
                rec = scores['test_recall_macro'].mean()
                f1 = 2 * pre * rec / (pre+rec)
                print(str(f1), end=', ')
            print('')
    else:
        print('############### skipped onset f1 ... ')
    
    #
    # 3. out-of-lab testing
    #
    print('')
    if SKIP3==False:
        # for tf in testing_files:
        # print('############### testing ' + tf)
        test_results = []
        nrep = 1
        for i in range(0, NREP3):
            test_results.append(test.do_test(testing_files))
        
        print('###############')
        for result in test_results:
            for entry in result:
                print(','.join([str(x) for x in entry]))
            print('')
    else:
        print('############### skipped testing ... ')