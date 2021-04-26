import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server

# Connect to your app pages
from apps import home
from apps import candidate

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
        html.P(['Source : '
                   , html.A("Our World in Data", href="https://ourworldindata.org/")
                   , ", "
                   ,
                html.A("Graduate Institute", href="https://www.knowledgeportalia.org/covid19-vaccine-arrangements")]),
        html.P(['Created with ❤️ by ', html.A("@sagelga", href="https://github.com/sagelga/covid-vaccine")]),
    ], className="footer", style={'background-color': '#e5ecf6', 'text-align': 'center'}),

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')]
              )
def display_page(pathname):
    if pathname == '/candidate':
        return candidate.layout

    # If URL does not match any page, returns to home layout
    return home.layout


if __name__ == '__main__':
    app.run_server(debug=True)
