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
df = df.dropna(subset=['new_tests'])
df = df.dropna(subset=['new_cases'])

df['test_detected'] = df['new_cases'] / df['new_tests']

fig = px.scatter(df, x="date", y="new_cases", title='Total Cases',
                 color="continent", size="test_detected", hover_data=['location', 'new_tests', 'new_cases'])

fig.show()
# Selection bar
# all_country = df.location.unique()

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     dcc.Dropdown(
#         id="dropdown",
#         options=[{"label": x, "value": x}
#                  for x in all_country],
#         value=['Thailand'],
#         multi=True
#     ),
#     dcc.Graph(id="line-chart"),
# ])


# @app.callback(
#     Output("line-chart", "figure"),
#     [Input("dropdown", "value")]
# )
# # Create line chart
# def update_line_chart(countries):
#     mask = df.location.isin(countries)
#     fig = px.line(df[mask], x="date", y="total_cases",
#                   color="continent", line_group="location", hover_name="location")
#     fig.update_layout(title='Total Case by Country',
#                       xaxis_title='Date', yaxis_title='Total Case',
#                       font_family='Jetbrains Mono', title_font_family='Jetbrains Mono')
#     return fig


# app.run_server(debug=True)
