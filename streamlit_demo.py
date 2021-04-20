import warnings
warnings.simplefilter("ignore")
import streamlit as st
st.set_page_config(layout="wide", page_title="Socialis", page_icon="socialis-logo.png")
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
import tweepy
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import pycountry


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


local_css("style.css")


class FileReference:
    def __init__(self, filename):
        self.filename = filename

class Socialis:
    def connect_engine(self):
        conn1 = sqlite3.connect('twitter.db')
        return conn1

    # @st.cache(hash_funcs={FileReference: connect_engine}, suppress_st_warning=True, show_spinner=False,
            # allow_output_mutation=True)
    def get_data(self, n):
        conn1=self.connect_engine()
        timenow = (datetime.datetime.utcnow() - datetime.timedelta(hours=0, minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        
        extract_data={
            1:"SELECT * FROM {} WHERE created_at <= '{}' ".format(settings.TABLE_NAME, timenow),
            "Overall":"select * from Facebook",
            "Positive":"select * from Facebook where polarity = 1",
            "Neutral":"select * from Facebook where polarity = 0",
            "Negative":"select * from Facebook where polarity = -1"
        }
        
        query = extract_data.get(n)
        df=pd.read_sql(query, con=conn1)
        return df

    # @st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
    def plot_line(self):
        df1 = self.get_data(1)
        df = self.get_freq_country(df1)
        df['created_at'] = pd.to_datetime(df['created_at'])
        result = df.groupby([pd.Grouper(key='created_at', freq='2s'), 'polarity']).count().unstack(
            fill_value=0).stack().reset_index()
        result = result.rename(
            columns={"id_str": "Num of '{}' mentions".format(settings.TRACK_WORDS[0]), "created_at": "Time in UTC"})
        time_series = result["Time in UTC"][result['polarity'] == 0].reset_index(drop=True)

        timefig = go.Figure()
        timefig.add_trace(go.Scatter(
            x=time_series,
            y=result["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity'] == 0].reset_index(
                drop=True),
            name="Neutral",
            opacity=0.8))
        timefig.add_trace(go.Scatter(
            x=time_series,
            y=result["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity'] == -1].reset_index(
                drop=True),
            name="Negative",
            opacity=0.8))
        timefig.add_trace(go.Scatter(
            x=time_series,
            y=result["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity'] == 1].reset_index(
                drop=True),
            name="Positive",
            opacity=0.8))

        return timefig


    @st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
    def plot_choro(self, n):
        df = self.get_data(n)
        normal_names = df["user_location"].dropna().tolist()
        counter = collections.Counter(normal_names)
        df1 = pd.DataFrame.from_dict(counter, orient='index').reset_index()
        df1 = df1.rename(columns={'index': 'CODE', 0: 'COUNT'})
        country = list()
        for i in df1['CODE']:
            country.append(coco.convert(names=i, to='name_short'))
        df1['COUNTRY'] = country
        g1 = go.Figure(go.Choropleth(
            locations=df1['CODE'],
            z=df1['COUNT'],
            text=df1['COUNTRY'],
            colorscale='Tealgrn',
            autocolorscale=False,
            marker_line_color='darkgrey',
            marker_line_width=0.3,
            # colorbar_tickprefix='',
            colorbar_title='Number of tweets',
            uirevision='constant', ),
            layout=go.Layout(geo=dict(bgcolor='rgba(0,0,0,0)', landcolor='#333', subunitcolor='grey'),
                            margin={"autoexpand": True, "r": 0, "t": 40, "l": 0, "b": 0}, plot_bgcolor='#4E5D6C'))
        return g1


    # @st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
    def plot_bar(self, n, m):
        df1 = self.get_data(n)
        df = self.get_freq_country(df1)
        new_stopwords = ["th", "i"]
        stop = stopwords.words('english')
        stop.extend(new_stopwords)
        df['text'] = df['text'].str.lower().apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
        li = list()

        if m == 1:
            for i in df['text']:
                te = i.split()
                li.extend(te)
        else:
            for i in df["named_ent"]:
                j=i.replace(" ", "")
                te = j.split(",")
                li.extend(te)
                # li.remove('RT')

        li = list(filter(None, li))
        fdist = FreqDist(li)
        fd = pd.DataFrame(fdist.most_common(10), columns=["Word", "Frequency"]).drop([0]).reindex()
        g1 = go.Figure(go.Bar(x=fd["Word"], y=fd["Frequency"], name="Freq Dist"))  # 59, 89, 152
        g1.update_traces(marker_color='rgb(59, 89, 152)', marker_line_color='rgb(8,48,107)', marker_line_width=0.5,
                        opacity=0.7)  # fig.update_layout( xaxis = dict(tickfont = dict(size=9)))
        return g1

    def plot_usernames(self):
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

    def get_freq_country(self, df):
        normal_names = df["user_location"].dropna().tolist()
        counter = collections.Counter(normal_names)      
        country=list()
        for i,j in counter.most_common(5):
            country.append(pycountry.countries.get(alpha_3=i).name)
        df1 = pd.DataFrame(country, columns =['Country'])

        Genres = st.sidebar.multiselect("Select country", df1['Country'])
        if Genres:            
            sg=coco.convert(names=Genres, to='ISO3')
            if type(sg)!= list:
                sg=[sg]
            df = df[df.user_location.isin(sg)]
        return df

    def select_sentiment(self):
        select_status = st.sidebar.radio("Select Sentiment", ('Overall', 'Positive', 'Negative', 'Neutral'))
        return select_status

    def get_bigram(self):
        stoplist = stopwords.words('english') + ['though']

        c_vec = CountVectorizer(stop_words=stoplist, ngram_range=(2,3))
        # matrix of ngrams

        df1=self.get_data('Overall')
        df = self.get_freq_country(df1)

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

    def plot_pie(self):
        df=self.get_data('Overall')
        val_list=list()
        val_list.append(df['polarity'].value_counts()[0])
        val_list.append(df['polarity'].value_counts()[1])
        val_list.append(df['polarity'].value_counts()[-1])
        labels=[0,1,-1]
        g1=go.Figure(go.Pie(labels=labels, values=val_list))
        return g1

graph = st.sidebar.selectbox('Select a Graph to be plotted',
                                ('Time Series', 'World Map Plot', 'Named Entities', 'Word Cloud', 'Influencers', 'Bigram', 'Volume Analysis'))
a=Socialis()


if graph == "Time Series":
    st.header("Time Series Chart: Sentiments Over Time")
    fig = a.plot_line()
    fig.update_layout(autosize=False, height=600)
    st.plotly_chart(fig, use_container_width=True)

elif graph == "World Map Plot":
    st.header("World Map: Sentiments by Region")
    n = a.select_sentiment()
    fig = a.plot_choro(n)
    fig.update_layout(autosize=False, height=600)
    st.plotly_chart(fig, use_container_width=True)

elif graph == "Named Entities":
    st.header("Named Entities: Bar Graph")
    n = a.select_sentiment()
    fig = a.plot_bar(n, 2)
    fig.update_layout(autosize=False, height=600)
    st.plotly_chart(fig, use_container_width=True)

elif graph == "Word Cloud":
    st.header("Word Cloud: Bar Graph")
    n = a.select_sentiment()
    fig = a.plot_bar(n, 1)
    fig.update_layout(autosize=False, height=600)
    st.plotly_chart(fig, use_container_width=True)

elif graph == "Influencers":
    st.header("Influencer Mentions")
    fig = a.plot_usernames()
    fig.update_layout(autosize=False, height=600)
    st.plotly_chart(fig, use_container_width=True)

elif graph == "Bigram":
    st.header("Bigram")
    fig = a.get_bigram()
    fig.update_layout(autosize=False, height=600)
    st.plotly_chart(fig, use_container_width=True)

elif graph == 'Volume Analysis':
    st.header("Volume Analysis by Words")
    fig = a.plot_pie()
    fig.update_layout(autosize=False, height=600)
    st.plotly_chart(fig, use_container_width=True)
