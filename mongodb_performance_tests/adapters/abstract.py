# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class AbstractDBAdapter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def prepare_db(self):
        pass

    @abstractmethod
    def create_users(self, data):
        pass

    @abstractmethod
    def create_new_test(self, test_name):
        pass

    @abstractmethod
    def update_user(self, user_id, params):
        pass

    @abstractmethod
    def save_results(self, test_id, result_lst, processes_num):
        pass

    @abstractmethod
    def get_available_tests(self):
        pass

    @abstractmethod
    def get_result_by_processes(self, test_id, process):
        pass