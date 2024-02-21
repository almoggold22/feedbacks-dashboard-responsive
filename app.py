import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Hello",
    page_icon= ":bar_chart:"
)
st.sidebar.success("Select a Page above")

#Compare Page:
#Display Title and Despcription
st.title(":grey[Feedbacks] :green[Dashboard]")
st.markdown("**Compare**")

#Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
url = 'https://docs.google.com/spreadsheets/d/1kSeOTYs4XPxA2Rqb3Jz5tezwjllUmbRfBO1csTILHvE/edit'

#---API Part Up To Here----------------------------------------------------------------------------------------------------------------------------------------

#-1-Set Connection with gsheets page:
left_chart = conn.read(spreadsheet=url, worksheet='1763036692', usecols=list(range(9, 72)), ttl=5)
right_chart = conn.read(spreadsheet=url, worksheet='1763036692', usecols=list(range(9, 72)), ttl=5)

#left - list of date's columns names and chosen buttons:
models_dates_col_left = ['Translation in date', 'Intents date', 'Embedding date', 'AI21 date', 'Rephrase date', 'Translation out date', 'Entire flow date', 'Score date']
buttons_col_of_each_model_left = ['Translation in buttons1', 'Intents buttons1', 'Closest questions (embedding) buttons1', 'Contextual answer (AI21) buttons1', 'Rephrase buttons1', 'Translation out buttons1', 'Entire flow buttons1', 'Score buttons1']

#right - list of date's columns names and chosen buttons:
models_dates_col_right = ['Translation in date', 'Intents date', 'Embedding date', 'AI21 date', 'Rephrase date', 'Translation out date', 'Entire flow date', 'Score date']
buttons_col_of_each_model_right = ['Translation in buttons1', 'Intents buttons1', 'Closest questions (embedding) buttons1', 'Contextual answer (AI21) buttons1', 'Rephrase buttons1', 'Translation out buttons1', 'Entire flow buttons1', 'Score buttons1']

#create right and left columns on streamlit for choosing model:
col_model_left, col_model_right = st.columns((2))
with col_model_left:
    model_type_left = st.selectbox("Choose Model (Left)", models_dates_col_left)

with col_model_right:
    model_type_right = st.selectbox("Choose Model (Right)", models_dates_col_right)

#Dates Range
if model_type_left:
    left_chart[model_type_left] = pd.to_datetime(left_chart[model_type_left])
    today1 = conn.read(spreadsheet=url, worksheet='1082314658', usecols=list(range(9)), ttl=5)
    start_date_1 = pd.to_datetime(left_chart[model_type_left]).min()
    end_date_1 = pd.to_datetime(today1['today']).max()
    #----
if col_model_right:
    right_chart[model_type_right] = pd.to_datetime(right_chart[model_type_right])
    today2 = conn.read(spreadsheet=url, worksheet='1082314658', usecols=list(range(9)), ttl=5)
    start_date_2 = pd.to_datetime(right_chart[model_type_right]).min()
    end_date_2 = pd.to_datetime(today2['today']).max()

col1, col2, col3, col4 = st.columns((4))
#---Make dates as columns---
with col1:
    date1 = pd.to_datetime(st.date_input("Start date", start_date_1))

with col2:
    date2 = pd.to_datetime(st.date_input("End date", end_date_1))

with col3:
    date3 = pd.to_datetime(st.date_input("Intents Start date", start_date_2))

with col4:
    date4 = pd.to_datetime(st.date_input("Intents End date", end_date_2))

#set range and terms for columns (gt, lt, eq)
left_range = left_chart[(left_chart[model_type_left] >= date1) & (left_chart[model_type_left] <= date2)].copy()
right_range = right_chart[(right_chart[model_type_right] >= date3) & (right_chart[model_type_right] <= date4)].copy()
#------------------- Up to here Date Part

#functions to fine the index of the relevant buttons' column and use it on pie charts:
def index_finder_left(models_dates_col_left):
    for model in models_dates_col_left:
        if model_type_left == model:
            name_of_buttons_col_left = models_dates_col_left.index(model_type_left)
            return name_of_buttons_col_left

def index_finder_right(models_dates_col_right):
    for model in models_dates_col_right:
        if model_type_right == model:
            name_of_buttons_col_right = models_dates_col_right.index(model_type_right)
            return name_of_buttons_col_right

#columns for pie charts
col_model1, col_model2 = st.columns((2))
#---2---Pie-Charts--
#'translation in' columns - left side
existing_data_left = conn.read(spreadsheet=url, worksheet='1763036692', usecols=list(range(9, 72)), ttl=5)
size_left = left_range.groupby(buttons_col_of_each_model_left[index_finder_left(models_dates_col_left)]).size()
pie_chart_left = px.pie(left_range, title=model_type_left, values=size_left, names=size_left.index, height = 500, width= 550)


#'intents' columns - right side
existing_data_right = conn.read(spreadsheet=url, worksheet='1763036692', usecols=list(range(9, 72)), ttl=5)
size_right = right_range.groupby(buttons_col_of_each_model_right[index_finder_right(models_dates_col_right)]).size()
pie_chart_right = px.pie(right_range, title=model_type_right, values=size_right, names=size_right.index, height = 500, width= 550)

with col_model1:
    st.plotly_chart(pie_chart_left)
with col_model2:
    st.plotly_chart(pie_chart_right)





###Relevant for second page
###'Closest questions (embedding)' columns
#existing_data_embedding = conn.read(spreadsheet=url, worksheet='1763036692', usecols=list(range(27, 35)), ttl=5)
#size_embedding = existing_data_embedding.groupby('Closest questions (embedding) buttons1').size()

###'Contextual answer (AI21)' columns
#existing_data_ai21 = conn.read(spreadsheet=url, worksheet='1763036692', usecols=list(range(36, 44)), ttl=5)
#size_ai21 = existing_data_ai21.groupby('Contextual answer (AI21) buttons1').size()

###'Rephrase' columns
#existing_data_rephrase = conn.read(spreadsheet=url, worksheet='1763036692', usecols=list(range(45, 53)), ttl=5)
#size_rephrase = existing_data_rephrase.groupby('Rephrase buttons1').size()

###'Translation Out' columns
#existing_data_translation_out = conn.read(spreadsheet=url, worksheet='1763036692', usecols=list(range(54, 62)), ttl=5)
#size_translation_out = existing_data_translation_out.groupby('Translation out buttons1').size()

###'Entire Flow' columns
#existing_data_entire_flow = conn.read(spreadsheet=url, worksheet='1763036692', usecols=list(range(63, 71)), ttl=5)
#size_entire_flow = existing_data_entire_flow.groupby('Entire flow buttons1').size()

st.divider()
