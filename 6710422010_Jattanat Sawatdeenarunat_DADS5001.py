import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime
import plotly.express as px

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(20000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

##### Ex.4 #####
st.subheader('Number of pickups by date')
@st.cache_data
def plot():
    fig = px.bar(
        data,
        x=data[DATE_COLUMN].dt.strftime('%d-%b-%Y'),
        labels={
            "x" : "วัน/เดือน/ปี",
            "count" : "จำนวนรายการ"
        }
        )
    return fig
fig = plot()
st.plotly_chart(fig)
################


##### Ex.3 #####

st.subheader('3D Map')
option = st.selectbox(
    "Data : ",
    ("Overall", "Selected Date")
)
################
if option == "Selected Date":
    ##### Ex.2 #####
    d = st.date_input(
    "Select Date", 
    data[DATE_COLUMN].iloc[0].date(),
    min_value=min(data[DATE_COLUMN]),
    max_value=max(data[DATE_COLUMN]))
    ################
    filter_date = data[data[DATE_COLUMN].dt.date == d]
else:
    filter_date = data


##### Ex.1 #####
st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=filter_date['lat'].mean(),
            longitude=filter_date['lon'].mean(),
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=filter_date,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=filter_date,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)
################


##### Ex.5 #####
if "x" not in st.session_state:
    st.session_state.x = 0

if st.button("Click"):
    st.session_state.x = st.session_state.x + 1
st.session_state.x
################
