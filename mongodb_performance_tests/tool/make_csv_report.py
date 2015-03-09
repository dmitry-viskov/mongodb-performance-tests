# -*- coding: utf-8 -*-

import os
import csv
import datetime

from mongodb_performance_tests.settings import MAX_PROCESSES, CSV_REPORTS_DIR
from mongodb_performance_tests.common import adapter_factory, get_adapter_from_command_line


class ReportsCreator(object):

    def make(self, db_adapter):
        adapter = adapter_factory(db_adapter)

        result = []

        for i in range(1, MAX_PROCESSES + 1):
            res = adapter.get_result_by_processes(i)
            result.append([str(v[0] if isinstance(v, (tuple, list)) else v.itervalues().next()).replace('.', ',')
                           for v in res])

        csv_path = os.path.join(CSV_REPORTS_DIR, 'result-%s %s.csv' % (str(db_adapter), str(datetime.datetime.now())))

        with open(csv_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([''.join(['proc', str(i)]) for i in range(1, MAX_PROCESSES + 1)])
            for row in zip(*result):
                writer.writerow(row)

        print 'Finish!'


if __name__ == '__main__':
    r = ReportsCreator()
    r.make(get_adapter_from_command_line())