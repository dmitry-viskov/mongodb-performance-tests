# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

import time
import datetime
import random
import argparse

from multiprocessing.pool import Pool
from mongodb_performance_tests import DOCS_PER_USER, MAX_PROCESSES, USERS_COUNT, DEFAULT_DATABASE_ADAPTER
from mongodb_performance_tests.common import adapter_factory


def create_users(params):
    start = time.time()

    user_id = params['user_id']
    docs_per_user = params['docs_per_user']
    db_adapter = params['db_adapter']
    is_deleted = bool(random.randint(0, 1))

    new_users = []

    for i in xrange(docs_per_user):
        name = 'Document %d for User %d' % (i, user_id)
        email = 'doc%d@user%d.com' % (i, user_id)
        new_users.append({'user_id': user_id, 'name': name, 'email': email, 'is_deleted': is_deleted})

    adapter = adapter_factory(db_adapter)
    adapter.create_users(new_users)

    return time.time() - start


def update_users(params):
    user_id = params['user_id']
    db_adapter = params['db_adapter']

    start = time.time()
    is_deleted = bool(random.randint(0, 1))

    adapter = adapter_factory(db_adapter)
    adapter.update_user(user_id, {"is_deleted": is_deleted})

    return time.time() - start


class MainTest(object):

    def run(self, test_name=None, db_adapter=None):

        if db_adapter is None:
            db_adapter = DEFAULT_DATABASE_ADAPTER
        if test_name is None:
            test_name = '_'.join([db_adapter, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")])

        print ''.join(['Running "', test_name, '" test'])
        print 'Prepare database'

        adapter = adapter_factory(db_adapter)
        adapter.prepare_db()
        test_id = adapter.create_new_test(test_name)

        print ''
        print 'Create user documents'

        pool = Pool(processes=10)
        params = [{'user_id': i, 'docs_per_user': DOCS_PER_USER, 'db_adapter': db_adapter}
                  for i in range(1, USERS_COUNT + 1)]

        start = time.time()
        try:
            pool.map(create_users, params)
            print 'Full time:', time.time() - start
        finally:
            pool.terminate()
        del pool

        print 'OK! Users were created!'
        print ''

        for i in range(1, MAX_PROCESSES + 1):
            print 'Run test with %d proceses' % i
            pool = Pool(processes=i)
            params = [{'user_id': j, 'db_adapter': db_adapter} for j in range(1, USERS_COUNT + 1)]
            start = time.time()
                
            try:
                res = pool.map(update_users, params)
                full_time = time.time() - start
            finally:
                pool.terminate()
            del pool

            print 'Test is finished! Save results'
            print ''

            adapter.save_results(test_id, res, i)

            print 'Full time:', full_time
            print ''

        print 'Finish!'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run performance test.')
    parser.add_argument('--name', help='test name (current timestamp will be used by default)')
    parser.add_argument('--adapter', help=''.join(['DB adapter ("',
                                                   DEFAULT_DATABASE_ADAPTER,
                                                   '" will be used by default)']))
    args = parser.parse_args()

    mt = MainTest()
    mt.run(args.name, args.adapter)