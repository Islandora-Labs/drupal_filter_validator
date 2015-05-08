#!/usr/bin/env python

"""
Script to test database connection parameters in Islandora
filter_drupal.xml files.

Usage: ./test_db_connection.py /path/to/filter_drupal.xml [-n]

Use the -n flag if your filter_drupal.xml file uses the "http://islandora.ca"
default namespace.
"""

# @todo: Add support for the Islandora namespace. Trick will be to make the
# namespace optional.

import sys
import os
import argparse
import re
from xml.etree import ElementTree
from subprocess import CalledProcessError, check_output

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

# Assume that the filter_drupal.xml file has been validated.
# Loop through each of the connection elements, grab the database
# connection attributes, and test them against the Drupal database.
for node in nodes:
    server = node.attrib.get('server')
    port = node.attrib.get('port')
    dbname = node.attrib.get('dbname')
    user = node.attrib.get('user')
    password = node.attrib.get('password')

    try:
        mysqlshowoutput = check_output('mysqlshow --host=' + server + ' --port=' + port + ' -u' + user + ' -p' + password + ' ' + dbname + ' users uid', shell=True)
        print mysqlshowoutput
        if re.search('select,insert,update', mysqlshowoutput):
            print "Connection to Drupal database successful, and user %s has select,insert,update privileges on the users table." % user
            sys.exit(0)
        else:
            print "Connection to Drupal database successful, but user %s does not have sufficient privileges on the users table." % user
            sys.exit(2)
    except CalledProcessError as e:
       sys.exit(e.returncode)

# @todo: Don't exit within loop since we want to check all the connections.
