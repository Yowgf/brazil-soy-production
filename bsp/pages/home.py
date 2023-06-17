import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.Div(
        html.Img(
            src="assets/soybeans-harvesting-autumn.jpeg",
            className="img"
        )
    ),
])
