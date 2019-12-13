from sklearn import linear_model
from sklearn.model_selection import train_test_split
from apis.utils import dynamic_get_dummies, save_print, over_sample, get_accuracy
import pandas as pd
import numpy as np
from config import lg_threshold, max_feature_try_numbers
from sklearn.feature_selection import RFE


def build_logistic_regression(df_feature, df_label):
    df_ohe = dynamic_get_dummies(df_feature)
    train_x, test_x, train_y, test_y = train_test_split(df_ohe, df_label, test_size=0.3, random_state=99)
    # dbg_recover = pd.concat([test_x, test_y], axis=1)
    # over sample
    train_x, train_y = over_sample(train_x, train_y)

    # build model
    nof_list = np.arange(1, max_feature_try_numbers)
    high_score = 0
    nof = 0
    score_list = []
    for n in range(len(nof_list)):
        save_print("********Current nof features are: " + str(nof_list[n]))
        lg_regression = linear_model.LogisticRegression(solver='lbfgs')
        rfe = RFE(lg_regression, nof_list[n])
        rfe_train_x = rfe.fit_transform(train_x, train_y)
        rfe_test_x = rfe.transform(test_x)
        lg_regression.fit(rfe_train_x, train_y)
        labels = df_label.unique()
        # predict
        # test_y_predict = lg_regression.predict(test_x)
        # get_accuracy("logistic regression predict", test_y, test_y_predict, labels)
        # probs
        test_y_predict_probs = lg_regression.predict_proba(rfe_test_x)
        test_y_predict_prob = test_y_predict_probs[:, 1]
        prob_df = pd.DataFrame(test_y_predict_prob)
        prob_df['predict'] = np.where(prob_df[0] >= lg_threshold, 1, 0)
        get_accuracy("logistic regression predict_probs", test_y, prob_df['predict'], labels)


