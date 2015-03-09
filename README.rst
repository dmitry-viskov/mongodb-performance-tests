mongodb-updates-performance-test
================================

Little utility for performance tests of concurrent updates in mongodb

Overview
========

This is a simple test that shows mongodb global lock detrimental effects on system performance. You could compare updates
operations in MongoDB with the same operations in other DB systems (MySQL out of the box, but you could implement adapter for
every other database and compare MongoDB updates with it).

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
  python mongodb_performance_tests/tool/run_test.py --adapter mongodb --name mongodb_test_num_42

  # to run performance test using MySQL as database
  python mongodb_performance_tests/tool/run_test.py --adapter mysql --name mysql_test_num_42

  # get results in csv format
  python mongodb_performance_tests/tool/make_csv_report.py --report_dir=/home/user/mongo.csv --adapter=mongodb --test_name=mongodb_test_num_42
  python mongodb_performance_tests/tool/make_csv_report.py --report_dir=/home/user/mysql.csv --adapter=mysql --test_name=mongodb_test_num_42

  # run simple web site that show result of performance tests in graphics
  python mongodb_performance_tests/web/main.py


MySQL recommended settings
=============

::

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

