from requests import get, put,post
import pprint
import json
from contextlib2 import contextmanager
from flask import Flask, render_template_string
from flask_bootstrap import Bootstrap
from examples.pages import create_demo_page
import api
from ooweb_client.examples.settings import *

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
api.create_api(app)

@app.route('/')
def demo():
    page = create_demo_page()
    print('html_page:\n{}'.format(pprint.pformat(page)))
    return render_template_string(page)

if __name__ == '__main__':
    print('running')
    app.run(port=8080)


