from apis.analysis_when import analysis_when
from apis.explore_data import data_explore
from apis.analysis_what import analysis_what
from apis.utils import get_configure_df


def main():
    # explore data
    df_whole, df_stolen, df_recover = data_explore()
    # set cur df
    df = get_configure_df(df_whole, df_stolen, df_recover)

    # what -- bike
    analysis_what(df)

    # when -- time
    analysis_when(df)


if __name__ == '__main__':
    main()

