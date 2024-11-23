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
    country,year=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select years",year)
    selected_country=st.sidebar.selectbox("Select country",country)
    medal_tally=helper.fetch_Medal_Tally(df,selected_country,selected_year)
    if selected_country=="Overall" and selected_year=="Overall":
        st.title("Overall Tally")
    if selected_country!="Overall" and selected_year=="Overall":
        st.title(str(selected_country) + "Overall Tally")
    if selected_country!="Overall" and selected_year!="Overall":
        st.title(str(selected_country)+"overall tally in"+str(selected_year))
    if selected_country=="Overall" and selected_year!="Overall":
        st.title("Overall Tally in "+str(year))
    st.table(medal_tally)