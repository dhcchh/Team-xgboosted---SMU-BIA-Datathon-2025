
import pandas as pd
import plotly.express as px

def line_builder(df, source_list):
    """
    Parameters:
        df (pandas.DataFrame): Processed dataset containing incident information.
        source_list (list): List of selected data sources ('news' or 'leaks').

    Returns:
        tuple: Four line charts (terrorism, cyber_security, espionage, communalism).
    """

    # Ensure 'source' column exists
    if 'source' not in df.columns:
        raise KeyError("The 'source' column is missing in the dataset.")

    # Filter dataset based on selected sources
    df_filtered = df[df["source"].isin(source_list)]
    df_filtered = df_filtered[df_filtered['year'] >= 2000]

    # Ensure 'year' column exists
    if 'year' not in df_filtered.columns:
        raise KeyError("The 'year' column is missing in the dataset.")

    # Ensure 'month' column exists, defaulting to January if missing
    if 'month' not in df_filtered.columns:
        df_filtered['month'] = 1  # Default to January

    # Convert 'year' and 'month' to numeric values, handling errors
    df_filtered["year"] = pd.to_numeric(df_filtered["year"], errors="coerce")
    df_filtered["month"] = pd.to_numeric(df_filtered["month"], errors="coerce")

    # Remove invalid year values (year=0 or NaN)
    df_filtered = df_filtered[df_filtered["year"] > 1900]  # Assuming valid years start from 1900

    # Ensure month is within valid range (1-12)
    df_filtered = df_filtered[df_filtered["month"].between(1, 12)]

    # Convert year/month into datetime format safely
    df_filtered['date'] = pd.to_datetime(
        df_filtered.assign(day=1)[['year', 'month', 'day']],
        errors='coerce'
    )

    # Drop rows where datetime conversion failed
    df_filtered = df_filtered.dropna(subset=['date'])

    # Aggregate counts for each category over time
    category_columns = ["terrorism", "cyber_security", "espionage", "communalism"]
    df_grouped = df_filtered.groupby("date")[category_columns].sum().reset_index()

    # Create line charts for each category
    line_figs = {}
    for category in category_columns:
        fig = px.line(
            df_grouped,
            x="date",
            y=category,
            title=f"Trend of {category.capitalize()} Incidents",
            labels={"date": "Date", category: "Incident Count"},
            markers=True
        )
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Count",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True),
            plot_bgcolor="white"
        )
        line_figs[category] = fig

    return line_figs["terrorism"], line_figs["cyber_security"], line_figs["espionage"], line_figs["communalism"]
