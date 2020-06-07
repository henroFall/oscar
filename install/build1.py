#!/usr/bin/env python
"""Initial setup script for Oscar. Run it on the device where Oscar will be running.
modified by H from the original at https://github.com/danslimmon/oscar"""

import os
import sys
import subprocess
import re

######################################## Digit-Eyes
print "You need accounts with a few APIs to use Oscar. First of all,"
print "go to"
print
print "    http://www.digit-eyes.com"
print
print "and sign up for an account there. This is the database that Oscar uses to"
print "match barcodes with names of products. When you're ready, enter your"
print "API credentials. They can be found on the \"My Account\" page."
print 
print "Want to use openfoodfacts.org? Customise /etc/oscar.yaml to set the barcode_api to 'openfoodfacts'"
print
digiteyes_app_key = raw_input('App Key ("K" Code): ')
digiteyes_auth_key = raw_input('Authorization Key ("M" Code): ')


######################################## Trello
trello_app_key = '95be613d21fcfa29f3580cc3ea4314cf'
print
print "You'll also need a Trello account. You can sign up at:"
print
print "    https://trello.com"
print
print "Once you have an account, go to this URL:"
print
print "    https://trello.com/1/authorize?key={0}&name=oscar&expiration=never&response_type=token&scope=read,write".format(trello_app_key)
print
print "You'll be shown a 'token'; enter it below."
print
trello_token = raw_input('Token: ')
print
print "Alright, now, we haven't yet found a way to create boards via the Trello"
print "API, so would you go ahead and create two Trello boards?"
print
print "First create a board called 'Groceries', and enter its URL here:"
print
trello_grocery_board_url = raw_input('Grocery Board URL: ')
print
print "And now create a board called 'oscar_db', and enter its URL here:"
print
trello_db_board_url = raw_input('Trello DB board URL: ')

# Get the board IDs from their URLs
m = re.search('/b/([^/]+)', trello_grocery_board_url)
trello_grocery_board = m.group(1)
m = re.search('/b/([^/]+)', trello_db_board_url)
trello_db_board = m.group(1)
trello_grocery_list = 'Groceries'

######################################## Communication
print
print "Oscar can email or text you when it scans something it doesn't recognize. This"
print "gives you the opportunity to teach Oscar about items you frequently buy."
print "Please choose whether you want oscar to email or text you by typing 'email' or 'text'."
print
communication_method = raw_input("Communication method ('email' or 'text'): ")
while communication_method not in ['email', 'text']:
    communication_method = raw_input("Please input 'email' or 'text': ")

gmail_user = ''
gmail_password = ''
email_dest = ''
twilio_src = ''
twilio_sid = ''
twilio_token = ''
twilio_dest = ''
if communication_method == 'email':
    ######################################## Email
    print
    print "To enable this functionality using email as the communication method, "
    print "you need an account with GMail:"
    print
    print "    https://mail.google.com/"
    print
    print "If you want to, you can sign up for a GMail account and enter your"
    print "information below. If not, no sweat: just leave the input blank. You"
    print "can always come back and modify Oscar's config file later."
    print
    gmail_user = raw_input('GMail Email Address: ')
    if gmail_user != '':
        gmail_password = raw_input('GMail Password: ')
        email_dest = raw_input('Destination email (the address you want emailed): ')
    else:
        gmail_password = ''
        email_dest = ''
else:
    ######################################## Twilio
    print
    print "To enable this functionality using text as the communication method, "
    print "you need an account with Twilio:"
    print
    print "    https://www.twilio.com/"
    print
    print "If you want to, you can sign up for a Twilio account and enter your"
    print "information below. If not, no sweat: just leave the input blank. You"
    print "can always come back and modify Oscar's config file later."
    print
    twilio_src = raw_input('Twilio number: ')
    if twilio_src != '':
        twilio_sid = raw_input('Twilio SID: ')
        twilio_token = raw_input('Twilio token: ')
        twilio_dest = raw_input('Destination number (the number you want texted): ')
    else:
        twilio_sid = ''
        twilio_token = ''
        twilio_dest = ''
    # Remove any non-digits from phone numbers
    twilio_src = re.sub('\D', '', twilio_src)
    twilio_dest = re.sub('\D', '', twilio_dest)

