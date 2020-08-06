Detect and Download
=============

## Description
A python project to **crawl the websites of different tools**, to **check for new releases** and **download them if not present locally**.
* For technical problems, please report to [Issues](https://github.com/maanas-talwar/Detect-and-Download/issues).

## Dependencies:
* For Python(3.8):  
> BeautifulSoup4

## Contents
```
.
├── plugins
│   └── <tool_name>_plugin
│       ├── code.py
│       └── data
│           ├── <tool_name>.json
│           └── downloads
├── README.md
└── setup.py
```

## Execution
* To run the process, first change your directory to `Detect-and-Download/` using the following command:
> cd Detect-and-Download/
* The process can be run by the following command:
> python setup.py
* The program will inherently work for the following tools:
  - Apache HTTP Server
  - Apache Tomcat
  - MaraiaDB
  - Nginx
  - Node.js
  - PHP
  - PostgreSQL
  - Python
  - Ubuntu
  - WordPress
* For operating systems, like Ubuntu, only the link to the iso webpage will be saved in `./<tool_name>/data/<tool_name>_OS.json`.
* For other tools, the downloaded `tarball(tar.gz or .tgz)` file for the new releases can be found in `./<tool_name>/data/downloads/`.
