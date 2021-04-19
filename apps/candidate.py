import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from plotly import express as px
from plotly import graph_objects as go
from datetime import datetime, timedelta
import time

from app import app

# Data Import
url = 'https://raw.githubusercontent.com/sagelga/covid-vaccine/main/data/knowledgeportalia-primary.csv'
df = pd.read_csv(url)

candidates = np.sort(df['Vaccine candidate'].unique())

# Website Builder
layout = html.Div([
    html.H2('Vaccine Deal'),
    html.Label('📊 Vaccine Candidates'),
    dcc.Dropdown(
        id="dropdown-chartoption"
        , options=[{"label": x, "value": x}
                   for x in candidates]
        , placeholder="Select an option (optional)"
        , multi=True
        , clearable=True
        , searchable=False
        , persistence=True
        , persistence_type='session'
        # , persistence=True
        # , persistence_type='session'
    ),
    html.Div(children=[
        dcc.Graph(id="company-result-chart")
    ], className="twelve columns"),

    html.H2('Insights'),

    html.Div(children=[
        dcc.Graph(id="company-insight-dashboard")
    ], className="twelve columns"),
])


@app.callback(
    Output("company-result-chart", "figure"),
    [
        Input("candidate-dropdown-candidate", "value")
    ]
)
def company_result_chart(candidates):
    fig = px.bar()

    return fig
