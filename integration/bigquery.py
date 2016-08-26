#!/usr/bin/env python

"""
This script loads streams data into BigQuery tables using the google python SDK.
Google Cloud Storage or Google BigQuery are both valid endpoints which can be used in this file.
"""
import secrets

import uuid
import os

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError


def get_authenticated_service():
    try:

        # Grab the application's default credentials from the environment.
        credentials = ServiceAccountCredentials.from_p12_keyfile(secrets.SERVICE_ACCOUNT_EMAIL, secrets.KEY_FILE)

        # Construct the service object for interacting with the BigQuery API.
        return build('bigquery', 'v2', credentials=credentials)

    except HttpError as err:
        print('Error: {}'.format(err.content))
        raise err

    except TypeError as error:
        # Handle errors in constructing a query.
        print('There was an error in constructing your query : %s' % error)

    except AccessTokenRefreshError as error:
        print error
        # Handle Auth errors.
        print ('The credentials have been revoked or expired, please re-run '
               'the application to re-authorize')


def create_bigquery_table(dataset_id, table_name, schema):
    try:
        os.system('bq mk --schema {} -t {}:{}.{}'.format(schema, secrets.PROJECT_ID, dataset_id, table_name))
        return 'Table creation successful'
    except OSError, error:
        return error


def stream_row_to_bigquery(table_name, row, num_retries=5, dataset_id='zwennes'):

    insert_all_data = {
        'rows': [{
            'json': row,
            'insertId': str(uuid.uuid4()),
        }]
    }
    bigquery = get_authenticated_service()
    try:
        return bigquery.tabledata().insertAll(
            projectId=secrets.PROJECT_ID,
            datasetId=dataset_id,
            tableId=table_name,
            body=insert_all_data).execute(num_retries=num_retries)
    except HttpError, http_error:
        print http_error
    except Exception, general_error:
        print general_error
