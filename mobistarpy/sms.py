# -*- coding: utf-8 -*

import requests
import re

from phonenumber import PhoneNumber

APP_ID = "5945678226665077779"


def _request(content):
    URL = "https://orangeuk.msgsend.com/mmpNG/ws_xml.html"
    HEADERS = {'Content-Type': 'application/xml'}
    return requests.post(URL, headers=HEADERS, data=content)


def _extract_message(response_text):
    match = re.search(
        r'<message><\!\[CDATA\[(.+)\]\]></message>',
        response_text
    )
    assert match
    return match.group(1).strip()


def auth(number, get_pin_callback=raw_input):
    """
    Return an authorization key for a phone number.
    The get_pin_callback should return the access code sent by SMS.
    """
    number = PhoneNumber(number)
    assert number.is_belgian_gsm()

    # 1. Register
    query = '<register appId="%s" phoneNumber="%s"/>' % (APP_ID, str(number))
    response = _request(query)
    assert '<result code="100">' in response.content

    # 2. Confirmation code
    pin_code = get_pin_callback("Confirmation code (SMS sent to %s) ? " % (
        repr(number)
    ))
    query = ''.join((
        '<sendRegistrationCode ',
        'appId="%s" ' % (APP_ID),
        'phoneNumber="%s" ' % (number),
        'code="%s"/>' % (pin_code)
    ))
    response = _request(query)
    assert '<result code="100">' in response.content
    return _extract_message(response.content)


def send_sms(token, message, recipient):
    number = PhoneNumber(recipient)
    assert number.is_belgian_gsm()

    query = ''.join((
        '<sendSMS appId="%s">' % (APP_ID),
        '<key>%s</key>' % (token),
        '<text><![CDATA[%s]]></text>' % (message),
        '<phoneNumber>%s</phoneNumber>' % (str(number)),
        '</sendSMS>'
    ))
    response = _request(query)
    assert '<result code="100">' in response.content
    return _extract_message(response.content)
