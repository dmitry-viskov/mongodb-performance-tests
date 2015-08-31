mongodb-updates-performance-test
================================

Little utility for performance tests of concurrent updates in mongodb

Overview
========

This is the simple test that shows mongodb global lock detrimental effects on system performance. You could compare updates
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
  
After you have created virtualenv directory you should create your settings.py file to implement your own enviroment settings:

.. code-block:: bash

  cd mongodb_performance_tests
  cp settings.example.py settings.py
  vim settings.py

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

  # to run performance test using PostgreSQL as database
  cd mongodb_performance_tests/tool
  python run_test.py --adapter postgresql --name postgresql_test_num_42
 
  # please, use "help" key to know all options of running tests command
  python run_test.py --help

  # get results in csv format
  cd mongodb_performance_tests/tool
  python make_csv_report.py --report_dir ~/Temp --adapter mongodb --test_name mongodb_test_num_42
  python make_csv_report.py --report_dir ~/Temp --adapter mysql --test_name mysql_test_num_42
  python make_csv_report.py --report_dir ~/Temp --adapter postgresql --test_name postgresql_test_num_42

  # please, use "help" key to know all options of report creation command
  python make_csv_report.py --help

  # run simple web site that show result of performance tests in graphics
  python mongodb_performance_tests/web/main.py

MySQL recommended settings
=============

As you know you could use any other database to check update operations performance. By default you can do it using MySQL database.
But before you do it please make sure that you have configured your database environment. Because tests with default settings don't show anything.
It is ugly way. Just below you could see recommended settings for MySQL database (they are oriented on c3.2xlarge Amazon instance:
15.0 GB RAM, 8 vCPU, 160 Gb SSD).

.. code-block:: bash

  [mysqld]
  ...
  max_connections = 10000
  ...
  query_cache_limit = 32M
  query_cache_size  = 1024M
  ...
  # recommended to use 70-80% of RAM
  innodb_buffer_pool_size = 8192M
  ...
  # very-very important param in case situation with a lot of writes
  innodb_log_file_size = 512M
  ...
  innodb_thread_concurrency = 16
  ...
  thread_cache = 32
  thread_cache_size = 16
  ...
  # the log buffer is written out to the file at each commit,
  # but the flush to disk operation is not performed on it
  innodb_flush_log_at_trx_commit = 2
  ...
  # uses only in the case MyISAM tables
  # but this benchmark should be done with InnoDB engine so
  # this options isn't important for us
  key_buffer = 32M
  key_buffer_size = 3072M
