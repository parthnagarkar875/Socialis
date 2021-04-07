import sqlite3
import pandas as pd
import country_converter as coco
from geopy.geocoders import Nominatim
import settings
import datetime



conn1 = sqlite3.connect('twitter.db')
print("Opened the database successfully")

conn = conn1.cursor()


# df = pd.read_sql("select * from Facebook LIMIT 5", conn1)
# print(df.head())
# # conn.execute('''CREATE TABLE SAMPLE
# #             (ID INT PRIMARY KEY NOT NULL,
# #              NAME TEXT NOT NULL
# #             );''')

# # # conn.execute("INSERT INTO SAMPLE (ID,NAME) \
# # #       VALUES (2, 'Parth')")

# # # # conn1.commit()
# timenow = (datetime.datetime.utcnow() - datetime.timedelta(hours=0, minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
    # query = "SELECT * FROM {} WHERE created_at <= '{}' " .format(settings.TABLE_NAME, timenow)
# query = "SELECT * FROM {} " .format(settings.TABLE_NAME)
# output=conn.execute(query)


# i = 0
# for row in output:
#    if i>20000:
#       break
#    else:
#       print("User Location: ",row[8])

#       i = i+1

# iso2_codes = coco.convert(names='Nono', to='ISO2')
# print(iso2_codes)

# if iso2_codes=='not found':
#     print("Yes")
# dataframe = pd.read_sql("""SELECT * FROM FACEBOOK """, con=conn1)
# # return your first five rows
# for i in dataframe['named_ent']:
#     print(i)


# print(len(dataframe['user_location']))

# conn.execute("DROP TABLE FACEBOOK")
# # # # conn.execute("DELETE from SAMPLE where ID = 1")

# # result=output.fetchall()
# # print(result)

# # # for row in output:
# # #     print("ID:", row[0])
# # #     print("Name:", row[1])
    

# conn1.commit()
# conn1.close()

# # import the module 
# import tweepy 
# import credentials

# # assign the values accordingly 

# # authorization of consumer key and consumer secret 
# auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret) 

# # set access to user's access key and access secret 
# auth.set_access_token(credentials.access_token, credentials.access_token_secret) 

# # calling the api 
# api = tweepy.API(auth) 

# # the ID of the status 
# id = 1358086426592751616

# # fetching the status 
# status = api.get_status(id, tweet_mode='extended') 

# # # printing the information

# # try:
# #    if hasattr(status, 'retweeted_status') and hasattr(status.retweeted_status, 'extended_tweet'):
# #          print("Extended tweet:", status.retweeted_status.extended_tweet['full_text'])
# #    if hasattr(status, 'extended_tweet'):
# #          print("Extended tweet:", status.extended_tweet['full_text'])
# #    else:
# #          print("Normal tweet", status.full_text)
# # except AttributeError as e:
# #    print("Error", AttributeError)

# # print("The status was created at : " + str(status.created_at)) 
# # print("The id is : " + str(status.id)) 
# # print("The id_str is : " + status.id_str) 
# # print("The text is : " + status.text) 
# # text1=status.text.replace('&amp;', 'and')
# # print("The text is : " + text1) 
# # print("The entitities are : " + str(status.entities)) 
# # print("The source is : " + status.source) 
# # print("The source_url is : " + status.source_url) 


# # print("The in_reply_to_status_id is : " + str(status.in_reply_to_status_id)) 
# # print("The in_reply_to_status_id_str is : " + str(status.in_reply_to_status_id_str)) 
# # print("The in_reply_to_user_id is : " + str(status.in_reply_to_user_id)) 
# # print("The in_reply_to_user_id_str is : " + str(status.in_reply_to_user_id_str)) 
# # print("The in_reply_to_screen_name is : " + str(status.in_reply_to_screen_name)) 


# # print("The poster's screen name is : " + status.user.screen_name) 
# # print("The geo is : " + str(status.geo)) 
# # print("The coordinates are : " + str(status.coordinates)) 
# # print("The place is : " + str(status.place)) 
# # print("The contributors are : " + str(status.contributors)) 
# # print("The is_quote_status is : " + str(status.is_quote_status)) 
# # print("The retweet_count is : " + str(status.retweet_count)) 
# print("The favorite_count is : " + status.favorite_count) 

# # print("Has the authenticated user favourited the status? : " + str(status.favorited)) 
# # print("Has the authenticated user retweeted the status? " + str(status.retweeted)) 
# # print("Is the status possibly_sensitive? : " + str(status.possibly_sensitive)) 
# # print("The lang is : " + status.lang) 


# import settings
# import mysql.connector
# import pandas as pd
# import time
# import itertools
# import math

# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# #%matplotlib inline
# import plotly.express as px
# import datetime
# from IPython.display import clear_output

# import plotly.offline as py
# import plotly.graph_objs as go
# from plotly.subplots import make_subplots
# # py.init_notebook_mode()

# import re
# import nltk
# # nltk.download('punkt')
# # nltk.download('stopwords')
# from nltk.probability import FreqDist
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# import sqlite3


# STATES = ['Alabama', 'AL', 'Alaska', 'AK', 'American Samoa', 'AS', 'Arizona', 'AZ', 'Arkansas', 'AR', 'California', 'CA', 'Colorado', 'CO', 'Connecticut', 'CT', 'Delaware', 'DE', 'District of Columbia', 'DC', 'Federated States of Micronesia', 'FM', 'Florida', 'FL', 'Georgia', 'GA', 'Guam', 'GU', 'Hawaii', 'HI', 'Idaho', 'ID', 'Illinois', 'IL', 'Indiana', 'IN', 'Iowa', 'IA', 'Kansas', 'KS', 'Kentucky', 'KY', 'Louisiana', 'LA', 'Maine', 'ME', 'Marshall Islands', 'MH', 'Maryland', 'MD', 'Massachusetts', 'MA', 'Michigan', 'MI', 'Minnesota', 'MN', 'Mississippi', 'MS', 'Missouri', 'MO', 'Montana', 'MT', 'Nebraska', 'NE', 'Nevada', 'NV', 'New Hampshire', 'NH', 'New Jersey', 'NJ', 'New Mexico', 'NM', 'New York', 'NY', 'North Carolina', 'NC', 'North Dakota', 'ND', 'Northern Mariana Islands', 'MP', 'Ohio', 'OH', 'Oklahoma', 'OK', 'Oregon', 'OR', 'Palau', 'PW', 'Pennsylvania', 'PA', 'Puerto Rico', 'PR', 'Rhode Island', 'RI', 'South Carolina', 'SC', 'South Dakota', 'SD', 'Tennessee', 'TN', 'Texas', 'TX', 'Utah', 'UT', 'Vermont', 'VT', 'Virgin Islands', 'VI', 'Virginia', 'VA', 'Washington', 'WA', 'West Virginia', 'WV', 'Wisconsin', 'WI', 'Wyoming', 'WY']
# STATE_DICT = dict(itertools.zip_longest(*[iter(STATES)] * 2, fillvalue=""))
# INV_STATE_DICT = dict((v,k) for k,v in STATE_DICT.items())

