#!/usr/bin/env python

"""
Script to test database connection parameters in Islandora
filter_drupal.xml files.

Usage: ./test_db_connection.py /path/to/filter_drupal.xml [-n]

Use the -n flag if your filter_drupal.xml file uses the "http://islandora.ca"
default namespace.
"""

import sys
import os
import argparse
import re
from xml.etree import ElementTree
from subprocess import CalledProcessError, check_output, STDOUT

argparser = argparse.ArgumentParser()
argparser.add_argument("path_to_filter_drupal_xml", help = "Path to the filter_drupal.xml file to test")
argparser.add_argument("-n", help = "The filter_drupal.xml file declares default namespace as 'http://islandora.ca'", action="store_true")
args = argparser.parse_args()

if not os.path.exists(args.path_to_filter_drupal_xml):
    print "Sorry, %s doesn't appear to exist." % args.path_to_filter_drupal_xml
    sys.exit(1)

with open(args.path_to_filter_drupal_xml, 'r') as f:
    tree = ElementTree.parse(f)

if args.n:
    nsmap = {'islandora': 'http://islandora.ca'}
    nodes = tree.findall('islandora:connection', namespaces=nsmap)
else:
    nodes = tree.findall('connection')

connection_number = 0
has_errors = False
# Loop through each of the connection elements, grab the database
# connection attributes, and test them against the Drupal database.
for node in nodes:
    connection_number += 1
    # Assumes that the filter_drupal.xml file has been validated
    # (i.e., we don't check for presence of the attributes).
    server = node.attrib.get('server')
    port = node.attrib.get('port')
    dbname = node.attrib.get('dbname')
    user = node.attrib.get('user')
    password = node.attrib.get('password')

    try:
        mysqlshowoutput = check_output('mysqlshow --host=' + server + ' --port=' + port + ' -u' + user + \
            ' -p' + password + ' ' + dbname + ' users uid', stderr=STDOUT, shell=True)
        if re.search('select,insert,update', mysqlshowoutput):
            print "Connection {0} - OK: connection to Drupal database successful, and user {1} " \
                .format(connection_number, user) + "has select,insert,update privileges on the users table."
        else:
            print "Connection {0} - Error: connection to Drupal database successful, but user {1} " \
                .format(connection_number, user) + "does not have sufficient privileges on the users table."
            has_errors = True
    except CalledProcessError as e:
        print "Connection {0} - Error: {1}".format(connection_number, e.output.rstrip())
        has_errors = True

if has_errors:
    sys.exit(1)
else:
    sys.exit(0)