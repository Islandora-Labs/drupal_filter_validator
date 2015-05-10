# filter-drupal.xml validation utilities

## Introduction

Utilities for validating [Islandora filter-drupal.xml files](https://github.com/Islandora/islandora_drupal_filter). The two utilities are:

* an XSD schema for validating filter-drupal.xml (e.g., `xmllint --schema filter-drupal.xsd filter-drupal.xml`).

Note that filter-drupal.xml files currently distributed with Islandora don't include a namespace declaration so they won't validate against this (or any other) schema. If you want to validate your filter-drupal.xml file against this schema, add `xmlns=http://islandora.ca` to the root element, like this:

```xml
<FilterDrupal_Connection xmlns="http://islandora.ca">
```

* a Python (2.7) script that parses your filter-drupal.xml file for your Drupal databaes connection details and tests each `<connection>` entry in the file.

## Requirements

* Python 2.7 or higher.
* `mysqlshow` must be intalled on the server where the script is running.


## Usage

You can use whatever tool you want to validate your filter-drupal.xml file, but the most common way of doing that would be using xmllint:

`xmllint --schema filter-drupal.xsd filter-drupal.xml`

Note that you will need to add the xmlns="http://islandora.ca" namespace declaration to your filter-drupal.xml file to validate it.

To run test_db_connection.py, provide the path to your filter-drupal.xml file as a parameter:

```./test_db_connection.py filter-drupal.xml [-n]```

This script returns 0 if all `<connection>` entries can successfully connect to their respective databases, and returns 1 if there are any errors.

The test_db_connection.py script takes an optional '-n' paramter to indicate that the filter-drupal.xml file declares the "http://islandora.ca" namespace.

## Troubleshooting/Issues

Having problems or solved a problem? Check out the Islandora google groups for a solution.

* [Islandora Group](https://groups.google.com/forum/?hl=en&fromgroups#!forum/islandora)
* [Islandora Dev Group](https://groups.google.com/forum/?hl=en&fromgroups#!forum/islandora-dev)

## Development

If you would like to contribute to this module, please check out our helpful [Documentation for Developers](https://github.com/Islandora/islandora/wiki#wiki-documentation-for-developers) info, as well as our [Developers](http://islandora.ca/developers) section on the Islandora.ca site.

## License

[GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt)
