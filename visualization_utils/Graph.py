import networkx as nx
import numpy as np
import pandas as pd

from functools import reduce
from itertools import combinations


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

def graph_builder(df: pd.DataFrame, category: list[str]) -> list[dict]:
    """
    Recieves a dataframe. Runs BFS from Singapore to find the closest 3 countries. Do
    include edges between countries that are not Singapore as well.

    Parameters:
        df (pandas.dataframe): Dataframe (refer to csv file given).
        category (list): List of strings, possible values
            are ["terrorism", "cyber_security", "espionage", "communal"]
    Returns:
        elements (list): Refer to above for format of answer. Returns an undirected graph.
            Maximum 3 edges away from Singapore.
    """
    G = nx.Graph()
    combiner = lambda x, y: x or row[y]  # checks if text is related to the given categories
    for i, row in df.iterrows():
        if reduce(combiner, category, False):
            try:
                ls = eval(row["countries"])
                G.add_nodes_from(ls)
                G.add_edges_from(combinations(ls, 2))
            except TypeError:  # "countries" is empty
                continue
    elements = []
    if "Singapore" not in G.nodes:
        return elements
    component = nx.subgraph(G, nx.node_connected_component(G, "Singapore"))
    for node in component.nodes:
        elements.append({
            "data": {
                "id": node,
                "label": node
            }
        })
    for edge in component.edges:
        elements.append({
            "data": {
                "source": edge[0],
                "target": edge[1]
            }
        })
    return elements