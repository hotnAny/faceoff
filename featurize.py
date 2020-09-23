#!/usr/bin/env python

# 
#  the script that extracts features from multiple files and merge them into a single file
# 
#  usage: > python featurize.py <name_of_output_file>
# 

from sys import argv
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

rawfiles = rawfiles2

if __name__ == "__main__":
    if len(argv) <= 1:
        quit()

    # preprocessing
    for f in rawfiles:
        subprocess.call('python preprocess.py ' + f + ' 1.0', shell=True)

    # merging
    strcmd = 'python merge.py ' + argv[1]
    for f in rawfiles:
        strcmd += ' p_' + f

    subprocess.call(strcmd, shell=True)
