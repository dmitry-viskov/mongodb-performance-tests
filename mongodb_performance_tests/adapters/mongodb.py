# -*- coding: utf-8 -*-

import time
import pymongo

from pymongo import MongoClient
from mongodb_performance_tests import MONGO_DATABASE_NAME, MONGO_DATABASE_HOST, MONGO_DATABASE_PORT
from mongodb_performance_tests.adapters.abstract import AbstractDBAdapter


class MongoDBAdapter(AbstractDBAdapter):
    conn = None

    def __init__(self):
        self.conn = MongoClient(MONGO_DATABASE_HOST, MONGO_DATABASE_PORT)

    def get_name(self):
        return 'MongoDB'

    def prepare_db(self):
        users_coll = self.conn[MONGO_DATABASE_NAME].users
        users_coll.drop()

        results_coll = self.conn[MONGO_DATABASE_NAME].results
        results_coll.create_index([("test_id", pymongo.ASCENDING),
                                   ("processes", pymongo.ASCENDING)])

    def create_users(self, data):
        coll = self.conn[MONGO_DATABASE_NAME].users
        coll.create_index([('user_id', pymongo.ASCENDING), ('is_deleted', pymongo.ASCENDING)])
        coll.insert(data)

    def create_new_test(self, test_name):
        test_id = int(time.time())
        test_names_coll = self.conn[MONGO_DATABASE_NAME].test_names
        test_names_coll.insert({'_id': str(test_id), 'name': test_name})
        return test_id

    def update_user(self, user_id, params):
        coll = self.conn[MONGO_DATABASE_NAME].users
        coll.update({"user_id": user_id}, {"$set": params}, upsert=False, multi=True)

    def save_results(self, test_id, result_lst, processes_num):
        results_coll = self.conn[MONGO_DATABASE_NAME].results
        results_coll.insert([{'test_id': str(test_id), 'processes': processes_num, 'value': v} for v in result_lst])

    def get_available_tests(self):
        res = self.conn[MONGO_DATABASE_NAME].test_names.find().sort('_id', pymongo.DESCENDING)
        data = []
        for val in res:
            data.append({'id': val['_id'], 'name': val['name']})
        return data

    def get_test_name_by_id(self, test_id):
        res = self.conn[MONGO_DATABASE_NAME].test_names.find_one({"_id": str(test_id)})
        return res['name'] if res else None

    def get_result_by_processes(self, test_id, process):
        res = self.conn[MONGO_DATABASE_NAME].results.find({"test_id": str(test_id), "processes": int(process)},
                                                          fields={'_id': False, 'value': True})
        data = []
        i = 1

        for val in res:
            data.append([i, val['value']])
            i += 1
        return data
