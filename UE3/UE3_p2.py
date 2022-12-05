#build a Streamlit application, that allows exploration of the dataset.
#mongodb airbnb dataset.

#connect to mongodb
import streamlit as st
import pandas as pd
import numpy as np
import pymongo
import ssl
from pymongo import MongoClient


def load_data():
    client = MongoClient(
        'mongodb+srv://student:nRfKfRqEtgWvznFD@cluster0.gu4ru.mongodb.net')
    #load 100 entries
    db = client.get_database('sample_airbnb')

    data = pd.DataFrame(db.listingsAndReviews.find().limit(100))
    data["price"] = data.price.astype(str).astype(float)
    return data






#def render_info():
def render_info():
    st.title('Airbnb data')
    st.header('Displaying the Airbnb dataset')
    st.markdown('Using streamlit to filter and display data fetched from a mongodb database.')


#draw map
def render_map(data):
    df_map      = pd.DataFrame([pd.Series(point['location']["coordinates"], index=['lon', 'lat']) for point in data["address"]], columns=['lon', 'lat'])
    st.map(df_map)

#make price slider
def filter_by_price(data):
    #adding a range slider, allowing to choose values in range 
    range = st.slider('Price', int(min(data['price'])), int(max(data['price'])), (20, 400))

    return data[(data['price'].between(*range))]

#filter by property_type
def filter_by_property_type(data):
    property_type = st.sidebar.selectbox('Filter by different property types:', [''] + list(data['property_type'].drop_duplicates()))
    if property_type:
        return data[data['property_type'] == property_type]
    return data

def split_list(list):
    new_list = []
    for sublist in list:
        for item in sublist:
            new_list.append(item)
    return new_list
#filter by amenities
def filter_by_amenieties(data):
    unique_a = pd.Series(split_list(data['amenities'])).drop_duplicates()
    amenities = st.sidebar.selectbox('Filter by different amenities:', [''] + list(unique_a))
    if amenities:
        data = data[[(amenities in x) for x in data['amenities']]]
    return data


render_info()
data = load_data()
data = filter_by_price(data)
data = filter_by_property_type(data)
data = filter_by_amenieties(data)

st.text_input('Insight 1:', value='There is only one Airbnb that costs more than 3000 a night', max_chars=None, key=None, type='default')

st.text_input('Insight 2:', value='There are only 3 Airbnb Locations that offer breakfast', max_chars=None, key=None, type='default')


print(data)
render_map(data)
