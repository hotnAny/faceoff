#!/usr/bin/env python
from sys import argv

if __name__ == "__main__":
    # print(argv)
    if len(argv) <= 3:
        quit()

    megastr = ''
    for i in range(2, len(argv)):
        datafile = open(argv[i], 'r')
        datalines = datafile.readlines()
        for j in range(0, len(datalines)):
            if i==2 and j==0:
                megastr = datalines[0]
            elif j > 0:
                megastr += datalines[j]
    
    file = open('m_' + argv[1] + '.csv', 'w')
    file.write(megastr)
    file.close()
