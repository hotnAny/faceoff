#!/usr/bin/env python

#
# merge instances across multiple files into one file
# 
# usage: > python merge <name_of_output_file> <file_to_merge_1> <file_to_merge_2> ...

from sys import argv

if __name__ == "__main__":
    if len(argv) <= 3:
        quit()

    megastr = ''
    for i in range(2, len(argv)):
        datafile = open(argv[i], 'r')
        datalines = datafile.readlines()
        for j in range(0, len(datalines)):
            # create the first line of feature/attribute names
            if i==2 and j==0:
                megastr = datalines[0]
            # add instances
            elif j > 0:
                megastr += datalines[j]
    
    file = open('m_' + argv[1] + '.csv', 'w')
    file.write(megastr)
    file.close()
