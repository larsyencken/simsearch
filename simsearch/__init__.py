# -*- coding: utf-8 -*-
#
#  __init__.py
#  simsearch
#
#  Created by Lars Yencken on 2011-10-02.
#  Copyright 2011 Lars Yencken. All rights reserved.
#

"""
The server for simsearch.
"""

import os

import flask

from mercurial import ui, hg, node

app = flask.Flask(__name__)
app.config.from_object('simsearch.settings')

if 'SIMSEARCH_SETTINGS' in os.environ:
    app.config.from_envvar('SIMSEARCH_SETTINGS')

@app.route('/help/')
def help():
    c = base_context()
    return flask.render_template('static/help.html', **c)

@app.route('/feedback/')
def feedback():
    c = base_context()
    return flask.render_template("static/feedback.html", **c)

@app.route('/about/')
def about():
    c = base_context()
    return flask.render_template("static/about.html", **c)

def base_context():
    c = {}
    c.update(mercurial_revision())
    c.update(site_settings())
    return c

def mercurial_revision():
    project_base = os.path.join(app.config['PROJECT_ROOT'], '..')
    repo = hg.repository(ui.ui(), project_base)
    fctx = repo.filectx(project_base, 'tip')

    return {'revision': {
                'short': node.short(fctx.node()),
                'number': fctx.rev(),
            }}

def site_settings():
    return {'settings': app.config, 'MEDIA_URL': app.config['MEDIA_URL']}
