# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

#DATABASE_NAME = 'test_database'
DATABASE_NAME = 'test'
DATABASE_HOST = '127.0.0.1'
#DATABASE_PORT = 27017
DATABASE_PORT = 3306
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'root'
#DATABASE_ADAPTER = 'mongodb'
DATABASE_ADAPTER = 'mysql'

USERS_COUNT = 1000
DOCS_PER_USER = 1000
MAX_PROCESSES = 20

CSV_REPORTS_DIR = '/home/strannik/Temp/mongotest/'
