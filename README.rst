mongodb-updates-performance-test
================================

Little utility for performance tests of concurrent updates in mongodb

Overview
========

This is a simple test that shows mongodb global lock detrimental effects on system performance. You could compare updates
operations in MongoDB with the same operations in other DB systems (MySQL out of the box, but you could implement adapter for
every other database and compare MongoDB updates with it).

Requirements
============

* Python 2.6 or 2.7
* virtualenv

Installation
============

The recommended way is to use virtualenv to run these tests:

.. code-block:: bash

  mkdir venv && echo "Virtualenv directory" > venv/README
  virtualenv --no-site-packages --prompt="(mongodb-performance-tests)" venv
  source venv/bin/activate
  pip install -r requirements.txt
  
After you have created virtualenv directory you should update settings.py file to implement your own enviroment settings:

.. code-block:: bash

  vim mongodb_performance_tests/settings.py

How to run it
=============

.. code-block:: bash
  
  source venv/bin/activate

  # to run performance test using MongoDB as database
  cd mongodb_performance_tests/tool
  python run_test.py --adapter mongodb --name mongodb_test_num_42

  # to run performance test using MySQL as database
  cd mongodb_performance_tests/tool
  python run_test.py --adapter mysql --name mysql_test_num_42
  
  # please, use "help" key to know all options of running tests command
  python run_test.py --help

  # get results in csv format
  cd mongodb_performance_tests/tool
  python make_csv_report.py --report_dir ~/Temp --adapter mongodb --test_name mongodb_test_num_42
  python make_csv_report.py --report_dir ~/Temp --adapter mysql --test_name mysql_test_num_42

  # please, use "help" key to know all options of report creation command
  python make_csv_report.py --help

  # run simple web site that show result of performance tests in graphics
  python mongodb_performance_tests/web/main.py

MySQL recommended settings
=============

.. code-block:: bash

  [mysqld]
  ...
  # uses only in the case MyISAM tables
  # but this benchmark should be done with InnoDB engine so
  # this option isn't important for us
  key_buffer = 32M
  ...
  # 70-80% RAM. It's used
  innodb_buffer_pool_size = 2048M
  ...
  # 1/4 of "innodb_buffer_pool_size" value
  innodb_log_file_size = 512M
  ...
  # the log buffer is written out to the file at each commit,
  # but the flush to disk operation is not performed on it
  innodb_flush_log_at_trx_commit = 2

