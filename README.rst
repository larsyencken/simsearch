SimSearch
=========

:Author: Lars Yencken <lars@yencken.org>
:Date: 12th Feb 2011

Overview
--------

SimSearch is a dictionary search-by-similarity interface for Japanese kanji,
providing a nice front-end for Kanjidic. If you're viewing this source code,
you should be a developer, or someone at least a little comfortable with
Python.

Developing/running
------------------

This is a quick guide to getting SimSearch up and running locally.

Dependencies
~~~~~~~~~~~~

SimSearch uses MongoDB as its database backend. If you don't already have it,
install MongoDB first.

Next, you need Python (2.6/2.7), pip and virtualenv. Then you can install the
necessary packages in an environment for simsearch::

    $ pip -E ss-env install $(cat requirements.txt)

Occasionally a dependency will fail to install cleanly (e.g. NLTK). In that
case, you will need to download a package for it, enter the virtual
environment and install the package from there::

    $ tar xfz nltk-v2.08b.tgz
    $ cd nltk-v2.08b
    $ source /path/to/simsearch/ss-env/bin/activate
    (ss-env) $ python setup.py install


Building
~~~~~~~~

Once you have all the packages, you are good to build! Source the environment
variables needed, and get to work.

Firstly, we build the Cython module using Scons::

    $ scons

Secondly, we set the database building::

    $ source environ_vars.sh
    (ss-env) $ ./simsearch/manage.py build
    Building similarity matrix
    Building neighbourhood graph

Now you're done, and can run it locally::

    $ source environ_vars.sh
    (ss-env) $ ./simsearch/manage.py runserver

The server will now be available at http://127.0.0.1:8000/.

Deploying
---------

Please see standard Django deployment docs for installing this on a web server, e.g. using Apache and mod_python.

