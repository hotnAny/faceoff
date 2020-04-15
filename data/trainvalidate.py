#!/usr/bin/env python
from sys import argv
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

RANDOM_SEARCH=0
RANDOM_GRID = {
    'bootstrap': [True, False],
    'max_depth': [50, 100, 150, 200, 250, 300, 350, 400, 450, None],
    'max_features': ['auto', 'sqrt', 'log2', None],
    'min_samples_leaf': [1, 2, 4, 8],
    'min_samples_split': [2, 5, 10, 15],
    'n_estimators': [100, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
}

GRID_SEARCH = 1
# {'n_estimators': 600, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'log2', 'max_depth': 60, 'bootstrap': False}
# {'n_estimators': 600, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'log2', 'max_depth': 200, 'bootstrap': False}
# {'n_estimators': 1600, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'log2', 'max_depth': 300, 'bootstrap': False}
# {'n_estimators': 200, 'max_depth': 350}
 # {'n_estimators': 1800, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'auto', 'max_depth': 350, 'bootstrap': False}
#  {'n_estimators': 1400, 'min_samples_split': 10, 'min_samples_leaf': 1, 'max_features': 'auto', 'max_depth': 100, 'bootstrap': False}
PARAM_GRID = {
    'bootstrap': [False],
    'max_depth': [50, 75, 100, 125, 150],
    'max_features': ['auto'],
    'min_samples_leaf': [1],
    'min_samples_split': [6, 8, 10, 12, 14],
    'n_estimators': [1200, 1300, 1400, 1500, 1600]
}

search_type = None

HAZTIME = True
CV = 10 if HAZTIME else 3
NITER = 300 if HAZTIME else 100

if __name__ == "__main__":
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
    if len(argv) <= 1:
        quit()

    datafile = open(argv[1], 'r')
    datalines = datafile.readlines()
    datalines.pop(0)
    
    xtrain = []
    ytrain = []
    for datastr in datalines:
        idxLastSep = datastr.rindex(',')
        labelstr = datastr[idxLastSep+1:len(datastr)-1]
        datastr = datastr[0: idxLastSep]
        dataline = list(map(float, datastr.split(',')))

        xtrain.append(dataline)
        ytrain.append(labelstr)

    print('# of features:', len(xtrain[0]))
    # print(ytrain)    

    ###################################################################################################
    # train
    
    #
    

    rf = RandomForestClassifier() 

    # random search
    if search_type == RANDOM_SEARCH:
        rf_random = RandomizedSearchCV(estimator = rf, param_distributions = RANDOM_GRID, 
        n_iter = NITER, cv = CV, verbose=2, random_state=42, n_jobs = -1)
        rf_random.fit(xtrain, ytrain)
        print(rf_random.best_params_)
        print(rf_random.best_score_)
    # grid search
    elif search_type == GRID_SEARCH:
        grid_search = GridSearchCV(estimator = rf, param_grid = PARAM_GRID, cv = CV, 
        n_jobs = -1, verbose = 2)
        grid_search.fit(xtrain, ytrain)
        print(grid_search.best_params_)
        print(grid_search.best_score_)
    # base model
    else:
        rf.fit(xtrain, ytrain)
        scores = cross_val_score(rf, xtrain, ytrain, cv=20)
        print("Base model accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        # {'bootstrap': False, 'max_depth': 350, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 7, 'n_estimators': 100}
        # {'bootstrap': False, 'max_depth': 300, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 5, 'n_estimators': 200}
        # {'n_estimators': 1400, 'min_samples_split': 10, 'min_samples_leaf': 1, 'max_features': 'auto', 'max_depth': 100, 'bootstrap': False}
        # {'bootstrap': False, 'max_depth': 125, 'max_features': 'auto', 'min_samples_leaf': 1, 'min_samples_split': 6, 'n_estimators': 1400}
        rf_tuned = RandomForestClassifier(n_estimators=1400, min_samples_split=6, min_samples_leaf=1, max_features='auto', max_depth=125, bootstrap=False)
        rf_tuned.fit(xtrain, ytrain)
        scores_tuned = cross_val_score(rf_tuned, xtrain, ytrain, cv=20)
        print("Tuned model accuracy: %0.2f (+/- %0.2f)" % (scores_tuned.mean(), scores_tuned.std() * 2))

    ###################################################################################################
    # test
    # 