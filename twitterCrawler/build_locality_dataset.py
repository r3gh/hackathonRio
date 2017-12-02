import numpy as np
import pickle
import nltk
import csv
import re
import json
import io
import codecs
from unicodedata import normalize
import urllib3
from xml.etree import ElementTree

locality_ds = {}

def getLatLong(address):
    try:
        convertedAdress = address.replace(" ","+")
        convertedAdress = norm(convertedAdress + "+Rio+de+Janeiro")
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://nominatim.openstreetmap.org/search?q=%s&format=xml&polygon=1&addressdetails=1'%(convertedAdress));
        htmlData = str(r.data)
        addressXmls = ElementTree.fromstring(htmlData)
        lat = float(addressXmls[0].attrib["lat"]) #Recover latitude from first address  XML response
        lon = float(addressXmls[0].attrib["lon"]) #Recover latitude from first address  XML response
        print (convertedAdress + " " + str([lat,lon]))
        return [lat,lon]
    except:
        print ("### ERROR : " + address)
        return None


def norm(s):
    try:
        s = normalize('NFKD', s).encode('ASCII','ignore').decode('ASCII')
    except:
        s = s.decode('utf-8')
        s = normalize('NFKD', s).encode('ASCII','ignore').decode('ASCII')
    return s

def clean_str(s):
    s = norm(s)
    s = re.sub(' ','_', s.lower() )
    s = re.sub('\W+','', s )
    return s

def readNeighborhoods(locality_path = "../dataset/localidades.csv" ):
    file = io.open(locality_path, "r")
    localitys = file.readlines()
    for locality in localitys:
        key = clean_str(locality)
        if key not in locality_ds:
            locality_ds[key] = dict()
            locality_ds[key]["type"] = "neighborhood"
            locality_ds[key]["latlong"] = getLatLong(locality.strip())
            locality_ds[key]["name"] = locality.strip()

def readStreets(locality_path="../dataset/LinkedGeoData.csv"):
    file = io.open(locality_path, "r")
    lines = file.readlines()
    for line in lines:
        row = line.split('\t')

        if len(row) <= 1:
            continue

        for i in range(0, len(row)):
            row[i] = row[i].replace("\n","")
            row[i] = row[i].replace("\"","")
            row[i] = row[i].strip()

        key = clean_str(row[2])
        if key not in locality_ds:
            locality_ds[key] = dict()
            locality_ds[key]["type"] = "street"
            locality_ds[key]["name"] = row[2].strip()
            if row[1] == '':
                locality_ds[key]["neighborhood"] = None
            else:
                locality_ds[key]["neighborhood"] = row[1].strip()

            if len(row) > 3:
                locality_ds[key]["latlong"] = [float(row[3]), float(row[4])]
            else:
                locality_ds[key]["latlong"] = getLatLong(row[2].strip())



if __name__ == "__main__":
    readNeighborhoods()
    readStreets()
    with open('../dataset/locality_ds.json', 'w+') as f:
        f.write(json.dumps(locality_ds,indent=2))
