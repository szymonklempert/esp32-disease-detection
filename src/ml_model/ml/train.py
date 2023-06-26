from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle
df = pd.read_csv('data/merged_cleaned.csv')

X = df.drop(['label'], axis=1)
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# DECISION TREE
from sklearn import tree

model = tree.DecisionTreeClassifier()
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print(score)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(acc)

filename = 'decisionTree_model.pkl'
pickle.dump(model, open(filename, 'wb'))




# BAGGING MODEL -  RANDOM FOREST ALGORITHM
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=40)  # doubt
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print(score)


y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(acc)
pickle.dump(model, open('randomForest.pkl', 'wb'))
