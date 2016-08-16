#!/usr/bin/env python

"""
This script is used to retrieve the most active tweets by location. We can use this data to find out how much
the tags are used in other social media platforms.
"""
import secrets

import pandas as pd
from pandas.io.json import json_normalize

from tweepy import OAuthHandler
from tweepy import API, Cursor


def get_latest_twitter_trends(country_or_city_id=23424909):
    """
    The whoid can be found using the following url: http://woeid.rosselliot.co.nz/
    Netherlands (23424909) is used as a default
    :param country_or_city_id: whoid of the city or country to find the most relevant tags
    :return: name of the most popular tags
    """
    auth = OAuthHandler(secrets.TWEET_CONSUMER_KEY, secrets.TWEET_CONSUMER_SECRET)
    auth.set_access_token(secrets.TWEET_ACCESS_TOKEN, secrets.TWEET_TOKEN_SECRET)
    api = API(auth)
    trend_information = api.trends_place(country_or_city_id)[0]['trends']

    tag_list = []
    df_tags = json_normalize(trend_information)
    tag_list.append(df_tags)

    return pd.DataFrame().append(tag_list)


def get_twitter_messages(subject, since, until, limit=5000):
    """
    Get a list of tweets and some information about the user who tweeted it.
    :param subject: text-string to search for
    :param since: start collecting tweets from this date (max = 2 weeks ago)
    :param until: only collect tweets before this date
    :param limit: amount of tweets to return (max = ???) # check the rate limit docs
    :return: a python dictionary with tweets organised by tweet_id
    """
    results = []
    auth = OAuthHandler(secrets.TWEET_CONSUMER_KEY, secrets.TWEET_CONSUMER_SECRET)
    auth.set_access_token(secrets.TWEET_ACCESS_TOKEN, secrets.TWEET_TOKEN_SECRET)
    api = API(auth)
    for tweet in Cursor(api.search, q=subject, since=since, until=until, lang="nl").items(limit):
        results.append(tweet)

    # define the dataset
    df = pd.DataFrame()

    df['tweetID'] = [tweet.id for tweet in results]
    df['tweetText'] = [tweet.text for tweet in results]
    df['tweetRetweetCount'] = [tweet.retweet_count for tweet in results]
    df['tweetFavoriteCount'] = [tweet.favorite_count for tweet in results]
    df['tweetSource'] = [tweet.source for tweet in results]
    df['tweetCreated'] = [tweet.created_at for tweet in results]
    df['userID'] = [tweet.user.id for tweet in results]
    df['userScreen'] = [tweet.user.screen_name for tweet in results]
    df['userName'] = [tweet.user.name for tweet in results]
    df['userCreateDt'] = [tweet.user.created_at for tweet in results]
    df['userDescription'] = [tweet.user.description for tweet in results]
    df['userFollowerCount'] = [tweet.user.followers_count for tweet in results]
    df['userFriendsCount'] = [tweet.user.friends_count for tweet in results]
    df['userLocation'] = [tweet.user.location for tweet in results]

    return df
