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

# candidates = np.sort(df['Vaccine candidate'].unique())

# Website Builder
layout = html.Div([
    html.H2('Vaccine Deal'),
    html.Label('📊 Vaccine Candidates'),
    dcc.Dropdown(
        id="dropdown-chartoption"
        , options=[]
        # , options=[{"label": x, "value": x}
        #            for x in candidates]
        , placeholder="Select an option (optional)"
        , multi=True
        , clearable=True
        , searchable=False
        , persistence=True
        , persistence_type='session'
    ),
    html.Div(children=[
        dcc.Graph(id="company-result-chart")
    ], className="twelve columns"),

    html.H2('Insights'),

    html.Div(children=[
        dcc.Graph(id="company-insight-dashboard")
    ], className="twelve columns"),

    html.H2('About each Vaccine'),
    html.P('DISCLOSURE : This information listed might be outdated. Please trust a latest information from reliable source.'),
    html.Br(),

    html.Div(children=[
        html.Div(children=[
            html.H4('Selected x of x available candidates'),
        ], className='eight columns'),

        html.Div(children=[
            dcc.Dropdown(
                id="candidate-dropdown-vaccineinfo-order"
                , options=[]
                # , options=[{"label": x, "value": x}
                #            for x in candidates]
                , placeholder="Filter by ..."
                , multi=True
                , clearable=True
                , searchable=False
                , persistence=True
                , persistence_type='session'
            ),
        ], className='two columns'),
        html.Div(children=[
            dcc.Dropdown(
                id="candidate-dropdown-vaccineinfo-filter"
                , options=[]
                # , options=[{"label": x, "value": x}
                #            for x in candidates]
                , placeholder="Order by ..."
                , multi=True
                , clearable=True
                , searchable=False
                , persistence=True
                , persistence_type='session'
            ),
        ], className='two columns'),
    ], className='row'),

    html.Br(),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Arcturus / Duke NUS"),
                    html.P("Country of Origin : Singapore/United States"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns"),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("AstraZeneca / Oxford"),
                    html.P("Country of Origin : United Kingdom / Sweden"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns")
    ], className='row'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Bharat Biotech"),
                    html.P("Country of Origin : Singapore/United States"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns"),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("CanSino Biologics"),
                    html.P("Country of Origin : United Kingdom / Sweden"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns")
    ], className='row'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Curevac"),
                    html.P("Country of Origin : Singapore/United States"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns"),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Gamaleya"),
                    html.P("Country of Origin : United States / Belgium"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns")
    ], className='row'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Johnson & Johnson"),
                    html.P("Country of Origin : Canada / United Kingdom"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns"),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Moderna"),
                    html.P("Country of Origin : United States"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns")
    ], className='row'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Novavax"),
                    html.P("Country of Origin : United States"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns"),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Pfizer / BioNTech"),
                    html.P("Country of Origin : United States / Germany"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns")
    ], className='row'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Providence Therapeutics"),
                    html.P("Country of Origin : Canada"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns"),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Sanofi / GSK"),
                    html.P("Country of Origin : France/United Kingdom"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns")
    ], className='row'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Sinopharm / Beijing"),
                    html.P("Country of Origin : China"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns"),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Sinovac"),
                    html.P("Country of Origin : China"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns")
    ], className='row'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("University of Queensland / CSL"),
                    html.P("Country of Origin : Australia"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns"),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id="company-insight-dashboard")
                ], className="six columns"),
                html.Div(children=[
                    html.H5("Valneva"),
                    html.P("Country of Origin : France"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas volutpat mauris quam, quis elementum elit facilisis sit amet. Nullam eleifend aliquam nulla, ut tempus nisi suscipit non. Suspendisse diam mi, vulputate eget mattis id, posuere vel ipsum. Ut tempor tortor sit amet purus dictum, aliquet rutrum metus feugiat. Proin pharetra imperdiet ante, eget pharetra ligula tempus sit amet. Duis sollicitudin mi in enim accumsan, sed vehicula nisi placerat. Vestibulum cursus tortor sit amet eros ultrices, et lobortis diam venenatis. Fusce pharetra, massa vitae ullamcorper feugiat, arcu eros maximus elit, efficitur faucibus eros erat id lacus. Curabitur bibendum semper nisi id interdum. Donec condimentum ultricies sapien sed finibus. Duis iaculis mi id magna vehicula aliquet. In ac tellus orci. Quisque aliquam ornare bibendum."),
                ], className="six columns"),
            ], className="row"),
        ], className="six columns")
    ], className='row'),
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
