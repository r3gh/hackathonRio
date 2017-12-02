import numpy as np
import pickle
import nltk
import urllib3
import json
from xml.etree import ElementTree

def readLocality(locality_path = "../dataset/locality_ds.json" ):
    with open(locality_path, encoding='utf-8') as json_file:
        text = json_file.read()
        locality_map = json.loads(text)

    return locality_map

def stemmingArray(words):
    stemmer = nltk.stem.RSLPStemmer()
    stemWords = []

    for word in words:
        word = word.replace("\n","")

        try:
            if(word != ""):
                stemWords.append(stemmer.stem(word))
        except:
            print("Error in word = %s"%(word))

    return stemWords

def comparelocality(locality,text):
    if(locality in text):
        return True
    else:
        return False

if __name__ == "__main__":

    
    stealKeywords= stemmingArray(['Roubo', 'Assalto'])

    locality_map = readLocality()

    results = {}

    for fname in twitterTrackings:
        with open(fname,'rb') as f:
            tweets = pickle.load(f)
            localitys = readLocality()
            for tweet in tweets:
                words = stemmingArray(tweet.text.split(' '))
                for word in words:
                    if(word in stealKeywords):
                        #print("%s = %s"%(word,stealKeywords))
                        #print(tweet.text)
                        for locality in locality_map:
                            if(comparelocality(locality_map[locality]["name"], tweet.text)):
                                print ("\n####")
                                print ("Tweet: " + tweet.text)
                                print ("Lat-long: " + str(locality_map[locality]["latlong"]))
                                print ("Detected locality: " + locality_map[locality]["name"])
                                print ("#####\n")
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



    #print(results)
