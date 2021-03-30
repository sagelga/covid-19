import pandas as pd
import numpy as np
import requests

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.io as pio

# Importing data
from df_import import df_import

# Data selection
df = df_import()
df = df.dropna(subset=['continent'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Selection bar
all_country = df.location.unique()
app.layout = html.Div([
    html.H1('covid-vaccines'),

    dcc.Graph(id="active-case"),
    dcc.Graph(id="vaccinate-timeline"),

    html.H5('Change visible countries'),

    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x}
                 for x in all_country],
        value=all_country,
        multi=True
    ),
], style={'font-family': 'Jetbrains Mono'})


# Create line chart
@app.callback(
    Output("vaccinate-timeline", "figure"),
    [Input("dropdown", "value")]
)
def vaccinate_timeline(countries):
    # df = df_import()

    # df = df.dropna(subset=['people_vaccinated'])
    mask = df.location.isin(countries)

    # Calculate fields
    df['ppl_vaccinated'] = df['people_vaccinated'] / df['population']

    fig = px.line(df[mask], x="date", y="ppl_vaccinated", title='Total Cases',
                  color="continent", hover_name="location")
    fig.update_layout(title='Vaccinated population by Country',
                      xaxis_title='Date', yaxis_title='Vaccinated (Percent)',
                      font_family='Jetbrains Mono', title_font_family='Jetbrains Mono')
    return fig


# Create line chart
@app.callback(
    Output("active-case", "figure"),
    [Input("dropdown", "value")]
)
def active_case(countries):
    mask = df.location.isin(countries)

    fig = px.line(df[mask], x="date", y="total_cases",
                  color="continent", line_group="location", hover_name="location")
    fig.update_layout(title='Total Case by Country',
                      xaxis_title='Date', yaxis_title='Total Case',
                      font_family='Jetbrains Mono', title_font_family='Jetbrains Mono')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
