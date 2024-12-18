import streamlit as st
import pandas as pd
import preprocessing,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


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

if user_menu=='Overall Analysis':

    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sport=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Host")
        st.title(cities)
    with col3:
        st.header("Sport")
        st.title(sport)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Event")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)
    nations_over_time=helper.participating_nations_over_time(df)
    fig=px.line(nations_over_time,x='Editions',y='no of countries')
    st.plotly_chart(fig)
    
    st.title("No of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)
    st.title('Most Sucessfully Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox("Select a sport",sport_list)
    x=helper.most_sucessful(df,selected_sport)
    st.table(x)



