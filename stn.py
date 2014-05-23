#!/usr/bin/env python3 -tt

import os, sys, urllib.request, urllib.parse
import xml.etree.ElementTree as ET

def stn(orig="plza"):
    key = os.environ.get("BART_API_KEY")
    url = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig={}&dir=s&key={}'.format(orig,key)
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
        print(dest)
        for estimate in etd.findall('estimate'):
            minutes = estimate.find('minutes').text
            platform = estimate.find('platform').text
            direction = estimate.find('direction').text
            length = estimate.find("length").text
            if minutes == 'leaving':
                minutes += ' now'
            else:
                minutes = '{:>2} minutes'.format(minutes)
            print("{:>2} car train in {} on platform {}".format(length, minutes, platform))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        stn(orig = sys.argv[1])
    else:
        stn()
