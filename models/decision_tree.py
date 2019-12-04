# def tbd:
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