import json
import pandas as pd
import dash
from dash import html, dcc, Input, Output
import dash_cytoscape as cyto

# Import visualization functions
from visualization_utils.Piechart import piechart_builder
from visualization_utils.Linechart import line_builder
from visualization_utils.Graph import graph_builder
from visualization_utils.Barchart import barchart_builder
from visualization_utils.WorldHeatMap import heatmap_builder

# Load datasets
LEAKS_DF = pd.read_csv("./Dataset/processed_leaks_2.csv")
NEWS_DF = pd.read_csv("./Dataset/processed_news_2.csv")

# Add source columns
LEAKS_DF["source"] = "leaks"
NEWS_DF["source"] = "news"

# Combine datasets
WORKING_DF = pd.concat([LEAKS_DF, NEWS_DF], ignore_index=True)

# Load color configuratiore
with open("./visualization_utils/config/colour_config.json", "r") as file:
    color_config = json.load(file)
BG = color_config["background"]
PAPER = color_config["paper"]
FONTCOLOR = color_config["font"]
EDGE = color_config["graph"]["edge"]
NODE = color_config["graph"]["node"]
TITLE = color_config["title"]

# Initialize Dash app
app = dash.Dash(__name__)


def apply_common_aesthetics(fig, title_color=TITLE):
    """Apply consistent styling across all figures."""
    fig.update_layout(
        plot_bgcolor=BG,
        paper_bgcolor=PAPER,
        font=dict(size=16, color=FONTCOLOR),
        title=dict(font=dict(size=20, color=title_color))
    )
    return fig


# Define layout
app.layout = html.Div(
    style={"backgroundColor": BG, "padding": "20px"},

    children=[
        html.H1(
            "ISD Monitoring Dashboard",
            style={"textAlign": "center", "color": TITLE, "fontfamily": "Arial", "fontsize": "36px"}
        ),

        ##############
        # Heatmap #
        ##############
        html.H2("Geospatial Threat Heatmap", style={"textAlign": "center", "color": TITLE}),
        dcc.Checklist(
            id="heatmap-checkbox",
            options=[{"label": "News", "value": "news"}, {"label": "Leaks", "value": "leaks"}],
            value=["news", "leaks"],
            inline=True,
            style={"textAlign": "center", "marginBottom": "10px", "color": FONTCOLOR}
        ),
        dcc.Graph(id="heatmap-graph"),
        html.P(
            "This heatmap provides a geographical visualization of threats. Lighter regions indicate higher "
            "frequency of incidents. This graph helps identify hotspots of threat activity globally.",
            style={"textAlign": "center", "color": FONTCOLOR, "padding": "10px"}
        ),

        ###################
        # Pie & Bar Chart #
        ###################
        html.H2("Pie & Bar Chart", style={"textAlign": "center", "color": TITLE}),
        dcc.Checklist(
            id="piebar-checkbox",
            options=[{"label": "News", "value": "news"}, {"label": "Leaks", "value": "leaks"}],
            value=["news", "leaks"],
            inline=True,
            style={"textAlign": "center", "marginBottom": "10px", "color": FONTCOLOR}
        ),
        html.Div([
            dcc.Graph(id="piechart", style={"width": "45%", "display": "inline-block"}),
            dcc.Graph(id="barchart", style={"width": "45%", "display": "inline-block"})
        ], style={"display": "flex", "justifyContent": "center", "gap": "20px"}),
        html.P(
            "The pie chart displays the proportional distribution of different threat categories. The bar chart "
            "provides the exact count for each category, making it easier to compare specific values.",
            style={"textAlign": "center", "color": FONTCOLOR, "padding": "10px"}
        ),

        ###############
        # Line Charts #
        ###############
        html.H2("Trend Analysis Over Time", style={"textAlign": "center", "color": TITLE}),
        dcc.Checklist(
            id="line-checkbox",
            options=[{"label": "News", "value": "news"}, {"label": "Leaks", "value": "leaks"}],
            value=["news", "leaks"],
            inline=True,
            style={"textAlign": "center", "marginBottom": "10px", "color": FONTCOLOR}
        ),
        html.Div(
            children=[
                dcc.Graph(id="linechart_t", style={"width": "100%"}),
                dcc.Graph(id="linechart_s", style={"width": "100%"}),
                dcc.Graph(id="linechart_e", style={"width": "100%"}),
                dcc.Graph(id="linechart_c", style={"width": "100%"})
            ],
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"}
        ),
        html.P(
            "These line charts depict trends in the occurrence of different threats over time. By analyzing these graphs, "
            "you can spot spikes, seasonal variations, or long-term patterns in threat activity.",
            style={"textAlign": "center", "color": FONTCOLOR, "padding": "10px"}
        ),

        #################
        # Network Graph #
        #################
        html.H2("Network Graph of Threat Incidents", style={"textAlign": "center", "color": TITLE}),
        dcc.Checklist(
            id="graph-checkbox",
            options=[
                {"label": "Terrorism", "value": "terrorism"},
                {"label": "Cybersecurity", "value": "cyber_security"},
                {"label": "Espionage", "value": "espionage"},
                {"label": "Communalism", "value": "communalism"}
            ],
            value=["cyber_security"],  # Default selection
            inline=True,
            style={"textAlign": "center", "marginBottom": "10px", "color": FONTCOLOR}
        ),
        cyto.Cytoscape(
            id="network-graph",
            elements=[],
            style={"width": "100%", "height": "700px"},
            layout={"name": "breadthfirst", "roots": ["Singapore"]},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "content": "data(label)",
                        "background-color": "#666666",  # Dark gray nodes
                        "color": "#FFFF00",  # Bright yellow text for contrast
                        "font-size": "18px",  # Larger text
                        "text-valign": "top",  # Move text above node
                        "text-halign": "center",
                        "text-margin-y": "-12px",  # Offset text upwards
                        "width": "20px",  # Bigger nodes
                        "height": "20px",
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "line-color": "#BBBBBB",  # Light gray edges
                        "target-arrow-color": "#BBBBBB",
                        "target-arrow-shape": "none",
                        "curve-style": "bezier"
                    }
                }
            ]
        ),
        html.P(
            "This network graph shows the connections between countries based on shared threat incidents. Clusters "
            "indicate regional connections or geopolitical ties, while isolated nodes represent independent threats.",
            style={"textAlign": "center", "color": FONTCOLOR, "padding": "10px"}
        )
    ]
)



###########################
# CALLBACKS FOR UPDATING #
###########################

# Heatmap Callback
@app.callback(
    Output("heatmap-graph", "figure"),
    Input("heatmap-checkbox", "value")
)
def update_heatmap(source_list):
    return apply_common_aesthetics(heatmap_builder(WORKING_DF, source_list))


# Pie & Bar Chart Callback
@app.callback(
    [Output("piechart", "figure"), Output("barchart", "figure")],
    Input("piebar-checkbox", "value")
)
def update_piebar_chart(source_list):
    piechart = apply_common_aesthetics(piechart_builder(WORKING_DF, source_list))
    barchart = apply_common_aesthetics(barchart_builder(WORKING_DF, source_list))
    return piechart, barchart


# Line Chart Callback
@app.callback(
    [Output("linechart_t", "figure"),
     Output("linechart_s", "figure"),
     Output("linechart_e", "figure"),
     Output("linechart_c", "figure")],
    Input("line-checkbox", "value")
)
def update_linechart(source_list):
    fig_t, fig_s, fig_e, fig_c = line_builder(WORKING_DF, source_list)
    return (apply_common_aesthetics(fig_t),
            apply_common_aesthetics(fig_s),
            apply_common_aesthetics(fig_e),
            apply_common_aesthetics(fig_c))


# Network Graph Callback
@app.callback(
    Output("network-graph", "elements"),
    Input("graph-checkbox", "value")
)
def update_network_graph(selected_categories):
    return graph_builder(WORKING_DF, selected_categories)


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
