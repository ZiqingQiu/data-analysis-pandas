histogram_percentile = 0.8
status_stolen = 0
status_recover = 1

col_what = ['Bike_Make', 'Bike_Model', 'Bike_Type', 'Bike_Speed', 'Bike_Colour', 'Cost_of_Bike']
col_when = ['Occurrence_Year', 'Occurrence_Month', 'Occurrence_Day', 'Occurrence_Time']
col_where = ['Division', 'Location_Type', 'Premise_Type', 'Hood_ID', 'Lat', 'Long']

bike_color_keep = ['BLK', 'BLU', 'GRY', 'WHI', 'RED']
month_to_season_enable = True
spring_months = [3, 4, 5]
summer_months = [6, 7, 8]
fall_months = [9, 10, 11]
winter_months = [1, 2, 12]
division_keep = ['52', '14', '51', '53', '55']
convert_hour = True

lg_threshold = 0.5
num_of_neighbors = 55
knn_weights = "uniform"

root_folder = "D:/3. GitHubMirrorReps/pandas/serialized_models/"

# core config
# STOLEN; RECOVERED; WHOLE
current_df_name = "STOLEN"
over_sample_enable = True
# DUPLICATE; SMOTE
over_sample_algorithm = "SMOTE"
max_feature_try_numbers = 38
# RFE; ONCE
run_mode = "ONCE"

