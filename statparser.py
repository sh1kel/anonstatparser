#!/usr/bin/python

import csv
import sys
import urllib3
urllib3.disable_warnings()
from time import sleep
import json

rawcsv = sys.argv[1]
uid_field_num = 72
uids = []
json_data_list = []
api_stat_url = 'https://product-stats.mirantis.com/api/v1/json/installation_info/'

def csv_get_data(csvfile):
    uidlist = []
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

def get_json_data(url, uidlist):
    json_list = []
    cnt = 0
    http = urllib3.PoolManager()
    for uid in uidlist:
        if cnt == 1:
            break
        resp = http.request('GET',url+uid)
        print url+uid
        json_list.append(resp.data)
        #parsed = json.dumps(resp.data)
        #print parsed['modification_date']
        sleep(0.2)
        cnt += 1
    return json_list

def parse_json(json_data):
    for json_ex in json_data:
        #print json.dump(jsonex)
        parsed = json.loads(json_ex)
        print parsed["modification_date"]
        print parsed["structure"]["fuel_release"]["release"]
        #print parsed["structure"]["clusters"]
        for cluster in parsed["structure"]["clusters"]:
            print cluster["status"]

uids = csv_get_data(rawcsv)
json_data_list = get_json_data(api_stat_url,uids)
parse_json(json_data_list)