from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from apis.utils import dynamic_get_dummies, over_sample, get_accuracy


def build_ada_boosting(df_feature, df_label):
    df_ohe = dynamic_get_dummies(df_feature)
    train_x, test_x, train_y, test_y = train_test_split(df_ohe, df_label, test_size=0.3, random_state=99)
    # over sample
    train_x, train_y = over_sample(train_x, train_y)
    ab = AdaBoostClassifier(n_estimators=1000)
    ab.fit(train_x, train_y)
    test_y_predict = ab.predict(test_x)
    labels = df_label.unique()
    get_accuracy("ada boosting", test_y, test_y_predict, labels)