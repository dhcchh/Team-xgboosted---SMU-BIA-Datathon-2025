import pandas as pd
import numpy as np

# sample return call
# result = [
#         {
#             "labels": ["Category A", "Category B", "Category C"],
#             "values": [30, 40, 30],
#             "type": "pie"
#         }
#     ]

def piechart_builder(df, source):
    """
    Function that takes in a dataframe, "news"/"leaks", and returns the count of each category
    after filtering based on source.

    Parameters:
        df (pandas.Dataframe): Refer to csv.
        source (list): List of strings, possible values are ["news", "leaks"].
        
    Returns:
        result (list): Refer to the format above.
    """
    print("To be implemented!")
    raise NotImplementedError