from __future__ import absolute_import, division, print_function

from flask import Flask
import os
from flask.ext import restful
from werkzeug.debug import DebuggedApplication

app = Flask(__name__)

if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

api_v1 = restful.Api(app, prefix='/v1')

# noinspection PyUnresolvedReferences
import play.v1

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
