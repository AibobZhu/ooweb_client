#########################################
# Author         : Haibo Zhu             
# Email          : haibo.zhu@hotmail.com 
# created        : 2019-08-09 20:19 
# Last modified  : 2019-08-09 20:19
# Filename       : components_client.py
# Description    :                       
#########################################
from interfaces import *

from flask import current_app, render_template_string, request, jsonify
import uuid
import pprint
import inspect
from requests import post
from contextlib2 import contextmanager
from share import create_payload, extract_data, APIs, _getStr, randDatetimeRange
import sys, os
import datetime
from flask_sqlalchemy import SQLAlchemy
import json
from test_class import *
import copy
import random

sys.setrecursionlimit(2000)


class ClientBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def id(self):
        pass

    @abc.abstractmethod
    def add_context(self, context):
        pass

    @abc.abstractmethod
    def _get_objcall_context(self,func,caller_id,params):
        pass

    def context_call(self, params):
        context = self._get_objcall_context(func='add_context', caller_id=self.id(), params=params)
        self.add_context(context)
        return context

    def func_call(self, params):
        context = self._get_objcall_context(func=inspect.stack()[1][3], caller_id=self.id(), params=params)
        context['sub_context'] = []
        self.add_context(context)
        return context

    def with_call(self, params):
        context = self._get_objcall_context(func='with', caller_id=self.id(), params={'function': inspect.stack()[1][3],
                                                                                      'params': params})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])

    def enter_call(self, params={}):
        context = self._get_objcall_context(func='with', params={'obj_id': self.id()})
        context['sub_context'] = []
        self.add_context(context)
        self._mycont.append(context)
        self._push_current_context(context['sub_context'])


'''
TODO: try with eval, just pass the function calling and express in string, then execute with 'eval' on server side
'''

class Action(CommandInf, ActionInf, Test, ClientBase):

    @contextmanager
    def if_w(self):
        params = {}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

    @contextmanager
    def else_w(self):
        params = {}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

    def equal(self,right, left=None):
        params = {'right': right, 'left':left}
        self.func_call(params=params)

    def for_w(self):
        raise NotImplementedError

    def is_js(self):
        raise NotImplementedError

    def set_js(self, js_):
        params = {'js_':js_}
        self.func_call(params=params)

    def is_condition(self):
        params = {'cond': cond}
        self.func_call(params=params)

    def set_condition(self, cond):
        params = {'cond': cond}
        self.func_call(params=params)

    @contextmanager
    def condition_w(self):
        params = {}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

    @contextmanager
    def cmds_w(self):
        params = {}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

    def has_class(self, class_):
        raise NotImplementedError

    def add_class(self, class_):
        params={'class_':class_}
        return self.func_call(params)

    def remove_class(self, class_):
        params={'class_':class_}
        return self.func_call(params)

    def add_attrs(self,attrs):
        params = {'attrs': attrs}
        return self.func_call(params)

    def remove_attrs(self, attrs):
        params = {'attrs', attrs}
        return self.func_call(params)

    @classmethod
    def on_post(cls):
        '''
        The process function to response the post request from the WebComponent itself
        TODO: Query data by user model

        :return: jsonify({'status':'success','data': data})
        '''
        r = json.loads(request.form.get('data'))
        return {"status": "sucess", 'data': r}
    
    @contextmanager
    def post_w(self, url=None, data=None, success=None):
        '''
        context = self._get_objcall_context(func='with', caller_id=self.id(), params={'function': inspect.stack()[0][3], 'params': {'url':url, 'data':data, 'success':success}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        '''
        params = {'url':url, 'data':data, 'success':success}
        self.with_call(params)
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()

    def alert(self, message=''):
        params = {'message': message}
        return self.func_call(params)
        
    def execute_list_name(self, action_name):
        params = {'action_name': action_name}
        return self.func_call(params)

    @contextmanager
    def on_event_w(self,event,filter=''):
        '''
        context = self._get_objcall_context(func='with', caller_id=self.id(),
                                            params={'function': inspect.stack()[0][3], 'params': {'event':event,'filter':filter}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        '''
        params = {'event':event,'filter':filter}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

    def stop_event(self,event,filter='',stop=False):
        params = {'event': event, 'filter':filter, 'stop': stop}
        self.func_call(params)

    def trigger_event(self,event):
        params = {'event': event}
        self.func_call(params)

    def val(self,value=''):
        params = {'value': value}
        self.func_call(params)

    def empty(self):
        params = {}
        self.func_call(params)

    def disable(self, disable):
        params = {'disable': disable}
        self.func_call(params)
    
    def _example_data(cls):
        raise NotImplementedError

    def add_url_rule(cls, app, extend=[]):
        if extend:
            for e in extend:
                if len(e) == 3:
                    app.add_url_rule(e[0], e[1], methods=e[2])
                elif len(e) == 2:
                    app.add_url_rule(e[0], e[1])
                else:
                    raise RuntimeError


class Format(BootstrapInf, FormatInf, ClientBase):

    def pad(self, pad=None):
        raise NotImplementedError

    def margin(self, margin=None):
        raise NotImplementedError

    def width(self, width=None):
        raise NotImplementedError

    def height(self, height=None):
        params = {'height': height}
        return self.func_call(params=params)

    def align(self, align=None):
        raise NotImplementedError

    def value(self, value=None):
        raise NotImplementedError

    def color(self, color=None):
        raise NotImplementedError

    def font(self, font=None):
        raise NotImplementedError

    def attrs(self, klass=None):
        raise NotImplementedError

    def attrs_str(self):
        raise NotImplementedError

    def add_attrs(self, att):
        raise NotImplementedError

    def remove_att(self, att):
        raise NotImplementedError

    def classes(self, classes=None):
        raise NotImplementedError

    def classes_str(self):
        raise NotImplementedError

    def add_class(self, class_):
        params = {'class_':class_}
        return self.func_call(params=params)

    def remove_class(self, class_):
        params = {'class_':class_}
        return self.func_call(params=params)

    def check_col_name(self, col):
        raise NotImplementedError

    def check_align(self, align):
        raise NotImplementedError

    def offset(self, offset=[]):
        raise NotImplementedError

    def get_offset_name(self, offset):
        raise NotImplementedError

    def _get_width_name(self, width):
        raise NotImplementedError

    def base_context(self):
        raise NotImplementedError

    def fix_cmd(self, cmd):
        raise NotImplementedError

    def has_class(self, class_):
        raise NotImplementedError

    def is_width(self, width):
        raise NotImplementedError

    def set_width(self, width):
        raise NotImplementedError

    def remove_width(self, width):
        raise NotImplementedError

    def remove_style(self, style):
        raise NotImplementedError

    def styles(self, style=None):
        raise NotImplementedError

    def styles_str(self):
        raise NotImplementedError

    def border_radius(self, radius=None):
        params = {'radius': radius}
        self.func_call(params)


class WebComponent(ComponentInf, ClientInf, ClientBase):

    _context = None
    _cur_context_stack = []

    @classmethod
    def _set_context(cls, context):
        WebComponent._context = context
        WebComponent._cur_context_stack=[WebComponent._context]

    def _get_objcall_context(self, func, caller_id=None, params=None, sub_context=[]):
        def convert_param_obj(params):
            if isinstance(params, str):
                print("error: params is instance of str")
            for k,v in params.items():
                if k == 'params':
                    convert_param_obj(v)
                if isinstance(v, WebComponent):
                    params[k] = {'obj_id':v.id()}
        convert_param_obj(params)
        return {
            'function': func,
            'caller_id': caller_id,
            'params': params,
            'sub_context': sub_context
        }

    def __init__(self, test=False, **kwargs):
        super().__init__(test=test,**kwargs)
        if 'id' in kwargs:
            self._id = kwargs['id']
        else:
            self._id = self.id()

        if 'name' in kwargs:
            self._name = kwargs['name']
        else:
            self._name = self.name()

        self._parent = None
        if 'parent' in kwargs:
            self._parent = kwargs['parent']

        self._children = set()
        if 'children' in kwargs:
            self._children = kwargs['children']

        kwargs['name'] = self.name()
        kwargs['id'] = self.id()
        if hasattr(self,'_nav_items'):
            kwargs['nav'] = self._nav_items
        if self.__class__.__name__.find("WebPage") != 0:
            kwargs['test'] = test
        else:
            kwargs['test'] = False

        if hasattr(self, '_value'):
            kwargs['_value'] = self._value

        context = self._get_objcall_context(func=self.type_(), params=kwargs)
        #self._mycont = self.add_context(context)
        self._mycont = [context]
        self.add_context(context)

    def add_app(self):
        if hasattr(self, "app") and self.app:
            self._api = self.app.config['API_URL'] + APIs['render'].format('v1.0')
        else:
            self._api = current_app.config['API_URL'] + APIs['render'].format('v1.0')

    def __enter__(self):
        '''
        context = self._get_objcall_context(func='with', params={'obj_id':self.id()})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        '''
        self.enter_call()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print('Error, {}, {}, {} '.format(exc_type, exc_val, exc_tb))
        self._pop_current_context()
        return False

    def name(self, name=None):
        if not name:
            if not hasattr(self, '_name') or not self._name:
                self._name = self.__class__.__name__ + '_' + self.id()
            return self._name
        else:
            self._name = name

    def id(self, _id=None):
        if not _id:
            if not hasattr(self, '_id') or not self._id:
                self._id = str(uuid.uuid4()).split('-')[0]
            return self._id
        else:
            self._id = _id

    def children(self, children=[]):
        if not children:
            return self._children
        else:
            self._children = children

    def add_child(self, child=None, child_id=None, objs=None):
        assert(child)
        assert(not child_id)
        assert (not objs)
        self._children.add(child)
        child._parent = self
        params = {'child_id': child.id()}
        self.func_call(params)
        return  child

    def remove_child(self,child=None, child_id=None,objs=None):
        pass

    def empty_children(self):
        self._children.clear()

    def parent(self, parent=None):
        raise NotImplementedError

    def module(self):
        raise NotImplementedError

    def type_(self):
        return self.__class__.__name__

    def url(self, url=None):
        raise NotImplementedError
    
    def url_for(self, context):
        pass

    def render(self):
        '''
        render and return a complete page information in html
        :return:
        '''
        #components = components_factory(self.context())
        payload = create_payload(self.context())
        #print('WebPage::render api:{}'.format(self._ap_i))
        r = post(url=self._api, json=payload)
        html = extract_data(r.json()['data'])
        return render_template_string(html)

    def render_content(self):
        '''
        render and return the component information in html, and its script,script files, style and style files
        :return : context in html, scripts, script files, styles, style files
        '''
        payload = create_payload(self._mycont)
        # print('WebPage::render api:{}'.format(self._ap_i))
        r = post(url=self._api + '_content', json=payload)
        rjson = extract_data(r.json()['data'])
        rdata = json.loads(rjson)
        return {
            'content': render_template_string(rdata['content']),
            'scripts':rdata['scripts'],
            'script_files':rdata['script_files'],
            'styles':rdata['styles'],
            'styles_files':rdata['style_files']
        }


    def context(self):
        if self._parent:
            return self._parent.context()
        else:
            return self._context

    def add_context(self, cont):
        return self._add_context(cont)

    def add_context_list(self, context_list, indent=True):
        '''
        for i,v in enumerate(context_list[1:]):
            context_list[i+1] = self.get_context_indent()*'    ' + context_list[i+1]
        '''
        self.context_call(params={'context':''.join(context_list)})

    def add_script_list(self, script_list):
        raise NotImplementedError

    def remove_context(self, cont):
        self._remove_context(cont)

    @classmethod
    def _remove_context(cls, cont=None):
        if not cont:
            del cls._cur_context_stack[-1]
        else:
            for i,v in enumerate(cls._cur_context_stack):
                if v == cont:
                    del cls._cur_context_stack[i]

    @classmethod
    def _add_context(cls, cont):
        cls._cur_context_stack[-1].append(cont)
        return cls._cur_context_stack[-1]

    @classmethod
    def _push_current_context(cls, cont):
        cls._cur_context_stack.append(cont)

    @classmethod
    def _pop_current_context(cls):
        cls._cur_context_stack.pop()

    def scripts(self):
        raise NotImplementedError

    def add_script(self, scripts):
        '''
        context = self._get_objcall_context(func=inspect.stack()[0][3],caller_id=self.id(),params={'scripts': scripts})
        self.add_context(context)
        '''
        params = {'scripts': scripts}
        return self.func_call(params)

    def add_script_list(self, script_list):
        '''
        Add scripts in a list
        :param ls: scripts in list
        :return: self.func_call(params)
        '''
        params = {'script_list',script_list}
        return self.func_call(params)

    def set_script_indent(self, indent):
        '''
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(),params={'indent': indent})
        self.add_context(context)
        '''
        params = {'indent': indent}
        return self.func_call(params)

    def get_script_indent(self):
        raise NotImplementedError

    def styles(self):
        raise NotImplementedError

    def add_styles(self, styles):
        raise NotImplementedError

    def add_style(self,styles):
        raise NotImplementedError

    @contextmanager
    def cmds(self):
        '''
        context = self._get_objcall_context(func='with', caller_id=self.id(), params={'function': inspect.stack()[0][3], 'params': {}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        '''
        self.with_call({})
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()

    def add__style(self, styles):
        raise NotImplementedError

    def global_styles(self):
        raise NotImplementedError

    def add_script_files(self, files):
        raise NotImplementedError

    def add_style_files(self, files):
        raise NotImplementedError

    def get_style(self):
        raise NotImplementedError

    def get_script_files(self):
        raise NotImplementedError

    def get_style_files(self):
        raise NotImplementedError

    def replace_scripts(self, stub, scripts):
        raise NotImplementedError

    @classmethod
    def test_request(cls, methods=['GET']):
        '''Create a testing page containing the component which is being tested'''

        '''
        TODO: Remove WebPageTest class and use WebPage(test=True)
        '''
        with WebPage() as page:
            with page.add_child(globals()[cls.__name__](test=True)) as test:
                pass
        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)

    @contextmanager
    def var_w(self, name='data'):
        '''
        context = self._get_objcall_context(func='with', caller_id=self.id(),
                                            params={'function': inspect.stack()[0][3], 'params': {'name':name}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        '''
        params = {'name':name}
        self.with_call(params)
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()

    def lvar_w(self, name='data'):
        raise NotImplementedError

    def gvar_w(self, name='data'):
        raise NotImplementedError

    @classmethod
    def get_data(cls, model=None, query=None):
        if not model or not query:
            return cls._example_data()
        else:
            data = model.query(query)
            if not data:
                return cls._example_data()
            else:
                return data


class WebComponentBootstrap(WebComponent, Action, Format, ClientBase):

    def has_class(self, class_):
        raise NotImplementedError

    def is_width(self, width):
        '''
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'width': width})
        context['sub_context'] = []
        self.add_context(context)
        '''
        params = {'width': width}
        return self.func_call(params)

    def remove_width(self, width):
        '''
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'width': width})
        context['sub_context'] = []
        self.add_context(context)
        '''
        params = {'width': width}
        return self.func_call(params)

    def set_width(self, width):
        '''
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'width': width})
        context['sub_context'] = []
        self.add_context(context)
        '''
        params={'width': width}
        return self.func_call(params)

    def value(self, value):
        '''
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'value': value})
        context['sub_context'] = []
        self.add_context(context)
        '''
        params = {'value': value}
        return self.func_call(params)

    def is_js_kw(self):
        pass

    def test_init(self):
        if (not hasattr(self, '_value')) or (not self._value):
            self._value = self.__class__.__name__ + 'Test'


class WebPage(WebComponentBootstrap,TestPage):

    def __init__(self,  test=False, **kwargs):
        self._set_context([])
        self._root_class = WebComponentBootstrap
        super().__init__(test=test, **kwargs)
        self.add_app()


class WebA(WebComponentBootstrap):
    pass


class WebRow(WebComponentBootstrap):
    pass


class WebColumn(WebComponentBootstrap):
    pass


class WebHead1(WebComponentBootstrap):
    pass


class WebField(WebComponentBootstrap):
    pass


class WebImg(WebComponentBootstrap):
    pass


class WebBtnToggle(WebComponentBootstrap):

    def toggle(self):
        '''
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={})
        self.add_context(context)
        '''
        params = {}
        return self.func_call(params)


class WebBtnGroup(WebComponentBootstrap):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class WebBtnGroupVertical(WebComponentBootstrap):
    pass


class WebBtnToolbar(WebComponentBootstrap):

    @classmethod
    def test_request(cls, methods=['GET']):
        '''Create a testing page containing the component which is being tested'''

        with WebPage() as page:
            with page.add_child(globals()[cls.__name__](test=True, name="Test")) as test:
                with test.add_child(OOGeneralSelector(test=True)) as sel1:
                    pass
                with test.add_child(WebBtnGroup(test=True)) as btng1:
                    with btng1.add_child(OODatePicker(test=True)) as dp1:
                        pass
        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)

    @classmethod
    def test_result(cls):
        r = request.form['test']
        return json.dumps({"status": "sucess"}), 201


class WebBtn(WebComponentBootstrap):
    pass


class WebBtnDropdown(WebBtn):

    def set_options(self,options=None):
        params={'options':options}
        self.func_call(params)

    @classmethod
    def test_request(cls, methods=['GET']):
        '''
        with WebPage() as page:
            with page.add_child(globals()[cls.__name__](value='测试',select_options=[{'name':'测试1','href':'#'},{'name':'测试2','href':'#'}])) as btn:
                pass

        with btn.on_event_w('change'):
            with LVar(parent=btn, var_name='text') as text:
                btn.val()
            with btn.if_w():
                with btn.condition_w():
                    text.equal(right='测试2')
                with btn.cmds_w():
                    page.alert('"Find 测试2"')

        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)
        '''

        with WebPage(test=True) as page:
            with page.add_child(WebBtnDropdown(value='测试', select_options=[{'name': '测试1', 'href': '#'}, {'name': '测试2', 'href': '#'}])) as btn:
                pass  # btn.clear(call=True)

        # response to change event and pop up an alert
        with btn.on_event_w('change'):
            page.alert('"WebBtnDropdown " + $(event.currentTarget).attr("id") + " is changed!"')
            with LVar(parent=btn, var_name='text') as text:
                btn.val()
            with btn.if_w():
                with btn.condition_w():
                    text.equal('测试2')
                with btn.cmds_w():
                    page.alert('"Find 测试2"')
                    new_options = [{'name': 'test1', 'href': '#'}, {'name': 'test2', 'href': '#'}]
                    btn.set_options(options=new_options)

        # trigger the click a event
        with btn.on_event_w(event='click', filter='a'):
            page.alert('"WebBtnDropdown " + $(event.currentTarget).attr("id") + " click a event triggered!"')

        # trigger a click a event and expect an alert poping up
        # btn.trigger_event(event='click',filter='a')

        btn.set_js(True)
        btn.val('"新测试"')  # expect a change event alert poping up
        btn.set_js(False)

        # set value of the dropdown button programingly, expecte poping up an alert of change event
        '''
        btn.set_js(True)
        btn.val('"新测试"')
        btn.set_js(False)
        '''
        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)

class WebFormGroup(WebComponentBootstrap):
    pass


class WebInputGroup(WebComponentBootstrap):
    pass


class WebInput(WebComponentBootstrap):
    pass


class WebInputGroup(WebComponentBootstrap):
    pass


class WebFormInline(WebComponentBootstrap):
    pass


class WebSpan(WebComponentBootstrap):
    pass


class WebBr(WebComponentBootstrap):
    pass


class WebUl(WebComponentBootstrap):
    pass


class WebDiv(WebComponentBootstrap):
    pass


class WebCheckbox(WebSpan):
    pass


class OODatePicker(WebInputGroup):
    pass
    '''
    @classmethod
    def on_post(cls):
        r = super().on_post()

        # just for test
        select_data = r['data']
        data = cls.default_data()
        for index, btn in enumerate(data):
            if index < len(select_data):
                sbtn = select_data[index]
                if sbtn['select']:
                    btn['select'] = sbtn['select']
            elif index == len(select_data):
                pass
            else:
                btn['options'].call_clear()
        # test end

        return jsonify({'status': 'success', 'data': data})
    '''

class WebSvg(WebComponentBootstrap):
    pass


class OOChartNVD3(WebSvg):

    @classmethod
    def test_request(cls, methods=['GET']):
        '''Create a testing page containing the component which is being tested'''

        '''
        TODO: Remove WebPageTest class and use WebPage(test=True)
        '''
        with WebPage() as page:
            with page.add_child(globals()[cls.__name__](value='example_data', height='400px')) as test:
                pass

        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)


class OOChartLineFinder(OOChartNVD3):
    pass

class OOChartPie(OOChartNVD3):
    pass

class OOChartComulativeLine(OOChartNVD3):
    pass

class OOChartLinePlusBar(OOChartNVD3):
    pass

class OOChartHorizontalGroupedStackedBar(OOChartNVD3):
    pass

class OOChartDescreteBar(OOChartNVD3):
    pass

class OOChartStackedArea(OOChartNVD3):
    pass
    
class OOChartLine(OOChartNVD3):
    pass

class OOChartScatterBubble(OOChartNVD3):
    pass


class OOChartMultiBar(OOChartNVD3):
    pass


class OOChartBullet(OOChartNVD3):
    pass


class OOGeneralSelector(WebBtnGroup):

    '''
    Create a general selector, contains several toggle drop down buttons in a line

    :param: btns=[
        {
            'name':'btn1',
            'options':[
                {
                    'name':'option1',
                    'href':'#'
                },
                {
                    ...
                }
            ],
            'select':'option1'
        },
        {
        ...
        }
    ]

    methods:
        on_event_w: own events: 'select', response function params: 'a', 'btn', 'me'

    '''

    @staticmethod
    def data_format():
        return {
            'button': {'name': '', 'select':'', 'options': []},
            'option': {'name': '', 'href': '#'}
        }

    @classmethod
    def test_request(cls, methods=['GET']):
        '''Create a testing page containing the component which is being tested'''

        with WebPage() as page:
            with page.add_child(globals()[cls.__name__](test=True, name="Test")) as test:
                pass
                '''
                with test.on_select():
                    test.set_script_indent(-1)
                    test.add_script('''"alert(btn.name + '.' + event.target.text);"''')
                    test.set_script_indent(1)
                    with test.post_w():
                        pass
                '''
        with test.on_event_w('select'):
            #test.add_script('''"var data = " + test.fix_cmd(test.val())''')
            with Var(parent=test) as data:
                test.val()
            with test.post_w():
                test.val(data)

        html = page.render()
        return render_template_string(html)

    @classmethod
    def test_result(cls):
        r = request.form['test']
        print("Got " + cls.__name__ + " testing post: " + r)
        return json.dumps({"status": "sucess"}), 201

    def call_on_select(self):
        pass

    @classmethod
    def _example_data(cls):
        fmt = OOGeneralSelector.data_format()
        data = []
        for i in range(3):
            button = copy.deepcopy(fmt['button'])
            button['name'] = 'testtest' + str(i)
            option1 = copy.deepcopy(fmt['option'])
            option1['name'] = button['name'] + '_testoption1'
            option2 = copy.deepcopy(fmt['option'])
            option2['name'] = button['name'] + '_testoption2'
            button['options'].append(option1)
            button['options'].append(option2)
            data.append(button)
        button = copy.deepcopy(fmt['button'])
        button['name'] = 'test' + str(3)
        data.append(button)
        return data

    @classmethod
    def on_post(cls):
        '''
        TODO: query data by user model
        :return:
        '''
        r = super().on_post()

        # just for test
        select_data = r['data']
        data = cls._example_data()
        for index, btn in enumerate(data):
            if index < len(select_data):
                sbtn = select_data[index]
                if sbtn['select']:
                    btn['select'] = sbtn['select']
            elif index == len(select_data):
                pass
            else:
                btn['options'].call_clear()
        # test end

        return jsonify({'status': 'success', 'data': data})


class OOCalendar(WebDiv):

    @classmethod
    def _week(cls):
        week = '''
                <div class="cal-week-box">
                    <div class="cal-offset1 cal-column"></div>
                    <div class="cal-offset2 cal-column"></div>
                    <div class="cal-offset3 cal-column"></div>
                    <div class="cal-offset4 cal-column"></div>
                    <div class="cal-offset5 cal-column"></div>
                    <div class="cal-offset6 cal-column"></div>
                    <div class="cal-row-fluid cal-row-head">
                        <% _.each(days_name, function(name) { %>
                            <div class="cal-cell1 <%= cal._getDayClass('week', start) %>" data-toggle="tooltip" title="<%= cal._getHolidayName(start) %>"><%= name %><br>
                                <small><span data-cal-date="<%= start.getFullYear() %>-<%= start.getMonthFormatted() %>-<%= start.getDateFormatted() %>" data-cal-view="day"><%= start.getDate() %> <%= cal.locale['ms' + start.getMonth()] %></span></small>
                            </div>
                            <% start.setDate(start.getDate() + 1); %>
                        <% }) %>
                    </div>
                    <hr>
                    <%= cal._week() %>
                </div>
            '''
        # return send_file('templates/calendar/tmpls/week.html')
        return week

    @classmethod
    def _week_day(cls):
        week_days = '''
                <% _.each(events, function(event){ %>
                <div class="cal-row-fluid">
                    <div class="cal-cell<%= event.days%> cal-offset<%= event.start_day %> day-highlight dh-<%= event['class'] %>" data-event-class="<%= event['class'] %>">
                        <a href="<%= event.url ? event.url : 'javascript:void(0)' %>" data-event-id="<%= event.id %>" class="cal-event-week event<%= event.id %>"><%= event.title %></a>
                    </div>
                </div>
                <% }); %>
            '''
        # return send_file('templates/calendar/tmpls/week-days.html')
        return week_days

    @classmethod
    def _day(cls):
        day = '''
                <div id="cal-day-box">
                    <div class="row-fluid clearfix cal-row-head">
                        <div class="span1 col-xs-1 cal-cell"><%= cal.locale.time %></div>
                        <div class="span11 col-xs-11 cal-cell"><%= cal.locale.events %></div>
                    </div>
                    <% if(all_day.length) {%>
                        <div class="row-fluid clearfix cal-day-hour">
                            <div class="span1 col-xs-1"><b><%= cal.locale.all_day %></b></div>
                            <div class="span11 col-xs-11">
                                <% _.each(all_day, function(event){ %>
                                    <div class="day-highlight dh-<%= event['class'] %>">
                                        <a href="<%= event.url ? event.url : 'javascript:void(0)' %>" data-event-id="<%= event.id %>"
                                           data-event-class="<%= event['class'] %>" class="event-item">
                                            <%= event.title %></a>
                                    </div>
                                <% }); %>
                            </div>
                        </div>
                    <% }; %>
                    <% if(before_time.length) {%>
                        <div class="row-fluid clearfix cal-day-hour">
                            <div class="span1 col-xs-3"><b><%= cal.locale.before_time %></b></div>
                            <div class="span5 col-xs-5">
                                <% _.each(before_time, function(event){ %>
                                    <div class="day-highlight dh-<%= event['class'] %>">
                                        <span class="cal-hours pull-right"><%= event.end_hour %></span>
                                        <a href="<%= event.url ? event.url : 'javascript:void(0)' %>" data-event-id="<%= event.id %>"
                                           data-event-class="<%= event['class'] %>" class="event-item">
                                            <%= event.title %></a>
                                    </div>
                                <% }); %>
                            </div>
                        </div>
                    <% }; %>
                    <div id="cal-day-panel" class="clearfix">
                        <div id="cal-day-panel-hour">
                            <% for(i = 0; i < hours; i++){ %>
                                <div class="cal-day-hour">
                                    <% for(l = 0; l < cal._hour_min(i); l++){ %>
                                        <div class="row-fluid cal-day-hour-part">
                                            <div class="span1 col-xs-1"><b><%= cal._hour(i, l) %></b></div>
                                            <div class="span11 col-xs-11"></div>
                                        </div>
                                <% }; %>
                                </div>
                            <% }; %>
                        </div>

                        <% _.each(by_hour, function(event){ %>
                            <div class="pull-left day-event day-highlight dh-<%= event['class'] %>" style="margin-top: <%= (event.top * 30) %>px; height: <%= (event.lines * 30) %>px">
                                <span class="cal-hours"><%= event.start_hour %> - <%= event.end_hour %></span>
                                <a href="<%= event.url ? event.url : 'javascript:void(0)' %>" data-event-id="<%= event.id %>"
                                   data-event-class="<%= event['class'] %>" class="event-item">
                                    <%= event.title %></a>
                            </div>
                        <% }); %>
                    </div>
                    <% if(after_time.length) {%>
                    <div class="row-fluid clearfix cal-day-hour">
                        <div class="span1 col-xs-3"><b><%= cal.locale.after_time %></b></div>
                        <div class="span11 col-xs-9">
                            <% _.each(after_time, function(event){ %>
                            <div class="day-highlight dh-<%= event['class'] %>">
                                <span class="cal-hours"><%= event.start_hour %></span>
                                <a href="<%= event.url ? event.url : 'javascript:void(0)' %>" data-event-id="<%= event.id %>"
                                   data-event-class="<%= event['class'] %>" class="event-item">
                                    <%= event.title %></a>
                            </div>
                            <% }); %>
                        </div>
                    </div>
                    <% }; %>
                </div>

            '''
        # return send_file('templates/calendar/tmpls/day.html')
        return day

    @classmethod
    def _month(cls):
        month = '''
                <div class="cal-row-fluid cal-row-head">
                    <% _.each(days_name, function(name){ %>
                        <div class="cal-cell1"><%= name %></div>
                    <% }) %>
                </div>
                <div class="cal-month-box" style="">
                    <% for(i = 0; i < 6; i++) { %>
                        <% if(cal.stop_cycling == true) break; %>
                        <div class="cal-row-fluid cal-before-eventlist">
                            <div class="cal-cell1 cal-cell" data-cal-row="-day1"><%= cal._day(i, day++) %></div>
                            <div class="cal-cell1 cal-cell" data-cal-row="-day2"><%= cal._day(i, day++) %></div>
                            <div class="cal-cell1 cal-cell" data-cal-row="-day3"><%= cal._day(i, day++) %></div>
                            <div class="cal-cell1 cal-cell" data-cal-row="-day4"><%= cal._day(i, day++) %></div>
                            <div class="cal-cell1 cal-cell" data-cal-row="-day5"><%= cal._day(i, day++) %></div>
                            <div class="cal-cell1 cal-cell" data-cal-row="-day6"><%= cal._day(i, day++) %></div>
                            <div class="cal-cell1 cal-cell" data-cal-row="-day7"><%= cal._day(i, day++) %></div>
                        </div>
                    <% } %>
                </div>        
            '''
        # return send_file('templates/calendar/tmpls/month.html')
        return month

    @classmethod
    def _month_day(cls):
        month_day = '''
                <div class="cal-month-day <%= cls %>">
                    <span class="pull-right" data-cal-date="<%= data_day %>" data-cal-view="day" data-toggle="tooltip" title="<%= tooltip %>"><%= day %></span>
                    <% if (events.length > 0) { %>
                        <div class="events-list" data-cal-start="<%= start %>" data-cal-end="<%= end %>">
                            <% _.each(events, function(event) { %>
                                <a href="<%= event.url ? event.url : 'javascript:void(0)' %>" data-event-id="<%= event.id %>" data-event-class="<%= event['class'] %>"
                                    class="pull-left event <%= event['class'] %>" data-toggle="tooltip"
                                    title="<%= event.title %>"></a>
                            <% }); %>
                        </div>
                    <% } %>
                </div>
            '''
        # return send_file('templates/calendar/tmpls/month-day.html')
        return month_day

    @classmethod
    def _year(cls):
        year = '''
                <div class="cal-year-box">
                    <div class="row row-fluid cal-before-eventlist">
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month1"><%= cal._month(0) %></div>
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month2"><%= cal._month(1) %></div>
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month3"><%= cal._month(2) %></div>
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month4"><%= cal._month(3) %></div>
                    </div>
                    <div class="row row-fluid cal-before-eventlist">
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month1"><%= cal._month(4) %></div>
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month2"><%= cal._month(5) %></div>
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month3"><%= cal._month(6) %></div>
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month4"><%= cal._month(7) %></div>
                    </div>
                    <div class="row row-fluid cal-before-eventlist">
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month1"><%= cal._month(8) %></div>
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month2"><%= cal._month(9) %></div>
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month3"><%= cal._month(10) %></div>
                        <div class="span3 col-md-3 col-sm-3 col-xs-3 cal-cell" data-cal-row="-month4"><%= cal._month(11) %></div>
                    </div>
                </div>
            '''
        # return send_file('templates/calendar/tmpls/year.html')
        return year

    @classmethod
    def _year_month(cls):
        year_month = '''
                <span class="pull-right" data-cal-date="<%= data_day %>" data-cal-view="month"><%= month_name %></span>
                <% if (events.length > 0) { %>
                    <small class="cal-events-num badge badge-important pull-left"><%= events.length %></small>
                    <div class="hide events-list" data-cal-start="<%= start %>" data-cal-end="<%= end %>">
                        <% _.each(events, function(event) { %>
                            <a href="<%= event.url ? event.url : 'javascript:void(0)' %>" data-event-id="<%= event.id %>" data-event-class="<%= event['class'] %>"
                                class="pull-left event <%= event['class'] %> event<%= event.id %>" data-toggle="tooltip"
                                title="<%= event.title %>"></a>
                        <% }); %>
                    </div>
                <% } %>
            '''
        # return send_file('templates/calendar/tmpls/year-month.html')
        return year_month

    @classmethod
    def _event_list(cls):
        event_list = '''
                <span id="cal-slide-tick" style="display: none"></span>
                <div id="cal-slide-content" class="cal-event-list">
                    <ul class="unstyled list-unstyled">
                        <% _.each(events, function(event) { %>
                            <li>
                                <span class="pull-left event <%= event['class'] %>"></span>&nbsp;
                                <a href="<%= event.url ? event.url : 'javascript:void(0)' %>" data-event-id="<%= event.id %>"
                                    data-event-class="<%= event['class'] %>" class="event-item">
                                    <%= event.title %></a>
                            </li>
                        <% }) %>
                    </ul>
                </div>

            '''
        # return send_file('templates/calendar/tmpls/events-list.html')
        return event_list

    @classmethod
    def _example_data(cls):
        return {
            "status": 'success',
            "result": [
                {
                    "id": "293",
                    "title": "This is warning class event with very long title to check how it fits to evet in day view",
                    "url": "http://www.example.com/",
                    "class": "event-warning",
                    "start": "1362938400000",
                    "end": "1363197686300"
                },
                {
                    "id": "256",
                    "title": "Event that ends on timeline",
                    "url": "http://www.example.com/",
                    "class": "event-warning",
                    "start": "1363155300000",
                    "end": "1363227600000"
                },
                {
                    "id": "276",
                    "title": "Short day event",
                    "url": "http://www.example.com/",
                    "class": "event-success",
                    "start": "1363245600000",
                    "end": "1363252200000"
                },
                {
                    "id": "294",
                    "title": "This is information class ",
                    "url": "http://www.example.com/",
                    "class": "event-info",
                    "start": "1363111200000",
                    "end": "1363284086400"
                },
                {
                    "id": "297",
                    "title": "This is success event",
                    "url": "http://www.example.com/",
                    "class": "event-success",
                    "start": "1363234500000",
                    "end": "1363284062400"
                },
                {
                    "id": "54",
                    "title": "This is simple event",
                    "url": "http://www.example.com/",
                    "class": "",
                    "start": "1363712400000",
                    "end": "1363716086400"
                },
                {
                    "id": "532",
                    "title": "This is inverse event",
                    "url": "http://www.example.com/",
                    "class": "event-inverse",
                    "start": "1364407200000",
                    "end": "1364493686400"
                },
                {
                    "id": "548",
                    "title": "This is special event",
                    "url": "http://www.example.com/",
                    "class": "event-special",
                    "start": "1363197600000",
                    "end": "1363629686400"
                },
                {
                    "id": "295",
                    "title": "Event 3",
                    "url": "http://www.example.com/",
                    "class": "event-important",
                    "start": "1364320800000",
                    "end": "1364407286400"
                }
            ]
        }

    @classmethod
    def _event(cls):
        events = cls._example_data()

        _from = request.args.get('from')
        if _from:
            _from = datetime.datetime.fromtimestamp(float(_from) / 1000.0)
        _to = request.args.get('to')
        if _to:
            _to = datetime.datetime.fromtimestamp(float(_to) / 1000.0)
        are = request.args.get('are')
        sch = request.args.get('sch')
        dep = request.args.get('dep')
        sta = request.args.get('sta')
        print("  _from:{} _to:{} are:{} sch:{} dep:{} sta:{}".format(_from, _to, are, sch, dep, sta))
        print("  ##got events:{}".format(events))
        if events:
            ret = events
        else:
            ret = {
                'status': 'error',
                'result': 'No events'
            }
        return jsonify(ret)

    @classmethod
    def add_url_rule(cls, app, extend=[]):
        super().add_url_rule(app,extend)
        app.add_url_rule('/oocalendar/year.html', view_func=cls._year)
        app.add_url_rule('/oocalendar/year-month.html', view_func=cls._year_month)
        app.add_url_rule('/oocalendar/month.html', view_func=cls._month)
        app.add_url_rule('/oocalendar/month-day.html', view_func=cls._month_day)
        app.add_url_rule('/oocalendar/week.html', view_func=cls._week)
        app.add_url_rule("/oocalendar/week-days.html", view_func=cls._week_day)
        app.add_url_rule("/oocalendar/day.html", view_func=cls._day)
        app.add_url_rule("/oocalendar/events-list.html", view_func=cls._event_list)
        app.add_url_rule('/oocalendar/events', view_func=cls._event)

    @classmethod
    def test_request(cls, methods=['GET']):
        '''Create a testing page containing the component which is being tested'''

        '''
        TODO: Remove WebPageTest class and use WebPage(test=True)
        '''

        cls.add_url_rule(app=current_app)

        with WebPage() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'],offset=['mdo2'])) as c1:
                    with c1.add_child(OOCalendarBar()) as bar:
                        pass
            with page.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c2:
                    with c2.add_child(globals()[cls.__name__](value='example_data')) as calendar:
                        pass

        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)


class OOCalendarBar(WebDiv):
    pass


class WebTable(WebComponentBootstrap):
    '''
    WebTable generates a html table from a data including schema and records.
    schema leads to table heads and records lead to table body.
    The implementation of this class is different from other classes. The not all rendering of WebTable is on the
    server side, some render is on client side.

    TODO: Change the members of model and query from class to object
    '''

    MODEL = None
    QUERY = None

    def __init__(self, model=None, query=None, head_classes=[], body_classes=[], head_styles=None, body_styles=None,**kwargs):
        super().__init__(**kwargs)
        WebTable._head_styles = head_styles
        WebTable._body_styles = body_styles
        WebTable._head_classes = head_classes
        WebTable._body_classes = body_classes
        WebTable.MODEL = model
        WebTable.QUERY = query

    @classmethod
    def _head_styles_str(cls):
        ret = ''
        if not cls._head_styles:
            return ''
        for key, value in cls._head_styles.items():
            if key != 'border-radius':
                ret += key + ':' + value + ';'
            else:
                raise NotImplementedError
        if ret and ret[-1:] == ';':
            ret = ret[:-1]
        return ret

    @classmethod
    def _body_styles_str(cls):
        ret = ''
        if not cls._body_styles:
            return ''
        for key, value in cls._body_styles.items():
            if key != 'border-radius':
                ret += key + ':' + value + ';'
            else:
                raise NotImplementedError
        if ret and ret[-1:] == ';':
            ret = ret[:-1]
        return ret

    @classmethod
    def _body_classes_str(cls):
        if cls._body_classes:
            return ' '.join(cls._body_classes)

    @classmethod
    def _head_classes_str(cls):
        if cls._head_classes:
            return ' '.join(cls._head_classes)

    @classmethod
    def _example_data(cls):
        '''
        return {
            'schema':[
                {'name': 'Firstname','subhead':[{'name':'Firstname', 'style':'width:16%','attr':''},{'name':'Middlename','style':'width:16%', 'attr':''}]},
                {'name': 'Lastname','style':'width:32%'},
                {'name': 'Email','style': 'width:32%'},
                {'name': 'registered', 'style': 'width:4%', 'type':'checkbox'}
            ],
            'records':[
                ({'data':'John'},{'data':''},{'data':'Doe'},{'data':'john@example.com'},{'data':True, 'attr':''}),
                ({'data':'Mary'},{'data':''},{'data':'Moe'},{'data':'mary@example.com'},{'data':False, 'attr':'disabled=\"disabled\"'}),
                ({'data':'July'},{'data':''},{'data':'Dooley'},{'data':'july@example.com'},{'data':True, 'attr':'disabled=\"disabled\"'}),
                ({'data':'David'}, {'data':''}, {'data':'Jones'}, {'data':'david@example.com'},{'data':False, 'attr':'disabled=\"disabled\"'}),
                ({'data':'Michael'}, {'data':''}, {'data':'Johnson'}, {'data':'michael@example.com'},{'data':True, 'attr':'disabled=\"disabled\"'}),
                ({'data':'Chris'}, {'data':''}, {'data':'Lee'}, {'data':'chris@example.com'},{'data':True, 'attr':'disabled=\"disabled\"'}),
                ({'data':'Mike'}, {'data':''}, {'data':'Brown'}, {'data':'Mike@example.com'},{'data':True, 'attr':''}),
                ({'data':'Mark'}, {'data':''}, {'data':'Williams'}, {'data':'mark@example.com'},{'data':False, 'attr':'disabled=\"disabled\"'}),
                ({'data':'Paul'}, {'data':''}, {'data':'Rodriguez'}, {'data':'paul@example.com'},{'data':True, 'attr':'disabled=\"disabled\"'}),
                ({'data':'David'}, {'data':''}, {'data':'Jones'}, {'data':'david@example.com'},{'data':False, 'attr':'disabled=\"disabled\"'}),
                ({'data':'Daniel'}, {'data':''}, {'data':'Rodriguez'}, {'data':'daniel@example.com'},{'data':False, 'attr':'disabled=\"disabled\"'}),
                ({'data':'James'}, {'data':''}, {'data':'Garcia'}, {'data':'james@example.com'},{'data':False, 'attr':'disabled=\"disabled\"'}),
                ({'data':'Maria'},{'data':''},{'data':'Lopez'},{'data':'maria@example.com'},{'data':True, 'attr':'disabled=\"disabled\"'})
            ]
        } ,
        '''

        data = {
            'schema': [
                {'name': '事件', 'style': '', 'attr': ''},
                {'name': '审批', 'style': '', 'attr': '', 'type':'checkbox'},
                {'name': '完成', 'style': '', 'attr': '', 'type':'checkbox'},
                {'name': '审核', 'style': '', 'attr': '', 'type':'checkbox'},
                {'name': '开始', 'style': '', 'attr': ''},
                {'name': '结束', 'style': '', 'attr': ''},
                {'name': '备份', 'style': '', 'attr': ''},
            ],
            'records': []
        }
        for i in range(16):
            approve = True if random.randint(0, 1) else False
            done = True if random.randint(0, 1) else False
            check = True if random.randint(0, 1) else False

            start, end = randDatetimeRange()
            data['records'].append(
                (
                    {'data': _getStr(random.randint(3,6)), 'attr':'nowrap'},
                    {'data': approve, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                    {'data': done, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                    {'data': check, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                    {'data': start},
                    {'data': end},
                    {'data': _getStr(random.randint(10,128))}
                )
            )

        return data,

    @classmethod
    def get_data(cls):
        if not cls.MODEL or not cls.QUERY:
            return cls._example_data()
        else:
            data = cls.MODEL.query(cls.QUERY)
            if not data:
                return cls._example_data()
            else:
                return data,cls.SETTING

    @classmethod
    def _html(cls):

        data = cls.get_data()[0]
        def _head_colspan(head):
            colspan = 0
            sub_max_levels = 0

            if 'subhead' not in head or not head['subhead']:
                colspan = 1
            else:
                for sh in head['subhead']:
                    cs, ml = _head_colspan(sh)
                    colspan = colspan + cs
                    if ml > sub_max_levels:
                        sub_max_levels = ml
            if colspan > 1:
                if 'attr' not in head:
                    head['attr'] = ''
                head['attr'] = head['attr'] + ' colspan="{}" '.format(str(colspan))

            return colspan, sub_max_levels+1

        def _head_rowspan(head, max_levels):

            if 'subhead' not in head or not head['subhead']:
                if max_levels > 1:
                    if 'attr' not in head:
                        head['attr'] = ''
                    head['attr'] = head['attr'] + ' rowspan="{}" '.format(max_levels)
                return
            else:
                assert(max_levels>1)
                for sh in head['subhead']:
                    _head_rowspan(sh, max_levels-1)

        def _head_matrix(head, matrix, index):
            attr = head['attr'] if 'attr' in head else ''
            style = head['style'] if 'style' in head else ''
            type = head['type'] if 'type' in head else ''
            classes = head['class'] if 'class' in head else ''
            if len(matrix) <= index:
                for i in range(len(matrix), index+1):
                    matrix.append([])
            if matrix[index]:
                matrix[index].append({'name': head['name'], 'class': classes, 'attr': attr, 'style':style, 'type':type})
            else:
                matrix[index] = [{'name': head['name'], 'class': classes, 'attr': attr, 'style':style, 'type':type}]
            if 'subhead' in head and head['subhead']:
                if len(matrix) <= index + 1:
                    matrix.append([])
                for sh in head['subhead']:
                    _head_matrix(sh, matrix, index+1)

        def _columns(matrix, matrix_index, columns, max_cs):
            columns_count = 0
            for th in matrix[matrix_index]:
                if th['attr'].find('colspan') >=0:
                    th_attr = th['attr'].split(' ')
                    for attr in th_attr:
                        if attr.find('colspan') >=0:
                            colspan = int(attr.split('=')[1].split('"')[1])
                            sub_matrix_index = matrix_index
                            while True:
                                sub_matrix_index = sub_matrix_index + 1
                                if sub_matrix_index >= len(matrix):
                                    return columns_count
                                columns_count = _columns(matrix, sub_matrix_index, columns, colspan)
                                if columns_count and columns_count >= colspan:
                                    break
                else:
                    col = {}
                    if 'attr' in th:
                        col['attr'] = th['attr']
                    if 'type' in th:
                        col['type'] = th['type']
                    if 'style' in th:
                        col['style'] = th['style']
                    columns.append(col)
                    columns_count = columns_count + 1
                if columns_count >= max_cs:
                    return max_cs

        def _head(html, schema):
            max_level = 0
            max_cs = 0
            for h in schema:
                cs, ml = _head_colspan(h)
                max_cs = max_cs + cs
                if ml > max_level:
                    max_level = ml

            for h in schema:
                _head_rowspan(h,max_level)

            matrix = []
            for h in schema:
                _head_matrix(h, matrix,0)

            for tr in matrix:
                html.append('    <tr class="{}" style="{}">\n'.format(cls._head_classes_str(), cls._head_styles_str()))
                for th in tr:
                    html.append('        <th class="{}" style="{}" {}>{}</th>\n'.format(th['class'], th['style'], th['attr'], th['name']))
                html.append('    </tr>\n')

            columns = []
            _columns(matrix, 0, columns, max_cs)

            return columns

        html = []
        columns = []
        if 'schema' in data and data['schema']:
            html.append('<thead>\n')
            columns = _head(html, data['schema'])
            html.append('</thead>\n')

        html.append('<tbody class="{}" style="{}">\n'.format(WebTable._body_classes_str(), WebTable._body_styles_str()))
        for tr in data['records']:
            html.append('    <tr>\n')
            for i,d in enumerate(tr):
                td = ''
                classes = d['class'] if 'class' in d else ''
                style = d['style'] if 'style' in d else ''
                attr = d['attr'] if 'attr' in d else ''
                if columns and 'type' in columns[i] and columns[i]['type']:
                    if columns[i]['type'].find('checkbox') == 0:
                        if d['data']:
                            td = '        <input type="checkbox" checked="checked" class="{}" style="{}" {}>'.format(classes, style, attr)
                        else:
                            td = '        <input type="checkbox" class="{}" style="{}" {}>'.format(classes, style, attr)
                    else:
                        raise NotImplementedError
                else:
                    td = d['data']
                html.append('<td class="{}" style="{}" {} >{}</td>'.format(classes, style, attr, td))
            html.append('    </tr>\n')
        html.append('</tbody>\n')

        return html

    def __enter__(self):
        ret = super().__enter__()
        self.add_context_list(self._html())
        return self

    @classmethod
    def test_request(cls, methods=['GET']):
        with WebPage() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'],height="400px")) as c1:
                    with c1.add_child(globals()[cls.__name__](mytype=['striped', 'hover', 'borderless', 'responsive'])) as bar:
                        pass

        html = page.render()
        return render_template_string(html)


class OOTable(WebTable):

    SETTING = {}

    def __init__(self, setting={}, **kwargs):
        OOTable.SETTING = setting
        super().__init__(**kwargs)

    @classmethod
    def get_data(cls):
        data = super().get_data()
        if len(data) == 1:
            return data[0], cls.SETTING
        else:
            return data

    def search(self, pattern):
        params = {'pattern': pattern}
        return self.func_call(params)

    def customer_search(self, search):
        params = {'search': search}
        return self.func_call(params)

    def draw(self):
        return self.func_call({})

    @classmethod
    def setting(cls, setting=None):
        if setting:
            cls.SETTING = setting
        else:
            return cls.SETTING

    @classmethod
    def _example_data(cls):
        table = super()._example_data()[0]
        if cls.setting():
            datatable = cls.setting()
        else:
            '''
            datatable = {
                'scrollY': '500px',
                'scrollX': True,
                'scrollCollapse': True,
                'paging': False,
                'searching': False,
                'columnDefs':[
                    {'orderable': False, 'targets': 1},
                    {'orderable': False, 'targets': 2},
                    {'orderable': False, 'targets': 3},
                    {'orderable': False, 'targets': 6}
                ],
                'order':[[5, 'asc']]
            }
            '''
            datatable = {
                'scrollY': '500px',
                'scrollX': True,
                'scrollCollapse': True,
                'paging': True,
                'searching': True,
            }
        return table, datatable

    @classmethod
    def on_html(cls, methods=['GET']):
        html_data = cls.get_data()[0]
        datatable_setting = cls.get_data()[1]
        html = ''.join(cls._html())
        return json.dumps({'html':html, 'setting':datatable_setting})

    @classmethod
    def add_url_rule(cls, app, extend=[]):
        super().add_url_rule(app, extend)
        app.add_url_rule('/ootable/ootable_html', view_func=cls.on_html)

    @classmethod
    def test_request(cls, methods=['GET']):
        cls.add_url_rule(app=current_app)
        with WebPage() as page:
            with page.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c2:
                    with c2.add_child(WebInput(value='search')) as input:
                        pass
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height="400px")) as c1:
                    with c1.add_child(globals()[cls.__name__](mytype=['striped', 'hover', 'borderless', 'responsive'])) as test:
                        customer_search = []
                        '''
                        customer_search.append('var time = $("#{}").val();\n')
                        customer_search.append('var half_day = $("#{}").val();\n')
                        customer_search.append('if (time === "时间段"){\n')
                        customer_search.append('    if(half_day === "全天"){\n')
                        customer_search.append('        return true;\n')
                        customer_search.append('     }else if(half_day === "上午"){\n')
                        customer_search.append('     }else if(half_day === "下午"){\n')
                        customer_search.append('     };\n')
                        customer_search.append('}else{\n')
                        customer_search.append('};\n')
                        '''
                        customer_search.append('var filter = $("#{}").val();\n'.format(input.id()))
                        customer_search.append('if (! filter || data[0] === filter){\n')
                        customer_search.append('    return true;\n')
                        customer_search.append('}else{\n')
                        customer_search.append('    return false;\n')
                        customer_search.append('};\n')
                        test.customer_search(customer_search)

        with input.on_event_w('change'):
            page.alert('"searching ... "')
            test.draw()

        html = page.render()
        return render_template_string(html)


class OOTagGroup(WebTable):

    SETTING = {
        'paging': False,
        'scrollY': '500px',
        'scrollX': True,
        'searching': True,
        'scrollCollapse': True,
    }

    COL_NUM = 3

    def __init__(self, value=[], col_num = 0, **kwargs):
        super().__init__(**kwargs)
        self._value = value
        if col_num:
            OOTagGroup.COL_NUM = col_num

    @classmethod
    def _example_data(cls):
        data = {
            'schema': [],
            'records': []
        }

        for j in range(cls.COL_NUM):
            data['schema'].append({'name':''})

        for i in range(2):
            approve = True if random.randint(0, 1) else False
            done = True if random.randint(0, 1) else False
            check = True if random.randint(0, 1) else False

            start, end = randDatetimeRange()
            td = []
            for i in range(len(data['schema'])):
                with WebCheckbox(value=_getStr(random.randint(2,5))) as locals()['wc'+str(i)]:
                    pass
                locals()['wc'+str(i)].add_app()
                wc_content = locals()['wc'+str(i)].render_content()
                td.append({'data': wc_content['content'], 'attr': 'nowrap'})
                del locals()['wc'+str(i)]
            data['records'].append(td)
        return data,

    @classmethod
    def test_request(cls, methods=['GET']):
        #cls.add_url_rule(app=current_app)
        with WebPage() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c1:
                    with c1.add_child(globals()[cls.__name__](mytype=['hover', 'borderless', 'responsive'], col_num=4, attrs={'border':'0'})) as test:
                        pass

        with test.on_event_w('change'):
            with LVar(parent=test, var_name='checked_var') as data:
                test.val()
            test.alert('checked_var')

        html = page.render()
        return render_template_string(html)


class Var(WebComponentBootstrap):

    def __init__(self, parent, **kwargs):
        kwargs['parent'] = parent
        super().__init__(**kwargs)


class LVar(Var):
    pass


class GVar(Var):
    pass
