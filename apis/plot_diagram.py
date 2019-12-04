from matplotlib import pyplot as plt

from apis.utils import save_print
from config import histogram_percentile


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

