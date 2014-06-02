#!/usr/bin/env python3 -tt

import os, sys, urllib.request, urllib.parse
import xml.etree.ElementTree as ET

def stn(orig = "plza", direct="s"):
    key = os.environ.get("BART_API_KEY")
    url = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig={}&dir={}&key={}'.format(orig,direct,key)
    with urllib.request.urlopen(url) as webpage:
        tree = ET.parse(webpage)
    root = tree.getroot()
    date = root.find('date').text
    time = root.find('time').text
    time = time[:-3]
    station = root.find('station/name').text
    print(station, date, time)
    for etd in root.findall('station/etd'):
        dest = etd.find('destination').text
#         print(dest)
        for estimate in etd.findall('estimate'):
            minutes = estimate.find('minutes').text
            platform = estimate.find('platform').text
            direction = estimate.find('direction').text
            length = estimate.find("length").text
            if minutes.lower() == 'leaving':
                minutes = 'now ' + minutes
            else:
                intmins = int(minutes)
                minutes = 'in {:>2} minutes'.format(minutes)
                if intmins == 1:
                    minutes = minutes[:-1]
#             print("{:>2} car {} train in {} on platform {},".format(length, dest, minutes, platform))
            print("{:>2} car {} train {},".format(length, dest, minutes))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        stn(orig = sys.argv[1])
    elif len(sys.argv) == 3:
        stn(orig = sys.argv[1], direct = sys.argv[2])
    else:
        stn(orig = "plza", direct = "s")
