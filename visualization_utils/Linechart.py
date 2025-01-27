import numpy as np
import pandas as pd

def line_builder(df, source, category):
    """
    Parameters:
        df (pandas.DataFrame): Dataframe containing threat data.
        source (str): Data source, either "news" or "leaks".
        category (str): The selected category (e.g., "terrorism", "security", etc.).
    
    Returns:
        elements (list): A list of dictionaries formatted for a line chart.
    """

    # Filter the dataset based on the selected source (news or leaks)
    df_filtered = df[df['source'] == source]

    # Convert boolean columns to integers for aggregation
    category_columns = ['terrorism', 'security', 'espionage', 'communalism']
    df_filtered[category_columns] = df_filtered[category_columns].astype(int)

    # Ensure date columns are properly combined and handled
    df_filtered['date'] = pd.to_datetime(df_filtered[['year', 'month', 'day']], errors='coerce')

    # Group data by year-month and sum numeric columns only
    time_series = df_filtered.groupby(df_filtered['date'].dt.to_period("M"))[category_columns].sum().reset_index()
    time_series['date'] = time_series['date'].astype(str)  # Convert to string for visualization

    # Prepare data for the line chart
    result = [
        {
            "x": time_series['date'].tolist(),
            "y": time_series[category].tolist(),
            "type": "line",
            "name": f"{category.capitalize()} Trends"
        }
    ]

    return result


# Example usage for testing
if __name__ == "__main__":
    # Load the processed data
    df_news = pd.read_csv("Dataset/processed_news_2.csv")
    df_news['source'] = 'news'

    df_leaks = pd.read_csv("Dataset/processed_leaks_2.csv")
    df_leaks['source'] = 'leaks'

    # Combine both datasets for flexibility
    combined_df = pd.concat([df_news, df_leaks], ignore_index=True)

    # Generate line chart data for "news" source
    line_chart_data = line_builder(combined_df, "news", "security")
    print(line_chart_data)
