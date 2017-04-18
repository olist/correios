correios
========

.. image:: https://img.shields.io/pypi/v/correios.svg
    :target: https://pypi.python.org/pypi/correios
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/olist/correios.png
   :target: https://travis-ci.org/olist/correios
   :alt: Latest Travis CI build status

.. image:: https://coveralls.io/repos/github/olist/correios/badge.svg?branch=master
   :target: https://coveralls.io/github/olist/correios?branch=master
   :alt: Latest Coveralls coverage status

A client library for Brazilian Correios APIs (SIGEP and SRO) and services.


Installation
------------

.. code-block::

   $ pip install correios  # basic model support
   $ pip install correios[pdf]  # label and posting list pdf generation support
   $ pip install correios[client]  # support for SIGEP/SRO API client
   $ pip install correios[pdf,client]  # full installation
