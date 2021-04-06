import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# App Initialize
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
    external_stylesheets=external_stylesheets
)
server = app.server

app.title = "COVID-19 Data Visualize"
app.config["suppress_callback_exceptions"] = True

# Data Import
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
df = pd.read_csv(url)

# Data Transform
df.date = pd.to_datetime(df.date)
df = df.sort_values(by=['date', 'location'])

# Data selection
df = df.dropna(subset=['continent'])
df = df.dropna(subset=['location'])

# Calculate fields
df['ppl_vaccinated'] = 100 * (df['people_vaccinated'] / df['population'])

# Selection bar
all_country = df.location.unique()
app.layout = html.Div([
    html.Div(children=[
        html.H1('covid-vaccines'),
        html.P('Datasource from https://github.com/owid/covid-19-data/'),
    ]),
    html.Div(children=[
        dcc.Graph(id="active-case"),
        dcc.Graph(id="vaccinate-timeline"),
    ]),
    html.Div(children=[
        html.H5('Change visible countries'),

        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x}
                     for x in all_country],
            value=all_country,
            multi=True
        ),
    ]),
])


@app.callback(
    Output("vaccinate-timeline", "figure"),
    Output("active-case", "figure"),
    [Input("dropdown", "value")]
)
def update_graph(countries):
    mask = df.location.isin(countries)
    country_count = df.location.nunique()
    country_selected = df[mask].location.nunique()

    # Create Vaccinated-Total Population Line Chart
    vcn_fig = px.line(
        df[mask],
        x="date",
        y="ppl_vaccinated",
        title='Total Cases',
        color="location",
        hover_name="location",
        hover_data=['date', 'continent', 'people_vaccinated', 'population', 'ppl_vaccinated']
    )
    title = "Vaccinated population in {} of {} countries".format(
        country_selected, country_count)
    vcn_fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Percent Vaccinated'
    )
    vcn_fig.update_traces(connectgaps=True)

    # Active Case Line Chart
    atv_fig = px.line(
        df[mask],
        x="date",
        y="total_cases",
        color="location",
        hover_name="location",
        hover_data=['date', 'continent', 'total_cases'],
        # category_orders={"location": df["location"].tolist().sort()}
    )

    title = "Total Case in {} of {} countries".format(
        country_selected, country_count)
    atv_fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Total Case'
    )
    atv_fig.update_traces(connectgaps=True)

    return vcn_fig, atv_fig


if __name__ == '__main__':
    app.run_server(debug=True)
