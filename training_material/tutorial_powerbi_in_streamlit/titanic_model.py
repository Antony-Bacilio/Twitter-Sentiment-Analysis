"""
Next, let’s make a model and save it in pickle file to avoid recalculation of the model every time.
For this example, I have used simple Logistic Regression from Scikit-learn for binary classification.
Our target variable is Survived. Let us see, how to make a pickle file.
Name the model building file as titanic_model.py.
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv('titanic.csv')
df = df.drop(['Name', 'PassengerId', 'Sex', 'Embarked', 'Ticket', 'Cabin'], axis=1)
# dropping null values.
df = df.dropna()
print(df)

y = df['Survived']
x = df.iloc[:, 1:]

# split into train test sets.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

# making model and fitting
log_reg = LogisticRegression()
log_reg.fit(x_train, y_train)

pickle.dump(log_reg, open('titanic_clf.pkl', 'wb'))


