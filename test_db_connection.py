#!/usr/bin/env python

"""
Script to test database connection parameters in Islandora
filter_drupal.xml files.

Usage: ./test_db_connection.py /path/to/filter_drupal.xml
"""

import sys
import os
import argparse
import re
from xml.etree import ElementTree
from subprocess import CalledProcessError, check_output, STDOUT

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("path_to_filter_drupal_xml", help="Path to the filter_drupal.xml file to test")
    args = argparser.parse_args()

    if not os.path.exists(args.path_to_filter_drupal_xml):
	print "Sorry, Drupal filter file {0} doesn't appear to exist.".format(args.path_to_filter_drupal_xml)
	sys.exit(1)

    with open(args.path_to_filter_drupal_xml, 'r') as f:
	tree = ElementTree.parse(f)

    # Check to see if the input file has the default namespace declaration
    # of 'http://www.islandora.ca'.
    root = tree.getroot()
    if re.search('{http://www.islandora.ca}', root.tag):
	nsmap = {'islandora': 'http://www.islandora.ca'}
	nodes = tree.findall('islandora:connection', namespaces=nsmap)
    else:
	nodes = tree.findall('connection')

    # Loop through each of the connection elements, grab the database
    # connection attributes, and test them against the Drupal database.
    connection_number = 0
    found_errors = False
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
		found_errors = True
	except CalledProcessError as e:
	    print "Connection {0} - Error: {1}".format(connection_number, e.output.rstrip())
	    found_errors = True

    if found_errors:
	sys.exit(1)
    else:
	sys.exit(0)
