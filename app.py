import warnings
warnings.simplefilter("ignore")
import streamlit as st
st.set_page_config(layout="wide", page_title="Socialis", page_icon="socialis-logo.png")
import pandas as pd
import plotly.graph_objects as go
import settings
import datetime
import credentials
from nltk.probability import FreqDist
import country_converter as coco
import collections
import tweepy
import pycountry
import time
import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import psycopg2
from tweepy import Stream
from tweepy.streaming import StreamListener


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("style.css")

code = """<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script><script>var intervalId = window.setInterval(function(){twttr.ready(() =>twttr.widgets.load(document.getElementById("stMarkdown")));}, 1000);</script>"""

directory = os.path.dirname(st.__file__) + '/static/index.html'
with open(directory, 'r') as file:
    data = file.read()
    if len(re.findall('https://platform.twitter.com/widgets.js', data)) == 0:
        with open(directory, 'w') as ff:
            newdata = re.sub('<head>', '<head>' + code, data)
            ff.write(newdata)


class TweetListener(StreamListener):
    
    twt=[st.empty()]*5

    def on_error(self, status):
        if status == 420:
            # return False to disconnect the stream
            return True

    def on_status(self, status):
        ist = status.created_at
        hours_added = datetime.timedelta(hours=5, minutes=30)
        created_at = ist + hours_added
        
        for i in range(5):
            TweetListener.twt[i]=st.markdown(
            f'<blockquote><p>{status.text}</p>&mdash; {status.user.screen_name} <br>&mdash; {status.favorite_count} likes {created_at}</blockquote>',
            unsafe_allow_html=True)
            time.sleep(0.5)

class FileReference:
    def __init__(self, filename):
        self.filename = filename


class Socialis:
    col1, col2, col3 = st.beta_columns([1, 1, 1])
    splash = col2.image("socialis.gif", use_column_width=True)
    time.sleep(2)
    splash.empty()

    def connect_engine(self):
        connect_str = f"dbname='{credentials.dbname}' user='{credentials.user}' host='{credentials.host}' " + \
                      f"password='{credentials.password}'"

        conn1 = psycopg2.connect(connect_str)
        return conn1

    # @st.cache(hash_funcs={FileReference: connect_engine}, suppress_st_warning=True, show_spinner=False,
    # allow_output_mutation=True)
    def get_data(self, data_select):
        conn1 = self.connect_engine()
        timenow = (datetime.datetime.utcnow() - datetime.timedelta(hours=0, minutes=10)).strftime('%Y-%m-%d %H:%M:%S')

        extract_data = {
            1: "SELECT * FROM {} WHERE created_at >= '{}' ".format(settings.TABLE_NAME, timenow),
            "Overall": f"select * from {settings.brand}",
            "Positive": f"select * from {settings.brand} where polarity = 1",
            "Neutral": f"select * from {settings.brand} where polarity = 0",
            "Negative": f"select * from {settings.brand} where polarity = -1"
        }

        query = extract_data.get(data_select)
        df = pd.read_sql(query, con=conn1)
        return df

    # @st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
    def plot_line(self):
        df1 = self.get_data('Overall')
        df = self.get_freq_country(df1)
        df['created_at'] = pd.to_datetime(df['created_at'])
        result = df.groupby([pd.Grouper(key='created_at', freq='10s'), 'polarity']).count().unstack(
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

    # @st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
    def plot_choro(self, choro_n):
        df = self.get_data(choro_n)
        normal_names = df["user_location"].dropna().tolist()
        counter = collections.Counter(normal_names)
        df1 = pd.DataFrame.from_dict(counter, orient='index').reset_index()
        df1 = df1.rename(columns={'index': 'CODE', 0: 'COUNT'})
        country = coco.convert(names=df1['CODE'].tolist(), to='name_short')
        # country = list()
        # for i in df1['CODE']:
        #     country.append(coco.convert(names=i, to='name_short'))
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
    def plot_bar(self, bar_n, m):
        df1 = self.get_data(bar_n)
        df = self.get_freq_country(df1)
        new_stopwords = ["th", "i"]
        stop = stopwords.words('english')
        stop.extend(new_stopwords)
        df['text'] = df['text'].str.lower().apply(lambda x: ' '
                                                  .join([word for word in x.split() if word not in stop]))
        li = list()

        if m == 1:
            for i in df['text']:
                te = i.split()
                li.extend(te)
        elif m == 2:
            for i in df['users_list']:
                j = i.replace(" ", "")
                te = j.split(',')
                li.extend(te)
        else:
            for i in df["named_ent"]:
                # j = i.replace(" ", "")
                te = i.split(",")
                li.extend(te)
                # li.remove('RT')

        print(li)
        li = list(filter(None, li))
        fdist = FreqDist(li)
        fd = pd.DataFrame(fdist.most_common(10), columns=["Word", "Frequency"]).drop([0]).reindex()
        g1 = go.Figure(go.Bar(x=fd["Word"], y=fd["Frequency"], name="Freq Dist"))  # 59, 89, 152
        g1.update_traces(marker_color='rgb(59, 89, 152)', marker_line_color='rgb(8,48,107)', marker_line_width=0.5,
                         opacity=0.7)  # fig.update_layout( xaxis = dict(tickfont = dict(size=9)))
        return g1

    def plot_usernames(self):

        previous_date = datetime.datetime.today() - datetime.timedelta(days=2)
        date_since = str(previous_date.strftime('%Y-%m-%d'))
        auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
        auth.set_access_token(credentials.access_token, credentials.access_token_secret)
        api = tweepy.API(auth)
        query = f"({settings.brand}) -{settings.brand}.com min_faves:500"
        status = api.search(query, lang="en", since=date_since, count=1000)

        like = dict()
        tweet_id = list()

        for i in status:
            like[i.user.screen_name] = i.favorite_count, i.id

        sort_orders = sorted(like.items(), key=lambda x: x[1], reverse=True)
        likes = list()
        usernames = list()
        j = 0
        for i in sort_orders:
            if j < 10:
                likes.append(i[1][0])
                usernames.append(i[0])
                tweet_id.append(i[1][1])
            j = j + 1

        twcol1, twcol2 = st.beta_columns([1, 1])
        for i in range(0, 5):
            twcol1.markdown(
                f'<blockquote class="twitter-tweet" data-theme="dark"><a href="https://twitter.com/{usernames[i]}/status/{tweet_id[i]}"></a></blockquote>',
                unsafe_allow_html=True)
        for i in range(5, 10):
            twcol2.markdown(
                f'<blockquote class="twitter-tweet" data-theme="dark"><a href="https://twitter.com/{usernames[i]}/status/{tweet_id[i]}"></a></blockquote>',
                unsafe_allow_html=True)
        figure = go.Figure([go.Bar(x=usernames, y=likes)])
        return figure

    def get_freq_country(self, df):
        normal_names = df["user_location"].dropna().tolist()
        counter = collections.Counter(normal_names)
        country = list()
        for i, j in counter.most_common(5):
            country.append(pycountry.countries.get(alpha_3=i).name)
        df1 = pd.DataFrame(country, columns=['Country'])

        genres = st.sidebar.multiselect("Select Country", df1['Country'])
        if genres:
            sg = coco.convert(names=genres, to='ISO3')
            if type(sg) != list:
                sg = [sg]
            df = df[df.user_location.isin(sg)]
        return df

    def select_sentiment(self):
        select_status = st.sidebar.radio("Select Sentiment", ('Overall', 'Positive', 'Negative', 'Neutral'))
        return select_status

    def get_bigram(self):
        stoplist = stopwords.words('english') + ['though']

        c_vec = CountVectorizer(stop_words=stoplist, ngram_range=(2, 3))
        # matrix of ngrams

        df1 = self.get_data('Overall')
        df = self.get_freq_country(df1)

        ngrams = c_vec.fit_transform(df['text'])
        # count frequency of ngrams
        count_values = ngrams.toarray().sum(axis=0)
        # list of ngrams
        vocab = c_vec.vocabulary_
        df = pd.DataFrame(sorted([(count_values[i], k) for k, i in vocab.items()], reverse=True)
                          ).rename(columns={0: 'Frequency', 1: 'Word'})
        fd = df.head(10)

        g1 = go.Figure(go.Bar(x=fd["Word"], y=fd["Frequency"], name="Freq Dist"))  # 59, 89, 152
        g1.update_traces(marker_color='rgb(59, 89, 152)', marker_line_color='rgb(8,48,107)', marker_line_width=0.5,
                         opacity=0.7)  # fig.update_layout( xaxis = dict(tickfont = dict(size=9)))
        return g1

    def plot_pie(self):
        df = self.get_data('Overall')
        val_list = list()
        val_list.append(df['polarity'].value_counts()[0])
        val_list.append(df['polarity'].value_counts()[1])
        val_list.append(df['polarity'].value_counts()[-1])
        labels = ["Neutral", "Positive", "Negative"]
        g1 = go.Figure(go.Pie(labels=labels, values=val_list))
        return g1

    def live_stream(self):

        auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
        auth.set_access_token(credentials.access_token, credentials.access_token_secret)
        twitterStream = Stream(auth, TweetListener())
        twitterStream.filter(languages=["en"], track=settings.TRACK_WORDS)



st.sidebar.image("socialis-logo.svg")
graph = st.sidebar.selectbox('Select a Graph to be plotted',
                             ('Time Series', 'World Map Plot', 'Named Entities', 'Word Cloud',
                              'Influencers', 'Bigram', 'Volume Analysis', 'Highest Mentions', 'Livestream'))
a = Socialis()

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
    fig = a.plot_bar(n, 3)
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

elif graph == 'Highest Mentions':
    st.header("Highest Twitter Account Mentions")
    n = a.select_sentiment()
    fig = a.plot_bar(n, 2)
    fig.update_layout(autosize=False, height=600)
    st.plotly_chart(fig, use_container_width=True)

elif graph == "Livestream":
    st.header("Live Stream of Tweets")
    a.live_stream()
