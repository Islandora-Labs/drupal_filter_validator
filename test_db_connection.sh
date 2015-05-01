#!/usr/bin/env bash

# Shell script to get database credentials from an Islandora filter-drupal.xml
# file and test a connection to MySQL using them.
#
# Usage: ./test_db_connection.sh filter-drupal.xml
 
# @todos:
# Check to see if xpath is installed and if not, bail with an error message.
# Modify to accommodate postgres.
# Modify to accommodate multiple connections in filter-drupal.xml.

MYSQL=$(which mysql)

# Get attributes via XPath, then clean up the output using sed and tr.
SERVER="$(xpath -q -e '//connection/@server' $1 | sed  "s/server=\"//" | sed s/\"// | sed -e 's/^[ \t]*//' | tr -d '\n')"
PORT="$(xpath -q -e '//connection/@port' $1 | sed  "s/port=\"//" | sed s/\"// | sed -e 's/^[ \t]*//' | tr -d '\n')"
DBNAME="$(xpath -q -e '//connection/@dbname' $1 | sed  "s/dbname=\"//" | sed s/\"// | sed -e 's/^[ \t]*//' | tr -d '\n')"
USER="$(xpath -q -e '//connection/@user' $1 | sed  "s/user=\"//" | sed s/\"// | sed -e 's/^[ \t]*//' | tr -d '\n')"
PASSWORD="$(xpath -q -e '//connection/@password' $1 | sed  "s/password=\"//" | sed s/\"// | sed -e 's/^[ \t]*//' | tr -d '\n')"

# Set up MySQL command to test credentials, then run the command.
MYSQLCOMMAND="$MYSQL --silent -h${SERVER} -u${USER} -p${PASSWORD} $DBNAME"
$MYSQLCOMMAND
ERROR_CODE=$?

# Test for success and exit with a useful code and message.
if [ $ERROR_CODE -eq 0 ]; then
	  printf "Connection to Drupal database successful\n"
      exit $ERROR_CODE
else
      printf "Can't connect to Drupal database with credentials provided\n"
      exit $ERROR_CODE
fi