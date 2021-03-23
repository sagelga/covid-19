import pandas as pd
import requests

# Import data from GH
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
r = requests.get(url, allow_redirects=True)
open('src/owid-covid-data.csv', 'wb').write(r.content)

# Read data to Dataframe
df = pd.read_csv('src/owid-covid-data.csv')
