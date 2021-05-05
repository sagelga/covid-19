import pandas as pd
import numpy as np

# Data Import
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
df = pd.read_csv(url)

# Data selection
df = df[['iso_code', 'continent', 'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
         'total_cases_per_million', 'new_cases_per_million', 'total_deaths_per_million', 'new_deaths_per_million',
         'icu_patients', 'icu_patients_per_million', 'hosp_patients', 'hosp_patients_per_million', 'new_tests',
         'total_tests', 'total_tests_per_thousand', 'new_tests_per_thousand', 'positive_rate', 'tests_per_case',
         'tests_units', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations',
         'stringency_index', 'population']]

# NA Data Drop
df = df.dropna(subset=[
    'date'
    , 'continent'
    , 'location'
])

# Data Transform
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by=['date', 'location'])

# Calculate fields
df['people_vaccinated_per_population'] = 100 * (df['people_vaccinated'] / df['population'])
df['people_fully_vaccinated_per_population'] = 100 * (df['people_fully_vaccinated'] / df['population'])
df['case_per_population'] = 100 * (df['total_cases'] / df['population'])
df['lethal_rate'] = 100 * (df['total_deaths'] / df['total_cases'])
