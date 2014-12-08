# -*- coding: utf-8 -*-

import pymongo

from pymongo import MongoClient
from ..settings import MONGO_DATABASE_NAME, MONGO_DATABASE_HOST, MONGO_DATABASE_PORT


class MongoDBAdapter(object):
    conn = None

    def __init__(self):
        self.conn = MongoClient(MONGO_DATABASE_HOST, MONGO_DATABASE_PORT)

    def get_name(self):
        return 'MongoDB'

    def prepare_db(self):
        self.conn.drop_database(MONGO_DATABASE_NAME)
        results_coll = self.conn[MONGO_DATABASE_NAME].results
        results_coll.create_index('processes')

    def create_users(self, data):
        coll = self.conn[MONGO_DATABASE_NAME].users
        coll.create_index([('user_id', pymongo.ASCENDING), ('is_deleted', pymongo.ASCENDING)])
        coll.insert(data)

    def update_user(self, user_id, params):
        coll = self.conn[MONGO_DATABASE_NAME].users
        coll.update({"user_id": user_id}, {"$set": params}, upsert=False, multi=True)

    def save_results(self, result_lst, processes_num):
        results_coll = self.conn[MONGO_DATABASE_NAME].results
        results_coll.insert([{'processes': processes_num, 'value': v} for v in result_lst])

    def get_result_by_processes(self, process):
        res = self.conn[MONGO_DATABASE_NAME].results.find({"processes": process}, fields={'_id': False, 'value': True})

        data = []
        i = 1

        for val in res:
            data.append([i, val['value']])
            i += 1
        return data
