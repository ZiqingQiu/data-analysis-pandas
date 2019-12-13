from apis.plot_diagram import plot_bar_value_counts, plot_histogram
from apis.utils import save_print, check_missing, check_unique
from config import col_when, convert_hour
import pandas as pd


def analysis_when(df):
    save_print("\nAnalysis when -- time")
    # check missing
    check_missing(df, col_when)
    # check unique
    check_unique(df, col_when)

    # [Occurrence_Year]
    annual_theft = df['Occurrence_Year'].value_counts()
    plot_bar_value_counts(annual_theft, 'Annual_Status')

    # [Occurrence_Month]
    month_theft = df['Occurrence_Month'].value_counts()
    plot_bar_value_counts(month_theft, 'Month_Status', 1.0)

    # [Occurrence_Day]
    day_theft = df['Occurrence_Day'].value_counts()
    plot_bar_value_counts(day_theft, 'Daily_Status', 2.0)

    # [Occurrence_Time]
    if convert_hour:
        df['Occurrence_Time'] = df['Occurrence_Time'].str.split(':').apply(lambda x: int(x[0]))
        # row_filter = df['Premise_Type'] != 'House'
        # index_names = df[row_filter].index
        # filter_df = df.drop(index_names, axis=0)
        # plot_histogram(filter_df, 'Occurrence_Time')
