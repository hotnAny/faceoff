#!/usr/bin/env python
from sys import argv
import subprocess
import math

if __name__ == "__main__":
    # print(argv)
    if len(argv) <= 1:
        quit()

    datafile = open(argv[1], 'r')
    datalines = datafile.readlines()
    strallins = ''

    for datastr in datalines:
        ##############################################################################
        datains = []

        # split into data and label
        idxLastSep = datastr.rindex(',')
        labelstr = datastr[idxLastSep+1:]
        datastr = datastr[0: idxLastSep]
        dataline = list(map(float, datastr.split(',')))
        n = int(len(dataline)/3)

        ##############################################################################
        # binning
        nbins = 20
        binsize = int(n / nbins + 0.9)
        if binsize < 1:
            print(binsize, "too few data points for binning!")
            continue

        bins = []
        onebin = [0, 0, 0]
        m = 0
        for i in range(0, n):
            onebin[0] += dataline[3 * i]
            onebin[1] += dataline[3 * i+1]
            onebin[2] += dataline[3 * i+2]
            m += 1

            if (i+1) % binsize == 0 or (i+1 >= n and len(bins)/3 < nbins):
                if m > 0:
                    onebin[0] /= m
                    onebin[1] /= m
                    onebin[2] /= m
                    bins.extend(onebin)

                onebin = [0, 0, 0]
                m = 0

        l = int(len(bins)/3)
        if l < nbins:
            bins.extend(bins[l-3: l])

        if len(bins)/3 < nbins:
            print(len(bins)/3, 'smaller than required # of bins')
            continue

        datains.extend(bins)

        # ##############################################################################
        # sqrt of sum per bin
        sumsqs = []
        l = int(len(bins)/3)
        for i in range(0, l):
            x = bins[i]
            y = bins[i+1]
            z = bins[i+2]
            sumsqs.append(math.sqrt(x*x + y*y + z*z))
        datains.extend(sumsqs)

        # ##############################################################################
        # sum, mean, sd
        sums = [0, 0, 0]
        for i in range(0, n):
            sums[0] += dataline[3 * i]
            sums[1] += dataline[3 * i + 1]
            sums[2] += dataline[3 * i + 2]
        datains.extend(sums)

        means = [s/n for s in sums]
        datains.extend(means)

        sds = [0, 0, 0]
        for i in range(0, n):
            sds[0] += pow(dataline[3 * i] - means[0], 2)
            sds[1] += pow(dataline[3 * i + 1] - means[1], 2)
            sds[2] += pow(dataline[3 * i + 2] - means[2], 2)
        sds = [math.sqrt(sd/n) for sd in sds]
        datains.extend(sds)

        # coefficient of variation
        cvs = [sds[i]/means[i] for i in range(0, len(means))]
        datains.extend(cvs)

        ##############################################################################
        #  median
        xs = [dataline[3 * i] for i in range(0, n)]
        ys = [dataline[3 * i + 1] for i in range(0, n)]
        zs = [dataline[3 * i + 2] for i in range(0, n)]

        xs.sort()
        ys.sort()
        zs.sort()

        medians = [xs[(int)(n/2)], ys[(int)(n/2)], zs[(int)(n/2)]]
        datains.extend(medians)

        ##############################################################################
        # meanabsdev, medianabsdev
        meanad = [0, 0, 0]
        medianad = [0, 0, 0]
        for i in range(0, n):
            for j in range(0, 3):
                meanad[j] += abs(dataline[3*i + j] - means[j]) / n
                medianad[j] += abs(dataline[3*i + j] - medians[j]) / n
        # print(meanad, medianad)
        datains.extend(meanad)
        datains.extend(medianad)

        ##############################################################################
        # zero crossings
        zeroxings = [0, 0, 0]
        for i in range(0, n-1):
            for j in range(0, 3):
                    if dataline[3*i+j] * dataline[3*(i+1)+j] < 0:
                        zeroxings[j] += 1
        # print(zeroxings)
        datains.extend(zeroxings)
        
        ##############################################################################
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
        datains.extend(skewness)
        datains.extend(kurtosis)
        ##############################################################################

        # for only outputing a specific axis
        # datains = datains[2::3]

        print(datains)

        for x in datains:
            strallins += "{:.3f}".format(x) + ','
        strallins += labelstr.strip() + '\n'

    strheader = ""
    for i in range(0, len(datains)):
        strheader += 'f' + str(i) + ','
    strheader += 'class\n'

    file = open('p_' + argv[1], 'w')
    file.write(strheader+strallins)
    file.close()
