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


Update Local WSDL Files
-----------------------

Local WSDL files are used to increase performance on SOAP requests. Enventually
you'll want to update them and withou having to update this lib.

If you want to maintain this files on a custom path you can pass the 'path'
option with the custom path. Don't use relative paths.

Just run on shell

.. code-block::

   $ update-correios-wsdl -p /path/to/your/custom/wsdl/folder

Arguments:
-p, --path : Custom path where wsdl files will be saved, note that this option
will have higher priority than the value of the envvar 'CORREIOS_WSDL_PATH'


Or you can use the method update_wsdl to do it.

.. code-block::

   from correios.update_wsdl import update_wsdl

   update_wsdl(path='/path/to/your/custom/wsdl/folder')

That's it!

