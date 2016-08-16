#!/usr/bin/env python

"""
This script starts a Twitter stream which runs for a specified amount of time and collects all tweets
that contain one ore more keywords that are given as input.

"""
import secrets
from integration import bigquery
from google_api import machine_learning as gml

import time
import json

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


class Listener(StreamListener):

    def __init__(self, start_time, time_limit, table, track):

        super(Listener, self).__init__()
        self.time = start_time
        self.limit = time_limit
        self.table = table
        self.keyword_list = track

    def on_data(self, data):
        while (time.time() - self.time) < self.limit:
            try:
                tweet = json.loads(data)
                sentiment = gml.analyze_sentiment(tweet['text'])
                keyword = None
                for word in self.keyword_list:
                    if word in tweet['text'].lower():
                        keyword = word

                data = {
                    'keyword': keyword,
                    'created_at': tweet['created_at'],
                    'id': tweet['id'],
                    'text': tweet['text'],
                    'user_id': tweet['user']['id'],
                    'user_name': tweet['user']['name'],
                    'user_location': tweet['user']['location'],
                    'user_screen_name': tweet['user']['screen_name'],
                    'user_friends_count': tweet['user']['friends_count'],
                    'user_followers_count': tweet['user']['followers_count'],
                    'user_listed_count': tweet['user']['listed_count'],
                    'user_favourites_count': tweet['user']['favourites_count'],
                    'user_statuses_count': tweet['user']['statuses_count'],
                    'sentiment_polarity': sentiment['polarity'],
                    'sentiment_magnitude': sentiment['magnitude']
                }
                print bigquery.stream_row_to_bigquery(self.table, data)
                return True

            except BaseException, e:
                print('failed to retrieve: ,', str(e))
                time.sleep(5)
                pass

        exit()

    def on_error(self, status):
        print(status)


def create_twitter_stream(keyword_list, language_list, runtime_in_seconds, gbq_table):
    """
    This script uses the Listener class to set up a Twitter Stream for a x amount of seconds
     based on the input values. The data is stored in a JSON file which is transferred to Cloud Storage or BigQuery.
    :param keyword_list: list of keywords to start the Twitter stream with (List)
    :param language_list: list of languages to include in the search (List)
    :param runtime_in_seconds: amount of seconds to run the stream
    :param gbq_table: name of the Google BigQuery table
    :return: status message to evaluate the status of the stream
    """
    auth = OAuthHandler(secrets.TWEET_CONSUMER_KEY, secrets.TWEET_CONSUMER_SECRET)
    auth.set_access_token(secrets.TWEET_ACCESS_TOKEN, secrets.TWEET_TOKEN_SECRET)

    while True:
        try:
            twitter_stream = Stream(auth,
                Listener(start_time=time.time(), time_limit=runtime_in_seconds, table=gbq_table, track=keyword_list)
            )
            twitter_stream.filter(track=keyword_list, languages=language_list, stall_warnings=False)

        except KeyboardInterrupt:
            break
        except Exception, e:
            continue
