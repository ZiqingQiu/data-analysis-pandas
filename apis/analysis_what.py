# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:20:10 2019

@author: group1
"""
# 1 Data Exploration
import pandas as pd
from apis.utils import save_print, check_missing
from apis.plot_diagram import plot_history_info
from config import col_what


def convert_time(df):
    save_print("\nSTEP -- convert_time")
    df['Occurrence_Time'] = df['Occurrence_Time'].str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]))
    save_print(df['Occurrence_Time'].head(5))


def fill_missing(df):
    save_print("\nSTEP -- fill_missing")
    save_print(df.groupby('Bike_Type').mean().Cost_of_Bike)

    # fill Cost_of_Bike based on the mean of Bike_Type
    df['Cost_of_Bike'] = df['Cost_of_Bike'].fillna(df.groupby('Bike_Type')['Cost_of_Bike'].transform('mean').round(2))


# get dummies for non-numeric col
def cat_data(df):
    save_print("\nSTEP -- cat_data")
    categorical_cols = []
    for col, col_type in df.dtypes.iteritems():
        if col_type == 'O':
            categorical_cols.append(col)
    save_print(categorical_cols)
    return pd.get_dummies(df, columns=categorical_cols, dummy_na=False)


def convert_value(df):
    save_print("\nSTEP -- convert_value")
    # col Occurrence_Date
    # -- convert
    convert_time(df)
    # col Bike_Make
    # -- trim from right
    df['Bike_Make'].str.rstrip(' \n\t')
    # -- convert
    plot_history_info(df, 'Bike_Make')
    # col Bike_Colour
    # -- trim from right spaces
    df['Bike_Colour'].str.rstrip(' \n\t')
    # -- convert
    plot_history_info(df, 'Bike_Colour')


def analysis_what(df):
    save_print("\nAnalysis what -- bike")
    # check missing
    check_missing(df, col_what)
    # fill_missing(df)


