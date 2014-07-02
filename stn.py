#!/usr/bin/env python2.7 -tt

import urllib
import os, sys
import argparse
import xml.etree.ElementTree as ET
# import pdb


def stn(origin="plza", direction="s"):
    # obtain system variable BART_API_KEY
    key = os.environ.get("BART_API_KEY")

    # build url
    url = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig={}&dir={}&key={}'.format(origin, direction, key)

    try:
        webpage = urllib.urlopen(url)
    except IOError as msg:
        sys.stderr.write("IOError: {}\nCould not connect to API:\n\t{}".format(msg, url))
        return 
    tree = ET.parse(webpage)
    webpage.close()
    root = tree.getroot()

    date = root.find('date').text
    time = root.find('time').text
    time = time[:-3]
    station = root.find('station/name').text
    print "{} at {}".format(station, time)

    for etd in root.findall('station/etd'):
        dest = etd.find('destination').text
        for estimate in etd.findall('estimate'):
            minutes = estimate.find('minutes').text
            platform = estimate.find('platform').text
            direction = estimate.find('direction').text
            length = estimate.find('length').text
            if minutes.lower() == 'leaving':
                minutes = 'now ' + minutes
            else:
                intmins = int(minutes)
                minutes = 'in {:>2} minutes'.format(minutes)
                if intmins == 1:
                    minutes = minutes[:-1]
#             print("{:>2} car {} train in {} on platform {},".format(length, dest, minutes, platform))
            print("{:>2} car {:<20} train {},".format(length, dest, minutes))


if __name__ == "__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument(  "station", help="display schedule for given station")
    parser.add_argument("direction", help="display routes for a given direction")
    parser.add_argument("-t", "--tracker", help="tracker: repeat command every minute until keyboard interrupt", action="store_true")
    args = parser.parse_args()
    if args.tracker:
        try:
            while 1:
                os.system("clear")
                print "{} {}".format(args.station, args.direction)
                stn(origin = args.station, direction = args.direction)
                exitstatus = os.system("sleep 59")
                if exitstatus:
                    break
        except msg:
            print msg
            print "catch keyboard error?"
            pass
    else:
        stn(origin = args.station, direction = args.direction)
