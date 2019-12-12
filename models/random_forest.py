from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from apis.utils import dynamic_get_dummies, over_sample, get_accuracy


def build_random_forest(df_feature, df_label):
    df_ohe = dynamic_get_dummies(df_feature)
    train_x, test_x, train_y, test_y = train_test_split(df_ohe, df_label, test_size=0.3, random_state=99)
    # over sample
    train_x, train_y = over_sample(train_x, train_y)
    rf = RandomForestClassifier(n_estimators=1000)
    rf.fit(train_x, train_y)
    test_y_predict = rf.predict(test_x)
    labels = df_label.unique()
    get_accuracy("random forest", test_y, test_y_predict, labels)
