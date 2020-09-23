# FaceOff

## Prerequisites
* [Python 3](https://www.python.org/downloads/)
* [scikit-learn](https://scikit-learn.org/stable/install.html)

## Data Description
All data files end with '.csv':
* Data files starting with '0' (e.g., `0401s1general.csv`) are raw data collected via several sessions to include both face touching and non face touching behaviors;
* Data files starting with 'm' (e.g., `m_onset_0.1.csv`) are training data; "onset_0.x" means there only contains data from the first 0.x portion of the time window (see the accompanying [paper](https://arxiv.org/abs/2008.01769) for more details);'
* Data files starting with 'p' (e.g., `p3_all.csv`) are testing data;

## Data Processing Scripts
* `experiment.py` runs several experiments reported in the aforementioned paper;
* `test.py` contains some testing routines used by `experiment.py`;
* `featurize.py` featurizes raw data using `preprocess.py` and merges different sessions' data using `merge.py`;
* `tunehyperparam.py` tunes hyperparameters for random forest models.



