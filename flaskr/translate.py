# coding=utf-8
"""
translation app
"""
import json
import requests
from flask_babel import _
from flaskr import app


def translate(text, source_language, dest_language):
    """
    allow users to translate posts into their native language
    :param text: original text from _() and _l() functions
    :param source_language: origin language
    :param dest_language: final language
    :return: translated text in string
    """
    if 'MS_TRANSLATOR_KEY' not in app.config or not app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured')
    auth = {'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY']}
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc/Translate?text={}&from={}&to={}'.format(
        text, source_language, dest_language
    ), headers=auth)
    if r.status_code is not 200:
        return _("Error: the translation service failed.")
    return json.loads(r.content.decode('utf-8-sig'))
