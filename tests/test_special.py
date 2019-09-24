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
from flask import Flask, render_template_string,url_for
from flask_bootstrap import Bootstrap
from tests.settings import *
from components_client import *
app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['API_URL'] = API_URL


def webinput():
    with WebPage(default_url='index') as page:
        with page.add_child(WebInput()) as test:
            pass
    html = page.render()
    return render_template_string(html)

def webbtndropdowntoggle():
    with WebPage(default_url='index') as page:
        with page.add_child(WebBtnDropdownToggle(value='test',select_options=[{'name':'options1','href':'#'}])) as test:
            pass
    with test.on_event_w('select'):
        page.alert('"selected!"')

    html = page.render()
    return render_template_string(html)

classes=[]
classes.append((WebInput,webinput))
classes.append((WebBtnDropdownToggle,webbtndropdowntoggle))

@app.route('/')
def index():
    with WebPage(default_url='index') as page:
        for c in classes:
            with page.add_child(WebA(href='{{url_for(\''+c[0].__name__.lower()+'\')}}')) as a:
                with a.add_child(WebBtn(value=c[0].__name__)) as btn:
                    pass
            current_app.add_url_rule('/' + c[0].__name__, endpoint=c[0].__name__.lower(), view_func=c[1])


    html = page.render()
    print(pprint.pformat(html))
    return render_template_string(html)


if __name__ == '__main__':
    print('running')
    app.run(host='localhost', port=80, threaded=True)
