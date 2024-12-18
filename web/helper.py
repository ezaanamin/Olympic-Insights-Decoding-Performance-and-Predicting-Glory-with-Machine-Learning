import numpy as np

def metal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','City','Year','Medal','Games','Event','Sport'])
    m_tally=medal_tally.groupby("region").sum()[['Bronze', 'Gold', 'Silver']].sort_values("Gold",ascending=False).reset_index()
    m_tally['total']=m_tally['Gold']+m_tally['Bronze']+m_tally['Silver']
    return m_tally


def country_year_list(df):
    year=df['Year'].unique().tolist()
    year.sort()
    year.insert(0,'Overall')
    country=np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    return country,year


def fetch_Medal_Tally(df,country,year):
    flag=0
    medal_tally=df.drop_duplicates(subset=['Team','NOC','City','Year','Medal','Games','Event','Sport'])
    if year=='Overall' and country =='Overall':
        temp_df=medal_tally
    if year=='Overall' and country!='Overall':
        flag=1
        temp_df=medal_tally[medal_tally['region']==country]
    if year!='Overall' and country=='Overall':
        temp_df=medal_tally[medal_tally['Year']==year]
    if year!='Overall' and country!='Overall':
          temp_df = medal_tally[(medal_tally['Year'] == int(year)) & (medal_tally['region'] == country)]
     
    if flag==1:
        x=temp_df.groupby("Year").sum()[['Bronze', 'Gold', 'Silver']].sort_values("Year",ascending=False).reset_index()

    else:
        x=temp_df.groupby("region").sum()[['Bronze', 'Gold', 'Silver']].sort_values("Gold",ascending=False).reset_index()

    x['total']=x['Gold']+x['Bronze']+x['Silver']


    return x
def participating_nations_over_time(df):
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('count')
    nations_over_time.rename(columns={'count':'Editions','Year':'no of countries'},inplace=True)
    return nations_over_time 


def most_sucessful(df,sport):
    temp_df=df.dropna(subset=['Medal'])
    if sport!='Overall':
        temp_df=temp_df[temp_df['Sport']==sport]
    x = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(15)
        .assign(count=lambda df_: df_['Name'].astype(str)) 
        .merge(df, left_on='count', right_on='Name', how='left')[['count', 'Name_x', 'Sport', 'region']]
        .drop_duplicates('count')
    )
    return x
