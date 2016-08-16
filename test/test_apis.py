#!/usr/bin/env python

import pprint

from twitter_api import twitter_batch
from twitter_api import twitter_stream
from instagram_api import instagram
from integration import bigquery
from google_api import machine_learning as gml


pp = pprint.PrettyPrinter(indent=4)

# twitter_trends = twitter_batch.get_latest_twitter_trends(country_or_city_id=23424977)
# pp.pprint(twitter_trends)

# tweets_by_trend = twitter_batch.get_twitter_messages('QuitYourJobIn5Words', 1)
# pp.pprint(tweets_by_trend)

# instagram_media_count = instagram.retrieve_tag_media_count('WorldLionDay')
# pp.pprint(instagram_media_count)

# instagram_media = instagram.get_recent_media('WorldLionDay')
# pp.pprint(instagram_media)

# amsterdam = twitter_batch.get_twitter_messages(subject='amsterdam', since='2016-08-09', until='2016-08-10', limit=10)
# pp.pprint(amsterdam.head(10))

# print bigquery.create_bigquery_table('zwennes', 'beer_tweets', 'schema.json')

stream = twitter_stream.create_twitter_stream(
    keyword_list=['clinton', 'trump'],
    language_list=['en'],
    runtime_in_seconds=1800,
    gbq_table='tweets'
)

