#!/usr/bin/env python
"""Second setup script for Oscar. Called by sh.
modified by H from the original at https://github.com/danslimmon/oscar"""

######################################## Scanner
import os
import sys
import subprocess
import re

usb_port=sys.argv[1]
print usb_port
scanner_device = usb_port
if scanner_device == '':
    scanner_device = '/dev/input/event0'

######################################## Create the appropriate Trello lists
import trello
trello_api = trello.TrelloApi(trello_app_key)
trello_api.set_token(trello_token)
# Grocery list
trello_api.boards.new_list(trello_grocery_board, 'Groceries')
# oscar_db lists
for db_list in ['description_rules', 'barcode_rules', 'learning_opportunities']:
    trello_api.boards.new_list(trello_db_board, db_list)

######################################## Create the default description rules
new_rules = [
    {'search_term': 'coffee', 'item': 'coffee'},
    {'search_term': 'soymilk', 'item': 'soy milk'},
    {'search_term': 'soy milk', 'item': 'soy milk'},
    {'search_term': 'soy sauce', 'item': 'soy sauce'},
    {'search_term': 'beer', 'item': 'beer'},
    {'search_term': 'ale', 'item': 'beer'},
    {'search_term': 'sriracha', 'item': 'sriracha'},
    {'search_term': 'milk', 'item': 'milk'},
    {'search_term': 'olive oil', 'item': 'olive oil'},
    {'search_term': 'cereal', 'item': 'cereal'},
    {'search_term': 'peanut butter', 'item': 'peanut butter'},
    {'search_term': 'ketchup', 'item': 'ketchup'},
    {'search_term': 'baking powder', 'item': 'baking powder'},
    {'search_term': 'yeast', 'item': 'yeast'},
    {'search_term': 'baking soda', 'item': 'soda'},
    {'search_term': 'beans', 'item': 'beans'},
    {'search_term': 'bread crumbs', 'item': 'bread crumbs'},
    {'search_term': 'broth', 'item': 'broth'},
    {'search_term': 'cereal', 'item': 'cereal'},
    {'search_term': 'chocolate', 'item': 'chocolate'},
    {'search_term': 'cooking spray', 'item': 'cooking spray'},
    {'search_term': 'cornmeal', 'item': 'cornmeal'},
    {'search_term': 'cornstarch', 'item': 'cornstarch'},
    {'search_term': 'crackers', 'item': 'crackers'},
    {'search_term': 'raisins', 'item': 'raisins'},
    {'search_term': 'vanilla extract', 'item': 'vanilla extract'},
    {'search_term': 'flour', 'item': 'flour'},
    {'search_term': 'mayo', 'item': 'mayo'},
    {'search_term': 'garlic', 'item': 'garlic'},
    {'search_term': 'pasta', 'item': 'pasta'},
    {'search_term': 'bacon', 'item': 'bacon'},
    {'search_term': 'bread', 'item': 'bread'},
    {'search_term': 'potatoes', 'item': 'potatoes'},
    {'search_term': 'rice', 'item': 'rice'},
    {'search_term': 'soup', 'item': 'soup'},
    {'search_term': 'sugar', 'item': 'sugar'},
    {'search_term': 'tea', 'item': 'tea'},
    {'search_term': 'tuna', 'item': 'tuna'},
    {'search_term': 'evaporated milk', 'item': 'evaporated milk'},
    {'search_term': 'vinegar', 'item': 'vinegar'},
    {'search_term': 'eggs', 'item': 'eggs'},
    {'search_term': 'chips', 'item': 'chips'},
]
os.chdir('/var/oscar')
from lib import trellodb
trello_db = trellodb.TrelloDB(trello_api, trello_db_board)
for rule in new_rules:
    trello_db.insert('description_rules', rule)

######################################## Oscar configs

oscar_yaml = open('/etc/oscar.yaml', 'w')
oscar_yaml.write('''---
port: 79
scanner_device: '{scanner_device}'

communication_method: '{communication_method}'

gmail_user: '{gmail_user}'
gmail_password: '{gmail_password}'
email_dest: '{email_dest}'

twilio_src: '{twilio_src}'
twilio_dest: '{twilio_dest}'
twilio_sid: '{twilio_sid}'
twilio_token: '{twilio_token}'

trello_app_key: '{trello_app_key}'
trello_token: '{trello_token}'
trello_grocery_board: '{trello_grocery_board}'
trello_grocery_list: '{trello_grocery_list}'
trello_db_board: '{trello_db_board}'

digiteyes_app_key: '{digiteyes_app_key}'
digiteyes_auth_key: '{digiteyes_auth_key}'

# possible values: 'digiteyes', 'openfoodfacts' or 'zeroapi'
barcode_api: digiteyes
'''.format(**locals()))
oscar_yaml.close()

sup_oscar_scan = open('/etc/supervisor/conf.d/oscar_scan.conf', 'w')
sup_oscar_scan.write('''[program:oscar_scan]

command=python /var/oscar/scan.py
stdout_logfile=/var/log/supervisor/oscar_scan.log
redirect_stderr=true''')
sup_oscar_scan.close()

sup_oscar_web = open('/etc/supervisor/conf.d/oscar_web.conf', 'w')
sup_oscar_web.write('''[program:oscar_web]

command=/usr/local/bin/node --inspect /var/oscar/web/app.js
directory=/var/oscar/web
stdout_logfile=/var/log/supervisor/oscar_web.log
redirect_stderr=true''')
sup_oscar_web.close()

print
print '############################################################'
print
print 'Done! Your new grocery list can be found at:'
print
print '    {0}'.format(trello_grocery_board_url)
print
print 'If everything worked, then you should be able to start scanning'
print 'barcodes with oscar. Check out the logs of the scanner process and'
print 'the web app, respectively, at'
print
print '    /var/lib/supervisor/log/oscar_scan.log'
print '    /var/lib/supervisor/log/oscar_web.log'
print
print 'And report any bugs at https://github.com/henrofall/oscar/issues.'
print 'Oscar 0.1.1 was modified by H from the original danslimmon/oscar.'
print 'All credit to danslimmon. All I did was hack it up to make it'
print 'work again on Raspberian and hopefully support more Linux OSes.'
print
print 'To add new product description keywords, the current method is to'
print 'edit the oscar_db board directly.'
