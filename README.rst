===============================
Crawler by David Avs
===============================

Simple crawler generating a sitemap.

Features
--------

* Crawls a single domain starting from the specified URL
* Outputs JSON sitemap
* For each page lists links to other pages within the domain, external links and images
* Writes to stdout or to a specified file
* Detailed logging for debug purposes


Installation
------------

Install as a standard Python module::

    python setup.py install

If you are using ``pip``, the module can be installed directly from GitHub::

    pip install https://github.com/avsd/davidavscrawler/archive/master.zip#davidavscrawler==0.1.0

Usage
-----

The package installs a command line script ``crawl``::

    usage: crawl [-h] [--verbose] url [file]

    Simple website parser that parses a single domain and creates a simple JSON
    sitemap.

    positional arguments:
    url            Starting URL to be parsed.
    file           File to write the JSON output (default: stdout).

    optional arguments:
    -h, --help     show this help message and exit
    --verbose, -v  Enable verbose logging to stderr

.. note::

    This version of script dumps raw JSON, which is difficult to read. In order
    to view the sitemap in readable form, you can use Python JSON tool::

        $ crawl http://davidavs.com | python -mjson.tool




Output format
^^^^^^^^^^^^^

The output format is JSON list of items. Each item contains following fields:

* ``url`` - absolute URL of the crawled page
* ``level`` - depth level of the current page from the initial one
* ``pages`` - list of pages (lnks within the domain)
* ``links`` - list of external links
* ``images`` - list of images used in the page

Development and Testing
-----------------------

To run unit tests use the command::

    make test

To run tests against all supported Python versions, use the command::

    make test-all

For more information about development see `CONTRIBUTING.rst`


Architecture
^^^^^^^^^^^^

The crawler is based on Scrapy (see http://scrapy.org/), using its built-in link extractor
and JSON generator. It's implemented as a command line tool using Argparse module
(see https://docs.python.org/2.7/library/argparse.html).

The project layout has been created using a cookiecutter template
(see http://cookiecutter.readthedocs.org/en/latest/readme.html#available-cookiecutters).


Limitations
-----------

* In this version static content returned by the crawler is limited to ``<img>`` tag images.
  CSS images and other types of objects are not supported.
* The standard Scrapy link extractor used in this project modifies order of query string parameters
  in the URLs, and makes them canonical (e.g. adds "=" where it's missing).
  Therefore, links returned by the crawler may differ from the real links on crawled pages.

TODO
----

* Add more unit tests
* Add support for other versions of Python (currently only tested for Python 2.7)
