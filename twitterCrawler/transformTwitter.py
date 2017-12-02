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

def comparelocality(locality,text):
    if(locality in text):
        return True
    else:
        return False
    


if __name__ == "__main__":
    
    
    '''
        Variables
    '''
    filesToRead = ['AlertaAssaltoRJ','alertario24hrs','UNIDOSPORJPA']    
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
                    
                    
    
    print(results)
                    
                
            
                                