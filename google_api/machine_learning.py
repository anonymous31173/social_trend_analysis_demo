"""Google Cloud Speech API sample application using the REST API for batch
processing."""

import secrets
import base64
import httplib2

from pydub import AudioSegment
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


def get_credentials():
    """
    Retrieves the Google Cloud credentials to connect with the services
    :return: a authenticated HTTP credential
    """
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    return credentials.authorize(http)


def format_to_flac(wav_file, current_format):
    """
    Transforms a wave file to a format valid for the Speech API
    Currently this is FLAC format because its a best practise
    :param wav_file: path/to/the/audio.wav / mp3
    :param current_format: audio format of the input audio file
    :return: the name of the newly created FLAC file
    """
    raw_flac_name = wav_file.replace(current_format.lower(), 'wav')
    song = AudioSegment.from_file(wav_file, sample_width=2)

    try:
        song.export(raw_flac_name, format='wav')
        return raw_flac_name
    except ReferenceError, err:
        print(err)


def speech_to_text(speech_file, audio_format):
    """
    Transcribe the given audio file.

    :param speech_file: the name of the audio file.
    :param audio_format: audio format of the input file (WAV, MP3)
    :return: result of the speech to text API in JSON format
    """
    raw_flac_file = format_to_flac(speech_file, audio_format)
    with open(raw_flac_file, 'rb') as speech:
        speech_content = base64.b64encode(speech.read())

    service = discovery.build('speech', 'v1beta1', http=get_credentials(), discoveryServiceUrl=DISCOVERY_URL)

    # if audio file length is > 1 min use reference to file instead of the decoded UTF-8
    # this file needs to be on cloud storage and asyncrecognize should be used together with the LINEAR16 format
    # content needs to be changed in uri
    service_request = service.speech().syncrecognize(
        body={
            'config': {
                'encoding': 'LINEAR16',
                'sampleRate': 48000,
                'languageCode': 'nl-NL',
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
            }
        })
    response = service_request.execute()
    print response
    translation = response['results'][0]['alternatives'][0]['transcript']
    confidence = response['results'][0]['alternatives'][0]['confidence']
    return translation, confidence


def translate_text(text_to_translate, source_lang, target_lang):
    """
    Build the Speech to Text Google API service object
    :param text_to_translate: text to translate in string format
    :param source_lang: language to translate from
    :param target_lang: language to translate to
    :return: a valid connection object for the speech API
    """

    service = discovery.build('translate', 'v2', developerKey=secrets.GOOGLE_API_KEY)
    translation_call = service.translations().list(
        source=source_lang,
        target=target_lang,
        q=text_to_translate
    ).execute()
    return translation_call['translations'][0]['translatedText']


def analyze_sentiment(text):
    """
    Calls the Natural Language API to retrieve the sentiment of a given text
    :param text: String of text
    :return: the polarity of the text (happiness), and the magnitude (confidence)
    """
    service = discovery.build('language', 'v1beta1', http=get_credentials(), discoveryServiceUrl=DISCOVERY_URL)

    # retrieve the syntactic text annotation
    try:
        syntactic_call = service.documents().annotateText(
            body={
                'document': {
                    'type': 'PLAIN_TEXT',
                    'content': text
                },
                'features': {
                  "extractSyntax": False,
                  "extractEntities": False,
                  "extractDocumentSentiment": True
                }
            }
        )
        return syntactic_call.execute()['documentSentiment']
    except Exception, err:
        return {'polarity': '', 'magnitude': ''}
