# functions for common usage
# from matplotlib import pyplot as plt
import os
import shutil
from os.path import dirname, join
import matplotlib.pyplot as plt
import pandas as pd
from config import histogram_percentile
import numpy as np
import matplotlib.pyplot as plt


project_root = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


# threshold when to stop including top n features for histogram


def save_print(cmd, filename="output/text.txt"):
    with open(filename, "a") as f:
        print(cmd, file=f)


def save_plt(plt_obj, filename):
    # tbd: not sure yet
    plt_obj.savefig(filename)


def del_output():
    output_path = join(project_root, 'output')
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
    data_path = join(project_root, 'data')
    return join(data_path, file_name)


def get_history_info(df, col):
    # this method will print top n index at console
    # also plot png for histogram on hard drive
    threshold = len(df) * histogram_percentile
    sum_value = 0
    n = 0
    for value in df[col].value_counts().values.tolist():
        sum_value += value
        if sum_value >= threshold:
            break
        else:
            n = n + 1
    top_cols = df[col].value_counts()[:n].index.tolist()
    console_str = 'Top ' + str(n) + '/' + str(df[col].nunique()) + ' [' + col + \
                  '] value that contributes ' + str(histogram_percentile*100) + '% data'
    save_print(console_str)
    save_print(df[col].value_counts()[:n])

    # plot
    plt.rcdefaults()
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 8)
    ax.barh(df[col].value_counts()[:n].index.tolist(),
            df[col].value_counts()[:n].values.tolist(), align='center')
    ax.set_ylabel(col, labelpad=10, weight='bold', size=12)
    ax.set_xlabel('value count', labelpad=3, weight='bold', size=12)
    ax.set_title(console_str)
    # ax.yaxis.tick_right()
    ax.invert_yaxis()
    for p in ax.patches:
        ax.annotate(str(p.get_width()), (p.get_width()+10, p.get_y()+p.get_height()*0.75))
    fig.savefig('output/' + col + '_histogram.png')
    return top_cols
