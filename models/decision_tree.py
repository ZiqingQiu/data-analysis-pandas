import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from apis.plot_diagram import plot_pre_recall
from apis.utils import save_print, dynamic_get_dummies, over_sample, get_accuracy
import numpy as np
from sklearn.feature_selection import RFE
from config import max_feature_try_numbers, run_mode, root_folder
import pandas as pd


best_nof_feature = 2


def run_rfe(df_feature, df_label):
    df_ohe = dynamic_get_dummies(df_feature)
    train_x, test_x, train_y, test_y = train_test_split(df_ohe, df_label, test_size=0.3, random_state=99)
    # dbg_recover = pd.concat([test_x, test_y], axis=1)
    # over sample
    train_x, train_y = over_sample(train_x, train_y)

    # build model
    nof_list = np.arange(1, (max_feature_try_numbers + 1))
    class_1_precision_list = []
    class_1_recall_list = []
    for n in range(len(nof_list)):
        save_print("********Current nof features are: " + str(nof_list[n]))
        dc_tree = DecisionTreeClassifier(criterion='entropy', min_samples_split=20, random_state=99)
        rfe = RFE(dc_tree, nof_list[n])
        rfe_train_x = rfe.fit_transform(train_x, train_y)
        rfe_test_x = rfe.transform(test_x)
        dc_tree.fit(rfe_train_x, train_y)
        labels = df_label.unique()
        # predict
        test_y_predict = dc_tree.predict(rfe_test_x)
        class_1_precision, class_1_recall = get_accuracy("decision tree", test_y, test_y_predict, labels)
        class_1_precision_list.append(class_1_precision)
        class_1_recall_list.append(class_1_recall)
    plot_pre_recall(nof_list, class_1_precision_list, class_1_recall_list, 'decision tree')


def run_once(df_feature, df_label):
    df_ohe = dynamic_get_dummies(df_feature)
    train_x, test_x, train_y, test_y = train_test_split(df_ohe, df_label, test_size=0.3, random_state=99)
    # dbg_recover = pd.concat([test_x, test_y], axis=1)
    # over sample
    train_x, train_y = over_sample(train_x, train_y)
    # build model
    dc_tree = DecisionTreeClassifier(criterion='entropy', min_samples_split=20, random_state=99)
    rfe = RFE(dc_tree, best_nof_feature)
    rfe_train_x = rfe.fit_transform(train_x, train_y)
    rfe_test_x = rfe.transform(test_x)
    dc_tree.fit(rfe_train_x, train_y)
    labels = df_label.unique()
    # predict
    test_y_predict = dc_tree.predict(rfe_test_x)
    get_accuracy("decision tree", test_y, test_y_predict, labels)
    # print features
    cols = list(df_ohe.columns)
    temp = pd.Series(rfe.support_, index=cols)
    selected_features_rfe = temp[temp == True].index
    save_print("Top " + str(best_nof_feature) + " features are: ")
    save_print(selected_features_rfe)
    # dump model
    joblib.dump(dc_tree, root_folder + "dc_tree.pkl")
    save_print("dc_tree Model dumped!")
    joblib.dump(selected_features_rfe, root_folder + "dc_tree_cols.pkl")
    save_print("dc_tree models columns dumped!")


def build_decision_tree(df_feature, df_label):
    if run_mode == "RFE":
        run_rfe(df_feature, df_label)
    else:
        run_once(df_feature, df_label)
