import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import numpy as np
import pickle
  
consumer_key = 'fFMLQkJnhV9QnDPiNaS8UCo7c'
consumer_secret = 'titJyd6Ffzfqgou4nK9Msx0zPiZiFete4yh56gAPDHYeDakByx'
access_token = '47490589-KpZY6dxjpIvGHSnZLawK7jAoIERnprYxgwVmGGPHr'
access_secret = 'QC0fdR6CqSOoq1v8s338WKAsqcyLPhiYYz04yh3trP9Um'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

stuff = api.user_timeline(screen_name = 'AlertaAssaltoRJ', count = 1000, include_rts = True)
with open("alertaAssaltoRJ.pkl",'wb') as f:
    pickle.dump(stuff, f)