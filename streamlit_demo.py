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
from nltk.probability import FreqDist
import time
import country_converter as coco
import warnings
import collections

class FileReference:
    def __init__(self, filename):
        self.filename = filename


# @st.cache(persist=True)
# @st.cache(allow_output_mutation=True)
def connect_engine():
    conn1 = sqlite3.connect('twitter.db')
    return conn1

# data=pd.read_sql("select * from facebook", conn1)

graph = st.sidebar.selectbox('Select a Graph to be plotted',('Time Series', 'Choropleth', 'Bar'))

# @st.cache(allow_output_mutation=True)
# @st.cache(persist=True)
@st.cache(hash_funcs={FileReference: connect_engine})
def get_data(n):
    conn1=connect_engine()
    if n==1:
        timenow = (datetime.datetime.utcnow() - datetime.timedelta(hours=0, minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        query = "SELECT * FROM {} WHERE created_at <= '{}' " .format(settings.TABLE_NAME, timenow)
        # query = "select * from Facebook"
        df = pd.read_sql(query, con=conn1)    
    if n==2:
        df = pd.read_sql("select * from Facebook", con=conn1)
    return df

# @st.cache(allow_output_mutation=True)
def plot_line():
    # timenow = (datetime.datetime.utcnow() - datetime.timedelta(hours=0, minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
    # query = "SELECT * FROM {} WHERE created_at <= '{}' " .format(settings.TABLE_NAME, timenow)
    # df = pd.read_sql(query, con=conn1)
    
    df=get_data(1)
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




@st.cache
def plot_choro():
    df=get_data(2)
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

def plot_bar(fd):
    
    g1=go.Figure(go.Bar(x=fd["Word"], y=fd["Frequency"], name="Freq Dist")) # 59, 89, 152
    g1.update_traces(marker_color='rgb(59, 89, 152)', marker_line_color='rgb(8,48,107)', marker_line_width=0.5, opacity=0.7) # fig.update_layout( xaxis = dict(tickfont = dict(size=9)))
    return g1

if graph == "Time Series":
    fig=plot_line()
    st.plotly_chart(fig)

elif graph == "Choropleth":
    fig=plot_choro()
    st.plotly_chart(fig)

elif graph == "Bar":
    df=get_data(2)
    select_status = st.sidebar.radio("Select Sentiment", ('Positive', 'Negative', 'Neutral'))
    # Plot Bar chart   
    li=list()
    for i in df["named_ent"]:    
        te=i.split(",")    
        li.extend(te)

    li = list(filter(None, li))
    fdist = FreqDist(li)
    fd = pd.DataFrame(fdist.most_common(10), columns = ["Word","Frequency"]).drop([0]).reindex()

    if select_status == 'Positive':
        fig=plot_bar(fd)
        st.plotly_chart(fig)

