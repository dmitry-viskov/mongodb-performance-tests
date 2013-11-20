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
  python -m mongodb_performance_tests.tool.run_test
  python -m mongodb_performance_tests.tool.make_csv_report