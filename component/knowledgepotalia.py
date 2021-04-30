import pandas as pd
import numpy as np

# Data Import
url = 'https://raw.githubusercontent.com/sagelga/covid-vaccine/main/data/knowledgeportalia-primary.csv'
l1_df = pd.read_csv(url)

# Select data
l1_df = l1_df[
    ['Buyer/recipient', 'Vaccine candidate', 'Deal Type', 'Finalized Commitment', 'Doses committed (in millions)',
     'Price (in USD million)', 'Price/Dose (in USD)', 'Doses/capita', 'Population covered']]
l1_df = l1_df.dropna()

# Sort data using Buyer + Vaccine candidate
l1_df = l1_df.sort_values(by=['Buyer/recipient', 'Vaccine candidate'])

all_buyer = l1_df['Buyer/recipient'].unique()
# all_candidates = df['Vaccine candidate'].unique()
price_options = [
    {'label': 'Vaccine Name', 'value': 'name'}
    , {'label': 'Vaccine Price', 'value': 'price'}
]
l1_df = l1_df.rename(columns={'Buyer/recipient': 'Country', 'Doses committed (in millions)': 'Doses'})

# Secondary Trade Data Import
url = 'https://raw.githubusercontent.com/sagelga/covid-vaccine/main/data/knowledgeportalia-secondary.csv'
l2_df = pd.read_csv(url)
l2_df = l2_df.loc[l2_df['Finalized Commitment'] == 'Yes']
l2_df = l2_df[['Recipient Country', 'Vaccine Candidate', 'Doses Committed (in millions)']]
l2_df['Doses Committed (in millions)'] = pd.to_numeric(
    l2_df['Doses Committed (in millions)'], errors='coerce').fillna(0)
l2_df['Vaccine Candidate'] = l2_df['Vaccine Candidate'].replace(np.nan, 'Unknown')

l2_df['Deal Type'] = 'Donation'
l2_df = l2_df.rename(columns={'Recipient Country': 'Country', 'Doses Committed (in millions)': 'Doses'})

df = pd.concat([l1_df, l2_df])
df = df.groupby(['Country', 'Vaccine Candidate', 'Deal Type']).sum()
