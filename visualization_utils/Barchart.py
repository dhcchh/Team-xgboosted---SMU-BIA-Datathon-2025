import numpy as np
import pandas as pd
import plotly.express as px

def barchart_builder(df, source):
    """
    Filters the dataframe according to source. Counts the number of entries that belongs to each
    category after filtering
    
    Parameters:
        df (pandas.Dataframe): Dataframe (refer to csv).
        source (list): List containing 1-2 strings, "leaks" & "news".
         
    Returns:

    """
    source_df = df.copy()
    source_df = source_df[source_df["source"].isin(source)]
    category_columns = ['terrorism', 'security', 'espionage', 'communalism']
    source_df[category_columns] = source_df[category_columns].astype(int)
    category_counts = source_df[category_columns].sum()
    category_counts_df = pd.DataFrame({
        "Category": category_counts.index,
        "Count": category_counts.values
    })
    barchart = px.bar(
        category_counts_df,         
        x = "Category",   
        y = "Count"
    )
    barchart.update_layout(
        xaxis_title=None, 
        yaxis_title=None  
    )
    return barchart