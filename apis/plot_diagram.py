from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from apis.utils import save_print, latlong_to_xy
from config import histogram_percentile, current_df_name
import pandas as pd
import numpy as np
import utm


def plot_history_info(df, col):
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
                  '] value that contributes ' + str(histogram_percentile * 100) + '% ' + current_df_name + ' data'
    save_print(console_str)
    save_print(df[col].value_counts()[:n])

    # plot
    plt.rcdefaults()
    # plt.autoscale(tight=False)
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
        ax.annotate(str(p.get_width()), (p.get_width(), p.get_y() + p.get_height() * 0.75))
    fig.savefig('output/' + col + '_histogram_' + current_df_name + '.png')
    return top_cols


def plot_box(df, col):
    fig, ax1 = plt.subplots()
    ax1.set_title('Box Plot for ' + col)
    red_diamond = dict(markerfacecolor='r', marker='D')
    ax1.boxplot(df[col], flierprops=red_diamond)
    fig.savefig('output/' + col + '_box_' + current_df_name + '.png')


def plot_bar_value_counts(s, title, x_tick=None):
    fig, ax = plt.subplots()
    ax.bar(s.index.tolist(), s.values.tolist(), align='center')
    ax.set_title(title + '_' + current_df_name)
    # ax.set_xlabel(x_col)
    # ax.set_ylabel(y_col)
    if x_tick is not None:
        ax.xaxis.set_ticks(np.arange(min(s.index.tolist()), max(s.index.tolist()) + 1, x_tick))
    fig.savefig('output/' + title + 'value_bar' + '_' + current_df_name + '.png')


def plot_scatter(df, x_col, y_col, title):
    fig, ax = plt.subplots()
    ax.scatter(df[x_col], df[y_col], s=0.2)
    ax.set_title(title + '_' + current_df_name)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    fig.savefig('output/' + title + 'scatter' + '_' + current_df_name + '.png')


def plot_toronto_scatter(df, x_col, y_col, title):
    fig, ax = plt.subplots()
    x, y = df.index.get_level_values(1), df.index.get_level_values(0)
    ax.scatter(x, y,
               s=[min(0.05 * 2 ** n, 16) for n in df.values])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title + '_scatter_' + current_df_name)
    fig.savefig('output/' + title + 'scatter' + '_' + current_df_name + '.png')
