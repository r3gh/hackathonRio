import numpy as np
import pickle
import nltk
import urllib3
import json
from functions import *
from xml.etree import ElementTree



if __name__ == "__main__":


    steal_words_syns = {
        "tiroteio":["tiroteio", "tiro", "bomba", "baleado", "bala", "pipoco", "perdida", "disparo"],
        "roubo": ["roubo","assalto","furto","carga","bater carteira","grupo", "tentativa","arrombamento"],
        "arrastao":["arrastao"],
        "sequestro":["sequestro", "relampago"],
        "estupro":["estupro"],
        "agressao":["agressao","insulto"],
        "homicidio": ["homicidio","morte", "morreu", "assassinato"],
        "outro": ["terror","trombadinha","pivete","suspeito","crime","violencia","trombadinha"]
    }


    reverse_map = {}
    stemming_words = []
    for key in steal_words_syns:
        for word in steal_words_syns[key]:
            stemming_words.append(word)
            reverse_map[word] = key


    stealKeywords = stemmingArray_keep_original(stemming_words)
    locality_map = readLocality()

    results = {}


    for fname in twitterTrackings:
        with open("../tweets/"+fname+".tweets",'rb') as f:
            tweets = pickle.load(f)
            localitys = readLocality()
            for tweet in tweets:
                words = stemmingArray(tweet.text.split(' '))
                for word in words:
                    if (word in stealKeywords):

                        #print("%s = %s"%(word,stealKeywords))
                        #print(tweet.text)
                        for locality in locality_map:
                            if(comparelocality(locality_map[locality]["name"], tweet.text)):
                                woriginal = norm(stealKeywords[word])
                                violence_type = reverse_map[woriginal]

                                print ("\n####")
                                print ("Tweet: " + tweet.text)
                                print ("User: " + tweet.user.screen_name)
                                print ("Lat-long: " + str(locality_map[locality]["latlong"]))
                                print ("Detected locality: " + locality_map[locality]["name"])
                                print ("Violence Type: " + violence_type)
                                print ("#####\n")

                                try:
                                    results[locality]
                                except:
                                    results[locality] = {}
                                try:
                                    results[locality]["size"] += 1
                                except:
                                    results[locality]["size"]  = 1



                                try:
                                    results[locality]["tweet"].append({"username":tweet.user.screen_name, "date":tweet.created_at,"text":tweet.text, "type_violence": violence_type})
                                except:
                                    print(word)
                                    results[locality]["tweet"] = []
                                    results[locality]["tweet"].append({"username":tweet.user.screen_name,"date":tweet.created_at,"text":tweet.text, "type_violence": violence_type})

                                results[locality]["latlong"] = locality_map[locality]["latlong"]

                                break
                        break



    #print(results)
