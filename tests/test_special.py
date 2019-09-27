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

def webinput_post():
    pass

def webinput():
    with WebPage(default_url="index") as page:
        with page.add_child(WebInput())as test:
            pass
    html = page.render()
    return render_template_string(html)

def webbtndropdowntoggle_post():
    return ""

def webbtndropdowntoggle():
    with WebPage(default_url="index") as page:
        with page.add_child(WebBtnDropdownToggle(value="'test'",select_options=[{'name':'options1','href':'#'},
                                                                              {'name':'options2','href':'#'}])) as test:
            pass
    with test.on_event_w('select'):
        page.alert('"selected!"')

    html = page.render()
    return render_template_string(html)

def oogeneralselector_post():
    return OOGeneralSelector.on_post()

def oogeneralselector():
    with WebPage(default_url="index") as page:
        '''
        with page.add_child(OOGeneralSelector(btns=[{'name':'test1','select':'','options':[{'name':'test1-options1','href':'#'},
                                                                                            {'name':'test1-options2', 'href':'#'}]},
                                                    {'name':'test2','select':'','options':[{'name':'test2-options1','href':'#'},
                                                                                            {'name':'test2-options2','href':'#'}]},
                                                    {'name':'test3','select':'','options':[{'name':'test2-options1','href':'#'},
                                                                                            {'name':'test2-options2','href':'#'}]}
                                                    ])) as test:
        '''
        with page.add_child(OOGeneralSelector()) as test:
            pass


    with test.on_event_w(event="select"):
        test.alert('"selected! a:" + a.text() + ", btn name: " + btn.attr("data-value") ')
        with Var(name="data", parent=test) as data:
            test.val()
        with test.post_w(url=url_for('oogeneralselector_post')):
            test.alert("'post success!'")
            test.val('data')

    html = page.render()
    return render_template_string(html)

def oodatepicker():
    with WebPage(default_url="index") as page:
        with page.add_child(OODatePicker()) as test:
            pass

    with page.add_child(WebBtn(value='测试-周清除')) as test_btn_week:
        pass
    with page.add_child(WebBtn(value="测试-月清除")) as test_btn_month:
        pass
    with page.add_child(WebBtn(value='测试-日清除')) as test_btn_day:
        pass
    with page.add_child(WebBtn(value='测试-清除')) as test_btn_clear:
        passd

    with test_btn_week.on_event_w(event="click"):
        test.val("{'select':'周', 'start_date': new Date, 'end_date': new Date}")

    with test_btn_month.on_event_w(event="click"):
        test.val("{'select':'月', 'start_date': new Date, 'end_date': new Date}")

    with test_btn_day.on_event_w(event="click"):
        test.val("{'select':'日', 'start_date': new Date, 'end_date': new Date}")

    '''
    with test.on_event_w(event="select"):
        test.alert('"selected! a:" + a.text() + ", btn name: " + btn.attr("data-value") ')
        with Var(name="data", parent=test) as data:
            test.val()
        with test.post_w(url=url_for('oogeneralselector_post')):
            test.alert("'post success!'")
            test.val('data')
    '''

    html = page.render()
    return render_template_string(html)

def oodatepicker_post():
    return oodatepicker.on_post()

classes=[]
classes.append((WebInput,webinput, webinput_post))
classes.append((WebBtnDropdownToggle,webbtndropdowntoggle,webbtndropdowntoggle_post))
classes.append((OOGeneralSelector, oogeneralselector, oogeneralselector_post))
classes.append((OODatePicker, oodatepicker, oodatepicker_post))

@app.route('/')
def index():
    with WebPage(default_url="index") as page:
        for c in classes:
            with page.add_child(WebA(href="{{url_for('"+c[0].__name__.lower()+"')}}")) as a:
                with a.add_child(WebBtn(value=c[0].__name__)) as btn:
                    pass
            current_app.add_url_rule('/' + c[0].__name__, endpoint=c[0].__name__.lower(), view_func=c[1])
            current_app.add_url_rule('/' + c[0].__name__ + '_post', endpoint=c[0].__name__.lower() + '_post', view_func=c[2], methods=['POST'])
    html = page.render()
    print(pprint.pformat(html))
    return render_template_string(html)


if __name__ == '__main__':
    print('running')
    app.run(host='localhost', port=80, threaded=True)
