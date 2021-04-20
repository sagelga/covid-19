import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, MATCH, ALL
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

# Select data
df = df[['Buyer/recipient', 'Vaccine candidate', 'Deal Type', 'Finalized Commitment', 'Doses committed (in millions)',
         'Price (in USD million)', 'Doses/capita', 'Population covered']]
df = df.dropna()

# Sort data using Buyer + Vaccine candidate
df = df.sort_values(by=['Buyer/recipient', 'Vaccine candidate'])

all_buyer = df['Buyer/recipient'].unique()
all_candidates = df['Vaccine candidate'].unique()

# Vaccine Provider Card Import
url = 'https://raw.githubusercontent.com/sagelga/covid-vaccine/main/data/knowledgeportalia-vaccineProvider.csv'
vp_df = pd.read_csv(url)


# Secondary Trade Data Import
# url = 'https://raw.githubusercontent.com/sagelga/covid-vaccine/main/data/knowledgeportalia-secondary.csv'
# l2_df = pd.read_csv(url)


def generate_dropdown_option(label, id, options, value, placeholder='Select ...'):
    layout = html.Div([
        html.Label(label),
        dcc.Dropdown(
            id=id
            , options=options
            , value=value
            , placeholder=placeholder
            , multi=True, clearable=True, searchable=False
            , persistence=True, persistence_type='session'
        )
    ])

    return layout


def generate_candidateinfo_card():
    vaccine_candidate = vp_df['Vaccine candidate'].tolist()
    location = vp_df['Developer Location'].tolist()
    phase = vp_df['Trial Phase'].tolist()
    doses = vp_df['Doses'].tolist()

    layout = []
    for x in range(len(vaccine_candidate)):
        graphid = "candidate-graph-candidateinfo-{}".format(x)

        layout.append(html.Div([dcc.Graph(id=graphid)], className="six columns"))
        layout.append(html.Div([
            html.H5(vaccine_candidate[x])
            , html.Li("Developer Location : {}".format(location[x]))
            , html.Li("Development Phase : {}".format(phase[x]))
            , html.Li("Dose(s) required : {}".format(doses[x]))
        ], className="six columns"))


    layout2 = []
    loop_count = len(layout) // 2
    for x in range(loop_count):
        pointer = x * 2
        layout2.append(html.Div(children=[layout[pointer], layout[pointer + 1]], className='six columns'))


    layout3 = []
    loop_count = len(layout2) // 2
    for x in range(loop_count):
        pointer = x * 2
        layout3.append(html.Div(children=[layout2[pointer], layout2[pointer + 1]], className='row'))

    if len(layout2) % 2:
        layout3.append(html.Div(children=[layout2[-1]], className='row'))


    return html.Div(layout3)


# Website Builder
layout = html.Div([
    html.H2('Vaccine Deal'),
    html.Div([
        generate_dropdown_option(label='📊 Vaccine Buyer', id='candidate-dropdown-chartoption-buyer',
                                 options=[{'label': x, 'value': x} for x in all_buyer],
                                 value=all_buyer,
                                 placeholder='Filter by Buyer'),
        html.Button('Reset', id='candidate-button-chartoption-buyer', n_clicks=0),
    ]),
    html.Div([
        generate_dropdown_option(label='📊 Vaccine Candidates', id='candidate-dropdown-chartoption-candidate',
                                 options=[{'label': x, 'value': x} for x in all_candidates],
                                 value=all_candidates,
                                 placeholder='Filter by Vaccine Candidate'),
        html.Button('Reset', id='candidate-button-chartoption-candidate', n_clicks=0),
    ]),
    html.Div(children=[
        dcc.Graph(id="company-result-chart")
    ], className="twelve columns"),

    html.H2('Insights'),

    html.Div(children=[
        dcc.Graph(id="company-insight-dashboard")
    ], className="twelve columns"),

    html.H2('About each Vaccine'),
    html.P(
        'DISCLAIMER : This information listed here might be outdated. Please trust a latest information from reliable source.'),
    html.Br(),

    html.Div(children=[
        html.Div(children=[
            html.H4('Showing x of x available candidates')
        ], className='eight columns'),

        html.Div(children=[
            generate_dropdown_option(label='Filter by'
                                     , id='candidate-dropdown-candidateinfo-filter'
                                     , options=[]
                                     , value=[]
                                     , placeholder='Filter by ...')
        ], className='two columns'),
        html.Div(children=[
            generate_dropdown_option(label='Order by'
                                     , id='candidate-dropdown-candidateinfo-order'
                                     , options=[]
                                     , value=[]
                                     , placeholder='Order by ...')
        ], className='two columns'),
    ], className='row'),

    html.Br(),

    html.Div(children=[
        generate_candidateinfo_card()
    ]),

])


@app.callback(
    Output("company-result-chart", "figure"),
    [Input("candidate-dropdown-chartoption-buyer", "value")
        , Input("candidate-dropdown-chartoption-candidate", "value")]
)
def company_result_chart(buyer, candidates):
    mask = df['Buyer/recipient'].isin(buyer) & df['Vaccine candidate'].isin(candidates)
    fig = px.bar(df[mask], x="Buyer/recipient", y="Doses committed (in millions)", color="Vaccine candidate")

    return fig

# @app.callback(
#     Output("candidate-heading-candidateinfo-cards", "children")
#     [
#         Input('candidate-dropdown-candidateinfo-filter', 'value')
#         , Input("candidate-dropdown-candidateinfo-order", "value")
#     ]
# )
# def candidate_candidateinfo_(filter, order):
#     if type(filter) == list:
#         pass

# # Generate cards
# graphid = 'candidate-indicator-candidateinfo-indicator'
# name = "Arcturus / Duke NUS"
# info_box = "Country of Origin : Singapore/United States"
# info = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."
#
# return generate_candidateinfo_card(graphid, name, info_box, info)
# return 'Hello'
#
#
