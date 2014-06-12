#!/usr/bin/env python2.7 -tt

import urllib
# import requests # <-- see if faster than urllib
import os, sys
# import os, sys, urllib.request, urllib.parse
import xml.etree.ElementTree as ET

def stn(orig = "plza", direct="s"):
    # obtain system variable BART_API_KEY
    key = os.environ.get("BART_API_KEY")

    # build url
    url = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig={}&dir={}&key={}'.format(orig, direct, key)

    with urllib.urlopen(url) as webpage:
        tree = ET.parse(webpage)
        root = tree.getroot()

#     try:
#         webpage = urllib.urlopen(url)
#     except IOError: 
#         sys.stderr.write("Couldn't connect to {}\n".format(url))
#         return 
#     except ValueError as ValueMsg:
#         sys.stderr.write("Value Error: {}\n".format(ValueMsg))
#         return

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
