# filter-drupal.xml validation utilities

## Introduction

Utilities for validating [Islandora filter-drupal.xml files](https://github.com/Islandora/islandora_drupal_filter). The two utilities are:

* an XSD schema for validating filter-drupal.xml files

Note that filter-drupal.xml files currently distributed with Islandora don't include a namespace declaration so they won't validate against this (or any other) schema. If you want to validate your filter-drupal.xml file against this schema, add `xmlns=http://www.islandora.ca` to the root element, like this:

```xml
<FilterDrupal_Connection xmlns="http://www.islandora.ca">
```

* a Python script that parses your filter-drupal.xml file for your Drupal databaes connection details and tests each `<connection>` entry in the file.

## Requirements

* Python 2.7 or higher, which should already be installed on any server that Fedora Commons runs on.
* `mysqlshow` must be installed on the server where the script is running.


## Usage

You can use whatever tool you want to validate your filter-drupal.xml file, but the most common way of doing that would be using xmllint:

`xmllint --schema filter-drupal.xsd filter-drupal.xml`

Remember that you will need to add the xmlns="http://www.islandora.ca" namespace declaration to your filter-drupal.xml file to validate it.

To run test_db_connection.py, provide the path to your filter-drupal.xml file as a parameter:

```./test_db_connection.py filter-drupal.xml```

This script returns 0 if all `<connection>` entries can successfully connect to their respective databases, and returns 1 if there are any errors.

Note that on Linux systems, MySQL connections to localhost use a local socket file and ignore specification of port numbers using the --port/-P paramter. This means that the value of the `port` attribute in your filter-drupal.xml file is ignored if the `host` is 'localhost'. However, if the `host` attribute contains a value other than 'localhost', the value of `port` is used.

## Troubleshooting/Issues

Having problems? Check out the Islandora google groups for a solution.

* [Islandora Group](https://groups.google.com/forum/?hl=en&fromgroups#!forum/islandora)
* [Islandora Dev Group](https://groups.google.com/forum/?hl=en&fromgroups#!forum/islandora-dev)

## Development

If you would like to contribute to this utility, please check out our helpful [Documentation for Developers](https://github.com/Islandora/islandora/wiki#wiki-documentation-for-developers) info, as well as our [Developers](http://islandora.ca/developers) section on the Islandora.ca site.

## License

[GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt)
