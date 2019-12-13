from flask import Flask, request, jsonify
import traceback
import pandas as pd
import joblib
import sys

# Your API definition
from apis.utils import keep_and_replace_value, convert_weekday, map_int_to_string
from config import root_folder, bike_color_keep, month_to_season_enable, spring_months, summer_months, fall_months, \
    winter_months, division_keep

app = Flask(__name__)


@app.route('/predict/lr/', endpoint='lr', methods=["POST", "GET"])
@app.route('/predict/dc/', endpoint='dc', methods=["POST", "GET"])
def predict():
    if request.endpoint == 'dc' and dc:
        try:
            json_ = request.json
            print(json_)
            query = pd.get_dummies(pd.DataFrame(json_))
            query = query.reindex(columns=dc_model_columns, fill_value=0)
            prediction = list(dc.predict(query))
            print({'prediction': str(prediction)})
            return jsonify({'prediction': str(prediction)})
        except:
            return jsonify({'trace': traceback.format_exc()})
    elif request.endpoint == 'lr' and lr:
        try:
            json_ = request.json
            print(json_)
            df_input = pd.DataFrame(json_)
            # pre process
            keep_and_replace_value(df_input, 'Bike_Colour', bike_color_keep, 'OTHER')
            convert_weekday(df_input)
            exclude_cols_when = ['Occurrence_Year', 'Occurrence_Day', 'Occurrence_Time']
            df_input.drop(exclude_cols_when, axis=1, inplace=True)
            if month_to_season_enable:
                map_int_to_string(df_input, 'Occurrence_Month', spring_months, 'Spring')
                map_int_to_string(df_input, 'Occurrence_Month', summer_months, 'Summer')
                map_int_to_string(df_input, 'Occurrence_Month', fall_months, 'Fall')
                map_int_to_string(df_input, 'Occurrence_Month', winter_months, 'Winter')
            keep_and_replace_value(df_input, 'Division', division_keep, 'OTHER')
            query = pd.get_dummies(df_input)
            print(query)
            query = query.reindex(columns=lr_model_columns, fill_value=0)
            prediction = list(lr.predict(query))
            print({'prediction': str(prediction)})
            return jsonify({'prediction': str(prediction)})
        except:
            return jsonify({'trace': traceback.format_exc()})
    else:
        print('Train the model first')
        return 'No model here to use'


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])  # This is for a command-line input
    except:
        port = 12345  # If you don't provide any port the port will be set to 12345

    # Load "model.pkl"
    lr = joblib.load(root_folder + "lg_regression.pkl")
    print('lr regression model loaded...')
    # Load "model_columns.pkl"
    lr_model_columns = joblib.load(root_folder + "lg_regression_cols.pkl")
    print('lr regression model columns loaded...')

    # Load "model.pkl"
    dc = joblib.load(root_folder + "dc_tree.pkl")
    print('dc tree model loaded...')
    # Load "model_columns.pkl"
    dc_model_columns = joblib.load(root_folder + "dc_tree_cols.pkl")
    print('dc tree  model columns loaded...')

    app.run(port=port, debug=True)
