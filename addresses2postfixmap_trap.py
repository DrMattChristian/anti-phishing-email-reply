#!/usr/bin/python
#************************************************************************ #
# addresses2postfixmap_trap.py
# 7/9/2008; tmg
# 7/10/2008; tmg
# 7/31/2008; zhs
# 8/5/2008; tmg
# 8/21/2008; tmg
#************************************************************************ #
#
'''phish_add -- Reads email addresses or files of email addresses and adds
them to the virtual domain file on the TAMU relays, in order to trap replies
to those addresses that pass through the relays.

Can parse the community file at:
https://svn.code.sf.net/p/aper/code/phishing_reply_addresses
'''

from __future__ import absolute_import, print_function
try:
    from subprocess import getstatusoutput
except ImportError:
    from commands import getstatusoutput
from getopt import getopt, GetoptError
import os
import re
try:  # Python 3 and newer only
    from urllib.request import urlopen
except ImportError:  # Python 2.7 and older
    from urllib2 import urlopen


def output_read(fname):
    """Open fname, read all the lines and write to list, returned."""
    wx_l = []
    filed = open(fname, 'r')
    lines = filed.readlines()
    filed.close()

    for line in lines:
        cur_addr = line.strip().split()[0].lower()
        if cur_addr:
            wx_l.append(cur_addr)

    return wx_l


def source_read(fname, verbose):
    """Read source from fname/URL and write into list, return."""
    wx_l = []
    addr_match = re.compile(r'^[\w][\w.-]*@[\w.-]+.(\w){2,4}').match

    if fname[:4] == 'http':
        filed = urlopen(fname)
        lines = filed.read()
        filed.close()
        lines = lines.split('\n')
    else:
        filed = open(fname, 'r')
        lines = filed.readlines()
        filed.close()

    for line in lines:
        if not line or line[0] == '#':
            continue
        new_address = line.strip().split(',')[0].lower()
        if new_address and addr_match(new_address):
            wx_l.append(new_address)
        elif verbose:
            print("Didn't match **%s**" % (new_address))

    return wx_l


def regex_write(new_l, out_file, verbose):
    """Write out a phisher header_check regex file for Postfix."""
    # An address for quarantined suspect senders; Could just as easily "DISCARD"
    #  or "REJECT"
    wx_str = '/(From:|Reply-To:).*%s/    REDIRECT phish-quarantine@ourdomain.edu\n'
    wx_l = []
    if verbose:
        print("Building header_check file")
    for address in new_l:
        wx_l.append(wx_str % (address))

    try:
        if verbose:
            print("Writing phisher header_check file")
        filed = open(out_file, 'w')
        for line in wx_l:
            filed.writelines(line)
        filed.close()
        results = True
    except IOError as err:
        print("Couldn't write regex!")
        print(err)
        results = False

    return results


def addr_merge(dest_l, new_l, verbose):
    """Merge two address lists together."""
    tmp_l = dest_l[:]
    if verbose:
        print("Merging %i addresses into %i existing addresses" % (len(new_l), len(dest_l)))
    for addr in new_l:
        if addr not in tmp_l:
            tmp_l.append(addr)
        elif verbose:
            print("Already listing %s" % (addr))

    tmp_l.sort()

    return tmp_l


def addr_write(f_name, addr_l):
    """Write address out to file."""
    try:
        tmp_name = f_name + '.prev'
        if os.path.isfile(tmp_name):
            os.remove(tmp_name)
        os.rename(f_name, tmp_name)
        filed = open(f_name, 'w')
    except OSError:
        print("Error! Can't open %s for writing." % (f_name))
        return False

    for elem in addr_l:
        # An address to trap outbound replies
        outline = '%s\tphish-reply-trap@ourdomain.edu\n' % (elem)
        filed.writelines(outline)

    filed.close()

    return True


def main(new_address, verbose, is_file=False, output=None):  # pylint: disable=too-many-branches
    """Write address to phishing trap files for Postfix."""
    if not output:
        output = '/etc/postfix/virtual_trap'
    regex_out = '/etc/postfix/phish_headers.regex'

    cur_addr_l = output_read(output)
    len_1 = len(cur_addr_l)

    if is_file:
        if new_address[:4] == 'http' or os.path.isfile(new_address):
            new_address_l = source_read(new_address, verbose)
        else:
            print("Couldn't find input file %s" % (new_address))
            exit(1)
    else:
        new_address_l = [new_address.split(',')[0]]

    new_address_l = addr_merge(cur_addr_l, new_address_l, verbose)
    len_2 = len(new_address_l)

    if len_1 == len_2:
        if verbose:
            print("No changes to the address list. Exiting now.")
        return 0
    else:
        update = addr_write(output, new_address_l)
        if update:
            status, output = getstatusoutput('/usr/sbin/postmap hash:%s' % output)
            if status != 0:
                print(output)
            else:
                print("Updated %s" % output)
            #TAMU mail is hosted in a load-balanced cluster. "config_sync.py" sync's
            # configuration files across the cluster.
            #status, output = getstatusoutput('/usr/local/sbin/config_sync.py %s' % output)
            #if status != 0:
            #    print(output)
            #else:
            #    print("Synched %s" % output)

            regex_res = regex_write(new_address_l, regex_out, verbose)
            if regex_res:
                # TAMU mail is hosted in a load-balanced cluster. "config_sync.py" sync's
                #  configuration files across the cluster.
                #status, output = getstatusoutput('/usr/local/sbin/config_sync.py %s' % regex_out)
                #if status != 0:
                #    print(output)
                #else:
                #    print("Updated and synched %s" % regex_out)
                print("Updated %s" % regex_out)
            else:
                print("Failed to update %s" % regex_out)
                return 3
            return 0
        else:
            return 2

if __name__ == '__main__':
    USAGE = '''addresses2postfixmap_trap.py -f <address_file> | -a <address> [ -o <output_file> ] [ -v ]

    Updates addresses in a virtual maps file, then synch's the new file between
    mail relays.
    Specify an address file of 'remote' to fetch the current list from SF SVN.'''

    REMOTE_URL = 'https://svn.code.sf.net/p/aper/code/phishing_reply_addresses'

    if len(os.sys.argv) < 2:
        print(USAGE)
        exit(1)
    else:
        try:
            OPTLIST, ARGS = getopt(os.sys.argv[1:], 'f:a:o:v', ['file-name', 'address',
                                                                'output-file', 'verbose'])
        except GetoptError as err:
            print(err)
            print(USAGE)
            exit(1)

    OUTPUT_FILE = ''
    INPUT_FILE = ''
    NEW_ADDR = ''
    VERBOSE = False

    for flag, value in OPTLIST:
        if flag in ('-f', '--file-name'):
            INPUT_FILE = value
            if INPUT_FILE == 'remote':
                INPUT_FILE = REMOTE_URL
        if flag in ('-a', '--address'):
            NEW_ADDR = value
        if flag in ('-o', '--output-file'):
            OUTPUT_FILE = value
        if flag in ('-v', '--verbose'):
            VERBOSE = True

    if not (NEW_ADDR or INPUT_FILE):
        print(USAGE)
        exit(1)

    if NEW_ADDR and INPUT_FILE:
        print(USAGE)
        exit(1)

    if INPUT_FILE:
        RES = main(INPUT_FILE, VERBOSE, is_file=True, output=OUTPUT_FILE)
    else:
        RES = main(NEW_ADDR, VERBOSE, is_file=False, output=OUTPUT_FILE)

    exit(RES)
