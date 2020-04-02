#!/usr/bin/env python
from sys import argv
import subprocess

rawfiles = [
    '0331s1touch.csv', '0401s1general.csv', '0401s1nearmiss.csv', 
    '0401s2general.csv' , '0401s2nearmiss.csv', '0401s2touch.csv',
    '0401s3general.csv' , '0401s3nearmiss.csv', '0401s3touch.csv'
    ]

if __name__ == "__main__":
    if len(argv) <= 1:
        quit()

    for f in rawfiles:
        subprocess.call('python preprocess.py ' + f, shell=True)
    
    strcmd = 'python merge.py ' + argv[1]
    for f in rawfiles:
        strcmd += ' p_' + f
    
    subprocess.call(strcmd, shell=True)
