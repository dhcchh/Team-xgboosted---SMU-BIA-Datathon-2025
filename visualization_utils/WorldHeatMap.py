import pandas as pd
import plotly.express as px

def heatmap_builder(df, source):
    """
    Parameters:
        df (pandas.DataFrame): Processed dataset containing geolocation information.
        source (str): Data source ('news' or 'leaks').

    Returns:
        fig (plotly.graph_objects.Figure): Heatmap figure.
    """

    # Add a 'source' column if it does not exist
    if 'source' not in df.columns:
        raise KeyError("The 'source' column is missing in the dataset.")

    # Filter based on selected source
    df_filtered = df[df['source'] == source]

    # Ensure 'countries' column exists
    if 'countries' not in df_filtered.columns:
        raise KeyError("The 'countries' column is missing in the dataset.")

    # Exploding the list of countries (handling comma-separated values if necessary)
    df_filtered['countries'] = df_filtered['countries'].apply(lambda x: x.split(', ') if isinstance(x, str) else x)
    df_exploded = df_filtered.explode('countries')

    # Count occurrences of each country
    country_counts = df_exploded['countries'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']

    # Create a choropleth heatmap using Plotly
    fig = px.choropleth(
        country_counts,
        locations='Country',
        locationmode='country names',
        color='Count',
        hover_name='Country',
        color_continuous_scale='Viridis',
        title=f"Heatmap of Incidents from {source.capitalize()} Data"
    )

    fig.update_geos(
        projection_type="natural earth",
        showcoastlines=True,
        coastlinecolor="RebeccaPurple",
        showland=True, landcolor="LightGray"
    )

    fig.update_layout(
        margin={"r":0,"t":30,"l":0,"b":0},
        coloraxis_colorbar=dict(title="Incident Count")
    )

    return fig
