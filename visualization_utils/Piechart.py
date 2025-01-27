import pandas as pd

def piechart_builder(df, source):
    """
    Function that takes in a dataframe and source ('news'/'leaks') and returns the count of each category
    after filtering based on source.

    Parameters:
        df (pandas.DataFrame): Input dataframe containing threat categories and source.
        source (str): String, possible values are "news" or "leaks".
        
    Returns:
        result (list): A list containing the aggregated count of each threat category 
                       formatted for a pie chart.
    """

    # Filter the dataset based on the source (e.g., news or leaks)
    df_filtered = df[df['source'] == source]

    # Ensure boolean columns are converted to integers for correct aggregation
    category_columns = ['terrorism', 'security', 'espionage', 'communalism']
    df_filtered[category_columns] = df_filtered[category_columns].astype(int)

    # Summing up occurrences of each category across all rows
    category_counts = df_filtered[category_columns].sum().to_dict()

    # Formatting results for pie chart in the required structure
    result = [
        {
            "labels": list(category_counts.keys()),  # Category names for pie chart labels
            "values": list(category_counts.values()),  # Corresponding counts for each category
            "type": "pie"
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

    # Generate pie chart data for "news" source
    pie_chart_data = piechart_builder(combined_df, "news")
    print(pie_chart_data)
