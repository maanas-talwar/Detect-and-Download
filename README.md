Detect and Download
================

## Introduction
A python project to crawl the package websites, for instance [PostgreSQL](https://www.postgresql.org/), [php](https://www.php.net/), to check for new releases and download them if not locally present.

* For technical problems, please report to [Issues](https://github.com/maanas-talwar/Detect-and-Download/issues).


## Dependencies
* For Python (3.7):
    > beautifulsoup4

## Architecture
```
.
├── plugins
│   ├── __init__.py
│   ├── MariaDB_plugin
│   │   ├── code.py
│   │   ├── data
│   │   │   ├── downloads
│   │   │   └── MariaDB.json
│   │   └── __init__.py
│   ├── PHP_plugin
│   │   ├── code.py
│   │   ├── data
│   │   │   ├── downloads
│   │   │   └── PHP.json
│   │   └── __init__.py
│   ├── pluginBlueprint
│   │   ├── __init__.py
│   │   └──pluginBlueprint.py
│   ├── PostgreSQL_plugin
│   │   ├── code.py
│   │   ├── data
│   │   │   ├── downloads
│   │   │   └── PostgreSQL.json
│   │   └── __init__.py
│   └── WordPress_plugin
│       ├── code.py
│       ├── data
│       │   ├── downloads
│       │   └── WordPress.json
│       └── __init__.py
├── README.md
├── setup.py
└── temp.py
```

<!--- ##Contents --->

## Execution
* The main driver program(setup.py) invokes the all the subroutines at runtime to check for latest releases of different tools.
* This data is then stored in the respective JSON file for each subroutine. The JSON file contains all the necessary information for the locally absent or present versions.
* Next in line is the downloading of the locally absent subroutine binaries.

Currently added subroutines are:
* MariaDB
* PHP
* PostgreSQL
* WordPress
