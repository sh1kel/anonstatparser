#!/usr/bin/python

import csv
import sys

rawcsv = sys.argv[1]
uid_field_num = 72
uidlist = []

def csv_get_data(csvfile):
    try:
        f = open(csvfile, 'rb')
    except:
        print "Can't open report file"
        exit(0)
    content = csv.reader(f)
    rownum = 0
    for row in content:
        if rownum == 0:
            header = row
        else:
            #print row[uid_field_num]
            uidlist.append(row[uid_field_num])
        rownum += 1
    f.close()
    return uidlist


csv_get_data(rawcsv)
