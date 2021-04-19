import pandas as pd
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

# Website Builder
layout = html.Div([
    html.H2('Vaccine Deal'),

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
    # [
    #     Input("dropdown-insight-timeaverage", "value")
    # ]
)
def company_result_chart():
    fig = px.bar()

    return fig
