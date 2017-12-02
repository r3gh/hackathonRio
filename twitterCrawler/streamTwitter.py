import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import numpy as np
import pickle
import json
import tweepy
import numpy as np
import pickle
import nltk
import urllib3

def readLocality(locality_path = "../dataset/localidades.csv" ):
    file = open(locality_path, "r")
    localitys = file.readlines()
    localitys = [locality.replace("\n","").strip()  for locality in localitys] 
    return localitys
    
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
  
tokenFile = open("tokens", "r")
tokensString = (tokenFile.read())
tokens = json.loads(tokensString )

consumer_key = tokens['consumer_key']
consumer_secret = tokens['consumer_secret']
access_token = tokens['access_token']
access_secret = tokens['access_secret']
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

stream_listener = StreamTwitter()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=['AlertaAssaltoRJ','alertario24hrs','UNIDOSPORJPA'])


localitys = readLocality()
            
