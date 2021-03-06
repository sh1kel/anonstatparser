#!/usr/bin/python

import csv
import sys
import urllib3

urllib3.disable_warnings()
from time import sleep
import json

rawcsv = sys.argv[1]
uid_field_num = 72
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
            # print row[uid_field_num]
            uidlist.append(row[uid_field_num])
        rownum += 1
    f.close()
    return uidlist


def get_json_data(url, uidlist):
    json_list = []
    cnt = 0
    http = urllib3.PoolManager()
    for uid in uidlist:
        if cnt == 10:
            break
        resp = http.request('GET', url + uid)
        print url + uid
        json_list.append(resp.data)
        # parsed = json.dumps(resp.data)
        # print parsed['modification_date']
        sleep(0.2)
        cnt += 1
    return json_list


def parse_json(json_data):
    reports_list = []
    for json_ex in json_data:
        clusters_list = []
        parsed = json.loads(json_ex)
        for cluster in parsed["structure"]["clusters"]:
            if cluster["status"] != "operational":
                continue
            nodes_list = []
            for node in cluster["nodes"]:
                interfaces_list = []
                for interface in node["nic_interfaces"]:
                    interfaces_list.append(interface["id"])
                nodes_list.append(
                    {'name': node["platform_name"], 'vendor': node["manufacturer"], 'interfaces': interfaces_list})
            clusters_list.append(nodes_list)
        reports_list.append(
            {'release': parsed["structure"]["fuel_release"]["release"], 'date': parsed["modification_date"],
             'clusters': clusters_list})
    return reports_list


uids = csv_get_data(rawcsv)
json_data_list = get_json_data(api_stat_url, uids)
reports = parse_json(json_data_list)

for report in reports:
    print "### NEW REPORT ###"
    print "Fuel version:", report["release"]
    print "Validation date:", report["date"]
    for cluster in report["clusters"]:
        for node in cluster:
            print node["vendor"], node["name"]
