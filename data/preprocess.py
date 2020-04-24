#!/usr/bin/env python
from sys import argv
import subprocess
import math

nexpected = 150

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
        try:
            dataline = list(map(float, datastr.split(',')))
        except ValueError:
            continue
        n = int(len(dataline)/3)

        if n < nexpected * 0.75:
            continue
        
        ### only look at the onset
        if len(argv) == 3:
            n = int(n*float(argv[2]))
            dataline = dataline[0: n*3]
            # print(n)

        ##############################################################################
        # binning
        nbins = 16
        binsize = int(n / nbins + 0.9)
        if binsize < 1:
            continue
        # print(binsize, "too few data points for binning!")

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
            continue
        # print(len(bins)/3, 'smaller than required # of bins')

        ##############################################################################
        # sqrt of sum per bin
        sumsqs = []
        l = int(len(bins)/3)
        for i in range(0, l):
            x = bins[i]
            y = bins[i+1]
            z = bins[i+2]
            sumsqs.append(math.sqrt(x*x + y*y + z*z))
        

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

        # datains.extend(bins)
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

        # for only outputing a specific axis
        xdatains = datains[0::3]
        nx = len(xdatains)
        datains.extend(xdatains[int(nx*0.6):nx-1])

        ydatains = datains[1::3]
        ny = len(ydatains)
        datains.extend(ydatains[0:int(ny*0.2)])

        zdatains = datains[2::3]
        nz = len(zdatains)
        datains.extend(zdatains[0:int(nz*0.2)])

        # datains.extend(sumsqs)

        # print(datains)

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