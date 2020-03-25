#!/usr/bin/env python
from sys import argv
import subprocess

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
        nbins = 10
        binsize = int(n / nbins + 0.9)
        print(n, n / nbins + 0.9, binsize)
        if binsize <= 1:
            print(binsize, "too few data points for binning!")
            continue

        databins = []
        onebin = [0, 0, 0]
        m = 0
        for i in range(0, n):
            onebin[0] += dataline[3 * i]
            onebin[1] += dataline[3 * i+1]
            onebin[2] += dataline[3 * i+2]
            m += 1

            if (i+1) % binsize == 0 or i+1 >= n:
                if m > 0:
                    onebin[0] /= m
                    onebin[1] /= m
                    onebin[2] /= m
                    databins.extend(onebin)
                onebin = [0, 0, 0]
                m = 0
        
        l = int(len(databins)/3)
        if l < nbins:
            databins.extend(databins[l-3: l])
        
        if len(databins)/3 < nbins:
            print(len(databins)/3, 'smaller than required # of bins')
            continue

        datains.extend(databins)
        # print(n, len(databins)/3)
        # print(databins)
        # print(len(databins)/3)
        # break

        ##############################################################################
        #
        print(datains)
        for x in datains:
            strallins += "{:.3f}".format(x) + ','
        strallins += labelstr.strip() + '\n'

        # print(strallins)
        # subprocess.call('rm ' + 'p_' + argv[1], shell=True)

    strheader = ""
    for i in range(0, len(datains)):
        strheader += 'f' + str(i) + ','
    strheader += 'class\n'

    file = open('p_' + argv[1], 'w')
    file.write(strheader+strallins)
    file.close()
