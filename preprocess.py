#!/usr/bin/env python

# 
# preprocessing data to extract features
# 
# usage: python preprocess.py <raw_data.csv>  t
#   - t: optional, to indicate that cropping the time window to here, e.g., to t=1.0s
# 

from sys import argv
import subprocess
import math

# HACK: expect an ideal raw data instance should have 150 values
nexpected = 150

def do_preprocess(datastr, onset):
        ##############################################################################
        datains = []

        # split into data and label
        idxLastSep = datastr.rindex(',')
        datastr = datastr[0: idxLastSep]
        try:
            dataline = list(map(float, datastr.split(',')))
        except ValueError:
            return None
        n = int(len(dataline)/3)

        if n < nexpected * 0.75:
            return None

        n = int(n*onset/1.5)
        dataline = dataline[0: n*3]

        ##############################################################################
        # sum, mean, sd
        sums = [0, 0, 0]
        for i in range(0, n):
            sums[0] += dataline[3 * i]
            sums[1] += dataline[3 * i + 1]
            sums[2] += dataline[3 * i + 2]

        means = [s/n for s in sums]

        sds = [0, 0, 0]
        for i in range(0, n):
            sds[0] += pow(dataline[3 * i] - means[0], 2)
            sds[1] += pow(dataline[3 * i + 1] - means[1], 2)
            sds[2] += pow(dataline[3 * i + 2] - means[2], 2)
        sds = [math.sqrt(sd/n) for sd in sds]

        # coefficient of variation
        cvs = [sds[i]/means[i] for i in range(0, len(means))]

        ##############################################################################
        #  median
        xs = [dataline[3 * i] for i in range(0, n)]
        ys = [dataline[3 * i + 1] for i in range(0, n)]
        zs = [dataline[3 * i + 2] for i in range(0, n)]

        xs.sort()
        ys.sort()
        zs.sort()

        medians = [xs[(int)(n/2)], ys[(int)(n/2)], zs[(int)(n/2)]]

        ##############################################################################
        # meanabsdev, medianabsdev
        meanad = [0, 0, 0]
        medianad = [0, 0, 0]
        for i in range(0, n):
            for j in range(0, 3):
                meanad[j] += abs(dataline[3*i + j] - means[j]) / n
                medianad[j] += abs(dataline[3*i + j] - medians[j]) / n
        # print(meanad, medianad)

        ##############################################################################
        # zero crossings
        zeroxings = [0, 0, 0]
        for i in range(0, n-1):
            for j in range(0, 3):
                    if dataline[3*i+j] * dataline[3*(i+1)+j] < 0:
                        zeroxings[j] += 1
        # print(zeroxings)
        
        #############################################################################
        # skewness, kurtosis
        mad2 = [0, 0, 0]
        mad3 = [0, 0, 0]
        mad4 = [0, 0, 0]
        for i in range(0, n):
            for j in range(0, 3):
                mad2[j] += math.pow(dataline[3*i + j] - means[j], 2) / n
                mad3[j] += math.pow(dataline[3*i + j] - means[j], 3) / n
                mad4[j] += math.pow(dataline[3*i + j] - means[j], 4) / n

        skewness = [0, 0, 0]
        kurtosis = [0, 0, 0]
        for j in range(0, 3):
            skewness[j] = mad3[j] / math.pow(sds[j], 3)
            kurtosis[j] = mad4[j] / math.pow(sds[j], 4)

        # print(skewness, kurtosis)
        
        #############################################################################
        # finally selecting features

        # datains.extend(bins)
        # datains.extend(sumsqs)
        datains.extend(sums)
        datains.extend(means)
        datains.extend(sds)
        datains.extend(cvs)
        datains.extend(zeroxings)
        datains.extend(medians)
        datains.extend(meanad)
        datains.extend(medianad)
        datains.extend(skewness)
        datains.extend(kurtosis)

        return datains

if __name__ == "__main__":
    if len(argv) <= 1:
        quit()
    elif len(argv) <= 2:
        argv.append(1.0)

    datafile = open(argv[1], 'r')
    datalines = datafile.readlines()
    strallins = ''

    # for each raw instance, extract features and attach a label to it
    for datastr in datalines:
        datains = do_preprocess(datastr, float(argv[2]))
        if datains==None:
            continue
        idxLastSep = datastr.rindex(',')
        labelstr = datastr[idxLastSep+1:]
        for x in datains:
            strallins += "{:.3f}".format(x) + ','
        strallins += labelstr.strip() + '\n'

    # create header
    strheader = ""
    for i in range(0, len(datains)):
        strheader += 'f' + str(i) + ','
    strheader += 'class\n'

    file = open('p_' + argv[1], 'w')
    file.write(strheader+strallins)
    file.close()