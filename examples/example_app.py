from requests import get, put,post
import pprint
import json
from contextlib2 import contextmanager
from flask import Flask, render_template_string
from flask_bootstrap import Bootstrap
from examples.pages import create_demo_page
from examples.settings import *

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['API_URL'] = API_URL

@app.route('/')
def demo():
    return create_demo_page()

if __name__ == '__main__':
    print('running')
    app.run(port=8080)