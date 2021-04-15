import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import sqlite3
import settings
import datetime
import credentials
from nltk.probability import FreqDist
import time
import country_converter as coco
import warnings
import collections
from nltk.corpus import stopwords
import tweepy
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords




class FileReference:
    def __init__(self, filename):
        self.filename = filename


# @st.cache(persist=True)
# @st.cache(allow_output_mutation=True)
def connect_engine():
    conn1 = sqlite3.connect('twitter.db')
    return conn1

# data=pd.read_sql("select * from facebook", conn1)

graph = st.sidebar.selectbox('Select a Graph to be plotted',('Time Series', 'World Map plot', 'Named Entities', 'Wordcloud', 'Influencers', 'Bigram', 'Volume Analysis'))



# @st.cache(allow_output_mutation=True)
# @st.cache(persist=True)
@st.cache(suppress_st_warning=True, hash_funcs={FileReference: connect_engine})
def get_data(n, m):
    conn1=connect_engine()
    if n==1 and m == 2:
        timenow = (datetime.datetime.utcnow() - datetime.timedelta(hours=0, minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        query = "SELECT * FROM {} WHERE created_at <= '{}' " .format(settings.TABLE_NAME, timenow)
        # query = "select * from Facebook"
        df = pd.read_sql(query, con=conn1)    
    if n==2 and m == 3:
        df = pd.read_sql("select * from Facebook", con=conn1)
    if n==2 and m == 1:
        df = pd.read_sql("select * from Facebook where polarity = 1", con=conn1)
    if n==2 and m == 0:
        df = pd.read_sql("select * from Facebook where polarity = 0", con=conn1)
    if n==2 and m == -1:
        df = pd.read_sql("select * from Facebook where polarity = -1", con=conn1)
    return df

# @st.cache(allow_output_mutation=True)
def plot_line():
    # timenow = (datetime.datetime.utcnow() - datetime.timedelta(hours=0, minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
    # query = "SELECT * FROM {} WHERE created_at <= '{}' " .format(settings.TABLE_NAME, timenow)
    # df = pd.read_sql(query, con=conn1)
    
    df=get_data(1, 2)
    df['created_at'] = pd.to_datetime(df['created_at'])
    result = df.groupby([pd.Grouper(key='created_at', freq='2s'), 'polarity']).count().unstack(fill_value=0).stack().reset_index()
    result = result.rename(columns={"id_str": "Num of '{}' mentions".format(settings.TRACK_WORDS[0]), "created_at":"Time in UTC"})  
    time_series = result["Time in UTC"][result['polarity']==0].reset_index(drop=True)

    fig=go.Figure()
    st.header("Time Series chart showing Sentiments throughout time")
    fig.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity']==0].reset_index(drop=True),
        name="Neutral",
        opacity=0.8))
    fig.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity']==-1].reset_index(drop=True),
        name="Negative",
        opacity=0.8))
    fig.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity']==1].reset_index(drop=True),
        name="Positive",
        opacity=0.8))

    fig.update_layout(
    autosize=False,
    width=1000,
    height=500,
    margin=dict(
        l=10,
        r=50,
        b=100,
        t=100,
        pad=4
    ))

    return fig


@st.cache(suppress_st_warning=True)
def plot_choro(n):
    df=get_data(2, n)
    normal_names = df["user_location"].dropna().tolist()
    counter=collections.Counter(normal_names)
    df1 = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    df1 = df1.rename(columns={'index':'CODE', 0:'COUNT'})
    country=list()
    for i in df1['CODE']:
        country.append(coco.convert(names = i, to = 'name_short'))    
    df1['COUNTRY']=country


    g1=go.Figure(go.Choropleth(
        locations = df1['CODE'],
        z = df1['COUNT'],
        text = df1['COUNTRY'],
        colorscale = 'Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '$',
        colorbar_title = 'GDP<br>Billions US$',
    ))
    return g1

def plot_bar(n, m):
    df=get_data(2, n)
    new_stopwords = ["th", "i"]
    stop = stopwords.words('english')
    stop.extend(new_stopwords)

    df['text'] = df['text'].str.lower().apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))    
    li=list()
    
    if m == 1:
        for i in df['text']:
            te=i.split()
            li.extend(te)
    else:
        for i in df["named_ent"]:    
            te=i.split(",")    
            li.extend(te)

    li = list(filter(None, li))
    fdist = FreqDist(li)
    fd = pd.DataFrame(fdist.most_common(10), columns = ["Word","Frequency"]).drop([0]).reindex()

    g1=go.Figure(go.Bar(x=fd["Word"], y=fd["Frequency"], name="Freq Dist")) # 59, 89, 152
    g1.update_traces(marker_color='rgb(59, 89, 152)', marker_line_color='rgb(8,48,107)', marker_line_width=0.5, opacity=0.7) # fig.update_layout( xaxis = dict(tickfont = dict(size=9)))
    return g1

def plot_usernames():
    date_since = "2021-04-10"
    auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret) 
    auth.set_access_token(credentials.access_token, credentials.access_token_secret) 
    api = tweepy.API(auth) 
    query="(facebook) -facebook.com min_faves:500"
    status = api.search(query, lang="en", since=date_since, count=1000) 

    like=dict()
    for i in status:
        like[i.user.screen_name]=i.favorite_count

    sort_orders = sorted(like.items(), key=lambda x: x[1], reverse=True)

    likes=list()
    usernames=list()
    j=0
    for i in sort_orders:
        if j<10:
            likes.append(i[1])
            usernames.append(i[0])
            j=j+1

    fig = go.Figure([go.Bar(x=usernames, y=likes)])
    return fig

def select_sentiment():
    select_status = st.sidebar.radio("Select Sentiment", ('Overall', 'Positive', 'Negative', 'Neutral'))
    if select_status == 'Positive':
        n=1
    elif select_status == 'Neutral':
        n=0
    elif select_status == 'Negative':
        n=-1    
    else:
        n=3
    return n


def get_bigram():
    stoplist = stopwords.words('english') + ['though']

    c_vec = CountVectorizer(stop_words=stoplist, ngram_range=(2,3))
    # matrix of ngrams

    df=get_data(2,3)
    ngrams = c_vec.fit_transform(df['text'])
    # count frequency of ngrams
    count_values = ngrams.toarray().sum(axis=0)
    # list of ngrams
    vocab = c_vec.vocabulary_
    df = pd.DataFrame(sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)
                ).rename(columns={0: 'Frequency', 1:'Word'})
    fd=df.head(10)

    g1=go.Figure(go.Bar(x=fd["Word"], y=fd["Frequency"], name="Freq Dist")) # 59, 89, 152
    g1.update_traces(marker_color='rgb(59, 89, 152)', marker_line_color='rgb(8,48,107)', marker_line_width=0.5, opacity=0.7) # fig.update_layout( xaxis = dict(tickfont = dict(size=9)))
    return g1


def plot_pie():
    df=get_data(2,3)
    val_list=list()
    val_list.append(df['polarity'].value_counts()[0])
    val_list.append(df['polarity'].value_counts()[1])
    val_list.append(df['polarity'].value_counts()[-1])
    labels=[0,1,-1]
    g1=go.Figure(go.Pie(labels=labels, values=val_list))
    return g1


if graph == "Time Series":
    fig=plot_line()
    st.plotly_chart(fig)

elif graph == "World Map plot":
    n=select_sentiment()
    fig=plot_choro(n)
    st.plotly_chart(fig)

elif graph == "Named Entities":
    n=select_sentiment()
    fig=plot_bar(n, 2)
    st.plotly_chart(fig)

elif graph == "Wordcloud":
    n=select_sentiment()
    fig=plot_bar(n, 1)
    st.plotly_chart(fig)

elif graph == "Influencers":
    fig=plot_usernames()
    st.plotly_chart(fig)

elif graph == "Bigram":
    fig=get_bigram()
    st.plotly_chart(fig)

elif graph == 'Volume Analysis':
    fig=plot_pie()
    st.plotly_chart(fig)

