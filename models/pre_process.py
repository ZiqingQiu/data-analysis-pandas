from apis.utils import keep_and_replace_value, save_print, map_int_to_string
from config import bike_color_keep, month_to_season_enable, spring_months, summer_months, \
    fall_months, winter_months


def pre_process(df):
    # what -- bike
    # exclude columns
    exclude_cols_what = ['Primary_Offence', 'ObjectId', 'Bike_Make', 'Bike_Model']
    df.drop(exclude_cols_what, axis=1, inplace=True)
    # [Bike_Colour] Keep value of ‘BLK’, ‘BLU’, ‘GRY’, ‘WHI’, ‘RED’, and replace the rest ‘OTHER’
    df['Bike_Colour'] = df['Bike_Colour'].str.rstrip()
    keep_and_replace_value(df, 'Bike_Colour', bike_color_keep, 'OTHER')

    # when -- time
    # tbd day and time not decided yet
    exclude_cols_when = ['Occurrence_Year', 'Occurrence_Day', 'Occurrence_Time']
    df.drop(exclude_cols_when, axis=1, inplace=True)
    # [Occurrence_Month] to season
    if month_to_season_enable:
        map_int_to_string(df, 'Occurrence_Month', spring_months, 'Spring')
        map_int_to_string(df, 'Occurrence_Month', summer_months, 'Summer')
        map_int_to_string(df, 'Occurrence_Month', fall_months, 'Fall')
        map_int_to_string(df, 'Occurrence_Month', winter_months, 'Winter')

    save_print("dbg")

