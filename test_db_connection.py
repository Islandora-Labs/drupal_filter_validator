#!/usr/bin/env python

"""
Script to test database connection parameters in Islandora
filter_drupal.xml files.

Usage: ./test_db_connection.py /path/to/filter_drupal.xml
"""

import sys
import os
import argparse
import subprocess
import re
from xml.etree import ElementTree

argparser = argparse.ArgumentParser()
argparser.add_argument("path_to_filter_drupal_xml", help = "The filter_drupal.xml file to test")
args = argparser.parse_args()

if not os.path.exists(args.path_to_filter_drupal_xml):
    print "Sorry, %s doesn't appear to exist." % args.path_to_filter_drupal_xml
    sys.exit(1)

with open(args.path_to_filter_drupal_xml, 'r') as f:
    tree = ElementTree.parse(f)

# Assume that the filter_drupal.xml file has been validated.
# Loop through each of the connection elements, grab the database
# connection attributes, and test them against the Drupal database.
for node in tree.findall('.//connection'):
    server = node.attrib.get('server')
    port = node.attrib.get('port')
    dbname = node.attrib.get('dbname')
    user = node.attrib.get('user')
    password = node.attrib.get('password')

    mysqlshowoutput = subprocess.check_output('mysqlshow -h' + server + ' -P' + port + ' -u' + user + ' -p' + password dbname + ' users uid', shell=True)
    if re.search('select,insert,update', mysqlshowoutput):
        print "Connection to Drupal database successful, and user %s has select,insert,update privileges on the users table." % user
        sys.exit(0)
    else:
        print "Connection to Drupal database successful, but user %s does not have sufficient privileges on the users table." % user
        sys.exit(2)


