#!/usr/bin/env python

"""This script retrieves trend information such as tags from the Instagram API.
The access token and client secret can be found here: https://www.instagram.com/developer/
"""
import secrets

import requests
from pandas.io.json import json_normalize
import pandas as pd


def retrieve_tag_media_count(tag):
    """
    Get relevant tags for the given search query
    :param tag: name of the tag to search for
    :return: pandas dataFrame containing the media count and the name of the tag
    """
    base_url = "https://api.instagram.com/v1"

    tag_list = []
    tags_search = "{0}/tags/search?q={1}&access_token={2}".format(base_url, tag, secrets.INSTA_ACCESS_TOKEN)
    tags = requests.get(tags_search).json()

    try:
        df_tags = json_normalize(tags['data'])
        tag_list.append(df_tags)
        df = pd.DataFrame().append(tag_list)
    except IndexError, error:
        print error
        df = pd.DataFrame()
    return df


def get_recent_media(tag):
    """
    Get the recent media for a given tag (does not work in sandbox mode)
    :param tag: name of the Instagram tag
    :return: pandas dataFrame containing ...
    """
    base_url = "https://api.instagram.com/v1"

    media_list = []
    url = '{0}/tags/{1}/media/recent?access_token={2}&count=20&min_tag_id={3}'.format(
        base_url, tag, secrets.INSTA_ACCESS_TOKEN, '0')
    media = requests.get(url).json()
    print media
    if 'data' in media:
        df_instance = json_normalize(media['data'])
        media_list.append(df_instance)
    df = pd.DataFrame().append(media_list)

    df_cols = df[['comments.count', 'likes.count']]
    df_clean = df_cols.rename(columns=lambda x: x.replace('.', ' ').title())

    return df_clean

