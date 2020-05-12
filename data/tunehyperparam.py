#!/usr/bin/env python

# 
# routines for performing hyperparameter tuning
# usage: (set the type of search in the code)
#   > python tunehyperparam.py
# 

from sys import argv
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.metrics import recall_score
import subprocess

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

rawfiles3 = [
    '0401s1nearmiss.csv', '0331s1touch.csv',
    '0401s2nearmiss.csv', '0401s2touch.csv',
    '0401s3nearmiss.csv', '0401s3touch.csv'
]

# training data sets for tuning
rawfiles = rawfiles2

# random search to locate a roughly optimal subspace
RANDOM_SEARCH=0
RANDOM_GRID = {
    'bootstrap': [True, False],
    'max_depth': [50, 100, 150, 200, 250, 300, 350, 400, 450, None],
    'max_features': ['auto', 'sqrt', 'log2', None],
    'min_samples_leaf': [1, 2, 4, 8],
    'min_samples_split': [2, 5, 10, 15],
    'n_estimators': [100, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
}

# grid search to fine tune parameters within a localized subspace
GRID_SEARCH = 1
PARAM_GRID = {
    'bootstrap': [False],
    'max_depth': [150, 200, 250, 300, 350],
    'max_features': ['log2'],
    'min_samples_leaf': [1, 2, 3, 4, 5],
    'min_samples_split': [1, 2, 3, 4, 5],
    'n_estimators': [100, 150, 200, 250, 300]
}

# start with random and then grid search
# search_type = RANDOM_SEARCH
search_type = GRID_SEARCH

# more time consuming settings:
HAZTIME = False
CV = 10 if HAZTIME else 3
NITER = 300 if HAZTIME else 100

onset = 1.0

if __name__ == "__main__":

    # 
    # merge individual training data files
    # 
    for f in rawfiles:
        subprocess.call('python preprocess.py ' + f + ' ' + str(onset), shell=True)
        
    strcmd = 'python merge.py ' + 'onset_' + str(onset)
    for f in rawfiles:
        strcmd += ' p_' + f
    subprocess.call(strcmd, shell=True)

    datafile = open('m_onset_' + str(onset) + '.csv', 'r')
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
 

    #
    # hyperparameter tuning
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
    # non search
    else:
        rf.fit(xtrain, ytrain)
        scoring = ['precision_macro', 'recall_macro']
        scores = cross_validate(rf, xtrain, ytrain, scoring=scoring)
        pre = scores['test_precision_macro'].mean()
        rec = scores['test_recall_macro'].mean()
        f1 = 2 * pre * rec / (pre+rec)
        print(f1)