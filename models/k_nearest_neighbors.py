from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from apis.utils import dynamic_get_dummies, over_sample, get_accuracy
from config import num_of_neighbors, knn_weights


def build_nearest_neighbors(df_feature, df_label):
    df_ohe = dynamic_get_dummies(df_feature)
    train_x, test_x, train_y, test_y = train_test_split(df_ohe, df_label, test_size=0.3, random_state=99)
    # over sample
    train_x, train_y = over_sample(train_x, train_y)
    knn = KNeighborsClassifier(num_of_neighbors, weights=knn_weights)
    knn.fit(train_x, train_y)
    test_y_predict = knn.predict(test_x)
    labels = df_label.unique()
    get_accuracy("nearest neighbors", test_y, test_y_predict, labels)

