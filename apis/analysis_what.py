# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:20:10 2019

@author: group1
"""
# 1 Data Exploration
import pandas as pd
from apis.utils import save_print, check_missing, check_unique, group_by_most_frequent
from apis.plot_diagram import plot_top_n_info, plot_box, plot_histogram
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
    plot_top_n_info(df, 'Bike_Make')
    # col Bike_Colour
    # -- trim from right spaces
    df['Bike_Colour'].str.rstrip(' \n\t')
    # -- convert
    plot_top_n_info(df, 'Bike_Colour')


def cal_corr_cost_speed(df):
    save_print('****\nSTEP -- cal_corr_cost_speed***')
    # fig, axs = plt.subplots(nrows=7, ncols=2, figsize=(6, 6), facecolor='w', edgecolor='k')
    # fig.subplots_adjust(hspace=.5, wspace=.001)

    unique_types = df['Bike_Type'].unique()
    # for u_type, ax in zip(unique_types, axs.flat):
    for u_type in unique_types:
        filter_cond = df["Bike_Type"] == u_type
        tmp_df = df.where(filter_cond)
        corr = tmp_df['Bike_Speed'].corr(tmp_df['Cost_of_Bike'])
        save_print(u_type + " " + str(corr))

        # ax.scatter(tmp_df['Bike_Speed'], tmp_df['Cost_of_Bike'], label=u_type)
    # fig.savefig('output/' + 'Speed_Cost_Corr_' + current_df_name + '.png')


def analysis_what(df):
    save_print("\nAnalysis what -- bike")
    # check missing
    check_missing(df, col_what)
    # check unique
    check_unique(df, col_what)

    # [Bike_Make]
    plot_top_n_info(df, 'Bike_Make')
    # [Bike_Type]
    plot_top_n_info(df, 'Bike_Type')
    # [Bike_Speed]
    plot_box(df, 'Bike_Speed')
    save_print('****Bike_Speed group by Bike_Type describe:****')
    save_print(df.groupby(['Bike_Type'])['Bike_Speed'].describe())
    plot_histogram(df, 'Bike_Speed')
    # [Bike_Colour]
    fill_missing_bike_color(df)
    plot_top_n_info(df, 'Bike_Colour')
    # [Cost_of_Bike]
    fill_missing_bike_cost(df)
    plot_box(df, 'Cost_of_Bike')
    plot_histogram(df, 'Cost_of_Bike', np.arange(0, 5000, 50), True)
    # [Bike_Speed, Cost_of_Bike]
    cal_corr_cost_speed(df)

    # recheck missing
    check_missing(df, col_what)

    # grp_by_cols = ['Bike_Type', 'Bike_Colour']
    # cal_col = 'Bike_Make'
    # group_by_statistics(df, grp_by_cols, cal_col)




