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
│   ├── pluginBlueprint
│   │   ├── __init__.py
│   │   └── pluginBlueprint.py
│   ├── php_plugin
│   │   ├── code.py
│   │   ├── data
│   │   │   ├── downloads
│   │   │   └── php.json
│   │   └── __init__.py
│   └── postgresql_plugin
│       ├── code.py
│       ├── data
│       │   ├── downloads
│       │   └── postgresql.json
│       └── __init__.py
├── README.md
└── setup.py
```

<!--- ##Contents --->

## Execution
* The main driver python program invokes the required plugins to detect the versions for various tools and download the binary files if they are not present locally.

