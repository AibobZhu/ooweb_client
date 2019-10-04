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
from datetime import datetime

from flask import Flask, render_template_string,url_for
from flask_bootstrap import Bootstrap
from tests.settings import *
from components_client import *
app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['API_URL'] = API_URL

def webbtn_post():
    pass

def webbtn():
    with WebPage(default_url="index") as page:
        with page.add_child(WebBtn(value='测试')) as test:
            pass

    with test.on_event_w('click'):
        test.alert(' $(event.target).text().trim() + " clicked!" ')

    return render_template_string(page.render())

def webinput_post():
    pass

def webinput():

    with WebPage() as page:
        with page.add_child(WebInput(value=datetime.datetime.now().strftime('%Y %m %d'))) as test1:
            pass
        with page.add_child(WebInput(value=datetime.datetime.now().strftime('%Y %m %d'))) as test2:
            pass

    # response change event of input1, then sync value to input2
    with test1.on_event_w(event='change'):
        test1.alert('"Input " + $(event.currentTarget).attr("id") + " Changed!"')
        with LVar(parent=page) as test1_data:
            test1.val()
        test2.val(test1_data)

    # response change event of input2, then sync value to input1
    with test2.on_event_w(event='change'):
        test2.alert('"Input " + $(event.currentTarget).attr("id") + " Changed!"')
        with LVar(parent=page) as test2_data:
            test2.val()
        test1.val(test2_data)

    # set value to input1, expect an alert pop up, jquery actually not pop, fixed in WebInput.val() by trigger change event manually
    test1.val("new Date()")

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
        with page.add_child(WebBtnGroupVertical()) as toolbar1:
            with toolbar1.add_child(OOGeneralSelector(styles={'display':'flex'})) as test:
                pass

    with test.on_event_w(event="change"):
        test.alert('"OOGeneralSelector changed by " + $(event.target).attr("data-value")')
        with Var(var_name="test_data", parent=test) as test_data:
            test.val()
        with test.post_w(url=url_for('oogeneralselector_post'), data=test_data):
            test.alert("'post success!'")
            test.val('data')

    html = page.render()
    return render_template_string(html)

def oodatepicker():

    with WebPage() as page:
        with page.add_child(OODatePicker()) as test1:
            pass
        with page.add_child(OODatePicker()) as test2:
            pass

    # process change event of OODatePicker test1, pops up alerts to show which widget triggered the change event
    # keep OODatePicker test2 the same
    with test1.on_event_w(event='change'):
        test1.add_scripts("if($(event.target).is('button')){\n")
        test1.add_scripts(
            "    alert('OODatePicker: test1 is changed by button, new text is ' + $(event.target).text());\n")
        test1.add_scripts("}else{\n")
        test1.add_scripts(
            "    alert('OODatePicker: test1 is changed by input, new value is ' + $(event.target).val());\n")
        test1.add_scripts("};\n")
        test2.val(value='data')

    # process change event of OODatePicker test2, keep OODatePicker test1 the same
    with test2.on_event_w(event='change'):
        test1.val(value='data')

    # trigger change event by programming, expect an alert of change event poping up
    # test1.trigger_event(event='change')

    # Add the buttons to set values into datepicker 1 and expect poping up an alert of change event
    with page.add_child(WebBtn(value='测试:周清除')) as test_btn_week:
        pass
    with page.add_child(WebBtn(value="测试:月清除")) as test_btn_month:
        pass
    with page.add_child(WebBtn(value='测试:日清除')) as test_btn_day:
        pass

    # set value into test1
    with test_btn_week.on_event_w(event="click"):
        test1.val("{'select':'周', 'start_date': new Date, 'end_date': new Date}")
    with test_btn_month.on_event_w(event="click"):
        test1.val("{'select':'月', 'start_date': new Date, 'end_date': new Date}")
    with test_btn_day.on_event_w(event="click"):
        test1.val("{'select':'日', 'start_date': new Date, 'end_date': new Date}")


    html = page.render()
    return render_template_string(html)

def oodatepicker_post():
    return OODatePicker.on_post()

classes=[]
classes.append((WebBtn,webbtn,webbtn_post))
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
