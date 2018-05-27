#!/usr/bin/python
""" Download the phishing reply addresses file, then
generate a Postfix phishing disallowed recipients hash map. """

from __future__ import absolute_import, print_function
from datetime import datetime, timedelta
from os import rename, system
try:  # Python 3 and newer only
    from urllib.error import URLError
    from urllib.request import Request, urlopen
except ImportError:  # Python 2.7 and older
    from urllib2 import Request, urlopen, URLError

# main
ADDRESSES_URL = 'https://svn.code.sf.net/p/aper/code/phishing_reply_addresses'
#REJECT_MAP_FILE = './phishing_disallowed_recipients'
REJECT_MAP_FILE = '/etc/postfix/phishing_disallowed_recipients'
POSTMAP = '/usr/sbin/postmap'
ADDRESSES = set()
# how far back do we care?
CUTOFF = (datetime.today() - timedelta(days=30)).date()

# first, make sure we can open the url
try:
    REQUEST = Request(ADDRESSES_URL)
    RESPONSE = urlopen(REQUEST)
except URLError as err:
    print('failed to open url ', ADDRESSES_URL)
    print('reason: ', err)
    exit()

# ok, try to make a BACKUP file
try:
    BACKUP = REJECT_MAP_FILE + '.bak'
    rename(REJECT_MAP_FILE, BACKUP)
except OSError as err:
    print(err)

# open eap file for writing
try:
    MAPFILE = open(REJECT_MAP_FILE, 'wb')
except IOError as err:
    print(err)
    exit()

# iterate through the address file and build a Postfix map
for line in RESPONSE:
    if line.startswith(b'#'):
        continue  # Skip comment lines
    address, code, datestamp = line.split(b',')
    if address == '' or datestamp is None:
        continue  # Skip blank/empty lines
    try:
        DATE = datetime.strptime(datestamp.rstrip().decode('utf-8'),
                                 '%Y%m%d').date()
        if DATE > CUTOFF:
            ADDRESSES.add(address)
    except ValueError as err:
        print(err)
        continue  # Skip malformed lines

for entry in sorted(ADDRESSES):
    MAPFILE.write(entry)
    MAPFILE.write(b'\t REJECT\n')
MAPFILE.close()

# call postmap on it
system(POSTMAP + ' ' + REJECT_MAP_FILE)

exit()
