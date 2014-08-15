#!/usr/bin/env python
# -*- coding: utf-8 -*

from os import path, environ as ENV
from sys import argv
from mobistarpy.sms import send_sms, auth

if len(argv) < 3:
    print "USAGE: %s NUMBER MESSAGE..." % (path.basename(argv[0]))
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
