#########################################
# Author         : Haibo Zhu             
# Email          : haibo.zhu@hotmail.com 
# created        : 2019-08-09 19:53 
# Last modified  : 2019-08-09 20:50
# Filename       : example_app.py
# Description    :                       
#########################################
from requests import get, put,post
import pprint
import json
from contextlib2 import contextmanager
from flask import Flask, render_template_string
from flask_bootstrap import Bootstrap
from pages import create_demo_page
from settings import *

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['API_URL'] = API_URL


@app.route('/')
def index():
    page = create_demo_page()
    print('page:{}'.format(page))
    return render_template_string(page)


if __name__ == '__main__':
    print('running')
    app.run(host='localhost', port=80, threaded=True)
