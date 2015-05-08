#!/usr/bin/env python

"""
Script to test database connection parameters in Islandora
filter_drupal.xml files.

Usage: ./test_db_connection.py /path/to/filter_drupal.xml
"""

import sys
import os
from xml.etree import ElementTree
import argparse
import subprocess

argparser = argparse.ArgumentParser()
argparser.add_argument("path_to_filter_drupal_xml", help = "The filter_drupal.xml file to test")
args = argparser.parse_args()

if not os.path.exists(args.path_to_filter_drupal_xml):
    print "Sorry, %s doesn't appear to exist." % args.path_to_filter_drupal_xml
    sys.exit(1)

with open(args.path_to_filter_drupal_xml, 'r') as f:
    tree = ElementTree.parse(f)

for node in tree.findall('.//connection'):
    server = node.attrib.get('server')
    port = node.attrib.get('port')
    dbname = node.attrib.get('dbname')
    user = node.attrib.get('user')
    password = node.attrib.get('password')

    foo = subprocess.check_output(['ls', '-l'])
    print "Work in progress..."
    print foo


