# -*- coding: utf-8 -*-

import sys
from mongodb_performance_tests import DEFAULT_DATABASE_ADAPTER


def adapter_factory(db_adapter):
    if db_adapter == 'mongodb':
        from mongodb_performance_tests.adapters.mongodb import MongoDBAdapter
        return MongoDBAdapter()
    elif db_adapter == 'mysql':
        from mongodb_performance_tests.adapters.mysql import MySqlDBAdapter
        return MySqlDBAdapter()
    else:
        raise Exception('Try to use unknown adapter')


def get_all_available_adapters():
    data = {}
    for v in ['mongodb', 'mysql']:
        try:
            data[v] = adapter_factory(v)
        except:
            data[v] = False
    return data


def get_adapter_from_command_line():
    if len(sys.argv) == 1:
        return DEFAULT_DATABASE_ADAPTER
    else:
        return sys.argv[1]
