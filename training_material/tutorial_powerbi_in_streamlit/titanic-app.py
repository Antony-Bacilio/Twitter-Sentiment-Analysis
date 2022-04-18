"""
Once we have the dashboard, we need to get a link to embed it in the streamlit app.
To fetch the url, go to File and click on Publish to Web.
Doing this will generate a url which can be copied and used to render the dashboard onto the web app.
Looking at the options closely, you’ll notice that the size of the dashboard can be tailored to your preference .
Moving forward, let’s build our web app using streamlit. Name the app file as titanic-app.py
"""

import streamlit as st
import streamlit.components.v1
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

st.header("Welcome to our Titanic StreamLit Web App")
st.subheader('''
The page is divided in two categories:
    1. PowerBI report on Titanic dataset
    2. Data preprocessing and predictions''')
options = st.selectbox("Please Select: ", ['PowerBI', 'Preprocessing & predictions'])

# As mentioned in the web app, the app is divided in two sections which are namely the PowerBI report and
# Preprocessing & predictions. The st.selectbox option helps us to create a dropdown menu which consists both the
# above options. Further ahead, now let’s connect our PowerBI report to the app.

# link_copied_from_powerbi_web_service
URL_POWERBI_RAPPORT_TWEETS = "https://app.powerbi.com/reportEmbed?reportId=a06f1e09-3902-445c-a29c-0f6cc8a5a63d" \
                             "&autoAuth=true&ctid=bc3dae5f-0b33-403d-b719-946457461af5&config" \
                             "=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLW5vcnRoLWV1cm9wZS1yZWRpcmVjdC5hbmFseXNpcy53aW5kb3dzLm5ldC8ifQ%3D%3D "
# URL_POWERBI_RAPPORT_VANARSDEL = "https://app.powerbi.com/reportEmbed?reportId=1c29d2f6-7ea6-4621-a43d-dae772190011
# &autoAuth=true&ctid=bc3dae5f-0b33-403d-b719-946457461af5&config
# =eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLW5vcnRoLWV1cm9wZS1yZWRpcmVjdC5hbmFseXNpcy53aW5kb3dzLm5ldC8ifQ%3D%3D"

if options == 'PowerBI':
    print("Hi!")

    st.components.v1.iframe(URL_POWERBI_RAPPORT_TWEETS, width=1000, height=700, scrolling=True)
    # src: https://docs.streamlit.io/library/components/components-api
    # st.markdown(URL_POWERBI_RAPPORT_VANARSDEL, unsafe_allow_html=True)

else:
    """
    The else part contains the logic behind pre-processing and predictions. 
    The above code imports the titanic dataset and prints out the first 5 rows of the dataset. 
    It also designs a sidebar with sliders and dropdowns to adjust the values of the input parameters and prints out those values for reference. 
    To understand the spread of the dataset, the app shows outputs of df.describe() and df.info(). 
    """
    df = pd.read_csv('titanic.csv')
    # df = df.drop(['Name', 'PassengerId', 'Sex', 'Embarked', 'Ticket', 'Cabin'], axis=1)
    df = df.dropna()
    st.write(df.head())

    def user_input_features():
        pclass = st.sidebar.selectbox('Pclass', [0, 1])
        sex = st.sidebar.selectbox('Sex', [0, 1])
        age = st.sidebar.slider('Age', 0.42, 80.00, 31.0)
        sibsp = st.sidebar.slider('SibSp', 0, 5, 2)
        parch = st.sidebar.slider('Parch', 0, 6, 2)
        fare = st.sidebar.slider('Fare', 0.0, 513.0, 2.0)
        embarked = st.sidebar.slider('Embarked', 1, 3, 2)
        data = {'pclass': pclass,
                'age': age,
                'sibsp': sibsp,
                'parch': parch,
                'fare': fare,
                }
        # data = {'pclass': pclass,'sex': sex,'age': age,'sibsp': sibsp, 'parch': parch, 'fare': fare, 'embarked':
        # embarked}
        features = pd.DataFrame(data, index=[0])
        return features

    st.sidebar.subheader('User Input parameters')
    df1 = user_input_features()
    print("df1:\n", df1)

    # print info and description
    st.write(df.info())
    st.write(df.describe())

    st.subheader('User input parameters')
    st.write(df1)
    y = df['Survived']
    x = df.iloc[:, 1:]

    # split into train test sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

    # Loading model
    load_clf = pickle.load(open('titanic_clf.pkl', 'rb'))

    prediction = load_clf.predict(df1)
    prediction_proba = load_clf.predict_proba(df1)

    st.subheader('Prediction Probability')
    st.write(prediction_proba)

