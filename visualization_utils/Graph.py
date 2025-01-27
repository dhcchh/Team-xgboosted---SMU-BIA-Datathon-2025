import numpy as np
import pandas as pd
import dash_cytoscape as cyto

# sample return call
# elements = [
#     # Nodes
#     {"data": {"id": "A", "label": "Node A"}},
#     {"data": {"id": "B", "label": "Node B"}},
#     {"data": {"id": "C", "label": "Node C"}},

#     # Edges
#     {"data": {"source": "A", "target": "B"}},  # Edge from A to B
#     {"data": {"source": "A", "target": "C"}},  # Edge from A to C
#     {"data": {"source": "B", "target": "C"}},  # Edge from B to C
# ]
# return elements

def graph_builder(df, source, category):
    """
    Recieves a dataframe. Runs BFS from Singapore to find the closest 3 countries. Do
    include edges between countries that are not Singapore as well.

    Parameters:
        df (pandas.dataframe): Dataframe (refer to csv file given).
        source(list): List of strings, possible values 
            are ["leaks", "news"].
        category (list): List of strings, possible values 
            are ["terrorism", "security", "espionage", "communal"]
    Returns:
        elements (list): Refer to above for format of answer. Returns an undirected graph.
            Maximum 3 edges away from Singapore. 
    """
    cyto.Cytoscape(
        id = "network-graph",
        elements = graph_builder(),  
        style = {
            "width": "100%",
            "height": "500px"
            },
        layout = {
            "name": "circle"
            },  # Specify graph layout (e.g., circle, grid)
        stylesheet = [
            {
                "selector": "node",
                "style": {
                    "content": "data(label)",
                    "background-color": BG,
                    "color": NODE,
                    "text-valign": "center"
                }
            },
            {
                "selector": "edge",
                "style": {
                    "line-color": EDGE,
                    "target-arrow-color": EDGE,
                    "target-arrow-shape": "triangle",
                    "curve-style": "bezier"
                }
            }
        ]
    )

    print("To be implemented!")
    raise NotImplementedError