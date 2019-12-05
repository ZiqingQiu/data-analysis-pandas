from apis.plot_diagram import plot_bar_value_counts
from apis.utils import save_print, check_missing, check_unique
from config import col_when


def analysis_when(df):
    save_print("\nanalysis_when what -- bike")
    # check missing
    check_missing(df, col_when)
    # check unique
    check_unique(df, col_when)

    # [Occurrence_Year]
    annual_theft = df['Occurrence_Year'].value_counts()
    plot_bar_value_counts(annual_theft, 'Annual_Status')

    # [Occurrence_Month]
    month_theft = df['Occurrence_Month'].value_counts()
    plot_bar_value_counts(month_theft, 'Month_Status')

    # [Occurrence_Day]
    day_theft = df['Occurrence_Day'].value_counts()
    plot_bar_value_counts(day_theft, 'Daily_Status')

