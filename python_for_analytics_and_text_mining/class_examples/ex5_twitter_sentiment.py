from TwitterSearch import *

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

import pandas as pd
from pandas import ExcelWriter

tweet_dict = {}

try:
    tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
    tso.set_keywords(['Hillary', 'Trump'])  # let's define all words we would like to have a look for
    tso.set_language('en')  # we want to see English tweets only
    tso.set_include_entities(True)  # and don't give us all those entity information


    # Please create a Twitter app key here https://apps.twitter.com
    ts = TwitterSearch(
        consumer_key='XXXXXXXXXX',
        consumer_secret='XXXXXXXXXXX',
        access_token='XXXXXXXXXXX',
        access_token_secret='XXXXXXXXXXXX'
    )

    count = 1
    # iterate through the tweets
    for tweet in ts.search_tweets_iterable(tso):
        #print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

        blob = TextBlob(tweet['text'], analyzer=NaiveBayesAnalyzer())
        #print (tweet['text'])
        #print (blob.sentiment)
        tweet_dict[count] = [str(tweet['id']), tweet['user']['screen_name'], tweet['text'], blob.sentiment[0]]
        print (tweet_dict[count])
        count = count + 1

    #print (tweet_dict)
    df = pd.DataFrame.from_dict(tweet_dict, orient='index')
    df.rename(columns={0: 'TweetID'}, inplace=True)
    df.rename(columns={1: 'User'}, inplace=True)
    df.rename(columns={2: 'Tweet'}, inplace=True)
    df.rename(columns={3: 'Sentiment'}, inplace=True)

    print (df)

except TwitterSearchException as e:  # take care of all those errors
    print(e)

#save to xls

writer = ExcelWriter('tweets_sentiment.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()
