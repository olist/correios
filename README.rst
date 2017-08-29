correios
========

.. image:: https://img.shields.io/pypi/v/correios.svg
    :target: https://pypi.python.org/pypi/correios
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/olist/correios.png
   :target: https://travis-ci.org/olist/correios
   :alt: Latest Travis CI build status

.. image:: https://codecov.io/gh/olist/correios/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/olist/correios
   :alt: Latest coverage status

A client library for Brazilian Correios APIs (SIGEP and SRO) and services.


Installation
------------

.. code-block::

   $ pip install correios  # basic model support
   $ pip install correios[pdf]  # label and posting list pdf generation support
   $ pip install correios[api]  # support for SIGEP/SRO API client
   $ pip install correios[pdf,api]  # full installation
