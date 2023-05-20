import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

import lib

df = lib.process().get_table()

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(children="Brazil Soy Production", style={"textAlign": "center"}),
        dcc.Dropdown(df.region.unique(), "Brasil", id="dropdown-selection"),
        dcc.Graph(id="graph-content"),
    ]
)


@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    dff = df[df.region == value]
    return px.line(dff, x="year", y="production")


if __name__ == "__main__":
    app.run_server(debug=True)
