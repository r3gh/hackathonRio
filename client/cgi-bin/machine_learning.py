from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_regression
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn import preprocessing
from sklearn import svm

#test
text = np.genfromtxt('modified_result.csv', delimiter="\t", dtype=None, skip_header=1)
arrData = []
for t in text:
	arrData.append(str(t).split(","))
arrData = np.array(arrData)

regr = RandomForestClassifier(max_depth=2, random_state=0)
clf = svm.SVC()
#le = preprocessing.LabelEncoder()

indices = np.where(arrData[:,2] == '2')[0] #crime type = 2
#print(indices)
data = arrData[indices, 2:3]
labels = arrData[indices, 0]
qtyTrain = len(indices)*0.8
trainData = data[:qtyTrain]
trainLabels = labels[:qtyTrain]
#le.fit(trainLabels)
regr.fit(trainData, trainLabels)
clf.fit(trainData, trainLabels)
testData = data[qtyTrain:]
testLabels = labels[qtyTrain:]
#le.fit(testLabels)
#testLabels = le.transform(testLabels)
#X, y = make_regression(n_features=4, n_informative=2, random_state=0, shuffle=False)
#print(regr.feature_importances_)
predicted = regr.predict(testData)
#print(testLabels)
#print(predicted)
print(accuracy_score(testLabels, predicted))

predicted = clf.predict(testData)
#print(testLabels)
#print(predicted)
print(accuracy_score(testLabels, predicted))