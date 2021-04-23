# import sqlite3
# import pandas as pd
# # import country_converter as coco
# # from geopy.geocoders import Nominatim
# # import settings
# # import datetime
# import collections
# import country_converter as coco
# import pycountry

# conn1 = sqlite3.connect('twitter.db')
# print("Opened the database successfully")

# conn = conn1.cursor()

# query="select * from Facebook"

# df=pd.read_sql(query, con=conn1)
# str1="hello, bye"
# print(str1.split(',').strip())
# for i in df.users_list:
#     print(i)
# li=['India', 'Italy']
# sg=coco.convert(names=li, to='ISO3')
# df = df[df.user_location.isin(sg)]


import psycopg2

try:
    connect_str = "dbname='test' user='postgres' host='localhost' " + \
                  "password='helloParth'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # create a new table with a single column called "name"
    cursor.execute("""CREATE TABLE tutorials (name char(40));""")
    # run a SELECT statement - no data in there, but we can try it
    cursor.execute("""SELECT * from tutorials""")
    conn.commit() # <--- makes sure the change is shown in the database
    rows = cursor.fetchall()
    print(rows)
    cursor.close()
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)


































# print(df.head())
# # normal_names = df["user_location"].dropna().tolist()
# counter = collections.Counter(normal_names)
# country=list()
# # freq=list()
# for i,j in counter.most_common(10):
#     country.append(pycountry.countries.get(alpha_3=i).name)
#     # freq.append(j)
# df = pd.DataFrame(country, columns =['Country'])
# print(df)
# df1 = pd.DataFrame.from_dict(counter, orient='index').reset_index()
# df1 = df1.rename(columns={'index': 'CODE', 0: 'COUNT'})
# country = list()


# print(df.head())
# from __future__ import unicode_literals, print_function
# # import plac
# import random
# from pathlib import Path
# import spacy
# from tqdm import tqdm


# TRAIN_DATA = [
#     ('Who is Nishanth?', {
#         'entities': [(7, 15, 'PERSON')]
#     }),
#      ('Who is Kamal Khumar?', {
#         'entities': [(7, 19, 'PERSON')]
#     }),
#     ('I like London and Berlin.', {
#         'entities': [(7, 13, 'LOC'), (18, 24, 'LOC')]
#     })
# ]

# model = None
# output_dir=Path("/home/unmodern/Parth")
# n_iter=100

# if model is not None:
#     nlp = spacy.load(model)  
#     print("Loaded model '%s'" % model)
# else:
#     nlp = spacy.blank('en')  
#     print("Created blank 'en' model")

# #set up the pipeline

# if 'ner' not in nlp.pipe_names:
#     ner = nlp.add_pipe('ner')
#     # nlp.add_pipe(ner, last=True)
# else:
#     ner = nlp.get_pipe('ner')


# for _, annotations in TRAIN_DATA:
#     for ent in annotations.get('entities'):
#         ner.add_label(ent[2])

# other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
# with nlp.disable_pipes(*other_pipes):  # only train NER
#     optimizer = nlp.begin_training()
#     for itn in range(n_iter):
#         random.shuffle(TRAIN_DATA)
#         losses = {}
#         for text, annotations in tqdm(TRAIN_DATA):
#             nlp.update(
#                 [text],  
#                 [annotations],  
#                 drop=0.5,  
#                 sgd=optimizer,
#                 losses=losses)
#         print(losses)









# import nltk
# # nltk.download('state_union')
# # nltk.download('maxent_ne_chunker')
# # nltk.download('averaged_perceptron_tagger')
# from nltk.corpus import state_union
# from nltk.tokenize import PunktSentenceTokenizer
# from nltk.tokenize import sent_tokenize

# train_text = state_union.raw("2005-GWBush.txt")
# sample_text = state_union.raw("2006-GWBush.txt")



# # custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
# # tokenized = custom_sent_tokenizer.tokenize(sample_text)

# tokenized=sent_tokenize(train_text)

# # print(tokenized)

# def process_content():
#     try:
#         for i in tokenized[5:]:
#             words = nltk.word_tokenize(i)
#             tagged = nltk.pos_tag(words)
#             namedEnt = nltk.ne_chunk(tagged, binary=True)
#             namedEnt.draw()
#     except Exception as e:
#         print(str(e))


# process_content()


# from sklearn.decomposition import LatentDirichletAllocation
# from sklearn.decomposition import NMF
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.pipeline import make_pipeline
# from sklearn.feature_extraction.text import CountVectorizer
# from nltk.corpus import stopwords


# df = pd.read_sql("select * from Facebook", conn1)

# stoplist = stopwords.words('english') + ['though']

# c_vec = CountVectorizer(stop_words=stoplist, ngram_range=(2,3))
# # matrix of ngrams
# ngrams = c_vec.fit_transform(df['text'])
# # count frequency of ngrams
# count_values = ngrams.toarray().sum(axis=0)
# # list of ngrams
# vocab = c_vec.vocabulary_
# df_ngram = pd.DataFrame(sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)
#             ).rename(columns={0: 'frequency', 1:'bigram/trigram'})

# print(df_ngram.head(10))


# from nltk import ne_chunk, pos_tag, word_tokenize
# from nltk.tree import Tree
# import nltk
# def get_continuous_chunks(text):
#     chunked = ne_chunk(pos_tag(word_tokenize(text)))
#     continuous_chunk = str()
#     current_chunk = []
#     for i in chunked:
#         if type(i) == Tree:
#             current_chunk.append(" ".join([token for token, pos in i.leaves()]))
#         if current_chunk:
#             named_entity = " ".join(current_chunk)
#             if named_entity not in continuous_chunk:
#                 # continuous_chunk.append(named_entity)
#                 continuous_chunk=continuous_chunk+", "+named_entity
#                 current_chunk = []
#         else:
#             continue
#     return continuous_chunk[2:]

# my_sent = "Looking back on a childhood in New York filled with events and memories, I find it rather difficult to pick one that leaves me with the fabled warm and fuzzy feelings. As the daughter of an Air Force major, I had the pleasure of traveling across America in many moving trips. I have visited the monstrous trees of the Sequoia National Forest, stood on the edge of the Grand Canyon and have jumped on the beds at Caesar's Palace in Lake Tahoe.The day I picked my dog up from the pound was one of the happiest days of both of our lives. I had gone to the pound just a week earlier with the idea that I would just 'look' at a puppy. Of course, you can no more just look at those squiggling little faces so filled with hope and joy than you can stop the sun from setting in the evening. I knew within minutes of walking in the door that I would get a puppy… but it wasn't until I saw him that I knew I had found my puppy. Looking for houses was supposed to be a fun and exciting process. Unfortunately, none of the ones that we saw seemed to match the specifications that we had established. They were too small, too impersonal, too close to the neighbors. After days of finding nothing even close, we began to wonder: was there really a perfect house out there for us?"

# print(nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(my_sent))))


# hello=nltk.ne_chunk(my_sent, binary=True)
# print(hello)
# print(get_continuous_chunks(my_sent))





# extract_data={
#             # 1:"SELECT * FROM {} WHERE created_at <= '{}' ".format(settings.TABLE_NAME, timenow),
#             2:"select * from Facebook",
#             3:"select * from Facebook where polarity = 1",
#             4:"select * from Facebook where polarity = 0",
#             5: "select * from Facebook where polarity = -1"
#         }
        
# query = extract_data.get(2)


# print(type(query))

















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

# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.tag import StanfordNERTagger
# import os
# import spacy
# from spacy.tokens import Span
# import nltk
# # nltk.download('punkt')

# def ner_tagging(text, n):
#     enti=str()
#     nlp1 = spacy.load('en_core_web_sm')
#     if n==1:
#         # os.environ['JAVAHOME'] = settings.java_path
#         st = StanfordNERTagger(settings.model_path, settings.ner_java_path, encoding='utf-8')
#         tokenized_text = word_tokenize(text)            # ['This', 'is', 'the', 'game']
#         classified_text = st.tag(tokenized_text)
#         cond = ['PERSON', 'LOCATION', 'ORGANIZATION']
#         for ent in classified_text: 
#             if ent[1] in cond:                  # Only choose person, location or organization
#                 enti = enti + "," + ent[0]                
#     if n==2:
#         doc = nlp1(text)
#         cond = ['PERSON', 'GPE', 'ORG']
#         # ORG=doc.vocab.strings['ORG']
#         # new_ent=Span(doc, 0, 1, label=ORG)
#         # doc.ents=list(doc.ents)+[new_ent]

#         for ent in doc.ents: 
#             if ent.label_ in cond:
#                 enti = enti + "," + ent.text                 
#     enti = enti[1:]       
#     return enti

# a="Hello, I work for Facebook"

# enti=ner_tagging(a, 2) 
# print(enti)


# i = 0
# for row in output:
#    if i>20000:
#       break
#    else:
#       print("\nText: ",row[2])

#       i = i+1


# from nltk.corpus import stopwords

# print(stopwords.words('english'))



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

