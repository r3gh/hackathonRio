import psycopg2
from datetime import datetime
from datetime import date
import calendar
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
import traceback

'''
    Variables
'''
twitterTrackings = ['AlertaAssaltoRJ','alertario24hrs','UNIDOSPORJPA','RJ_OTT','CaosNoRio','InformeRJO','OperacoesRio','AndeSeguroApp']


def db_open():
    try:
       db_conn = psycopg2.connect("dbname='hackathon' user='postgres' host='10.20.3.181' password='123456'")
       return db_conn
    except:
       print ("I am unable to connect to the database")
       return false


def db_close(db_conn):
    db_conn.close()

def shift(hour):
    if hour > 0 and hour < 6:
      return 'dawn'
    elif hour >=6  and hour < 12:
      return 'morning'
    elif hour >= 12 and hour < 18:
      return 'afternoon'
    else:
      return 'night'

def insert_violence(db_conn,violence):
    cur = db_conn.cursor()
    # event_data, source, lat_long
    queryStr = "INSERT INTO violence_data(latitude, longitude, event_data, neighborhood, username, type, description, address, source, day_of_week, shift) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    print (queryStr)

    try:
        print (violence['latitude'],violence["longitude"],violence["event_data"],violence["neighborhood"], violence["username"], violence["type"], violence['description'], violence['address'], violence['source'], violence['day_of_week'], violence['shift'])
        cur.execute(queryStr,(violence['latitude'],violence["longitude"],violence["event_data"],violence["neighborhood"], violence["username"], violence["type"], violence['description'], violence['address'], violence['source'], violence['day_of_week'], violence['shift']))
        db_conn.commit()
    except psycopg2.Error as e:
        print(e)
        print "Skiping (may be because it's unique)" + violence['latitude'],violence["longitude"],violence["event_data"]
    cur.close()

def readLocality(locality_path = "../dataset/locality_ds.json" ):
    file = io.open(locality_path, "r")
    text = file.read()
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
        htmlData = str(r.data.decode('utf-8'))
        addressXmls = ElementTree.fromstring(htmlData)
        lat = float(addressXmls[0].attrib["lat"]) #Recover latitude from first address  XML response
        lon = float(addressXmls[0].attrib["lon"]) #Recover latitude from first address  XML response
        print (convertedAdress + " " + str([lat,lon]))
        return [lat,lon]
    except:
        traceback.print_exc()
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
