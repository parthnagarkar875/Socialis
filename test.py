import credentials # Import api/access_token keys from credentials.py
import re
import tweepy
import settings
import mysql.connector
import pandas as pd
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import StanfordNERTagger
import spacy
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import sqlite3
import warnings
import country_converter as coco
import numpy
from google_trans_new import google_translator 
from sqlite3 import OperationalError
import numpy
import preprocessor as p
import os
from geopy.geocoders import Nominatim
from time import sleep
from multiprocessing import Process, Queue
import multiprocessing
import threading
from time import time
class MyStreamListener(tweepy.StreamListener):
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    nlp1 = spacy.load('en_core_web_sm')

    def __init__(self, status_queue):
        super(MyStreamListener, self).__init__()
        self.status_queue=status_queue

    def lemma(self,comment):
        doc = MyStreamListener.nlp(comment)
        return " ".join([token.lemma_ for token in doc])    

    def decontracted(self, phrase):
        # specific
        phrase = re.sub(r"won\'t", "will not", phrase)
        phrase = re.sub(r"can\'t", "can not", phrase)
        
        phrase = re.sub(r"won\’t", "will not", phrase)
        phrase = re.sub(r"can\’t", "can not", phrase)

        # general
        phrase = re.sub(r"n\'t", " not", phrase)
        phrase = re.sub(r"\'re", " are", phrase)
        phrase = re.sub(r"\'s", " is", phrase)
        phrase = re.sub(r"\'d", " would", phrase)
        phrase = re.sub(r"\'ll", " will", phrase)
        phrase = re.sub(r"\'t", " not", phrase)
        phrase = re.sub(r"\'ve", " have", phrase)
        phrase = re.sub(r"\'m", " am", phrase)

        phrase = re.sub(r"n\’t", " not", phrase)
        phrase = re.sub(r"\’re", " are", phrase)
        phrase = re.sub(r"\’s", " is", phrase)
        phrase = re.sub(r"\’d", " would", phrase)
        phrase = re.sub(r"\’ll", " will", phrase)
        phrase = re.sub(r"\’t", " not", phrase)
        phrase = re.sub(r"\’ve", " have", phrase)
        phrase = re.sub(r"\’m", " am", phrase)    

        return phrase

    def deEmojify(self, text):
        try:             
            regrex_pattern = re.compile(pattern = "["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags = re.UNICODE)
            return regrex_pattern.sub(r'',text)
        except TypeError: 
            pass

    def get_continuous_chunks(self, text):
        chunked = ne_chunk(pos_tag(word_tokenize(text)))
        continuous_chunk = str()
        current_chunk = []
        for i in chunked:
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            if current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk=continuous_chunk+", "+named_entity
                    current_chunk = []
            else:
                continue
        return continuous_chunk[2:]


    def ner_tagging(self, text, n):
        enti=str()
        if n==1:
            os.environ['JAVAHOME'] = settings.java_path
            st = StanfordNERTagger(settings.model_path, settings.ner_java_path, encoding='utf-8')
            tokenized_text = word_tokenize(text)            # ['This', 'is', 'the', 'game']
            classified_text = st.tag(tokenized_text)
            cond = ['PERSON', 'LOCATION', 'ORGANIZATION']
            for ent in classified_text: 
                if ent[1] in cond:                  # Only choose person, location or organization
                    enti = enti + "," + ent[0]                
        if n==2:
            doc = MyStreamListener.nlp1(text)
            cond = ['PERSON', 'GPE', 'ORG']
            for ent in doc.ents: 
                if ent.label_ in cond:
                    enti = enti + "," + ent.text                 
        enti = enti[1:]   
        if n==3:
            enti=self.get_continuous_chunks(text)
        return enti

    def preprocess(self, tweet):    
        try:
            text3 = self.decontracted(tweet).replace('&amp;', 'and')        # Decontract i.e convert can't to cannot and Replacing "&amp;" with "and"
            text2 = p.clean(text3)                              # Remove URLs, Emojis, etc.
            text1 = self.lemma(text2)                           # Lemmatization
            text = re.sub(r'[^\w\s]', '', text1)                # Remove punctuation

            # text = re.sub(r'http\S+', '', tweet.lower(), flags=re.MULTILINE)
            # res = re.sub(r'[^\w\s]', '', text)
            # deemo = self.deEmojify(res)
            # le = self.lemma(deemo)
            return text
        except TypeError:
            pass

    def get_location(self, temp_location):
        geolocator = Nominatim(user_agent="myGeocoder")         # Initializing geolocator object for getting address
        try:
            location = geolocator.geocode(temp_location)
            # print(location.raw['address']['country'])                
            location_list = location.raw['display_name'].split(",")
            user_location1=location_list[len(location_list)-1].strip()               # Extracting only country name
            translator = google_translator()  
            temp_location = translator.translate(user_location1, lang_tgt='en')         #Translate the location to english
            if temp_location == "Luzon ":
                temp_location="Philippines "
            if temp_location == "ایران ":
                temp_location == "Iran "
            user_location = coco.convert(names=temp_location, to='ISO3')  
            if user_location=='not found':
                user_location = None          
            warnings.filterwarnings("ignore")
        except Exception as e:
            user_location = None

        return user_location

    def get_full_text(self, status):
        final_text=str()

        # Get full text from a tweet
        try:
            if hasattr(status, 'retweeted_status') and hasattr(status.retweeted_status, 'extended_tweet'):
                final_text=status.retweeted_status.extended_tweet['full_text']
                # print("Extended Tweet:", status.retweeted_status.extended_tweet['full_text'])
            elif hasattr(status, 'extended_tweet'):
                final_text=status.extended_tweet['full_text']
                # print("Extended Tweet:", status.extended_tweet['full_text'])                
            else:
                final_text=status.text
                # print("Printing Full text", status.text)
        except AttributeError as e:
            pass
        
        return final_text

    def get_user_list(self, final_text):
        # Getting list of users
        users=re.findall("@([a-zA-Z0-9_]+)", final_text) 
        user_list=str()
        for i in users:
            user_list = user_list + "," + i
        user_list=user_list[1:]            
        return user_list


    def on_status(self, status):
        # Extract info from tweets
        print(status.text)
        self.status_queue.put(status)

    def check_conn(self, conn):
        try:
            conn.cursor()
            return True
        except Exception as ex:
            return False

    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, 
        stop srcraping data as it exceed to the thresold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return True

def stream():
    auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)    
    api = tweepy.API(auth,wait_on_rate_limit=True)

    myStreamListener = MyStreamListener(status_queue)
    myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener, tweet_mode='extended')

    myconn =sqlite3.connect('twitter.db')

    if myStreamListener.check_conn(myconn) == True:        
        mycursor = myconn.cursor()
        try:
            output=myconn.execute("SELECT COUNT(*) FROM {}".format(settings.TABLE_NAME))
            result=output.fetchall()
        except OperationalError:
            myconn.execute("CREATE TABLE {} ({})".format(settings.TABLE_NAME, settings.TABLE_ATTRIBUTES))
            myconn.commit()

        myconn.close()

    try:
        myStream.filter(languages=["en"], track = settings.TRACK_WORDS)
    except Exception as e:
        print("Error. Restarting Stream.... Error: ")
        print(e.__doc__)
        print(e.message)

    myconn.close()


def main_method(status_queue):
    while True:
        print("\n\n\n\n\n\n\nStarted\n\n\n\n\n\n\n")
        a=MyStreamListener(status_queue)
        status=status_queue.get()
        final_text=a.get_full_text(status)    
        id_str = status.id_str
        created_at = status.created_at
        
        # Removing "RT @username:" from the text
        if final_text[:2] == 'RT':
            result = final_text.index(':')
            final_text=final_text[(result+1):]
        
        # Getting list of users
        user_list=a.get_user_list(final_text)            
        text = a.preprocess(final_text)    # Pre-processing the text          
        print("\n\n\n\n\n", text, "\n\n\n\n\n")
        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        if polarity > 0.5:
            polarity=1
        elif polarity < -0.5:
            polarity=-1
        else:
            polarity = 0
        subjectivity = sentiment.subjectivity
        enti=a.ner_tagging(text, 3)      # Named entity recognition
        user_created_at = status.user.created_at
        temp_location = a.deEmojify(status.user.location)        
        user_location=a.get_location(temp_location)        
        user_description = a.deEmojify(status.user.description)
        user_followers_count =status.user.followers_count
        longitude = None
        latitude = None
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]
            
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count
        
        # print(status.text)
        print(final_text)
        
        print(text)
        print("Long: {}, Lati: {}".format(longitude, latitude))

        myconn =sqlite3.connect('twitter.db')

        if a.check_conn(myconn) == True:        
            mycursor = myconn.cursor()
            sql = "INSERT INTO {} (id_str, created_at, text, polarity, subjectivity, named_ent, users_list, user_created_at, user_location, user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(settings.TABLE_NAME)
            val = (id_str, created_at, text, polarity, subjectivity, enti, user_list, user_created_at, user_location, user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count)
            mycursor.execute(sql, val)
            myconn.commit()
            print("Inserted")
            mycursor.close()

status_queue=Queue()    


if __name__=="__main__":

    # p1 = multiprocessing.Process(target=stream) 
    p2 = multiprocessing.Process(target=main_method, args=(status_queue,))

    p2.daemon=True

    # p1.start() 
    p2.start() 
    stream()
    # p1.join() 
    p2.join() 

    print("Done!") 

# Close the MySQL connection as it finished
# However, this won't be reached as the stream listener won't stop automatically
# Press STOP button to finish the process