# filter-drupal.xml validation utilities

## Introduction

Utilities for validating [Islandora filter-drupal.xml files](https://github.com/Islandora/islandora_drupal_filter). The two utilities are:

* an XSD schema for validating filter-drupal.xml (e.g., `xmllint --schema filter-drupal.xsd filter-drupal.xml`).

Note that filter-drupal.xml files currently distributed with Islandora don't include a namespace declaration so they won't validate against this (or any other) schema. If you want to validate your filter-drupal.xml file against this schema, add `xmlns=http://islandora.ca` to the root element, like this:

```xml
<FilterDrupal_Connection xmlns="http://islandora.ca">
```

* a shell script that parses your filter-drupal.xml file for your Drupal database connection details, tests the connection, and tests the user's privileges on the Drupal user table.

## Requirements

* The shell script uses the `xpath` utility ([manpage](http://manpages.ubuntu.com/manpages/precise/en/man1/xpath.1p.html)) that ships with Ubuntu.
* `mysqlshow` must be intalled on the server where the script is running.


## Usage

You can use whatever tool you want to validate your filter-drupal.xml file, but the most common way of doing that would be using xmllint:

`xmllint --schema filter-drupal.xsd filter-drupal.xml`

To run test_db_connection.sh, provide the path to your filter-drupal.xml file as a parameter:

```./test_db_connection.sh filter-drupal.xml```

This script returns 0 on successful connection, and uses MySQL's error code if it can't.

## Troubleshooting/Issues

Having problems or solved a problem? Check out the Islandora google groups for a solution.

* [Islandora Group](https://groups.google.com/forum/?hl=en&fromgroups#!forum/islandora)
* [Islandora Dev Group](https://groups.google.com/forum/?hl=en&fromgroups#!forum/islandora-dev)

## Development

If you would like to contribute to this module, please check out our helpful [Documentation for Developers](https://github.com/Islandora/islandora/wiki#wiki-documentation-for-developers) info, as well as our [Developers](http://islandora.ca/developers) section on the Islandora.ca site.

## License

[GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt)
