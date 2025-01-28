import pandas as pd
import plotly.express as px

def heatmap_builder(df, source_list):
    """
    Parameters:
        df (pandas.DataFrame): Processed dataset containing geolocation information.
        source_list (list): List of selected data sources ('news' or 'leaks').

    Returns:
        fig (plotly.graph_objects.Figure): Heatmap figure.
    """

    # Ensure 'source' column exists
    if 'source' not in df.columns:
        raise KeyError("The 'source' column is missing in the dataset.")

    # Filter dataset based on selected sources (handles multiple sources)
    df_filtered = df[df["source"].isin(source_list)]

    # Ensure 'countries' column exists
    if 'countries' not in df_filtered.columns:
        raise KeyError("The 'countries' column is missing in the dataset.")

    # Convert country entries into lists if stored as strings
    df_filtered['countries'] = df_filtered['countries'].apply(
        lambda x: x.split(', ') if isinstance(x, str) else x
    )

    # Explode the 'countries' column to have one country per row
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
        title=f"Heatmap of Incidents from {', '.join(source_list).capitalize()} Data"
    )

    fig.update_geos(
        projection_type="natural earth",
        showcoastlines=True,
        coastlinecolor="RebeccaPurple",
        showland=True,
        landcolor="LightGray"
    )

    fig.update_layout(
        margin={"r":0, "t":30, "l":0, "b":0},
        coloraxis_colorbar=dict(title="Incident Count")
    )

    return fig