mongodb-updates-performance-test
================================

Little utility for performance tests of concurrent updates in mongodb

Overview
========

This is a simple test that shows mongodb global lock detrimental effects on system performance.

Installation
============

The recommended way to use virtualenv to run these tests::

  mkdir venv && echo "Virtualenv directory" > venv/README
  virtualenv --no-site-packages --prompt="(mongodb-performance-tests)" venv
  source venv/bin/activate
  pip install -r requirements.txt

How to run it
=============

::

  source venv/bin/activate

  # to run performance test using MongoDB as database
  python -m mongodb_performance_tests.tool.run_test mongodb

  # to run performance test using MySQL as database
  python -m mongodb_performance_tests.tool.run_test mysql

  # get results in csv format
  python -m mongodb_performance_tests.tool.make_csv_report mongodb
  python -m mongodb_performance_tests.tool.make_csv_report mysql

  # run simple web site that show result of performance tests in graphics
  python -m mongodb_performance_tests.web.main


MySQL recommended settings
=============

::

  [mysqld]
  ...
  # 30-40% RAM
  key_buffer = 1024M
  ...
  # 70-80% RAM
  innodb_buffer_pool_size = 2048M
  ...
  # 1/4 of "innodb_buffer_pool_size" value
  innodb_log_file_size = 512M

