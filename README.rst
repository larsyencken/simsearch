SimSearch
=========

:Author: Lars Yencken <lars@yencken.org>
:Date: 21st Jan 2011

Overview
--------

SimSearch is a dictionary search-by-similarity interface for Japanese kanji,
providing a nice front-end for Kanjidic. It lets you find a kanji you don't
know, using kanji that are visually similar.

.. image:: http://files.gakusha.info/simsearch/homepage/ss-example-med.png

If you're viewing this source code, you should be a developer, or someone at
least a little comfortable with Python.

Developing/running
------------------

This is a quick guide to getting SimSearch up and running locally.

Dependencies
~~~~~~~~~~~~

SimSearch uses MongoDB as its database backend. If you don't already have it,
install MongoDB first. By default, it will create and use a database called
``simsearch`` in MongoDB.

Next, you need Python (2.6/2.7), pip and virtualenv. Then you can install the
necessary packages in an environment for simsearch::

    $ pip -E ss-env install ./simsearch

Occasionally a dependency will fail to install cleanly (e.g. NLTK). In that
case, you will need to download a package for it, enter the virtual
environment and install the package from there::

    $ tar xfz nltk-v2.08b.tgz
    $ cd nltk-v2.08b
    $ source /path/to/simsearch/ss-env/bin/activate
    (ss-env) $ python setup.py install

Building and running
~~~~~~~~~~~~~~~~~~~~

Once installed, build the database with::

    $ python -m simsearch.models
    Building similarity matrix
    Building neighbourhood graph

You can then run the debug server with the command ``simsearch.py``. The
server will be available at http://localhost:5000/.

Deploying
---------

Please see Flask documentation around deployment. Feel free to email me as
well, if you have any issues.

