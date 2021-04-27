import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server

# Connect to your app pages
from apps import home
from apps import candidate
from apps import mobility

# Website Builder
app.layout = html.Div([
    html.Div([
        html.Div([], className="one columns"),
        html.Div([
            html.H1('COVID-19 Data Explorer'),

            html.Nav([
                dcc.Location(id='url', refresh=False),
                html.Div([
                    dcc.Link('Home', href='/'),
                    dcc.Link(' ● ', href=''),
                    dcc.Link('Mobility Report', href='/mobility'),
                    dcc.Link(' ● ', href=''),
                    dcc.Link('Vaccine Candidate', href='/candidate'),
                ], className="row"),
            ]),

            html.Br(),

            html.Div([
                html.Div(id='page-content', children=[])
            ]),

        ], className="ten columns"),

        html.Div([], className="one columns"),

    ], className="row"),

    # Footer Area
    html.Br(),
    html.Div(children=[
        html.Center('Source : Our World in Data'),
        html.Center('Created with ❤️ by @sagelga'),
    ], className="footer"),

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')]
              )
def display_page(pathname):
    if pathname == '/candidate':
        return candidate.layout
    if pathname == '/mobility':
        return mobility.layout

    # If URL does not match any page, returns to home layout
    return home.layout


if __name__ == '__main__':
    app.run_server(debug=True)
