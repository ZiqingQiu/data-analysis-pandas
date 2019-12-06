from apis.plot_diagram import plot_history_info, plot_bar_value_counts, plot_scatter, plot_toronto_scatter
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
    plot_history_info(df, 'Division')

    # [Location_Type]
    plot_history_info(df, 'Location_Type')

    # [Premise_Type]
    pt_vc = df['Premise_Type'].value_counts()
    plot_bar_value_counts(pt_vc, 'Premise_Type')

    # [Hood_ID]
    df['Hood_ID'] = df['Hood_ID'].astype(str)
    plot_history_info(df, 'Hood_ID')

    # [Lat/Long]
    grouped = df.groupby(['Lat', 'Long'])['ObjectId'].count()
    plot_toronto_scatter(grouped, 'Lat', 'Long', 'Lat_Long')

