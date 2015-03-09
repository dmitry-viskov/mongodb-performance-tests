# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

import csv
import datetime
import argparse

from mongodb_performance_tests.settings import MAX_PROCESSES, CSV_REPORTS_DEFAULT_DIR, DEFAULT_DATABASE_ADAPTER
from mongodb_performance_tests.common import adapter_factory


class ReportsCreator(object):

    def make(self, test_name, report_dir, db_adapter):
        if db_adapter is None:
            db_adapter = DEFAULT_DATABASE_ADAPTER
        if report_dir is None:
            report_dir = CSV_REPORTS_DEFAULT_DIR

        adapter = adapter_factory(db_adapter)

        test_id = None

        tests = adapter.get_available_tests()
        for v in tests:
            if (test_name is None) and ((test_id is None) or (test_id > v['id'])):
                test_id = v['id']
                test_name = v['name']
            elif test_name == v['name']:
                test_id = v['id']

        if test_id is None:
            raise Exception("Undefined test name")

        csv_path = os.path.join(report_dir, 'result-%s %s.csv' % (str(db_adapter), str(datetime.datetime.now())))
        print "Creating csv report for test '%s' (%s)" % (test_name, csv_path)

        result = []
        for i in range(1, MAX_PROCESSES + 1):
            res = adapter.get_result_by_processes(test_id, i)
            result.append([str(v[1]) for v in res])

        with open(csv_path, 'w+') as f:
            writer = csv.writer(f)
            writer.writerow([''.join(['proc', str(i)]) for i in range(1, MAX_PROCESSES + 1)])
            for i in range(1, MAX_PROCESSES + 1):
                tmp_lst = []
                for v in result:
                    try:
                        tmp_lst.append(v[i-1])
                    except IndexError:
                        pass
                writer.writerow(tmp_lst)

        print 'Finish!'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create CSV with performance tests results.')
    parser.add_argument('--report_dir', help=''.join(['Directory to store tests cvs reports ("',
                                                      CSV_REPORTS_DEFAULT_DIR,
                                                      '" will be used by default)']))
    parser.add_argument('--adapter', help=''.join(['DB adapter ("',
                                                   DEFAULT_DATABASE_ADAPTER,
                                                   '" will be used by default)']))
    parser.add_argument('--test_name', help='By default will be used last test')
    args = parser.parse_args()

    r = ReportsCreator()
    r.make(args.test_name, args.report_dir, args.adapter)
