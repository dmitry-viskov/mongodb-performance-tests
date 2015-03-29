# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from json import dumps
from bottle import route, request, response, run, template, static_file, default_app
from mongodb_performance_tests.common import adapter_factory, get_all_available_adapters
from mongodb_performance_tests.settings import MAX_PROCESSES, WEBSERVER_HOST, WEBSERVER_PORT

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
            data[key] = ''.join([key, ' is unavailable'])

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

    for i in proc_count:
        res.append(atr.get_result_by_processes(test_id, i))
    return prepare_template('result', json_data=res, adapter_name=atr.get_name(),
                            labels=['proc count: %s' % i for i in proc_count])


@route('/compare/<proc_count:int>/')
def compare(proc_count=None):
    res = []
    labels=[]
    adapters=[]

    if not proc_count:
        proc_count = int(MAX_PROCESSES / 2)

    for adapter, test_id in dict(request.query).iteritems():
        atr = adapter_factory(adapter)
        res.append(atr.get_result_by_processes(test_id, proc_count))
        labels.append(' - '.join([adapter, "%d proc" % proc_count]))
        adapters.append(adapter)

    return prepare_template('compare', json_data=res, labels=labels,
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