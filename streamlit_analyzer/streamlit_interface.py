import streamlit.components.v1
import time
import streamlit as st
import get_tweets_api as api


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center; color: red;'>Analyse de sentiment sur des tweets</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style=\"text-align: center\"> Analyse de sentiment sur des tweets</h1>")
    st.header("Analyse de sentiment sur des tweets")
    st.subheader('''
                    Le site est divisé en 3 sections :
                        1. Tweets en anglais analysés avec la bibliothèque 'TextBlob'.
                        2. Tweets en français analysés avec la bibliothèque 'Afinn'.
                        3. Prediction du sexe des utilisateurs ayant publié des tweets en français.''')

    # The st.selectbox option helps us to create a dropdown menu which consists both the
    # above options. Further ahead, now let’s connect our PowerBI report to the app.
    # options = st.selectbox("Please Select: ", ['English tweets', 'French tweets'])

    # link_copied_from_powerbi_web_service
    URL_GET_POWERBI_RAPPORT_TWEETS_EN = "https://app.powerbi.com/reportEmbed?reportId=8e46e37b-5da1-4965-95c5-2977428760f6&autoAuth=true&ctid=bc3dae5f-0b33-403d-b719-946457461af5&config" \
                                        "=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLW5vcnRoLWV1cm9wZS1yZWRpcmVjdC5hbm" \
                                        "FseXNpcy53aW5kb3dzLm5ldC8ifQ%3D%3D"
    URL_GET_POWERBI_RAPPORT_TWEETS_FR = "https://app.powerbi.com/reportEmbed?reportId=361a10a6-60a3-4927-9875" \
                                        "-faa2f3a6eb3a&autoAuth=true&ctid=bc3dae5f-0b33-403d-b719-946457461af5&" \
                                        "config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLW5vcnRoLWV1cm9wZS1yZWRpcmVj" \
                                        "dC5hbmFseXNpcy53aW5kb3dzLm5ldC8ifQ%3D%3D"

    st.header("Rapport PowerBI - Tweets en anglais :")
    # if options == 'English tweets':
    print("English tweet!")
    st.components.v1.iframe(URL_GET_POWERBI_RAPPORT_TWEETS_EN, width=1500, height=700, scrolling=True)
        # src: https://docs.streamlit.io/library/components/components-api
        # st.markdown(URL_POWERBI_RAPPORT_VANARSDEL, unsafe_allow_html=True)

    st.header("Rapport PowerBI - Tweets en français :")
    # else:
    print("French tweets!")
    st.components.v1.iframe(URL_GET_POWERBI_RAPPORT_TWEETS_FR, width=1500, height=700, scrolling=True)

    st.header("Sexe des utilisateurs - Tweets français :")
    # Address from the flask api
    url_localhost_flask = "http://localhost:5001/api/tweets/twitterdata1"

    # Get tweets from an API and analyse data.
    api.analysis(url_localhost_flask)
