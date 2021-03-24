import pandas as pd
import requests


def df_import():

    # Import data from GH
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    r = requests.get(url, allow_redirects=True)
    open('owid-covid-data.csv', 'wb').write(r.content)

    return pd.read_csv(url)
