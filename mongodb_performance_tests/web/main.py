# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from json import dumps
from bottle import route, request, run, template, static_file, default_app, abort
from mongodb_performance_tests import MAX_PROCESSES, WEBSERVER_HOST, WEBSERVER_PORT
from mongodb_performance_tests.common import adapter_factory, get_all_available_adapters

CURRENT_SCRIPT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'views')
PATH_FOR_STATIC_RES = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')

app = application = default_app()


def prepare_template(tpl, **kwargs):
    return template(tpl, template_lookup=[CURRENT_SCRIPT_PATH], **kwargs)


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=PATH_FOR_STATIC_RES)


@route('/')
def index():
    data = {}

    available_adapters_cnt = 0
    adps = get_all_available_adapters()

    for key, ad in adps.iteritems():
        if ad:
            data[key] = ad.get_available_tests()
            available_adapters_cnt += 1
        else:
            data[key] = False

    may_compare = available_adapters_cnt > 1

    return prepare_template('main', adapters=[i for i,v in adps.iteritems() if v],
                            adapters_tests_json=dumps(data),
                            available_tests=data,
                            may_compare=may_compare)


@route('/result/<adapter>/<test_id>')
def result(adapter, test_id):
    atr = adapter_factory(adapter)
    res = []
    proc_count = [1]

    if MAX_PROCESSES > 2:
        middle_proc_count = int(MAX_PROCESSES / 2)
        if middle_proc_count > 1:
            proc_count.append(middle_proc_count)
        proc_count.append(MAX_PROCESSES)

    test_name = atr.get_test_name_by_id(test_id)
    if not test_name:
        abort(404, "Test with id %s not found" % str(test_id))

    for i in proc_count:
        res.append(atr.get_result_by_processes(test_id, i))
    return prepare_template('result', json_data=res, graph_title=': '.join([atr.get_name(), test_name]),
                            labels=['proc count: %s' % i for i in proc_count])


@route('/compare/<proc_count:int>')
def compare(proc_count=None):
    res = []
    labels = []
    adapters = []

    if not proc_count:
        proc_count = int(MAX_PROCESSES / 2)

    for t, adapter_and_test_id in dict(request.query).iteritems():
        adapter, test_id = tuple(adapter_and_test_id.split('|'))
        atr = adapter_factory(adapter)
        test_name = atr.get_test_name_by_id(test_id)
        if not test_name:
            abort(404, "Test with id %s not found" % str(test_id))

        res.append(atr.get_result_by_processes(test_id, proc_count))
        labels.append("%s (%s) %d proc" % (adapter, test_name, proc_count))
        adapters.append("%s (%s)" % (adapter, test_id))

    return prepare_template('compare', json_data=res, labels=dumps(labels),
                            current_proc_count=proc_count, max_proc=MAX_PROCESSES,
                            graph_title="Compare %s" % ', '.join(adapters))


class StripPathMiddleware(object):
    """
    Get that slash out of the request
    """
    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)


if __name__ == '__main__':
    run(app=StripPathMiddleware(app),
        host=WEBSERVER_HOST,
        port=WEBSERVER_PORT)