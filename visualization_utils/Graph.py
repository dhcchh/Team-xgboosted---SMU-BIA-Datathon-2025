import networkx as nx

def graph_builder(df, category):
    """
    Builds a network graph based on relationships between countries for a specific category.

    Parameters:
        df (pd.DataFrame): The dataset containing relationships and categories.
        category (str): The specific category to filter on (e.g., 'terrorism', 'security').

    Returns:
        list: Elements for Dash Cytoscape (nodes and edges).
    """

    # Ensure the category exists in the dataframe
    if category not in df.columns:
        raise ValueError(f"Category '{category}' not found in the dataset.")

    # Filter rows where the selected category is True
    filtered_df = df[df[category] == True]

    # Ensure the 'countries' column exists
    if 'countries' not in filtered_df.columns:
        raise ValueError("The dataset must contain a 'countries' column.")

    # Process countries into a list of tuples (country pairs)
    filtered_df['countries'] = filtered_df['countries'].apply(
        lambda x: x.split(', ') if isinstance(x, str) else []
    )
    edges = [
        (pair[0], pair[1]) for countries in filtered_df['countries']
        for pair in zip(countries[:-1], countries[1:])
    ]

    # Build the graph using NetworkX
    G = nx.Graph()
    G.add_edges_from(edges)

    # Format the nodes and edges for Cytoscape
    elements = [
        {"data": {"id": node, "label": node}} for node in G.nodes()
    ] + [
        {"data": {"source": edge[0], "target": edge[1]}} for edge in G.edges()
    ]

    return elements
