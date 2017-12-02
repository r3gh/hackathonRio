import numpy as np
import pickle
import nltk

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

if __name__ == "__main__":
    
    filesToRead = ['alertaAssaltoRJ.pkl']
    
    stealKeywords= stemmingArray(['Roubo', 'Assalto'])
    results = {}
    
    for fname in filesToRead:
        with open(fname,'rb') as f:
            tweets = pickle.load(f)
            localitys = readLocality()
            for tweet in tweets:
                words = stemmingArray(tweet.text.split(' '))
                for word in words:
                    if(word in stealKeywords):
                        #print("%s = %s"%(word,stealKeywords))
                        #print(tweet.text)
                        for locality in localitys:
                            
                            if(locality in tweet.text):
                                try:
                                    results[locality] = results[locality] + 1
                                except:
                                    results[locality] = 1
                        

                                
                                break
                        break
                    
                    
    
    print(results)
                    
                
            
                                