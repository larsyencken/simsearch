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
from cjktools import scripts
import mercurial.hg
import mercurial.ui
import mercurial.node
import simplejson
import mongoengine

import models

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

@app.route('/')
def index():
    "Renders the search display."
    kanji = flask.request.args.get('kanji', '')
    kanji_ok = _is_kanji(kanji)
    context = base_context()

    context.update({
            'kanji': kanji,
            'kanji_ok': kanji_ok,
        })
    if not kanji or not kanji_ok:
        # show the search dialog
        if kanji:
            context['error'] = 'Please enter a single kanji only as input.'
        return flask.render_template('search/index.html', **context)

    try:
        node = models.Node.objects.get(pivot=kanji)
    except mongoengine.queryset.DoesNotExist:
        context['error'] = u'Sorry, %s not found' % kanji
        return flask.render_template('search/index.html', **context)

    # make sure the path is ok
    path = flask.request.args.get('path', '')
    if not all(map(_is_kanji, path)):
        path = []

    path = list(path) + [kanji]
    neighbours = [n.kanji for n in sorted(node.neighbours, reverse=True)]
    neighbours = neighbours[:app.config['N_NEIGHBOURS_RECALLED']]

    context.update({'data': simplejson.dumps({
                    'kanji': kanji,
                    'tier1': neighbours[:4],
                    'tier2': neighbours[4:9],
                    'tier3': neighbours[9:],
                    'path': ''.join(path),
                })})
    return flask.render_template('search/display.html', **context)

@app.route('/translate/<kanji>/')
def translate(kanji):
    "Updates the query model before redirecting to the real translation."
    kanji = kanji or flask.request.args.get('kanji')
    if not _is_kanji(kanji):
        flask.abort(404)

    path = flask.request.args.get('path')
    if path and len(path) > 1 and all(map(_is_kanji, path)) \
            and path.endswith(kanji):
        models.Node.update(path)
        models.Trace.log(flask.request, path)

    t = models.Translation.objects.get(kanji=kanji)
    if t is None:
        flask.abort(404)

    c = base_context()
    c['translation'] = t
    return flask.render_template('translate/kanji.html', **c)

@app.route('/search/<pivot>/')
def search_json(pivot):
    "Returns the search display data as JSON."
    pivot = pivot or flask.request.args.get('pivot')
    node = models.Node.objects.get(pivot=pivot)
    neighbours = [n.kanji for n in sorted(node.neighbours, reverse=True)]
    neighbours = neighbours[:app.conf['N_NEIGHBOURS_RECALLED']]

    return flask.jsonify(
            pivot_kanji=pivot,
            tier1=neighbours[:4],
            tier2=neighbours[4:9],
            tier3=neighbours[9:],
        )

def _is_kanji(kanji):
    return isinstance(kanji, unicode) and len(kanji) == 1 \
            and scripts.script_type(kanji) == scripts.Script.Kanji

def base_context():
    c = {}
    c.update(mercurial_revision())
    c.update(site_settings())
    return c

def mercurial_revision():
    project_base = os.path.join(app.config['PROJECT_ROOT'], '..')
    repo = mercurial.hg.repository(mercurial.ui.ui(), project_base)
    fctx = repo.filectx(project_base, 'tip')

    return {'revision': {
                'short': mercurial.node.short(fctx.node()),
                'number': fctx.rev(),
            }}

def site_settings():
    return {'settings': app.config, 'MEDIA_URL': app.config['MEDIA_URL']}
