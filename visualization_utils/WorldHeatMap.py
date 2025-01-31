import pandas as pd
import plotly.express as px

CUTOFF = 20

def heatmap_builder(df, source_list):
    """
    Parameters:
        df (pandas.DataFrame): Processed dataset containing geolocation information.
        source_list (list): List of selected data sources ('news' or 'leaks').

    Returns:
        fig (plotly.graph_objects.Figure): Heatmap figure with consistent color scaling.
    """
    if 'source' not in df.columns:
        raise KeyError("The 'source' column is missing in the dataset.")
    
    df_filtered = df[df["source"].isin(source_list)]
    if 'countries' not in df_filtered.columns:
        raise KeyError("The 'countries' column is missing in the dataset.")

    df_filtered['countries'] = df_filtered['countries'].apply(
        lambda x: eval(x)
    )

    df_exploded = df_filtered.explode('countries')

    country_counts = df_exploded['countries'].value_counts().reset_index()
    country_counts = country_counts[country_counts['count'] >= CUTOFF]
    country_counts.columns = ['Country', 'Count']

    fig = px.scatter_geo(
        country_counts,
        locations="Country",
        locationmode="country names",
        size="Count",  
        hover_name="Country",
        color="Count", 
        color_continuous_scale="RdBu",
        projection="equirectangular",
        size_max=80
    )

    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        geo=dict(
            showland=True,
            showocean=True,
            oceancolor="#1B2444",  # Dark blue ocean
            landcolor="#161D33",  
            showframe=False,  # No frame around the map
            projection_scale=1  # Adjust projection scale if needed
        ),
        coloraxis_colorbar=dict(
            title="Count",
            title_font=dict(size=12),  # Smaller font size for title
            tickfont=dict(size=10),  # Smaller font size for ticks
            thickness=10,  # Adjust the thickness of the color bar
            len=0.35,  # Adjust the length of the color bar (relative to the plot height)
            x=0.75,  # Shift the legend inward horizontally (0.0 is far left, 1.0 is far right)
            xanchor="center",  # Anchor the legend position horizontally
            y=0.2,  # Position vertically (0.0 is bottom, 1.0 is top)
            yanchor="middle"  # Anchor the legend position vertically
        )
    )
    fig.update_layout({
        'geo': {
            'resolution': 50
        }
    })
    return fig
