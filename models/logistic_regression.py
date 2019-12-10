from sklearn import linear_model
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from apis.utils import dynamic_get_dummies, over_sample, save_print
from config import over_sample_enable, status_recover, status_stolen
import pandas as pd
import numpy as np


def build_logistic_regression(df_feature, df_label):
    df_ohe = dynamic_get_dummies(df_feature)
    train_x, test_x, train_y, test_y = train_test_split(df_ohe, df_label, test_size=0.3, random_state=99)
    # dbg_recover = pd.concat([test_x, test_y], axis=1)
    # over sample recovered
    if over_sample_enable:
        df_train = pd.concat([train_x, train_y], axis=1)
        df_stolen = df_train[df_train.Status == status_stolen]
        df_recover = df_train[df_train.Status == status_recover]
        df_recover_up_sampled = over_sample(df_recover, df_stolen)
        df_train_up_sampled = pd.concat([df_stolen, df_recover_up_sampled])
        save_print("After over sample:\n" + str(df_train_up_sampled['Status'].value_counts()))
        train_y = df_train_up_sampled.Status
        train_x = df_train_up_sampled.drop('Status', axis=1)

    lg_regression = linear_model.LogisticRegression(solver='lbfgs')
    lg_regression.fit(train_x, train_y)
    # predict
    test_y_predict = lg_regression.predict(test_x)
    save_print("predict accuracy: " + str(metrics.accuracy_score(test_y, test_y_predict)))
    labels = df_label.unique()
    print("predict Confusion matrix \n", confusion_matrix(test_y, test_y_predict, labels))
    # probs
    test_y_predict_probs = lg_regression.predict_proba(test_x)
    test_y_predict_prob = test_y_predict_probs[:, 1]
    prob_df = pd.DataFrame(test_y_predict_prob)
    prob_df['predict'] = np.where(prob_df[0] >= 0.5, 1, 0)
    save_print("predict_proba accuracy: " + str(metrics.accuracy_score(test_y, prob_df['predict'])))
    print("predict_proba Confusion matrix \n", confusion_matrix(test_y, prob_df['predict'], labels))


