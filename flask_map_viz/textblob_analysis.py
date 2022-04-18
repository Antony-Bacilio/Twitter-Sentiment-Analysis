from textblob import TextBlob


def sentiment_analysis(tweet):
    def get_subjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    # Create a function to get the polarity
    def get_polarity(text):
        return TextBlob(text).sentiment.polarity

    # Create two new columns ‘Subjectivity’ & ‘Polarity’
    # tweet['TextBlob_Subjectivity'] = tweet['tweet'].apply(get_subjectivity)
    # tweet['TextBlob_Polarity'] = tweet['tweet'].apply(get_polarity)

    def get_analysis(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    # tweet['TextBlob_Analysis'] = tweet['TextBlob_Polarity'].apply(get_analysis)
    sentiment = get_analysis(get_polarity(tweet))
    return sentiment


if __name__ == "__main__":
    print(sentiment_analysis("Now is better than never"))
