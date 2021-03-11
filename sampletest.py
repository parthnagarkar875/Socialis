import tweepy
# import settings
# import credentials




import settings
# import mysql.connector
import pandas as pd
import time
import itertools
import math
# import credentials
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
#%matplotlib inline
import plotly.express as px
import datetime
from IPython.display import clear_output

import plotly.offline as py
import plotly.graph_objs as go
from plotly.subplots import make_subplots
# py.init_notebook_mode()

import re
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sqlite3
import country_converter as coco
import numpy as np
import collections
import warnings
import tweepy









#override tweepy.StreamListener to add logic to on_status


# class MyStreamListener(tweepy.StreamListener):


#     def get_full_text(self, status):
#         final_text=str()

#         # Get full text from a tweet
#         try:
#             if hasattr(status, 'retweeted_status') and hasattr(status.retweeted_status, 'extended_tweet'):
#                 final_text=status.retweeted_status.extended_tweet['full_text']
#                 # print("Extended Tweet:", status.retweeted_status.extended_tweet['full_text'])
#             elif hasattr(status, 'extended_tweet'):
#                 final_text=status.extended_tweet['full_text']
#                 # print("Extended Tweet:", status.extended_tweet['full_text'])                
#             else:
#                 final_text=status.text
#                 # print("Printing Full text", status.text)
#         except AttributeError as e:
#             pass
        
#         return final_text

#     def on_status(self, status):
#         final_text=self.get_full_text(status)
#         if final_text[:2] != 'RT':
#             print("https://twitter.com/"+status.user.screen_name+"/status/"+status.id_str, "\t", status.favorite_count)
#             # print(final_text)

# auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
# auth.set_access_token(credentials.access_token, credentials.access_token_secret)    
# api = tweepy.API(auth,wait_on_rate_limit=True)

# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener, tweet_mode='extended')

# try:
#     myStream.filter(languages=["en"], track = settings.TRACK_WORDS)
# except Exception as e:
#     print("Error. Restarting Stream.... Error: ")
#     print(e.__doc__)
#     print(e.message)





# import multiprocessing
# import os
# from time import sleep
# import threading 
# import time


# def odd(msg):
#     print("Executing our P1 Task with {} on Process: {}".format(msg, os.getpid()))    
#     for i in range(1,10,2):
#         print("Odd number: ",i)
                

# def even():
#     print("Executing our p2 Task on Process: {}".format(os.getpid()))
#     # sleep(5)
#     for i in range(2,10,2):
#         print("Even number: ",i)


# if __name__ == "__main__": 

#     start_time = time.time()
   
#     p1 = multiprocessing.Process(target=odd, args=("In Process",)) 
#     p2 = multiprocessing.Process(target=even) 

#     # t1 = threading.Thread(target=odd, args=("In Process",)) 
#     # t2 = threading.Thread(target=even) 

#     # starting process 1 
#     p1.start() 
#     # starting process 2 
#     p2.start() 
#     odd("Out of Process")
#     # wait until process 1 is finished 
#     # p1.join() 
#     # wait until process 2 is finished 
#     p1.join()
#     p2.join() 

#     # both processes finished 
#     print("Done!") 
#     print("--- %s seconds ---" % (time.time() - start_time))






# date_since = "2021-03-01"

# # authorization of consumer key and consumer secret 
# auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret) 

# # set access to user's access key and access secret 
# auth.set_access_token(credentials.access_token, credentials.access_token_secret) 

# # calling the api 
# api = tweepy.API(auth) 

# # the ID of the status 
# query="(facebook) -facebook.com min_faves:500"

# # fetching the status 
# status = api.search(query, lang="en", since=date_since, count=1000) 

# like=dict()
# for i in status:
#     url="https://twitter.com/"+i.user.screen_name+"/status/"+i.id_str
#     like[url]=i.favorite_count

# sort_orders = sorted(like.items(), key=lambda x: x[1], reverse=True)
# print(sort_orders)



# import snscrape.modules.twitter as sntwitter
# import pandas as pd

# # Creating list to append tweet data to
# tweets_list2 = []

# # Using TwitterSearchScraper to scrape data and append tweets to list
# for i,tweet in enumerate(sntwitter.TwitterSearchScraper('its the elephant since:2020-06-01 until:2020-07-31').get_items()):
#     if i>500:
#         break
#     tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

# # Creating a dataframe from the tweets list above
# tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
















