# -*- coding: utf-8 -*-

import os
from bottle import route, run, template, static_file
from ..common import adapter_factory
from ..settings import MAX_PROCESSES

CURRENT_SCRIPT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'views')
PATH_FOR_STATIC_RES = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')


def prepare_template(tpl, **kwargs):
    return template(tpl, template_lookup=[CURRENT_SCRIPT_PATH], **kwargs)

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=PATH_FOR_STATIC_RES)

@route('/')
def index():
    return prepare_template('main_template')

@route('/result/<adapter>')
def result(adapter):
    atr = adapter_factory(adapter)
    res = []
    proc_count = [1]

    if MAX_PROCESSES > 2:
        middle_proc_count = int(MAX_PROCESSES / 2)
        if middle_proc_count > 1:
            proc_count.append(middle_proc_count)
        proc_count.append(MAX_PROCESSES)

    for i in proc_count:
        res.append(atr.get_result_by_processes(i))
    return prepare_template('result_template', json_data=res, adapter_name=atr.get_name(),
                            labels=['proc count: %s' % i for i in proc_count])

run(host='localhost', port=8080)