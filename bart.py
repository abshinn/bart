#!/usr/bin/env python3

# estimated time of departure
# http://api.bart.gov/api/etd.aspx?cmd=etd&orig=RICH
import xml.etree.ElementTree as ET

    #tree = ET.parse('route.xml')
    #root = tree.getroot()
    #for route in root.findall('routes/route'):
    #    name = route.find('name').text
    #    abbr = route.find('abbr').text
    #    routeID = route.find('routeID').text
    #    print name, abbr, routeID

class bartAPI(object):
    def __init__(self, cmd = "", **params):
        envkey = os.environ.get("BART_API_KEY")
        if envkey:
            self.key = envkey
        else:
            print("BART_API_KEY environment variable does not exist")
        self.cmd = cmd
        self.parameters = params
        self.querystr = urllib.parse.urlencode(self.parameters)
        self.response, self.tree = self.query()
        if   cmd ==   "bsa": self.bsa()
        elif cmd == "count": self.count()
        elif cmd ==  "elev": self.elev()
        elif cmd ==  "help": self.hlp()
        elif cmd ==   "ver": self.ver()
        else: print("NO cmd GIVEN")
    def bsa(self):
        root = self.tree.getroot()
        date = root.find('date').text
        time = root.find('time').text
        print(date, time)
        for bsa in root.findall('bsa'):
            station = bsa.find('station').text
            typeadv = bsa.find('type').text
            descrip = bsa.find('description').text
            #posted = bsa.find('posted').text
            #expire = bsa.find('expires').text
            print(station, typeadv)
            print(descrip)
            #print posted, expire
    def count(self):
        pass
    def elev(self):
        pass
    def hlp(self):
        pass
    def ver(self):
        pass
    def query(self):
        """query BART API at: http://api.bart.gov/api/stn.aspx?"""
        url = "http://api.bart.gov/api/stn.aspx?cmd={self.cmd}&{self.querystr}".format(self=self)
        print("Querying BART with: {}".format(url))
        with urllib.request.urlopen(url) as BART:
            response = BART.read()
            tree = ET.parse(response)
        return response, tree

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

#if __name__ == '__main__':
#    advisories()
#    main()


