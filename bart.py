#!/usr/bin/env python3

# estimated time of departure
# http://api.bart.gov/api/etd.aspx?cmd=etd&orig=RICH
import os, sys, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
import pdb
    #tree = ET.parse('route.xml')
    #root = tree.getroot()
    #for route in root.findall('routes/route'):
    #    name = route.find('name').text
    #    abbr = route.find('abbr').text
    #    routeID = route.find('routeID').text
    #    print name, abbr, routeID


envkey = os.environ.get("BART_API_KEY")
if envkey:
    key = envkey
else:
    print("BART_API_KEY environment variable does not exist")
    sys.exit()

def query(cmd, querystr):
    """query BART API at: http://api.bart.gov/api/{cmd}.aspx?"""
    url = "http://api.bart.gov/api/{}.aspx?{}".format(cmd, querystr)
    print("Querying BART with: {}".format(url))
    with urllib.request.urlopen(url) as BART:
        #response = BART.read()
        tree = ET.parse(BART)
    return tree

class APIquery(object):
    def __init__(self, **params):
        self.parameters = params
        self.cmd = self.parameters["cmd"]
        self.key = key 
        self.parameters["key"] = self.key
        self.querystr = self._getquerystr()
    def _getquerystr(self):
        return urllib.parse.urlencode(self.parameters)
    def getxmlroot(self):
        """query BART API at: http://api.bart.gov/api/{cmd}.aspx?"""
        url = "http://api.bart.gov/api/{self.cmd}.aspx?{self.querystr}".format(self=self)
        print("Querying BART with: {}".format(url))
        with urllib.request.urlopen(url) as BART:
            #response = BART.read()
            tree = ET.parse(BART)
        return tree.getroot()

class BSAstruct:
    def __init__(self, xmlroot):
        self.date = xmlroot.find("date").text
        self.time = xmlroot.find("time").text
        self.advisory = []
        for bsa in xmlroot.findall("bsa"):
            station = bsa.find("station").text
            descrip = bsa.find("description").text
            try:
                typeadv = bsa.find("type").text
            except AttributeError:
                typeadv = None
            self.advisory.append({"station":station, "descrip":descrip, "type":typeadv})
    def __str__(self):
        strResult = "BART Service Advisory {self.date}; {self.time}\n".format(self=self)
        for bsa in self.advisory:
            strResult += "Station: {}\n" \
                         "Description: [{}] {}\n".format(bsa["station"], bsa["type"], bsa["descrip"])
        return strResult

class bsa(object):
    def __init__(self, **params):
        self.root = APIquery(cmd = "bsa", params = params).getxmlroot()
        self.result = BSAstruct(self.root)
    def __str__(self):
        return self.result.__str__()

class COUNTstruct:
    def __init__(self, xmlroot):
        pass

class count(object):
    def __init__(self, **params):
        pass

#class bsa(object):
#    def __init__(self, **params):
#        self.cmd = "bsa"
#        params["cmd"] = self.cmd
#        params["key"] = key
#        self.parameters = params
#        self.querystr = urllib.parse.urlencode(self.parameters)
#        root = query(self.cmd, self.querystr).getroot()
#        date = root.find("date").text
#        time = root.find("time").text
#        print(date, time)
#        for advisory in root.findall("bsa"):
#            station = advisory.find("station").text
#            descrip = advisory.find("description").text
#            try:
#                typeadv = advisory.find("type").text
#            except AttributeError:
#                typeadv = None
#            print( "BART Service Advisory\n" \
#                   "Type: {}; Station: {}\n" \
#                   "Description: {}".format(typeadv, station, descrip) )

#class bartAPI(object):
#    def __init__(self, cmd = "", **params):
#        envkey = os.environ.get("BART_API_KEY")
#        if envkey:
#            self.key = envkey
#        else:
#            print("BART_API_KEY environment variable does not exist")
#            sys.exit()
#        self.cmd = cmd
#        params["key"] = self.key
#        params["cmd"] = self.cmd
#        self.parameters = params
#        self.querystr = urllib.parse.urlencode(self.parameters)
#        self.root = self.query().getroot()
#        if   cmd ==   "bsa": self.bsa()
#        elif cmd == "count": self.count()
#        elif cmd ==  "elev": self.elev()
#        elif cmd ==  "help": self.hlp()
#        elif cmd ==   "ver": self.ver()
#        else: print("NO cmd GIVEN")
#    def bsa(self):
#        date = self.root.find('date').text
#        time = self.root.find('time').text
#        print(date, time)
#        for advisory in self.root.findall('bsa'):
#            station = advisory.find('station').text
#            descrip = advisory.find('description').text
#            try:
#                typeadv = advisory.find('type').text
#            except AttributeError:
#                typeadv = None
#            print( "BART Service Advisory\nStation: {}; Type: {}\nDescription: {}".format(station, typeadv, 
#                                                                                          descrip) )
#    def count(self):
#        pass
#    def elev(self):
#        pass
#    def hlp(self):
#        pass
#    def ver(self):
#        pass
#    def query(self):
#        """query BART API at: http://api.bart.gov/api/{cmd}.aspx?"""
#        url = "http://api.bart.gov/api/{self.cmd}.aspx?{self.querystr}".format(self=self)
#        print("Querying BART with: {}".format(url))
#        with urllib.request.urlopen(url) as BART:
#            #response = BART.read()
#            tree = ET.parse(BART)
#        return tree

#def stations():
#    import urllib
#    key = 'TVKZ-JUDR-UTYY-VMGK' # adam.b.shinn@gmail.com API key
#    url = 'http://api.bart.gov/api/stn.aspx?cmd=stns&key={}'.format(key)
#    try:
#        webpage =  urllib.urlopen(url)
#    except IOError:
#        print "not connected"
#        return
#    tree = ET.parse(webpage)
#    webpage.close()
#    root = tree.getroot()
#    for station in root.findall('stations/station'):
#        name = station.find('name').text
#        abbr = station.find('abbr').text
#        city = station.find('city').text
#        gtfs_latitude = station.find('gtfs_latitude').text
#        gtfs_longitude = station.find('gtfs_longitude').text
#        print abbr, name

#def advisories():
#    import urllib
#    #key = 'MW9S-E7SL-26DU-VV8V' # whereisbart API key
#    key = 'TVKZ-JUDR-UTYY-VMGK' # adam.b.shinn@gmail.com API key
#    url = 'http://api.bart.gov/api/bsa.aspx?cmd=bsa&date=today&key={}'.format(key)
#    try:
#        webpage =  urllib.urlopen(url)
#    except IOError:
#        print "not connected"
#        return
#    tree = ET.parse(webpage)
#    webpage.close()
#    root = tree.getroot()
#    date = root.find('date').text
#    time = root.find('time').text
#    print date, time
#    for bsa in root.findall('bsa'):
#        station = bsa.find('station').text
#        typeadv = bsa.find('type').text
#        descrip = bsa.find('description').text
#        #posted = bsa.find('posted').text
#        #expire = bsa.find('expires').text
#        print station, typeadv
#        print descrip
#        #print posted, expire

#def main():
#    import urllib
#    #key = 'MW9S-E7SL-26DU-VV8V' # whereisbart API key
#    key = 'TVKZ-JUDR-UTYY-VMGK' # adam.b.shinn@gmail.com API key
#    url = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig=PLZA&dir=s&key={}'.format(key)
#    #url = 'http://api.bart.gov/api/stn.aspx?cmd=stns&key={}'.format(key)
#    try:
#        webpage =  urllib.urlopen(url)
#    except IOError:
#        print "not connected"
#        return
#    #xml = str(webpage.read())
#    tree = ET.parse(webpage)
#    webpage.close()
#    root = tree.getroot()
#    date = root.find('date').text
#    time = root.find('time').text
#    station = root.find('station/name').text
#    print station, date, time
#    for etd in root.findall('station/etd'):
#        dest = etd.find('destination').text
#        print dest
#        for estimate in etd.findall('estimate'):
#            minutes = estimate.find('minutes').text
#            platform = estimate.find('platform').text
#            direction = estimate.find('direction').text
#            length = estimate.find("length").text
#            if minutes == 'Leaving':
#                minutes += ' now'
#            else:
#                minutes = '{:>2} minutes'.format(minutes)
#            print "{:>2} car train in {} on platform {}".format(length, minutes, platform)
#        #name = etd.find('name').text
#        #abbr = etd.find('abbr').text
#        #city = station.find('city').text
#        #print name, abbr
#    #webpage.close()

#if 0:
#    from xml.dom.minidom import parse
#    dom = parse('route.xml')
#    xmlTag = dom.getElementsByTagName('route')
#    for Tag in xmlTag:
#        print Tag.toxml()

if __name__ == '__main__':
    #bartAPI(cmd = "bsa")
    print(bsa())

