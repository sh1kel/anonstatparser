#!/usr/bin/python

import csv
import sys

rawcsv = sys.argv[1]

def csv_get_data(csvfile):
    try:
        f = open(csvfile, 'rb')
        content = csv.reader(f)
        rownum = 0
        for row in content:
            if rownum == 0:
                header = row
            else:
                colnum = 0
                for col in row:
                    print '%-8s: %s' % (header[colnum], col)
                    colnum += 1
            rownum += 1
        f.close()
    except:
        print "Can't open report file"
        exit(0)

csv_get_data(rawcsv)
