import tweepy
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

'''
    Variables
'''
twitterTrackings = ['AlertaAssaltoRJ','alertario24hrs','UNIDOSPORJPA','RJ_OTT','CaosNoRio','InformeRJO','OperacoesRio','AndeSeguroApp']

def readLocality(locality_path = "../dataset/locality_ds.json" ):
    with open(locality_path, encoding='utf-8') as json_file:
        text = json_file.read()
        locality_map = json.loads(text)

    return locality_map

def comparelocality(locality,text):
    if(locality in text):
        return True
    else:
        return False


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
    locality_ds = {}
    file = io.open(locality_path, "r")
    localitys = file.readlines()
    for locality in localitys:
        key = clean_str(locality)
        if key not in locality_ds:
            locality_ds[key] = dict()
            locality_ds[key]["type"] = "neighborhood"
            locality_ds[key]["latlong"] = getLatLong(locality.strip())
            locality_ds[key]["name"] = locality.strip()

    return locality_ds

def readStreets(locality_ds,locality_path="../dataset/LinkedGeoData.csv"):
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

def stemmingArray_keep_original(words):
    stemmer = nltk.stem.RSLPStemmer()
    stemWords = {}

    for word in words:
        word = norm(word.replace("\n","").lower())

        try:
            if(word != ""):
                stemWords[stemmer.stem(word)] = word
        except:
            print("Error in word = %s"%(word))

    return stemWords

def stemmingArray(words):
    stemmer = nltk.stem.RSLPStemmer()
    stemWords = []

    for word in words:
        word = norm(word.replace("\n","").lower())

        try:
            if(word != ""):
                stemWords.append(stemmer.stem(word))
        except:
            print("Error in word = %s"%(word))

    return stemWords


class StreamTwitter(tweepy.StreamListener):

    def on_status(self, tweet):
        print(tweet.text)
        stealKeywords= stemmingArray(['Roubo', 'Assalto'])
        words = stemmingArray(tweet.text.split(' '))
        for word in words:
            if(word in stealKeywords):
                #print("%s = %s"%(word,stealKeywords))
                #print(tweet.text)
                for locality in localitys:

                    if(comparelocality(locality, tweet.text)):
                        try:
                            results[locality]
                        except:
                            results[locality] = {}
                        try:
                            results[locality]["size"] = results[locality]["size"] + 1
                        except:
                            results[locality]["size"]  = 1

                        try:
                            results[locality]["tweet"].append({"date":tweet.created_at,"text":tweet.text})
                        except:
                            results[locality]["tweet"] = []


                        break
                break
