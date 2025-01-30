import numpy as np
import pandas as pd
import plotly.express as px

def barchart_builder(df, source):
    """
    Filters the dataframe according to source. Counts the number of entries that belong to each
    category after filtering.
    
    Parameters:
        df (pandas.DataFrame): Dataframe (refer to csv).
        source (list): List containing 1-2 strings, "leaks" & "news".
         
    Returns:
        plotly.graph_objects.Figure: A bar chart with matching colors from the pie chart.
    """

    source_df = df.copy()
    source_df = source_df[source_df["source"].isin(source)]
    category_columns = ['terrorism', 'cyber_security', 'espionage', 'communalism']
    source_df[category_columns] = source_df[category_columns].astype(int)
    category_counts = source_df[category_columns].sum()

    category_counts_df = pd.DataFrame({
        "Category": category_counts.index,
        "Count": category_counts.values
    })

    # Define the color mapping to match the pie chart
    color_map = {
        "cyber_security": "#636efa",     # Blue (same as pie chart)
        "terrorism": "#EF553B",    # Red
        "communalism": "#00cc96",  # Green
        "espionage": "#ab63fa"     # Purple
    }

    # Create bar chart with the same colors
    barchart = px.bar(
        category_counts_df,         
        x="Category",   
        y="Count",
        color="Category",
        color_discrete_map=color_map  # Apply the same colors as the pie chart
    )

    # Improve layout for consistency
    barchart.update_layout(
        xaxis_title=None, 
        yaxis_title=None,
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
        paper_bgcolor="rgba(0,0,0,0)", 
        font=dict(color="cyan")  # Match font color to maintain contrast
    )

    return barchart
