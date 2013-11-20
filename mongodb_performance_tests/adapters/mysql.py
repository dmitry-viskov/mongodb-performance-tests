# -*- coding: utf-8 -*-

import MySQLdb
from ..settings import DATABASE_NAME, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, DATABASE_PASSWORD


class MySqlDBAdapter(object):
    conn = None
    cursor = None

    def __init__(self):
        self.conn = MySQLdb.connect(host=DATABASE_HOST, port=DATABASE_PORT,
                                    user=DATABASE_USER, passwd=DATABASE_PASSWORD, db=DATABASE_NAME)
        self.cursor = self.conn.cursor()

    def prepare_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS users')
        self.cursor.execute(
            "CREATE TABLE `users` (\
                `id` int(11) NOT NULL AUTO_INCREMENT,\
                `user_id` int(11) NOT NULL DEFAULT '0',\
                `name` varchar(255) NOT NULL,\
                `email` varchar(255) NOT NULL,\
                `is_deleted` tinyint(1) NOT NULL DEFAULT '0',\
                PRIMARY KEY (`id`),\
                KEY `user_id_is_deleted` (`user_id`,`is_deleted`)\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8")

        self.cursor.execute('DROP TABLE IF EXISTS results')
        self.cursor.execute(
            "CREATE TABLE `results` (\
                `id` int(11) NOT NULL AUTO_INCREMENT,\
                `processes` int(11) NOT NULL DEFAULT '0',\
                `value` decimal(30,15) NOT NULL DEFAULT 0,\
                PRIMARY KEY (`id`),\
                KEY `processes` (`processes`)\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8")
        self.conn.commit()

    def create_users(self, data):
        self.cursor.executemany(
            """INSERT INTO users (user_id, name, email, is_deleted)
                VALUES (%s, %s, %s, %s)""",
            [[v['user_id'], v['name'], v['email'], v['is_deleted']] for v in data])
        self.conn.commit()

    def update_user(self, user_id, params):
        update_str = ','.join([''.join([v, '=%s']) for v in params.keys()])
        values = params.values()
        values.append(user_id)

        self.cursor.execute(''.join(['UPDATE test SET ', update_str, ' WHERE user_id=%s']), values)
        self.conn.commit()

    def save_results(self, result_lst, processes_num):
        self.cursor.executemany(
            """INSERT INTO results (processes, value)
                VALUES (%s, %s)""",
            [[processes_num, '%.6f' % round(v, 6)] for v in result_lst])
        self.conn.commit()

    def get_result_by_processes(self, process):
        self.cursor.execute("""SELECT value FROM results WHERE processes = %s""", (process,))
        results = self.cursor.fetchall()
        self.conn.commit()
        return results