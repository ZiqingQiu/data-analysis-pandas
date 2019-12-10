from sklearn.metrics import confusion_matrix, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from apis.utils import save_print, dynamic_get_dummies, over_sample, get_accuracy


def build_decision_tree(df_feature, df_label):
    df_ohe = dynamic_get_dummies(df_feature)
    train_x, test_x, train_y, test_y = train_test_split(df_ohe, df_label, test_size=0.3, random_state=99)
    # dbg_recover = pd.concat([test_x, test_y], axis=1)
    # over sample
    train_x, train_y = over_sample(train_x, train_y)
    dc_tree = DecisionTreeClassifier(criterion='entropy', max_depth=10, min_samples_split=20, random_state=99)
    dc_tree.fit(train_x, train_y)
    test_y_predict = dc_tree.predict(test_x)
    labels = df_label.unique()
    get_accuracy("decision tree", test_y, test_y_predict, labels)
    # print("feature importance " + str(dt1_james.feature_importances_))
    #
    # rfe = RFE(dt1_james, 5)
    # cols = list(train_x.columns)
    # print(cols)
    # importances = list(zip(dt1_james.feature_importances_, cols))
    # importances.sort(reverse=True)
    # pd.DataFrame(importances, index=[x for (_, x) in importances]).plot(kind='bar')