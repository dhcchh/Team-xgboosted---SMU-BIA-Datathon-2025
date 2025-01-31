import pandas as pd
import plotly.express as px

CATEGORY_COLUMNS = ['terrorism', 'cyber_security', 'espionage', 'communalism']
RENAME_COLUMNS = {'terrorism': 'Terrorism',
                 'cyber_security': 'Cyber Security',
                 'espionage': 'Espionage',
                 'communalism': 'Communalism'}
COLOR_MAP = {
    "Cyber Security": "#636efa",     # Blue (same as pie chart)
    "Terrorism": "#EF553B",    # Red
    "Communalism": "#00cc96",  # Green
    "Espionage": "#ab63fa"     # Purple
}

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
    category_counts = category_counts[category_counts != 0].to_frame().reset_index()
    category_counts.columns = ['Category', 'Count']
    category_counts['Category'] = category_counts['Category'].apply(lambda x:RENAME_COLUMNS[x])
    piechart = px.pie(
        data_frame = category_counts,
        names = 'Category',
        values = 'Count',
        color="Category",
        color_discrete_map=COLOR_MAP 
    )
    piechart.update_layout(showlegend=False)
    return piechart