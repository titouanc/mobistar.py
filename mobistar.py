#!/usr/bin/env python
# -*- coding: utf-8 -*

import requests
import re

APP_ID = "5945678226665077779" 

def _mobistar_request(content):
    URL = "https://orangeuk.msgsend.com/mmpNG/ws_xml.html"
    HEADERS = {'Content-Type': 'application/xml'}
    return requests.post(URL, headers=HEADERS, data=content)

def _mobistar_extract_message(response_text):
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
    assert re.match(r'^\+32\d{9}$', number)

    # 1. Register
    query = '<register appId="%s" phoneNumber="%s"/>' % (APP_ID, number)
    response = _mobistar_request(query)
    assert '<result code="100">' in response.content
    
    # 2. Confirmation code
    pin_code = get_pin_callback("Confirmation code (wait for SMS…) ? ")
    query = ''.join((
        '<sendRegistrationCode ',
        'appId="%s" ' % (APP_ID),
        'phoneNumber="%s" ' % (number),
        'code="%s"/>' % (pin_code)
    ))
    response = _mobistar_request(query)
    assert '<result code="100">' in response.content 
    return _mobistar_extract_message(response.content)   

def send_sms(token, message, recipient):
    assert re.match(r'^\+32\d{9}$', recipient)
    query = ''.join((
        '<sendSMS appId=%s>' % (APP_ID),
        '<key>%s</key>' % (token),
        '<text>%s</text>' % (message),
        '<phoneNumber>%s</phoneNumber>' % (recipient),
        '</sendSMS>'
    ))
    response = _mobistar_request(query)
    assert '<result code="100">' in response.content
    return _mobistar_extract_message(response.content)

if __name__ == "__main__":
    from os import environ as ENV
    from sys import argv

    if len(argv) < 3:
        print "USAGE: sms NUMBER MESSAGE..."
        exit()

    token_file = ENV['HOME']+'/.mobistar_token'
    try:
        token = open(token_file).read().strip()
    except:
        number = raw_input("Your phone number ? ")
        token = auth(number, raw_input)
        open(token_file, 'w').write(token)

    dest = argv[1]
    if dest[0] == '0':
        dest = '+32' + dest[1:]
    msg = " ".join(argv[2:])
    send_sms(token, msg, dest)
    print "SMS sent"
