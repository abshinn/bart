#!/usr/bin/env python3

import os, sys, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
import pdb


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
        self.date = xmlroot.find("date").text
        self.time = xmlroot.find("time").text
        self.traincount = xmlroot.find("tarincount").text
    def __str__(self):
        return "BART train count {self.date}; {self.time}\n{self.traincount} trains".format(self=self)

class count(object):
    def __init__(self, **params):
        self.root = APIquery(cmd = "count", params = params).getxmlroot()
        self.result = COUNTstruct(self.root)
    def __str__(self):
        return self.result.__str__()

class ELEVstruct:
    def __init__(self, xmlroot):
        self.date = xmlroot.find("date").text
        self.time = xmlroot.find("time").text
        self.bsa_id = []
        for bsa in xmlroot.findall("bsa id"):
            station = bsa.find("station").text
            typeof  = bsa.find("type").text
            descrip = bsa.find("description").text
            self.bsa_id.append({"station":station, "type":typeof, "descrip":descrip})
    def __str__(self):
        strResult = "BART Elevator Advisory {self.date}; {self.time}\n".format(self=self)
        for bsa in self.bsa_id:
            strResult += "Station: {}\n" \
                         "Description: [{}] {}\n".format(bsa["station"], bsa["descrip"])
        return strResult



# estimated time of departure: et
# http://api.bart.gov/api/etd.aspx?cmd=etd&orig=RICH

if __name__ == '__main__':
    #bartAPI(cmd = "bsa")
    print(bsa())

