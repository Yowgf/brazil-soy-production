import dash
from dash import Dash, dcc, html
from flask import Flask

# Main page
app = Dash(__name__,
           use_pages=True,
           # Necessary to allow callbacks to be registered after app
           # initialization.
           suppress_callback_exceptions=True)
app.layout = html.Div(
    [
        html.Header(
            [
                html.Span(
                    dcc.Link(
                        f"{page['name']}", href=page["relative_path"]
                    ),
                    className='header-elem',
                )
                for page in dash.page_registry.values()
            ],
            className='header',
        ),
        dash.page_container,
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
