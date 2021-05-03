import pandas as pd
import numpy as np

# Data Import
url = 'https://raw.githubusercontent.com/sagelga/covid-vaccine/main/data/knowledgeportalia-primary.csv'
l1_df = pd.read_csv(url, encoding='latin-1')

# Select data
l1_df = l1_df[
    ['Buyer/recipient', 'Vaccine candidate', 'Deal Type', 'Finalized Commitment', 'Doses committed (in millions)',
     'Price (in USD million)', 'Price/Dose (in USD)']]
l1_df = l1_df.loc[l1_df['Finalized Commitment'] == 'Yes']

# Rename columns
l1_df = l1_df.rename(columns={'Buyer/recipient': 'Country',
                              'Doses committed (in millions)': 'Doses',
                              'Vaccine candidate': 'Vaccine Candidate',
                              'Price (in USD million)': 'Price',
                              'Price/Dose (in USD)': 'Price/Dose'})

# Drop/Fix error data
l1_df= l1_df.dropna(subset=['Doses'])
# l1_df = l1_df.replace('Not available', np.nan)
l1_df['Doses'] = pd.to_numeric(l1_df['Doses'] * 1000000, errors='coerce')
l1_df['Price'] = pd.to_numeric(l1_df['Price'], errors='coerce')
l1_df['Price/Dose'] = pd.to_numeric(l1_df['Price/Dose'], errors='coerce')


# Sort data using Buyer + Vaccine candidate
l1_df = l1_df.sort_values(by=['Country', 'Vaccine Candidate'])

# ------------------------------------------------------------------------

# Secondary Trade Data Import
url = 'https://raw.githubusercontent.com/sagelga/covid-vaccine/main/data/knowledgeportalia-secondary.csv'
l2_df = pd.read_csv(url, encoding='latin-1')

# Select data
l2_df = l2_df.loc[l2_df['Finalized Commitment'] == 'Yes']
l2_df = l2_df[['Recipient Country ', 'Vaccine Candidate', 'Doses Committed (in millions)', 'Finalized Commitment']]

# Rename columns
l2_df = l2_df.rename(columns={'Recipient Country ': 'Country', 'Doses Committed (in millions)': 'Doses'})
l2_df['Doses'] = pd.to_numeric(l2_df['Doses'], errors='coerce').fillna(0)
l2_df['Doses'] = pd.to_numeric(l2_df['Doses'] * 1000000)
l2_df['Vaccine Candidate'] = l2_df['Vaccine Candidate'].replace('Not available', 'Unknown')
l2_df['Vaccine Candidate'] = l2_df['Vaccine Candidate'].replace(np.nan, 'Unknown')
l2_df['Deal Type'] = 'Donation'

df = pd.concat([l1_df, l2_df])
# df['Country'] = df['Country'].sort_values()
df.dropna(subset=['Country', 'Doses'])
