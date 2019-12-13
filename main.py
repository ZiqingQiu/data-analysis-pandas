from apis.analysis_when import analysis_when
from apis.analysis_where import analysis_where
from apis.explore_data import data_explore
from apis.analysis_what import analysis_what
from apis.utils import get_configure_df, save_print
from models.decision_tree import build_decision_tree
from models.gradient_boosting import build_gradient_boosting
from models.k_nearest_neighbors import build_nearest_neighbors
from models.logistic_regression import build_logistic_regression
from models.pre_process import pre_process
import pandas as pd

from models.random_forest import build_random_forest


def main():
    # explore data
    df_whole, df_stolen, df_recover = data_explore()
    # set cur df
    df = get_configure_df(df_whole, df_stolen, df_recover)

    # what -- bike
    analysis_what(df)
    # when -- time
    analysis_when(df)
    # where -- location
    analysis_where(df)

    # pre process
    pre_process(df)

    label_col = ['Status']
    df_label = df.Status
    df.drop(label_col, axis=1, inplace=True)

    # logistic regression
    # build_logistic_regression(df, df_label)

    # decision_tree
    build_decision_tree(df, df_label)

    # advanced trees
    # random forest
    # build_random_forest(df, df_label)
    # build_gradient_boosting(df, df_label)

    # nearest neighbors
    # build_nearest_neighbors(df, df_label)


if __name__ == '__main__':
    main()

