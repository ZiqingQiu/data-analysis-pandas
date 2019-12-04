# functions for common usage
import os
import shutil
from os.path import join

import pandas as pd
from sklearn import preprocessing

from config import current_df_name

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
    save_print("STEP -- check_missing")
    save_print(len(df) - df[cols].count())


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

