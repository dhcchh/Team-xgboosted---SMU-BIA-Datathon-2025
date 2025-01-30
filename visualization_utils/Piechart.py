import pandas as pd
import plotly.express as px

CATEGORY_COLUMNS = ['terrorism', 'cyber_security', 'espionage', 'communalism']

def piechart_builder(df, source):
    """
    Function that takes in a dataframe and source ('news'/'leaks') and returns the count of each category
    after filtering based on source.

    Parameters:
        df (pandas.DataFrame): Input dataframe containing threat categories and source.
        source (str): String, possible values are "news" or "leaks".
        
    Returns:
        piechart
    """
    source_df = df.copy()
    source_df = source_df[source_df['source'].isin(source)]
    source_df[CATEGORY_COLUMNS] = source_df[CATEGORY_COLUMNS].astype(int)
    category_counts = source_df[CATEGORY_COLUMNS].sum()
    category_counts = category_counts[category_counts != 0].to_dict()
    piechart = px.pie(
        names = list(category_counts.keys()),
        values = list(category_counts.values())
    )
    return piechart