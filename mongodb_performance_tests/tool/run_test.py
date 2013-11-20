import time
import random

from multiprocessing.pool import Pool
from ..settings import DOCS_PER_USER, MAX_PROCESSES, USERS_COUNT
from ..common import adapter_factory


def create_users(params):
    start = time.time()

    user_id = params['user_id']
    docs_per_user = params['docs_per_user']
    is_deleted = bool(random.randint(0, 1))

    new_users = []

    for i in xrange(docs_per_user):
        name = 'Document %d for User %d' % (i, user_id)
        email = 'doc%d@user%d.com' % (i, user_id)
        new_users.append({'user_id': user_id, 'name': name, 'email': email, 'is_deleted': is_deleted})

    adapter = adapter_factory()
    adapter.create_users(new_users)

    return time.time() - start


def update_users(user_id):
    start = time.time()
    is_deleted = bool(random.randint(0, 1))

    adapter = adapter_factory()
    adapter.update_user(user_id, {"is_deleted": is_deleted})

    return time.time() - start


class MainTest(object):

    def run(self):
        print 'Prepare database'
        adapter = adapter_factory()
        adapter.prepare_db()

        print ''
        print 'Create user documents'

        pool = Pool(processes=10)
        params = [{'user_id': i, 'docs_per_user': DOCS_PER_USER}
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
            params = range(1, USERS_COUNT + 1)
            start = time.time()
                
            try:
                res = pool.map(update_users, params)
                full_time = time.time() - start
            finally:
                pool.terminate()
            del pool

            print 'Test is finished! Save results'
            print ''

            adapter.save_results(res, i)

            print 'Full time:', full_time
            print ''

        print 'Finish!'


if __name__ == '__main__':
    mt = MainTest()
    mt.run()