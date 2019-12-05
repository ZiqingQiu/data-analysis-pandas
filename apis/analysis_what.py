# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:20:10 2019

@author: group1
"""
# 1 Data Exploration
import pandas as pd
from apis.utils import save_print, check_missing, check_unique, group_by_statistics, group_by_most_frequent
from apis.plot_diagram import plot_history_info, plot_box
from config import col_what
import numpy as np


def convert_time(df):
    save_print("\nSTEP -- convert_time")
    df['Occurrence_Time'] = df['Occurrence_Time'].str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]))
    save_print(df['Occurrence_Time'].head(5))


def fill_missing_bike_cost(df):
    save_print("\nSTEP -- fill_missing_bike_cost")
    median = df.groupby('Bike_Type').median().Cost_of_Bike
    save_print(median)
    df['Cost_of_Bike'].fillna(
        df.groupby('Bike_Type')['Cost_of_Bike'].transform('median'), inplace=True)


def fill_missing_bike_color(df):
    save_print("\nSTEP -- fill_missing_bike_color")
    grp_by_cols = ['Bike_Type']
    cal_col = 'Bike_Colour'
    tmp_df = group_by_most_frequent(df, grp_by_cols, cal_col)
    s = df['Bike_Type'].map(tmp_df.set_index('Bike_Type')['Bike_Colour'])
    df.loc[df['Bike_Colour'].isnull(), 'Bike_Colour'] = s
    save_print("\nSTEP -- fill_missing_bike_color")



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
    # check unique
    check_unique(df, col_what)

    # [Bike_Make]
    plot_history_info(df, 'Bike_Make')
    # [Bike_Type]
    plot_history_info(df, 'Bike_Type')
    # [Bike_Speed]
    plot_box(df, 'Bike_Speed')
    # [Bike_Colour]
    fill_missing_bike_color(df)
    # [Cost_of_Bike]
    fill_missing_bike_cost(df)
    check_missing(df, col_what)

    # grp_by_cols = ['Bike_Type', 'Bike_Colour']
    # cal_col = 'Bike_Make'
    # group_by_statistics(df, grp_by_cols, cal_col)




