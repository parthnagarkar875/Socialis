import credentials # Import api/access_token keys from credentials.py
import re
import tweepy
import settings
import mysql.connector
import pandas as pd
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import sqlite3
from sqlite3 import OperationalError
import numpy
import preprocessor as p

class MyStreamListener(tweepy.StreamListener):

    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    nlp1 = spacy.load('en_core_web_sm')

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

    def preprocess(self, tweet):    
        try:
            text3 = self.decontracted(tweet).replace('&amp;', 'and')        
            text2 = p.clean(text3)
            text1 = self.lemma(text2)
            text = re.sub(r'[^\w\s]', '', text1)    

            # text = re.sub(r'http\S+', '', tweet.lower(), flags=re.MULTILINE)
            # res = re.sub(r'[^\w\s]', '', text)
            # deemo = self.deEmojify(res)
            # le = self.lemma(deemo)
            return text
        except TypeError:
            pass
    
    def on_status(self, status):
        if status.retweeted:
        #Avoid retweeted info, and only original tweets will be received
            return True
        # Extract info from tweets
        id_str = status.id_str
        created_at = status.created_at
        text = self.preprocess(status.text)    # Pre-processing the text          
        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity
        doc = MyStreamListener.nlp1(text)
        enti = str()
        cond = ['PERSON', 'GPE', 'ORG']
        for ent in doc.ents: 
            if ent.label_ in cond:
                enti = enti + "," + ent.text                 
        enti = enti[1:]
        user_created_at = status.user.created_at
        user_location = self.deEmojify(status.user.location)
        user_description = self.deEmojify(status.user.description)
        user_followers_count =status.user.followers_count
        longitude = None
        latitude = None
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]
            
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count
        
        print(status.text)
        print(text)
        print("Long: {}, Lati: {}".format(longitude, latitude))

        myconn =sqlite3.connect('twitter.db')

        if self.check_conn(myconn) == True:        
            mycursor = myconn.cursor()
            sql = "INSERT INTO {} (id_str, created_at, text, polarity, subjectivity, named_ent, user_created_at, user_location, user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(settings.TABLE_NAME)
            val = (id_str, created_at, text, polarity, subjectivity, enti, user_created_at, user_location, user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count)
            mycursor.execute(sql, val)
            myconn.commit()
            print("Inserted")
            mycursor.close()

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
            return False


auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)    
api = tweepy.API(auth,wait_on_rate_limit=True)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)

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


myStream.filter(languages=["en"], track = settings.TRACK_WORDS)
# Close the MySQL connection as it finished
# However, this won't be reached as the stream listener won't stop automatically
# Press STOP button to finish the process.
myconn.close()