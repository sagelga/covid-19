import pandas as pd
import numpy as np

# Data Import
url = 'https://raw.githubusercontent.com/sagelga/covid-vaccine/main/data/knowledgeportalia-primary.csv'
df = pd.read_csv(url, encoding='latin-1')

# Rename columns
df = df.rename(columns={
    'Buyer/recipient': 'Country',
    'Doses committed (in millions)': 'Doses',
    'Vaccine candidate': 'Vaccine Candidate',
    'Price (in USD million)': 'Price',
    ' Price/Dose (in USD) ': 'Price/Dose',
    ' Population ': 'Population'
}
)

# l1_df Select data
l1_df = df[
    ['Country', 'Vaccine Candidate', 'Deal Type', 'Finalized Commitment', 'Doses',
     'Price', 'Price/Dose', 'Income level', 'Population']]
l1_df = l1_df.loc[l1_df['Finalized Commitment'] == 'Yes']

# Drop/Fix error data
l1_df = l1_df.dropna(subset=['Country', 'Doses'])
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
l2_df = l2_df[[
    'Recipient Country ', 'Vaccine Candidate', 'Doses Committed (in millions)', 'Finalized Commitment',
    'Recipient Income Level', ' Population size '
]]

# Rename columns
l2_df = l2_df.rename(columns={
    'Recipient Country ': 'Country'
    , 'Doses Committed (in millions)': 'Doses'
    , 'Recipient Income Level': 'Income Level'
    , ' Population size ': 'Population'
})

# Fix data inconsistencies
l2_df = l2_df.loc[l2_df['Finalized Commitment'] == 'Yes']

l2_df = l2_df.dropna(subset=['Country', 'Doses'])

l2_df['Doses'] = pd.to_numeric(l2_df['Doses'] * 1000000, errors='coerce').fillna(0)
l2_df['Vaccine Candidate'] = l2_df['Vaccine Candidate'].replace('Not available', 'Unknown')
l2_df['Vaccine Candidate'] = l2_df['Vaccine Candidate'].replace(np.nan, 'Unknown')
l2_df['Deal Type'] = 'Donation'

# ------------------------------------------------------------------------

# Vaccine Candidate info
columns = ['Vaccine Candidate', 'Developer Location', 'Trial Phase', '1 or 2 doses']
info_df = df[columns] \
    .drop_duplicates(subset=columns) \
    .rename(columns={'1 or 2 doses': 'Dose Needed'}) \
    .dropna(subset=['Vaccine Candidate'])

# ------------------------------------------------------------------------

# Merge data from both acquisition mode
df = pd.concat([l1_df, l2_df])
