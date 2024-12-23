import streamlit as st
import pandas as pd
import preprocessing,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
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

if user_menu=='Country wise Analysis':
    st.sidebar.title("Country wise Analysis")
    country_list=df['region'].unique().astype(str).tolist()
    country_list.sort()
    country_list_selected=st.sidebar.selectbox("Select a country",country_list)
    country_df=helper.yearwise_sucessful(df,country_list_selected)
    fig=px.line(country_df,x='Year',y='Medal')
    st.title(country_list_selected+"  medal over the years")
    st.plotly_chart(fig)
    pt=helper.country_event_heatmap(df,country_list_selected)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax=sns.heatmap(pt,annot=True)
    st.title(country_list_selected+" excels in the following sports")

    st.pyplot(fig)
    st.title("Top 10 athletes of " + country_list_selected)
    top_10_df=helper.most_sucessful_countrywise(df,country_list_selected)
    st.table(top_10_df)

if user_menu=='Athlete wise Analysis':
    athletes_df=df.drop_duplicates(subset=['Name','region'])
    x1=athletes_df['Age'].dropna()
    x2=athletes_df[athletes_df['Medal']=="Gold"]['Age'].dropna()
    x3=athletes_df[athletes_df['Medal']=="Silver"]['Age'].dropna()
    x4=athletes_df[athletes_df['Medal']=="Bronze"]['Age'].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall_Age','Gold_medalist','Silver_Medalist','Bronze_Medalist'],show_hist=False,show_rug=False)
    st.title("Distribution of Age")
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athletes_df[athletes_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(
    x='Weight', 
    y='Height', 
    hue='Medal', 
    style='Sex', 
    s=60, 
    data=temp_df
)
    st.pyplot(fig)




