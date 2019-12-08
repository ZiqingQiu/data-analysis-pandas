# functions for common usage
import os
import shutil
from os.path import join
import pandas as pd
from sklearn import preprocessing

from config import current_df_name
import pyproj
import numpy as np

project_root = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


# threshold when to stop including top n features for histogram


def save_print(cmd):
    filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output/text.txt'))
    with open(filename, "a") as f:
        print(cmd, file=f)


def del_output():
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
    print("dbg output_path: " + output_path)
    for the_file in os.listdir(output_path):
        file_path = os.path.join(output_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def get_csv_full_path():
    file_name = 'Bicycle_Thefts.csv'
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    return join(data_path, file_name)


# check missing
def check_missing(df, cols):
    save_print("\nSTEP -- check_missing")
    # save_print(len(df) - df[cols].count())
    percent = df[cols].isnull().sum() * 100 / len(df)
    tmp_df = pd.DataFrame({'missing_value': df.isnull().sum(),
                           'percentage': percent}, index=cols)
    save_print(tmp_df)


# standardize data
def standardize_data(df):
    save_print("STEP -- standardize_data")
    names = df.columns
    scaler = preprocessing.StandardScaler()
    scaled_df = scaler.fit_transform(df)
    return pd.DataFrame(scaled_df, columns=names)


# get configured df
def get_configure_df(df_whole, df_stolen, df_recover):
    switcher = {
        "STOLEN": df_stolen,
        "RECOVERED": df_recover,
        "WHOLE": df_whole
    }
    save_print("\n************************\n"
               + current_df_name
               + " df returned...\n************************")
    return switcher.get(current_df_name, "Invalid df configure!!!!!!")


# check unique
def check_unique(df, cols):
    save_print("\nSTEP -- check_unique")
    percent = df[cols].nunique() * 100 / len(df)
    tmp_df = pd.DataFrame({'unique_value': df[cols].nunique(),
                           'percentage': percent}, index=cols)
    save_print(tmp_df)


# group by value and percentage
def group_by_statistics(df, grp_by_cols, count_col):
    save_print("\nSTEP -- group_by_statistics")
    tmp_df = df.groupby(grp_by_cols)[count_col] \
        .count() \
        .reset_index(name='count') \
        .sort_values(['count'], ascending=False) \
        .head(100)
    save_print(tmp_df)


# group by and display the most frequent
def group_by_most_frequent(df, grp_by_cols, count_col):
    save_print("\nSTEP -- group_by_most_frequent")
    tmp_df = df.groupby(grp_by_cols)[count_col].apply(lambda x: x.value_counts().index[0]).reset_index()
    save_print(tmp_df)
    return tmp_df


# keep is in keep list, if not replace it
def keep_and_replace_value(df, col, keep_list, replace_value):
    save_print("\nSTEP -- keep_and_replace_value " + col)
    df.loc[~df[col].isin(keep_list), col] = replace_value


# map int to string
def map_int_to_string(df, col, int_list, str_value):
    save_print("\nSTEP -- map_int_to_string " + col)
    df.loc[df[col].isin(int_list), col] = str_value


# convert year month day to weekday
def convert_weekday(df):
    df['Week_days'] = df.apply(lambda row: str(row.Occurrence_Year) + '-' + str(row.Occurrence_Month) + '-' +
                                           str(row.Occurrence_Day), axis=1)
    df['Week_days'] = pd.to_datetime(df['Week_days'])
    df['Week_days'] = df['Week_days'].dt.weekday_name

