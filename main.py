from apis.analysis_when import analysis_when
from apis.analysis_where import analysis_where
from apis.explore_data import data_explore
from apis.analysis_what import analysis_what
from apis.utils import get_configure_df
from models.pre_process import pre_process


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


if __name__ == '__main__':
    main()

