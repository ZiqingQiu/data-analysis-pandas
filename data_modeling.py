# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:20:10 2019

@author: group1
"""
# 1 Data Exploration
import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from utils import save_print, get_history_info
from sklearn import preprocessing
from sklearn import metrics
from sklearn.metrics import confusion_matrix, f1_score, recall_score


def convert_time(df):
    save_print("\nSTEP -- convert_time")
    df['Occurrence_Time'] = df['Occurrence_Time'].str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]))
    save_print(df['Occurrence_Time'].head(5))


def fill_missing(df):
    save_print("\nSTEP -- fill_missing")
    save_print(df.groupby('Bike_Type').mean().Cost_of_Bike)

    # fill Cost_of_Bike based on the mean of Bike_Type
    df['Cost_of_Bike'] = df['Cost_of_Bike'].fillna(df.groupby('Bike_Type')['Cost_of_Bike'].transform('mean').round(2))


# get dummies for non-numeric col
def cat_data(df):
    save_print("\nSTEP -- cat_data")
    # drop unknown rows for Status
    df = df.drop(df[df.Status == 'UNKNOWN'].index)
    # replace STOLEN as 1 and RECOVERED as 0
    df.loc[df['Status'] == 'STOLEN', 'Status'] = 0
    df.loc[df['Status'] == 'RECOVERED', 'Status'] = 1

    categorical_cols = []
    for col, col_type in df.dtypes.iteritems():
        if col_type == 'O':
            categorical_cols.append(col)
    save_print(categorical_cols)
    return pd.get_dummies(df, columns=categorical_cols, dummy_na=False)


# standardize data
def standardize_data(df):
    save_print("\nSTEP -- standardize_data")
    names = df.columns
    scaler = preprocessing.StandardScaler()
    scaled_df = scaler.fit_transform(df)
    return pd.DataFrame(scaled_df, columns=names)


def convert_value(df):
    save_print("\nSTEP -- convert_value")
    # col Occurrence_Date
    # -- convert
    convert_time(df)
    # col Bike_Make
    # -- trim from right
    df['Bike_Make'].str.rstrip(' \n\t')
    # -- convert
    get_history_info(df, 'Bike_Make')
    # col Bike_Colour
    # -- trim from right spaces
    df['Bike_Colour'].str.rstrip(' \n\t')
    # -- convert
    get_history_info(df, 'Bike_Colour')


def data_modeling(df):
    # 2a - Data transformations includes missing data handling, categorical data management,
    # data normalization and standardizations as needed.
    save_print('****2a output:****')
    convert_value(df)
    # df = cat_data(df)
    # split feature and label
    # label_col = ['Status']
    # df_feature = df[df.columns.difference(label_col)]
    # df_label = df['Status']
    # standardize data
    # df_feature = standardize_data(df_feature)
    # save_print(df_feature.head(5))

    # tbd below part is just for quick verify
    # trainX, testX, trainY, testY = train_test_split(df_feature, df_label, test_size=0.25)
    # dt1_james = DecisionTreeClassifier(criterion='entropy', max_depth=10, min_samples_split=20, random_state=99)
    # dt1_james.fit(trainX, trainY)
    # testY_predict = dt1_james.predict(testX)
    # # testY_predict = testY_predict.astype(int)
    # # save_print("Accuracy:", metrics.accuracy_score(testY, testY_predict))
    # labels = df_label.unique()
    # print("Confusion matrix \n", confusion_matrix(testY, testY_predict, labels))
    # print("recall_score: " + str(recall_score(testY, testY_predict)))
    # print("feature importance " + str(dt1_james.feature_importances_))
    #
    # rfe = RFE(dt1_james, 5)
    # cols = list(trainX.columns)
    # print(cols)
    # importances = list(zip(dt1_james.feature_importances_, cols))
    # importances.sort(reverse=True)
    # pd.DataFrame(importances, index=[x for (_, x) in importances]).plot(kind='bar')
