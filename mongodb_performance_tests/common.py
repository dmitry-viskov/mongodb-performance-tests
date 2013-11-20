from mongodb_performance_tests.settings import DATABASE_ADAPTER
from mongodb_performance_tests.adapters.mongodb import MongoDBAdapter
from mongodb_performance_tests.adapters.mysql import MySqlDBAdapter


def adapter_factory():
    db_adapter = DATABASE_ADAPTER.lower()

    if db_adapter == 'mongodb':
        return MongoDBAdapter()
    elif db_adapter == 'mysql':
        return MySqlDBAdapter()
    else:
        raise Exception('Try to use unknown adapter')





