import pandas as pd
import plotly.express as px
import numpy as np

def heatmap_builder(df, source_list):
    """
    Parameters:
        df (pandas.DataFrame): Processed dataset containing geolocation information.
        source_list (list): List of selected data sources ('news' or 'leaks').

    Returns:
        fig (plotly.graph_objects.Figure): Heatmap figure with consistent color scaling.
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

    # Calculate range for color scaling
    min_count = country_counts["Count"].min()
    max_count = country_counts["Count"].max()
    range_color = [min_count, max_count]  # Ensuring full range is covered

    import numpy as np

    # Apply logarithmic transformation to prevent outliers from skewing scale
    country_counts["Normalized Count"] = np.log1p(country_counts["Count"])  # log(Count + 1) to avoid log(0)

    fig = px.choropleth(
        country_counts,
        locations='Country',
        locationmode='country names',
        color='Normalized Count',  # Use log-transformed values for better distinction
        hover_name='Country',
        color_continuous_scale='Viridis',
        title=f"Heatmap of Incidents from {', '.join(source_list).capitalize()} Data"
)



    fig.update_geos(
        projection_type="natural earth",
        showcoastlines=True,
        coastlinecolor="black",  # Makes coastlines more visible
        showland=True,
        landcolor="LightGray"
)

    fig.update_layout(
        title={
            "text": f"Heatmap of Incidents from {', '.join(source_list).capitalize()} Data",
            "x": 0.5,  # Center the title
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=20)
        },
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        coloraxis_colorbar=dict(title="Incident Count")
)

    return fig
