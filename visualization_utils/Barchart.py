import numpy as np
import pandas as pd
import plotly.express as px

CATEGORY_COLUMNS = ['terrorism', 'cyber_security', 'espionage', 'communalism']
FINAL_COLUMNS = ['Terrorism', 'Cyber Security', 'Espionage', 'Communalism']
COLOR_MAP = {
    "Cyber Security": "#636efa",     # Blue (same as pie chart)
    "Terrorism": "#EF553B",    # Red
    "Communalism": "#00cc96",  # Green
    "Espionage": "#ab63fa"     # Purple
}
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
    
    source_df[CATEGORY_COLUMNS] = source_df[CATEGORY_COLUMNS].astype(int)
    source_df = source_df.rename(
        columns={
            'terrorism': 'Terrorism',
            'cyber_security': 'Cyber Security',
            'espionage' : 'Espionage',
            'communalism': 'Communalism'
        }
    )
    category_counts = source_df[FINAL_COLUMNS].sum()

    category_counts_df = pd.DataFrame({
        "Category": category_counts.index,
        "Count": category_counts.values
    })

    barchart = px.bar(
        category_counts_df,         
        x="Category",   
        y="Count",
        color="Category",
        color_discrete_map=COLOR_MAP
    )

    barchart.update_layout(
        xaxis_title=None, 
        yaxis_title=None,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)", 
        font=dict(color="cyan"),
        legend=dict(
            x=1.3,  # Move legend to the right (1.0 is the default right edge of the plot)
            y=0.8,  # Keep the legend vertically centered
            xanchor="left",  # Anchor the legend's left edge at the x position
            yanchor="middle",  # Anchor the legend's middle at the y position
        ),
        bargap=0.5
    )
    barchart.update_layout(
    height=450,  # Set chart height
    width=800,   # Set chart width
    )
    barchart.update_xaxes(showticklabels=False)

    return barchart
