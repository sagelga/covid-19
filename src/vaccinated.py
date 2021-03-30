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
df = df.dropna(subset=['people_vaccinated'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Selection bar
all_country = df.location.unique()
app.layout = html.Div([
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x}
                 for x in all_country],
        value=all_country,
        multi=True
    ),
    dcc.Graph(id="line-chart"),
], style={'font-family': 'Jetbrains Mono'})


@app.callback(
    Output("line-chart", "figure"),
    [Input("dropdown", "value")]
)
# Create line chart
def update_line_chart(countries):
    mask = df.location.isin(countries)

    # Calculate fields
    df['ppl_vaccinated'] = df['people_vaccinated'] / df['population']

    fig = px.line(df[mask], x="date", y="ppl_vaccinated", title='Total Cases',
                  color="continent", hover_name="location")
    fig.update_layout(title='Vaccinated population by Country',
                      xaxis_title='Date', yaxis_title='Vaccinated (Percent)',
                      font_family='Jetbrains Mono', title_font_family='Jetbrains Mono')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
