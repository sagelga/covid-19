import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from app import server

# Connect to your app pages
from apps import home
from apps import world
from apps import candidate
from apps import mobility
from apps import fourOfour

# Website Builder
location = dcc.Location(id='url', refresh=False)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("World Trends", href="/world")),
        dbc.NavItem(dbc.NavLink("Mobility Reports", href="/mobility")),
        dbc.NavItem(dbc.NavLink("Vaccine Candidate", href="/candidate")),
    ],
    brand="COVID-19 Data Explorer",
    fluid=True,
    color="dark",
    dark=True,
)

# padding for the page content
CONTENT_STYLE = {
    # "margin-left": "2rem",
    # "margin-right": "2rem",
    "padding": "2rem 2rem",
}

content = html.Div([
    html.Div(children=[], className='one column'),
    html.Div(id='page-content', children=[], style=CONTENT_STYLE, className='ten columns'),
    html.Div(children=[], className='one column'),
], className='row')

footer = html.Div(
    [
        html.P(['Source : '
                   , html.A("Our World in Data", href="https://ourworldindata.org/")
                   , ", ",
                html.A("Graduate Institute", href="https://www.knowledgeportalia.org/covid19-vaccine-arrangements")]),

        html.P(['This Data Explorer is '
                   , html.A("Open Source", href="https://github.com/sagelga/covid-vaccine")
                   , '. Buy us a ☕ by '
                   , html.A('Donate via Crypto',
                            href='https://commerce.coinbase.com/checkout/aed305a0-d6ae-4d98-b993-b1e85e0a99f6')
                   , ' or '
                   , html.A('via PayPal',
                            href='https://paypal.me/son9912')
                ]),

        html.P(['Created with ❤️ by ', html.A("@sagelga", href="https://github.com/sagelga/covid-vaccine")]),
    ]
    , className="footer", style={'backgroundColor': '#e5ecf6', 'textAlign': 'center'}
)

app.layout = html.Div([
    navbar,
    content,
    footer,
    location])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')]
              )
def display_page(pathname):
    if pathname == '/':
        return home.layout
    if pathname == '/world':
        return world.layout
    if pathname == '/candidate':
        return candidate.layout
    if pathname == '/mobility':
        return mobility.layout

    # If URL does not match any page, returns to home layout
    return fourOfour.layout


if __name__ == '__main__':
    app.run_server(debug=True)
