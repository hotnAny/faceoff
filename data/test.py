#!/usr/bin/env python
from sys import argv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

if __name__ == "__main__":
    
    # arguments:
    #   1. training dataset
    #   2. testing dataset
    if len(argv) <= 2:
        quit()
    
    # 
    # train the model
    # 
    trainfile = open(argv[1], 'r')
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

    rf = RandomForestClassifier() 
    # rf = RandomForestClassifier(n_estimators=1400, min_samples_split=6, min_samples_leaf=1, max_features='auto', max_depth=125, bootstrap=False)
    rf.fit(xtrain, ytrain)
    scores = cross_val_score(rf, xtrain, ytrain, cv=10)
    print("Base model accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    # 
    # segmenting testing data
    # 
    testfile = open(argv[2], 'r')
    testlines = testfile.readlines()
    testlines.pop(0)
    xtest = []
    ytest = []

    for datastr in testlines:
        idxLastSep = datastr.rindex(',')
        labelstr = datastr[idxLastSep+1:len(datastr)-1]
        datastr = datastr[0: idxLastSep]
        dataline = list(map(float, datastr.split(',')))

        xtest.append(dataline)
        ytest.append(labelstr)

    xtest_touches = []
    xtest_nontouches = []
    xtouch = []
    for i in range(0, len(xtest)):
        if ytest[i] == 'Touching':
            xtouch.append(xtest[i])
        elif ytest[i] == 'No Touching':
            if len(xtouch) > 0:
                xtest_touches.append(xtouch)
                xtouch = []
            xtest_nontouches.append(xtest[i])

    if len(xtouch) > 0:
        xtest_touches.append(xtouch)

    print(len(xtest_touches), 'touching instances')
    print(len(xtest_nontouches), 'non-touching trials')

    # 
    # testing
    # 
    thres_nconsec = 2
    tp_touch = 0
    fn_touch = 0
    for xtouch in xtest_touches:
        prediction = rf.predict(xtouch)
        # results = np.where(prediction=='Touching')
        nconsec = 0
        for y in prediction:
            if y == 'Touching':
                nconsec += 1
                if nconsec >= thres_nconsec:
                    tp_touch += 1
                    break
            else:
                nconsec = 0
        
        # if len(results[0]) > 0:
        #     tp_touch += 1
        # else:
        #     fn_touch += 1
    print('true positive rate', tp_touch / len(xtest_touches))

    
    prediction = rf.predict(xtest_nontouches)
    fp_touch = 0

    # results = np.where(prediction=='Touching')
    # fp_touch = len(results[0])
    
    for y in prediction:
            if y == 'Touching':
                nconsec += 1
                if nconsec >= thres_nconsec:
                    fp_touch += 1
                    break
            else:
                nconsec = 0
       
    print('true positive rate',  fp_touch / len(xtest_nontouches), fp_touch, len(xtest_nontouches))



