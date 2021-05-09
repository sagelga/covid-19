import pandas as pd


def get_aapl_df():
    url = 'https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/apple_reports/apple_mobility_report.csv'
    df = pd.read_csv(url)
    return df


def get_goog_df():
    url = 'https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/google_reports/mobility_report_countries.csv'
    df = pd.read_csv(url)
    return df


def get_waze_df():
    url = 'https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/waze_reports/waze_mobility.csv'
    df = pd.read_csv(url)
    return df


def get_tom_df():
    url = 'https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/tomtom_reports/tomtom_trafic_index.csv'
    df = pd.read_csv(url)
    return df
