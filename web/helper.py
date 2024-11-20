def metal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','City','Year','Medal','Games','Event','Sport'])
    m_tally=medal_tally.groupby("region").sum()[['Bronze', 'Gold', 'Silver']].sort_values("Gold",ascending=False).reset_index()
    m_tally['total']=m_tally['Gold']+m_tally['Bronze']+m_tally['Silver']
    return m_tally

