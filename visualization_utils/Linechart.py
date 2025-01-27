import numpy as np
import pandas as pd
import plotly.express as px
# sample return call
# result = [
#         {
#             "x": ["2023-01-01", "2023-01-02", "2023-01-03"],  
#             "y": [10, 15, 7], 
#             "type": "line", 
#             "name": "Example Line"
#         }
#     ]

CATEGORY_COLUMNS = ["terrorism", "security", "espionage", "communalism"]

def line_builder(df, source):
    """
    Parameters:
        df (pandas.Dataframe): Dataframe, refer to csv for details.
    
    Returns:
        elements (list): Refer to above for the required format.
    """
    source_df = df.copy()
    source_df = source_df[source_df["year"] != 0]
    source_df[CATEGORY_COLUMNS] = source_df[CATEGORY_COLUMNS].astype(int)
    source_df["date"] = pd.to_datetime(source_df[['year', 'month']], errors='coerce')
    source_df = source_df.groupby("date").sum().reset_index()
    
    terrorism = px.line(source_df, x = "date", y = "terrorism", title = "Terrorism")
    security = px.line(source_df, x = "date", y = "security", title = "Terrorism")
    espionage = px.line(source_df, x = "date", y = "espionage", title = "Terrorism")
    communalism = px.line(source_df, x = "date", y = "communalism", title = "Terrorism")
    return terrorism, security, espionage, communalism