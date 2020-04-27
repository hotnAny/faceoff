#!/usr/bin/env python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
import subprocess

SKIP1 = True

rawfiles1 = [
    '0401s1general.csv', '0401s1nearmiss.csv', '0331s1touch.csv',
    '0401s2general.csv', '0401s2nearmiss.csv', '0401s2touch.csv',
    '0401s3general.csv', '0401s3nearmiss.csv', '0401s3touch.csv'
    ]

rawfiles2 = [
    '0401s1general.csv', '0331s1touch.csv',
    '0401s2general.csv', '0401s2touch.csv',
    '0401s3general.csv', '0401s3touch.csv'
]

# set_rawfiles = [rawfiles1, rawfiles2]
set_rawfiles = [rawfiles2]

touch_v_general = 'm_04221701_touch_v_general.csv'
touch_v_nearmiss = 'm_04221701_touch_v_nearmiss.csv'
touch_v_nearmuss_v_general = 'm_04241449_touch_nearmiss_notouch.csv'
testingfiles = 'p1_all.csv', 'p2_all.csv', 'p3_all.csv', 'p_all.csv'


cutpoints = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# cutpoints = [1.0]

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
    # 1. validation
    #

    # 1.1 touch vs. general and touch vs. nearmiss 
    if SKIP1==False:
        print('############### validation ... ')
        xtg, ytg = unpack(touch_v_general)
        xtn, ytn = unpack(touch_v_nearmiss)
        rf = RandomForestClassifier()
        rf.fit(xtg, ytg)
        scores_tg = cross_val_score(rf, xtg, ytg, cv=10)
        print("Touch vs. General: %0.4f (+/- %0.4f)" % (scores_tg.mean(), scores_tg.std() * 2))
        rf.fit(xtn, ytn)
        scores_tn = cross_val_score(rf, xtn, ytn, cv=10)
        print("Touch vs. Near Miss: %0.4f (+/- %0.4f)" % (scores_tn.mean(), scores_tn.std() * 2))
    else:
        print('############### skipped validation ... ')

    #
    # 2. testing
    #
    for onset in cutpoints:
        print('############### onset=' + str(onset))
        for rawfiles in set_rawfiles:
            print('############### ' + ','.join(rawfiles))    

            print('############### preprocessing training file ... ')
            for f in rawfiles:
                subprocess.call('python preprocess.py ' + f + ' ' + str(onset), shell=True)
            
            strcmd = 'python merge.py ' + 'roc_' + str(onset)
            for f in rawfiles:
                strcmd += ' p_' + f
            subprocess.call(strcmd, shell=True)

            print('############### done! ')

            print('############### preprocessing testing files ...')
            str_testingfiles = ''
            for testing in testingfiles:
                subprocess.call('python preprocess.py ' + testing + ' ' + str(onset), shell=True)
                str_testingfiles += 'p_' + testing + ' '
            print('############### done: ' + str_testingfiles)

            print('############### testing ...')
            subprocess.call('python test.py m_roc_' + str(onset) + '.csv ' + str_testingfiles, shell=True)
            print('############### done! ')
        

    # # rf = RandomForestClassifier(
    #     n_estimators=1400, 
    #     min_samples_split=6, 
    #     min_samples_leaf=1, 
    #     max_features='auto', 
    #     max_depth=125, 
    #     bootstrap=False)