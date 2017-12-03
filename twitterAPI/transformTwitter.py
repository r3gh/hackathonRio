import numpy as np
import pickle
import nltk
import urllib3
import json
from functions import *
from xml.etree import ElementTree
import calendar
if __name__ == "__main__":

    db_conn = db_open()

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
        file = io.open("../tweets/"+fname+".tweets", "rb")
        tweets = pickle.load(file)
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

                            if locality_map[locality]["type"] == "neighborhood":
                                neighborhood = locality_map[locality]["name"]
                                address = neighborhood
                            else:
                                address = (locality_map[locality]['name'] if locality_map[locality]['name'] != None  else 'Não Informado')
                                neighborhood = (locality_map[locality]['neighborhood'] if locality_map[locality]['neighborhood'] != None  else 'Não Informado')

                            if locality_map[locality]["latlong"] == None:
                                continue
                            #"type":violence_type


                            violence_json = {
                                "latitude": locality_map[locality]["latlong"][0],
                                "longitude": locality_map[locality]["latlong"][1],
                                "event_data": tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                "description": tweet.text,
                                "type": 1,
                                "neighborhood": neighborhood,
                                "username": tweet.user.screen_name,
                                "address":address,
                                "source": "Twitter",
                                "shift": shift(tweet.created_at.hour),
                                "day_of_week": calendar.day_name[tweet.created_at.weekday()]
                            }
                            print(shift(tweet.created_at.hour))
                            insert_violence(db_conn,violence_json)
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
                                results[locality]["tweet"] = []
                                results[locality]["tweet"].append({"username":tweet.user.screen_name,"date":tweet.created_at,"text":tweet.text, "type_violence": violence_type})

                            results[locality]["latlong"] = locality_map[locality]["latlong"]

                            break
                    break


    db_close(db_conn)
    #print(results)
