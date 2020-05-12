# idx = 2
    # while(idx < len(argv)):
    #     print('spliting test data set ...')
    #     testfile = open(argv[idx], 'r')
    #     testlines = testfile.readlines()
    #     testlines.pop(0)
    #     xtest = []
    #     ytest = []

    #     nfeats = len(xtrain[0])

    #     # for datastr in testlines:
    #     #     nfeats = min(len(datastr.split(','))-1, nfeats)
        
    #     # print(nfeats)

    #     for datastr in testlines:
    #         if len(datastr.split(','))-1 < nfeats:
    #             continue
    #         idxLastSep = datastr.rindex(',')
    #         labelstr = datastr[idxLastSep+1:len(datastr)-1]
    #         datastr = datastr[0: idxLastSep]

    #         lsdatastr = datastr.split(',')
    #         lsdatastr = lsdatastr[0: nfeats]

    #         try:
    #             dataline = list(map(float, lsdatastr))
    #         except ValueError:
    #             print('value error!')
    #             continue

    #         xtest.append(dataline)
    #         ytest.append(labelstr)

    #     xtest_touches = []
    #     xtest_nontouches = []
    #     xtouch = []
    #     for i in range(0, len(xtest)):
    #         if ytest[i] == 'Touching':
    #             xtouch.append(xtest[i])
    #         elif ytest[i] == 'No Touching':
    #             if len(xtouch) > 0:
    #                 xtest_touches.append(xtouch)
    #                 xtouch = []
    #             xtest_nontouches.append(xtest[i])

    #     if len(xtouch) > 0:
    #         xtest_touches.append(xtouch)

    #     print(len(xtest_touches), 'touching instances')
    #     print(len(xtest_nontouches), 'non-touching trials')

    #     # 
    #     # testing
    #     # 
    #     print('testing model ...')
    #     thres_nconsec = 1
    #     tp_touch = 0
    #     fn_touch = 0
    #     for xtouch in xtest_touches:
    #         prediction = rf.predict(xtouch)
            
    #         nconsec = 0
    #         for y in prediction:
    #             if y == 'Touching':
    #                 nconsec += 1
    #                 if nconsec >= thres_nconsec:
    #                     tp_touch += 1
    #                     break
    #             else:
    #                 nconsec = 0
            
    #         # results = np.where(prediction=='Touching')
    #         # if len(results[0]) > 0:
    #         #     tp_touch += 1
    #         # else:
    #         #     fn_touch += 1
    #     print('__________________________________________________________________________true positive rate', tp_touch / len(xtest_touches), tp_touch, len(xtest_touches))

    #     # print(xtest_nontouches)
        
    #     prediction = rf.predict(xtest_nontouches)
    #     fp_touch = 0

    #     # results = np.where(prediction=='Touching')
    #     # fp_touch = len(results[0])
        
    #     infer_rate = 4
    #     wind_size = 1.5
    #     nskip = infer_rate * wind_size
    #     cntr_skip = 0
    #     eval_count = 0
    #     for y in prediction:
    #         if cntr_skip > 0:
    #             cntr_skip -= 1
    #             continue

    #         eval_count += 1
    #         if y == 'Touching':
    #             nconsec += 1
    #         else:
    #             if nconsec >= thres_nconsec:
    #                 fp_touch += 1
    #                 cntr_skip = nskip
    #             nconsec = 0
        
    #     # print('__________________________________________________________________________false positive rate',  fp_touch / len(xtest_nontouches), fp_touch, len(xtest_nontouches))
    #     print('__________________________________________________________________________false positive rate',  fp_touch / eval_count, fp_touch, eval_count)

    #     idx+=1


# for onset in cutpoints:
    #     print('############### onset=' + str(onset))
    #     for rawfiles in set_rawfiles:
    #         print('############### ' + ','.join(rawfiles))    

    #         print('############### preprocessing training file ... ')
    #         for f in rawfiles:
    #             subprocess.call('python preprocess.py ' + f + ' ' + str(onset), shell=True)
            
    #         strcmd = 'python merge.py ' + 'roc_' + str(onset)
    #         for f in rawfiles:
    #             strcmd += ' p_' + f
    #         subprocess.call(strcmd, shell=True)

    #         print('############### done! ')

    #         print('############### preprocessing testing files ...')
    #         str_testingfiles = ''
    #         for testing in testingfiles:
    #             subprocess.call('python preprocess.py ' + testing + ' ' + str(onset), shell=True)
    #             str_testingfiles += 'p_' + testing + ' '
    #         print('############### done: ' + str_testingfiles)

    #         print('############### testing ...')
    #         subprocess.call('python test.py m_roc_' + str(onset) + '.csv ' + str_testingfiles, shell=True)
    #         print('############### done! ')
        

    # # rf = RandomForestClassifier(
    #     n_estimators=1400, 
    #     min_samples_split=6, 
    #     min_samples_leaf=1, 
    #     max_features='auto', 
    #     max_depth=125, 
    #     bootstrap=False)

    # {'n_estimators': 600, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'log2', 'max_depth': 60, 'bootstrap': False}
# {'n_estimators': 600, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'log2', 'max_depth': 200, 'bootstrap': False}
# {'n_estimators': 1600, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'log2', 'max_depth': 300, 'bootstrap': False}
# {'n_estimators': 200, 'max_depth': 350}
 # {'n_estimators': 1800, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'auto', 'max_depth': 350, 'bootstrap': False}
#  {'n_estimators': 1400, 'min_samples_split': 10, 'min_samples_leaf': 1, 'max_features': 'auto', 'max_depth': 100, 'bootstrap': False}
# {'n_estimators': 1000, 'min_samples_split': 10, 'min_samples_leaf': 4, 'max_features': 'sqrt', 'max_depth': None, 'bootstrap': True}
# {'n_estimators': 100, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'log2', 'max_depth': 450, 'bootstrap': False}
# {'n_estimators': 100, 'min_samples_split': 15, 'min_samples_leaf': 4, 'max_features': 'log2', 'max_depth': 50, 'bootstrap': False}
# {'n_estimators': 100, 'min_samples_split': 5, 'min_samples_leaf': 4, 'max_features': None, 'max_depth': 300, 'bootstrap': True}

# {'n_estimators': 200, 'min_samples_split': 2, 'min_samples_leaf': 2, 'max_features': 'log2', 'max_depth': 250, 'bootstrap': False}

 # {'bootstrap': False, 'max_depth': 350, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 7, 'n_estimators': 100}
            # {'bootstrap': False, 'max_depth': 300, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 5, 'n_estimators': 200}
            # {'n_estimators': 1400, 'min_samples_split': 10, 'min_samples_leaf': 1, 'max_features': 'auto', 'max_depth': 100, 'bootstrap': False}
            # {'bootstrap': False, 'max_depth': 125, 'max_features': 'auto', 'min_samples_leaf': 1, 'min_samples_split': 6, 'n_estimators': 1400}
            # {'bootstrap': True, 'max_depth': None, 'max_features': 'sqrt', 'min_samples_leaf': 3, 'min_samples_split': 6, 'n_estimators': 800}
            # {'bootstrap': False, 'max_depth': 550, 'max_features': 'auto', 'min_samples_leaf': 1, 'min_samples_split': 6, 'n_estimators': 100}
            # {'bootstrap': False, 'max_depth': 100, 'max_features': 'auto', 'min_samples_leaf': 8, 'min_samples_split': 10, 'n_estimators': 100}
            # {'bootstrap': True, 'max_depth': 325, 'max_features': None, 'min_samples_leaf': 5, 'min_samples_split': 7, 'n_estimators': 100}
            
            # rf_tuned = RandomForestClassifier(n_estimators=100, min_samples_split=7, min_samples_leaf=5, max_features=None, max_depth=325, bootstrap=True)
            # rf_tuned.fit(xtrain, ytrain)
            # scores_tuned = cross_val_score(rf_tuned, xtrain, ytrain, cv=10)
            # print("Tuned model accuracy: %0.2f (+/- %0.2f)" % (scores_tuned.mean(), scores_tuned.std() * 2))

#  X, y = make_classification(n_samples=1000, n_features=4, n_informative=2, n_redundant=0, random_state=0, shuffle=False)
    #  print(X)
    #  print(y)
    #  clf = RandomForestClassifier(max_depth=2, random_state=0)
    #  clf.fit(X, y)
    #  RandomForestClassifier(max_depth=2, random_state=0)
    #  print(clf.feature_importances_)
    #  print(clf.predict([[0, 0, 0, 0]]))

    ###################################################################################################
    # read input dataset
    # if len(argv) <= 1:
        # quit()

    # for onset in onsets:
        # print('--------------------------------onset=', str(onset))

        # subprocess.call('python preprocess.py ' + argv[1] + ' ' + str(onset), shell=True)
        # subprocess.call('mv p_' + argv[1] + ' p_' + argv[1] + '_' + str(onset), shell=True)