# -*- coding: utf-8 -*-

import os
import sys
import tempfile

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

WEBSERVER_HOST = '0.0.0.0'
WEBSERVER_PORT = 8000

MYSQL_DATABASE_NAME = 'test'
MYSQL_DATABASE_HOST = '127.0.0.1'
MYSQL_DATABASE_PORT = 3306
MYSQL_DATABASE_USER = 'root'
MYSQL_DATABASE_PASSWORD = 'root'

MONGO_DATABASE_NAME = 'test'
MONGO_DATABASE_HOST = '127.0.0.1'
MONGO_DATABASE_PORT = 27017

DEFAULT_DATABASE_ADAPTER = 'mongodb'

USERS_COUNT = 1000
DOCS_PER_USER = 5000
MAX_PROCESSES = 30

CSV_REPORTS_DEFAULT_DIR = tempfile.gettempdir()
