#!/usr/bin/env python2.7 -tt -B

from datetime import datetime, timedelta
import urllib
import os
import argparse
import xml.etree.ElementTree as ET


class BARTbsa(object):
    """
    BART service advisories
    """

    def __init__(self):
        """see BART API documentation for information on BSA API queries"""

        self.key = os.environ.get("BART_API_KEY")

        if self.key == None:
            raise OSError("BART_API_KEY system variable not found.\n--> See README.md <--")

        self.url = "http://api.bart.gov/api/bsa.aspx?cmd=bsa&date=today&key={self.key}".format(self=self)

    def bsa(self):
        """call bart bsa api"""

        try:
            webpage = urllib.urlopen(self.url)
        except IOError as msg:
            print "IOError: {}\nCould not connect to API:\n\t{}".format(msg, self.url)
            return 

        tree = ET.parse(webpage)
        webpage.close()
        root = tree.getroot()

        print "Bart Service Status"

        for advisory in root.findall("bsa"):
            print "\t{}".format(advisory.find("description").text)

        print


class BARTstn(object):
    """
    list BART station information
    """

    def __init__(self, abbr=True, gtfs=False, city=False):
        """see BART API documentation for information on STN API queries"""

        self.abbr = abbr
        self.gtfs = gtfs
        self.city = city
        self.key = os.environ.get("BART_API_KEY")

        if self.key == None:
            raise OSError("BART_API_KEY system variable not found.\n--> See README.md <--")

        self.url = "http://api.bart.gov/api/stn.aspx?cmd=stns&key={self.key}".format(self=self)

    def stns(self):
        """call bart stn api"""

        try:
            webpage = urllib.urlopen(self.url)
        except IOError as msg:
            print "IOError: {}\nCould not connect to API:\n\t{}".format(msg, self.url)
            return 

        tree = ET.parse(webpage)
        webpage.close()
        root = tree.getroot()
  
        for station in root.findall("stations/station"):
            name = station.find("name").text
            abbr = station.find("abbr").text
            city = station.find("city").text
            lat = station.find("gtfs_latitude").text
            lon = station.find("gtfs_longitude").text

            if self.abbr:
                print "{:>5} -- {}".format(abbr, name)


class BARTetd(object):
    """
    BART estimated time of departure object
    
    Instantiate with origin station and direction kwargs, e.g.: 
        mission = BARTetd(origin="16th", direction="n") 

    Call BART API with etd method:
        mission.etd()

    Note: system variable BART_API_KEY is requred
    """

    def __init__(self, origin="plza", direction="s"):
        """see BART API documentation for information on ETD API queries"""

        self.origin = origin
        self.direction = direction
        self.key = os.environ.get("BART_API_KEY")

        if self.key == None:
            raise OSError("BART_API_KEY system variable not found.\n--> See README.md <--")

        self.url = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig={self.origin}&dir={self.direction}&key={self.key}".format(self=self)


    def etd(self):
        """given a station of origin and direction, list train departure times"""

        try:
            webpage = urllib.urlopen(self.url)
        except IOError as msg:
            print "IOError: {}\nCould not connect to API:\n\t{}".format(msg, self.url)
            return 

        tree = ET.parse(webpage)
        webpage.close()
        root = tree.getroot()

        try:
            time = root.find("time").text
        except AttributeError:
            print "\n".join(ET.tostringlist(root, method="text"))
            return

        station = root.find("station/name").text
        print "{} at {}".format(station, time)

        for etd in root.findall("station/etd"):
            dest = etd.find("destination").text
            for estimate in etd.findall("estimate"):
                minutes = estimate.find("minutes").text

                if minutes.lower() == "leaving":
                    minute_str = "now " + minutes

                else:
                    minute_str = "in {:>2} minutes".format(minutes)
                    if minute_str.strip() == "1":
                        minute_str = minute_str[:-1]

                    departure = datetime.strptime(time, "%H:%M:%S %p %Z") + timedelta(minutes=int(minutes))
                    depart_at = datetime.strftime(departure, "%H:%M")

                    minute_str = "{} [{}]".format(minute_str, depart_at)

                print "{:>18} train {:>13},".format(dest.replace(" ",""), minute_str)


def main():

    # assumes bart/ is in the user's home directory
    with open(os.path.expanduser("~/bart/stationkey.txt"), "r") as Skey:
        station_key = "station key\n" + "-"*11 + "\n" + Skey.read()

    parser = argparse.ArgumentParser(prog="bart", 
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=station_key)
    parser.add_argument(  "station", help="display schedule for given station")
    parser.add_argument("direction", help="display routes for a given direction")
    parser.add_argument("-t", "--tracker", help="tracker: repeat command every minute until keyboard interrupt", action="store_true")
    args = parser.parse_args()

    trains = BARTetd(origin = args.station, direction = args.direction)

    if args.tracker:
        while 1:
            os.system("clear")
            print "{} {}".format(args.station, args.direction)
            trains.etd()
            exitstatus = os.system("sleep 59")
            if exitstatus:
                break
    else:
        BARTbsa().bsa()
        trains.etd()


if __name__ == "__main__":
    main()
