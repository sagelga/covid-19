import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
from plotly import express as px


from app import app

from component import knowledgepotalia

candidate_df = knowledgepotalia.df
candidateinfo_df = knowledgepotalia.info_df

all_country = sorted(candidate_df['Country'].unique().tolist())

price_options = [
    {'label': 'Vaccine Name', 'value': 'name'}
    , {'label': 'Vaccine Price', 'value': 'price'}
]


def generate_dropdown_option(label, id, options, value, placeholder, multi, searchable):
    layout = html.Div([
        html.Label(label),
        dcc.Dropdown(
            id=id
            , options=options
            , value=value
            , placeholder=placeholder
            , multi=multi, clearable=multi
            , searchable=searchable
            , persistence=True, persistence_type='session'
        )
    ])

    return layout


# Website Builder
layout = html.Div([
    html.H1('Vaccine Candidate'),
    html.P('Last data update: 30 April 2021'),
    html.Div([
        html.Div([
            html.Div([
                html.H2('Vaccine on Hand'),
            ], className='ten columns'),
            html.Div([
                html.Button(children='Switch to Vaccine Candidate', id='candidate-button-chartoption-buyer',
                            n_clicks=0),
            ], className='two columns'),
        ], className='row'),

        html.Div([
            generate_dropdown_option(label='📊 Vaccine Buyer', id='candidate-dropdown-chartoption-buyer',
                                     options=[{'label': x, 'value': x} for x in all_country],
                                     value=[x for x in all_country],
                                     placeholder='Filter by Buyer'
                                     , multi=True, searchable=True),
            # html.Button('Reset', id='candidate-button-chartoption-buyer', n_clicks=0),
        ]),

        html.Div(children=[
            dcc.Graph(id="candidate-graph-vaccinecount")
        ], className="twelve columns"),
    ]),  # Vaccine on Hand

    html.Div([
        html.H2('Vaccine Price'),
        html.P('DISCLAIMER : Price-disclosed or Donation deals/arrangements are excluded.'),
        html.Div([
            html.Div([
                generate_dropdown_option(label='Order by'
                                         , id='candidate-dropdown-priceoption-category'
                                         , options=price_options
                                         , value='name'
                                         , placeholder='Order by ...'
                                         , multi=False
                                         , searchable=True),

            ], className='two columns'),
            html.Div([
                generate_dropdown_option(label='Order'
                                         , id='candidate-dropdown-priceoption-order'
                                         , options=[{'label': 'Ascending', 'value': 'asc'},
                                                    {'label': 'Descending', 'value': 'desc'}]
                                         , value='asc'
                                         , placeholder='Order by ...'
                                         , multi=False
                                         , searchable=True),
            ], className='two columns'),
        ], className='row'),

        html.Div(children=[
            dcc.Graph(id="candidate-graph-price")
        ], className="twelve columns"),

    ]),  # Vaccine Price

    html.Div([
        #     html.H2('Insights'),
        #
        #     html.Div(children=[
        #         dcc.Graph(id="company-insight-dashboard")
        #     ], className="twelve columns"),
        #
    ]),  # Insights

    html.Div([
        html.H2('About each Vaccine'),
        html.P(
            'DISCLAIMER : This information listed here might be outdated. Please trust a latest information from reliable source.'),
        html.Br(),

        html.Div(children=[
            html.Div(children=[
                html.H4(id='candidate-heading-candidateinfo-candidatecount')
            ], className='six columns'),

            html.Div(children=[
                generate_dropdown_option(label='Filter by'
                                         , id='candidate-dropdown-candidateinfo-filter'
                                         , options=[{'label': x, 'value': x} for x in candidateinfo_df.head()]
                                         , value=[]
                                         , placeholder='Filter by ...'
                                         , multi=False
                                         , searchable=True),
                generate_dropdown_option(label='Filter using'
                                         , id='candidate-dropdown-candidateinfo-filtervalue'
                                         , options=[]
                                         , value=[]
                                         , placeholder='Filter using ...'
                                         , multi=True
                                         , searchable=True)
            ], className='three columns'),
            html.Div(children=[
                generate_dropdown_option(label='Order by'
                                         , id='candidate-dropdown-candidateinfo-ordercategory'
                                         , options=[{'label': x, 'value': x} for x in candidateinfo_df.head()]
                                         , value='Vaccine Candidate'
                                         , placeholder='Order by ...'
                                         , multi=False
                                         , searchable=False)
            ], className='three columns'),
        ], className='row'),

        html.Br(),
        html.Div(id='candidate-components-candidateinfo'),
    ]),  # Vaccine Info Card
])


@app.callback(
    Output("candidate-graph-vaccinecount", "figure"),
    Input("candidate-dropdown-chartoption-buyer", "value")
)
def candidate_graph_vaccinecount(buyer):
    if not buyer:
        raise PreventUpdate
    mask = candidate_df['Country'].isin(buyer)

    fig = px.bar(candidate_df[mask],
                 x="Doses", y="Vaccine Candidate",
                 color="Vaccine Candidate", orientation='h',
                 hover_data=['Country'])
    fig.update_layout(showlegend=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


@app.callback(
    Output("candidate-graph-price", "figure"),
    [
        Input("candidate-dropdown-priceoption-category", "value")
        , Input("candidate-dropdown-priceoption-order", "value")
    ]
)
def candidate_graph_vaccineprice(order_category, order):
    fig = px.box(candidate_df, x='Vaccine Candidate', y='Price/Dose')
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


@app.callback(
    Output("candidate-dropdown-candidateinfo-filtervalue", 'options'),
    [Input("candidate-dropdown-candidateinfo-filter", 'value')]
)
def candidate_dropdown_filteroption_update(search_value):
    if not search_value:
        raise PreventUpdate

    return [{'label': x, 'value': x} for x in candidateinfo_df[search_value].sort_values().unique()]


@app.callback(
    Output("candidate-heading-candidateinfo-candidatecount", "children"),
    Output("candidate-components-candidateinfo", "children"),
    [
        Input('candidate-dropdown-candidateinfo-filter', 'value')
        , Input('candidate-dropdown-candidateinfo-filtervalue', 'value')
        , Input("candidate-dropdown-candidateinfo-ordercategory", "value")
    ]
)
def candidate_component_candidateinfo_card(filter, filter_value, order_category):
    def get_candidateinfo_cardinfo(candidate):
        ddf = candidate_df.loc[candidate_df['Vaccine Candidate'] == candidate]
        fig = px.pie(ddf, values='Doses', names='Income level')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    ddf = candidateinfo_df

    # Filter data from candidateinfo_df
    if bool(filter) & bool(filter_value):
        mask = ddf[filter].isin(filter_value)
        ddf = ddf[mask]

    # Sort data from info_df to match `order_category`
    ddf = ddf.sort_values(by=['Vaccine Candidate'])  # set baseline sorting as Vaccine Candidate
    ddf = ddf.sort_values(by=[order_category]) if len(order_category) else ddf

    # Fetch data from info_df
    candidate = ddf['Vaccine Candidate'].tolist()
    location = ddf['Developer Location'].tolist()
    phase = ddf['Trial Phase'].tolist()
    doses = ddf['Dose Needed'].tolist()

    # Create subsection header
    heading = html.H4('Showing {} candidates'.format(len(candidate)))

    layout = []

    # Creating elements
    for x in range(len(candidate)):
        layout.append(html.Div([
            html.Div([
                html.Div([
                    html.H4(candidate[x])
                ], className='row'),
                html.Div([
                    html.Div([
                        html.Li("Developer Location : {}".format(location[x]))
                        , html.Li("Development Phase : {}".format(phase[x]))
                        , html.Li("Dose(s) required : {}".format(doses[x]))
                    ], className="six columns"),
                    html.Div([
                        dcc.Graph(id='candidate-graph-candidateinfo-candidateincome-{}'.format(candidate[x])
                                  , figure=get_candidateinfo_cardinfo(candidate[x]))
                    ], className='six columns')
                ], className='row')
            ], style={'borderRadius': '10px', 'border': '2px solid #3d4e76', 'padding': '20px'}),

            html.Br(),
        ])
        )

    return heading, layout
