import pandas as pd
import numpy as np
import requests
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.io as pio

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "COVID-19 Data Visualize"

"""
Create Vaccinated-Total Population Line Chart
"""


@app.callback(
    Output("vaccinate-timeline", "figure"),
    [Input("dropdown", "value")]
)
def vaccinate_timeline(countries):
    mask = df.location.isin(countries)
    country_count = df.location.nunique()
    country_selected = df[mask].location.nunique()

    fig = px.line(df[mask], x="date", y="ppl_vaccinated", title='Total Cases',
                  color="continent", hover_name="location")
    title = "Vaccinated population in {} of {} countries".format(
        country_selected, country_count)
    fig.update_layout(title=title,
                      xaxis_title='Date', yaxis_title='Percent Vaccinated')
    fig.update_traces(connectgaps=True, selector=dict(type='scatter'))
    return fig


"""
Create Active Case Line Chart
"""


@app.callback(
    Output("active-case", "figure"),
    [Input("dropdown", "value")]
)
def active_case(countries):
    mask = df.location.isin(countries)
    country_count = df.location.nunique()
    country_selected = df[mask].location.nunique()

    fig = px.line(df[mask], x="date", y="total_cases",
                  color="continent", hover_name="location")

    title = "Total Case in {} of {} countries".format(
        country_selected, country_count)
    fig.update_layout(title=title,
                      xaxis_title='Date', yaxis_title='Total Case')
    fig.update_traces(connectgaps=True, selector=dict(type='scatter'))
    return fig


"""
Function df_import() will imports the data from datasource
and returns DataFrame that contains Pandas data.
"""


def df_import():

    # Import data from GH
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    r = requests.get(url, allow_redirects=True)
    open('owid-covid-data.csv', 'wb').write(r.content)

    return pd.read_csv(url)


# Data selection
df = df_import()
df = df.dropna(subset=['continent'])
df = df.dropna(subset=['location'])
df = df.dropna(subset=['date'])

# Calculate fields
df['ppl_vaccinated'] = (df['people_vaccinated'] / df['population'])*100

# Selection bar
all_country = df.location.unique()
app.layout = html.Div([
    html.Div([
        html.H1('covid-vaccines'),
        html.P('Datasource from https://github.com/owid/covid-19-data/'),
    ]),
    html.Div([
        dcc.Graph(id="active-case"),
        dcc.Graph(id="vaccinate-timeline"),
    ]),
    html.Div([
        html.H5('Change visible countries'),

        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x}
                     for x in all_country],
            value=all_country,
            multi=True
        ),
    ]),
],)

# app.run_server(debug=True, host='0.0.0.0')
app.run_server(debug=True, use_reloader=False)
