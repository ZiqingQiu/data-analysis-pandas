from apis.plot_diagram import plot_top_n_info, plot_bar_value_counts, plot_scatter, plot_toronto_scatter
from apis.utils import save_print, check_missing, check_unique
from config import col_where


def analysis_where(df):
    save_print("\nAnalysis where -- location")
    # check missing
    check_missing(df, col_where)
    # check unique
    check_unique(df, col_where)

    # [Division]
    df['Division'] = df['Division'].astype(str)
    plot_top_n_info(df, 'Division')

    # [Location_Type]
    plot_top_n_info(df, 'Location_Type')

    # [Premise_Type]
    pt_vc = df['Premise_Type'].value_counts()
    plot_bar_value_counts(pt_vc, 'Premise_Type')
    # plot top n for Premise_Type == 'Other'
    row_filter = df['Premise_Type'] != 'Other'
    index_names = df[row_filter].index
    filter_df = df.drop(index_names, axis=0)
    plot_top_n_info(filter_df, 'Location_Type', 'Other_PType')

    # [Hood_ID]
    df['Hood_ID'] = df['Hood_ID'].astype(str)
    plot_top_n_info(df, 'Hood_ID')

    # [Lat/Long]
    grouped = df.groupby(['Lat', 'Long'])['ObjectId'].count()
    plot_toronto_scatter(grouped, 'Long', 'Lat', 'Lat_Long')

