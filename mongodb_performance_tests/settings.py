# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

MYSQL_DATABASE_NAME = 'test'
MYSQL_DATABASE_HOST = '127.0.0.1'
MYSQL_DATABASE_PORT = 3306
MYSQL_DATABASE_USER =  'root'
MYSQL_DATABASE_PASSWORD = 'root'

MONGO_DATABASE_NAME = 'test'
MONGO_DATABASE_HOST = '127.0.0.1'
MONGO_DATABASE_PORT = 27017

DEFAULT_DATABASE_ADAPTER='mongo'

USERS_COUNT = 1000
DOCS_PER_USER = 1000
MAX_PROCESSES = 20

CSV_REPORTS_DIR = '~/Temp/mongotest/'
