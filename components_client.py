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
from share import create_payload, extract_data, APIs
import sys, os
import datetime
from flask_sqlalchemy import SQLAlchemy
import json
from test_class import *
import copy

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
        self._push_current_context(context['sub_context'])


'''
TODO: try with eval, just pass the function calling and express in string, then execute with 'eval' on server side
'''

class Action(CommandInf, ActionInf, Test, ClientBase):

    def if_w(self):
        raise NotImplementedError

    def else_w(self):
        raise NotImplementedError

    def for_w(self):
        raise NotImplementedError

    def var(self, value=None):
        raise NotImplementedError

    def g_var(self, value=None):
        raise NotImplementedError

    def is_js(self):
        raise NotImplementedError

    def set_js(self, js):
        raise NotImplementedError

    def is_condition(self):
        raise NotImplementedError

    def set_condition(self, cond):
        raise NotImplementedError

    def condition_w(self):
        raise NotImplementedError

    def cmds_w(self):
        raise NotImplementedError

    def has_class(self, class_):
        raise NotImplementedError

    def add_class(self, class_):
        raise NotImplementedError

    def remove_class(self, class_):
        raise NotImplementedError

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
        except:
            pass
        finally:
            self._pop_current_context()
        
    def trigger_event(self,event):
        params = {'event': event}
        self.func_call(params)

    def val(self,value=''):
        params = {'value': value}
        self.func_call(params)

    '''
    TODO: replace with on_event_w, trigger_event
    '''
    '''
    
    def clear(self, call=False):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'call': call})
        self.add_context(context)

    @contextmanager
    def on_window_resize(self):
        context = self._get_objcall_context(func='with', caller_id=self.id(), params={'function': inspect.stack()[0][3],'params': {}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()

    def on_resize(self):
        pass
    
    def on_click(self):
        raise NotImplementedError

    def on_change(self):
        raise NotImplementedError

    def on_ready(self):
        raise NotImplementedError
        
    def call_clear(self, data="''"):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(),params={'data': data})
        self.add_context(context)

    def clear_declare(self):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={})
        self.add_context(context)

    def event_declare(self, event, filter=''):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'event':event,'filter':filter})
        self.add_context(context)

    def execute_list_declare(self, action_name):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(),params={'action_name': action_name})
        self.add_context(context)

    def on_change_event(self, filter=''):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(),params={'filter': filter})
        self.add_context(context)

    def on_clear(self):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={})
        self.add_context(context)

    def select_declare(self):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={})
        self.add_context(context)

    def call_select(self, event):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'event':event})
        self.add_context(context)
    '''
    
    
class Format(BootstrapInf, FormatInf, ClientBase):

    def pad(self, pad=None):
        raise NotImplementedError

    def margin(self, margin=None):
        raise NotImplementedError

    def width(self, width=None):
        raise NotImplementedError

    def height(self, height=None):
        raise NotImplementedError

    def align(self, align=None):
        raise NotImplementedError

    def value(self, value=None):
        raise NotImplementedError

    def color(self, color=None):
        raise NotImplementedError

    def font(self, font=None):
        raise NotImplementedError

    def atts(self, klass=None):
        raise NotImplementedError

    def atts_str(self):
        raise NotImplementedError

    def add_atts(self, att):
        raise NotImplementedError

    def remove_att(self, att):
        raise NotImplementedError

    def classes(self, classes=None):
        raise NotImplementedError

    def classes_str(self):
        raise NotImplementedError

    def add_class(self, class_):
        raise NotImplementedError

    def remove_class(self, class_):
        raise NotImplementedError

    def check_col_name(self, col):
        raise NotImplementedError

    def check_align(self, align):
        raise NotImplementedError

    def offset(self, offset=[]):
        raise NotImplementedError

    def get_offset_name(self, offset):
        raise NotImplementedError

    def get_width_name(self, width):
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
            for k,v in params.items():
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
        self.add_context(context)

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
            print('Error, tb:{}'.format(exc_tb))
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
        #components = components_factory(self.context())
        payload = create_payload(self.context())
        #print('WebPage::render api:{}'.format(self._api))
        r = post(url=self._api, json=payload)
        html = extract_data(r.json()['data'])
        return render_template_string(html)

    def context(self):
        if self._parent:
            return self._parent.context()
        else:
            return self._context

    def add_context(self, cont):
        return self._add_context(cont)

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

    @classmethod
    def _push_current_context(cls, cont):
        cls._cur_context_stack.append(cont)

    @classmethod
    def _pop_current_context(cls):
        cls._cur_context_stack.pop()

    def scripts(self):
        raise NotImplementedError

    def add_scripts(self, scripts):
        '''
        context = self._get_objcall_context(func=inspect.stack()[0][3],caller_id=self.id(),params={'scripts': scripts})
        self.add_context(context)
        '''
        params = {'scripts': scripts}
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

    '''
    Replace with on_event_w
    '''
    '''
    @contextmanager
    def on_click(self):
        context = self._get_objcall_context(func='with', caller_id=self.id(), params={'function': inspect.stack()[0][3],'params':{}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()

    @contextmanager
    def on_select(self):
        context = self._get_objcall_context(func='with', caller_id=self.id(), params={'function': inspect.stack()[0][3], 'params': {}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()

    @contextmanager
    def on_select_declare(self):
        context = self._get_objcall_context(func='with', caller_id=self.id(), params={'function': inspect.stack()[0][3], 'params': {}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()
    '''

    @contextmanager
    def if_w(self):
        raise NotImplementedError
        '''
        context = self._get_objcall_context(func='with', caller_id=self.id(),params={'function': inspect.stack()[0][3], 'params': {}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()
        '''

    @contextmanager
    def else_w(self):
        raise  NotImplementedError
        '''
        context = self._get_objcall_context(func='with', caller_id=self.id(),
                                            params={'function': inspect.stack()[0][3], 'params': {}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()
        '''

    @contextmanager
    def condition_w(self):
        '''
        context = self._get_objcall_context(func='with', caller_id=self.id(),
                                            params={'function': inspect.stack()[0][3], 'params': {}})
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

    def add_global_styles(self, styles):
        raise NotImplementedError

    def global_styles(self):
        raise NotImplementedError

    def add_script_files(self, files):
        raise NotImplementedError

    def add_style_files(self, files):
        raise NotImplementedError

    def get_global_styles(self):
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
            with page.add_child(globals()[cls.__name__](test=True))[1] as test:
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
        if hasattr(self, "app") and self.app:
            self._api = self.app.config['API_URL'] + APIs['render'].format('v1.0')
        else:
            self._api = current_app.config['API_URL'] + APIs['render'].format('v1.0')


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


class WebBtnDropdownToggle(WebComponentBootstrap):
    pass


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


class OODatePicker(WebInputGroup):

    @classmethod
    def on_post(cls):
        '''
        TODO: query data by user model
        :return:
        '''
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
                '''
                with test.on_select():
                    test.set_script_indent(-1)
                    test.add_scripts('''"alert(btn.name + '.' + event.target.text);"''')
                    test.set_script_indent(1)
                    with test.post_w():
                        pass
                '''
        with test.on_event_w('select'):
            #test.add_scripts('''"var data = " + test.fix_cmd(test.val())''')
            with Var() as data:
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

    @staticmethod
    def default_data():
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


class Var(WebComponentBootstrap):
    pass


class LVar(Var):
    pass


class GVar(Var):
    pass
