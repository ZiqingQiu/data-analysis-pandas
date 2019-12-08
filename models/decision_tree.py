from sklearn.metrics import confusion_matrix, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from apis.utils import save_print, dynamic_get_dummies, over_sample
from config import over_sample_enable, status_stolen, status_recover
import pandas as pd


def build_decision_tree(df_feature, df_label):
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
    dc_tree = DecisionTreeClassifier(criterion='entropy', max_depth=10, min_samples_split=20, random_state=99)
    dc_tree.fit(train_x, train_y)
    test_y_predict = dc_tree.predict(test_x)
    # testY_predict = testY_predict.astype(int)
    save_print("Decision Tree Accuracy:" + str(metrics.accuracy_score(test_y, test_y_predict)))

    # confusion matrix
    labels = df_label.unique()
    print("Confusion matrix \n", confusion_matrix(test_y, test_y_predict, labels))
    save_print("Decision Tree Recall score: " + str(recall_score(test_y, test_y_predict)))
    save_print("Decision Tree F1 score: " + str(f1_score(test_y, test_y_predict, average='weighted')))
    # print("feature importance " + str(dt1_james.feature_importances_))
    #
    # rfe = RFE(dt1_james, 5)
    # cols = list(train_x.columns)
    # print(cols)
    # importances = list(zip(dt1_james.feature_importances_, cols))
    # importances.sort(reverse=True)
    # pd.DataFrame(importances, index=[x for (_, x) in importances]).plot(kind='bar')