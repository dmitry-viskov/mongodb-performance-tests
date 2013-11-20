# -*- coding: utf-8 -*-

import pymongo

from pymongo import MongoClient
from ..settings import DATABASE_NAME, DATABASE_HOST, DATABASE_PORT


class MongoDBAdapter(object):
    conn = None

    def __init__(self):
        self.conn = MongoClient(DATABASE_HOST, DATABASE_PORT)

    def prepare_db(self):
        self.conn.drop_database(DATABASE_NAME)
        results_coll = self.conn[DATABASE_NAME].results
        results_coll.create_index('processes')

    def create_users(self, data):
        coll = self.conn[DATABASE_NAME].users
        coll.create_index([('user_id', pymongo.ASCENDING), ('is_deleted', pymongo.ASCENDING)])
        coll.insert(data)

    def update_user(self, user_id, params):
        coll = self.conn[DATABASE_NAME].users
        coll.update({"user_id": user_id}, {"$set": params}, upsert=False, multi=True)

    def save_results(self, result_lst, processes_num):
        results_coll = self.conn[DATABASE_NAME].results
        results_coll.insert([{'processes': processes_num, 'value': v} for v in result_lst])

    def get_result_by_processes(self, process):
        return self.conn[DATABASE_NAME].results.find({"processes": process}, fields={'_id': False, 'value': True})
