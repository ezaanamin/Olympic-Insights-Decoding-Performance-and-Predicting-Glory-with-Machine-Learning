import streamlit as st
import pandas as pd
import preprocessing,helper

df=pd.read_csv("/home/ezaan-amin/Documents/PortFolio/Olympic Insights_Decoding Performance and Predicting Glory with Machine Learning/Model/DataSet/athlete_events.csv")
region_df=pd.read_csv("/home/ezaan-amin/Documents/PortFolio/Olympic Insights_Decoding Performance and Predicting Glory with Machine Learning/Model/DataSet/noc_regions.csv")


df=preprocessing.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis ")
user_menu=st.sidebar.radio(
    'Select an Option',
    ("Medal Tally",'Overall Analysis','Country wise Analysis','Athlete wise Analysis')
)



if user_menu=="Medal Tally":
    st.header("Medal Tally")
    year,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select years",year)
    selected_year=st.sidebar.selectbox("Select country",country)
    medal_tally=helper.metal_tally(df)
    st.dataframe(medal_tally)