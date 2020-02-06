#########################################
# Author         : Haibo Zhu             
# Email          : haibo.zhu@hotmail.com 
# created        : 2019-08-09 20:19 
# Last modified  : 2019-08-09 20:19
# Filename       : components_client.py
# Description    :                       
#########################################
from interfaces import *

import flask
from flask import current_app, render_template_string, request, jsonify, url_for
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

    def class_func_call(self, cls, params):
        context = self._get_clscall_context(func=inspect.stack()[1][3], cls=cls, params=params)
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

class Action(CommandInf, ActionInf, TestClient, ClientBase):

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
    def elif_w(self):
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

    def equal(self,right, left=None, force_condition=False):
        params = {'right': right, 'left':left, 'force_condition':force_condition}
        self.func_call(params=params)

    def is_(self, element_name):
        params = {'element_name':element_name}
        self.func_call(params=params)

    @contextmanager
    def assign_w(self):
        params = {}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

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
        data = json.loads(request.form.get('data'))
        return data
        #return {"status": "sucess", 'data': data, 'me': req['me']}

    @contextmanager
    def each_w(self):
        self.with_call({})
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()

    @contextmanager
    def post_w(self, url=None, data=None, success=None):
        '''
        context = self._get_objcall_context(func='with', caller_id=self.id(), params={'function': inspect.stack()[0][3], 'params': {'url':url, 'data':data, 'success':success}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        '''
        data_ = data
        if not isinstance(data, str):
            data_ = '{}'.format(str(data))
        url_ = url
        if not isinstance(url, str):
            url_ = '"{}"'.format(str(url))
        params = {'url':str(url), 'data':data_, 'success':success}
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

    def val(self,value=None):
        if value:
            params = {'value': value}
        else:
            params = {}
        self.func_call(params)

    def empty(self):
        params = {}
        self.func_call(params)

    def disable(self, disable):
        params = {'disable': disable}
        self.func_call(params)
    
    def _example_data(cls):
        raise NotImplementedError

    @classmethod
    def add_url_rule(cls, app, extend=[]):
        if extend:
            for e in extend:
                if 'endpoint' in e and e['endpoint'] and 'methods' in e and e['methods']:
                    app.add_url_rule(rule=e['rule'], endpoint=e['endpoint'], view_func=e['view_func'], methods=e['methods'])
                elif 'endpoint' in e and e['endpoint']:
                    app.add_url_rule(rule=e['rule'], endpoint=e['endpoint'], view_func=e['view_func'])
                elif 'methods' in e and e['methods']:
                    app.add_url_rule(rule=e['rule'], view_func=e['view_func'], methods=e['methods'])
                elif not 'rule' in e or not e['rule'] or not 'view_func' in e or not e['view_func']:
                    raise RuntimeError('add_url_rule extend should have "rule" and "view_func"')
                else:
                    url = e['rule']
                    app.add_url_rule(rule=url, view_func=e['view_func'])

    def declare_custom_func(self, fname='', fparams=[], fbody=[]):
        params={'fname':fname,'fparams':fparams,'fbody':fbody}
        return self.func_call(params)

    def declare_custom_global_func(self, fname, fparams=[], fbody=[]):
        params={'fname':fname, 'fparams':fparams,'fbody':fbody}
        return self.func_call(params)

    def call_custom_func(self, fname='', fparams={}):
        params={'fname':fname,'fparams':fparams}
        return self.func_call(params)

    @property
    def true(self):
        params={}
        return self.func_call(params)

    @property
    def false(self):
        params = {}
        return self.func_call(params)

    @property
    def null(self):
        params = {}
        return self.func_call(params)

    def declare_event(self, event, use_clsname=False, selector=None, filter=''):
        params = {'event':event, 'use_clsname':use_clsname, 'selector':selector, 'filter':filter}
        return self.func_call(params)

    def sync(self, sync=True):
        params = {'sync':sync}
        return self.func_call(params)

    @contextmanager
    def render_post_w(self):
        params = {}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            print("Error: exception err:{}".format(err))
            raise Exception(err)
        finally:
            self._pop_current_context()

    def render_for_post(self, trigger_event=False):
        params={'trigger_event':trigger_event}
        return self.func_call({})

    @contextmanager
    def timeout_w(self, time=None):
        params = {'time':time}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            print('Error: exception err:{}'.format(err))
            raise Exception(err)
        finally:
            self._pop_current_context()


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

    def _get_clscall_context(self, func, cls, params=None, sub_context=[]):
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
            'function': 'classmethod:'+cls+'.'+func,
            'params': params,
            'sub_context': sub_context
        }

    def __init__(self, test=False, client=True, **kwargs):
        self._client = client
        kwargs['client'] = client
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

        if hasattr(self, '_value') and 'value' not in kwargs:
            kwargs['value'] = self._value

        context = self._get_objcall_context(func=self.type_(), params=kwargs)
        #self._mycont = self.add_context(context)
        self._mycont = [context]
        self.add_context(context)

    def add_app(self):
        if hasattr(self, "app") and self.app:
            self._api = self.app.config['API_URL'] + APIs['render'].format('v1.0')
        else:
            if current_app:
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

    def url(self, url=None, js=True):

        if not js:
            if not url:
                if self._parent:
                    return self._parent.url()
                else:
                    return self._url
            else:
                self._url = url
                return url
        else:
            params = {'url':url, 'js':js}
            self.func_call(params)

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

    '''
    def add_script_list(self, script_list):
        raise NotImplementedError
    '''

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

    def add_script(self, scripts, indent=True, place=None):
        '''
        context = self._get_objcall_context(func=inspect.stack()[0][3],caller_id=self.id(),params={'scripts': scripts})
        self.add_context(context)
        '''
        params = {'scripts': scripts,'indent':indent, "place":place}
        return self.func_call(params)

    def add_script_list(self, script_list, indent=True, place=None):
        '''
        Add scripts in a list
        :param ls: scripts in list
        :return: self.func_call(params)
        '''
        params = {'script_list':script_list,'indent':indent, 'place':place}
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
        params={'files':files}
        return self.func_call(params)

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

    def get_data(self):

        _model = None
        if hasattr(self,'_value') and 'model' in self._value:
            _model = self._value['model']

        _query = None
        if hasattr(self, '_value') and 'query' in self._value:
            _query = self._value['query']

        if not _model or not _query:
            return self._example_data()
        else:
            data = _model.query(**_query)
            if not data:
                return self._example_data()
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

    def val(self,value=''):
        params = {'value':value}
        return self.func_call(params)

    def is_js_kw(self):
        pass

    def test_init(self):
        if (not hasattr(self, '_value')) or (not self._value):
            self._value = self.__class__.__name__ + 'Test'


class WebPage(WebComponentBootstrap,TestPageClient):

    URL = '/WebPage'

    PAGE = None

    '''
    Create an unique instance of page, which add a rule for on_post, and register current page view in app
    '''
    @classmethod
    def get_page(cls, app):
        '''
        if not cls.PAGE:
            cls.PAGE = Page(default_url='view.index', nav=CustomPage.NAV, value=CustomPage.TITLE, app=view)
            app.register_blueprint(blueprint=view, url_prefix=url_prefix)
            print('app.run, app.url_map:{}'.format(pprint.pformat(app.url_map)))
            print('app.run, app.view_functions:{}'.format(pprint.pformat(app.view_functions)))
        return cls.PAGE
        '''
        raise NotImplemented

    def __init__(self, app=None, test=False, **kwargs):
        self._set_context([])
        self._root_class = WebComponentBootstrap
        self._url = self.URL
        kwargs['url'] = self.URL

        if app:
            self.app = app
        if not hasattr(self, 'app'):
            self.app = current_app
        super().__init__(test=test, **kwargs)
        self.add_app()

    @classmethod
    def init_page(cls, app, blueprint=None, url_prefix=None, endpoint=None, on_post=None):
        try:
            if blueprint:
                cls.add_url_rule(app=blueprint, extend=[
                        {'rule': '/on_post', 'endpoint': endpoint, 'view_func': on_post,
                         'methods': ['POST']}])
                app.register_blueprint(blueprint=blueprint, url_prefix=url_prefix)
            else:
                cls.add_url_rule(app, extend=[{'rule': cls.URL, 'endpoint': endpoint, 'view_func': on_post, 'methods': ['POST']}])

        except AssertionError:
            print("Add url rule error!")


class WebA(WebComponentBootstrap):
    pass


class WebRow(WebComponentBootstrap):
    pass


class WebColumn(WebComponentBootstrap):
    pass


class WebHead1(WebComponentBootstrap):

    @classmethod
    def test_request(cls, methods=['GET']):
        '''Create a testing page containing the component tested'''

        # current_app.add_url_rule('/calendar/tmpls/week', view_func=cls.week)

        def on_post():
            req = WebPage.on_post()
            for r in req:
                if r['me'] == 'webhead':
                    r['data'] = 'WebHead Testing'
            return jsonify({'status': 'success', 'data': req})

        class Page(WebPage):
            URL = '/WebHead_test'

            def type_(self):
                return 'WebPage'

        Page.init_page(app=current_app, endpoint=cls.__name__ + '.test', on_post=on_post)
        with Page() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='200px')) as c1:
                    with c1.add_child(globals()[cls.__name__](parent=page, value="WebHead", name='webhead')) as test:
                        pass

        with page.render_post_w():
            test.render_for_post()

        html = page.render()
        return render_template_string(html)


class WebHead2(WebHead1):
    pass


class WebHead3(WebHead1):
    pass


class WebHead4(WebHead1):
    pass


class WebHead5(WebHead1):
    pass


class WebHead6(WebHead1):
    pass


class WebField(WebComponentBootstrap):
    pass


class WebImg(WebComponentBootstrap):

    def __init__(self, value=None, **kwargs):

        if value:
            kwargs['value'] = value
        super().__init__(**kwargs)

    @classmethod
    def test_request(cls, methods=['GET']):
        '''Create a testing page containing the component tested'''
        # current_app.add_url_rule('/calendar/tmpls/week', view_func=cls.week)
        COMPONENT_NAME = 'img_test'

        def on_post():
            req = WebPage.on_post()
            data = []
            for r in req:
                if r['me'] == COMPONENT_NAME:
                    data.append({'me': COMPONENT_NAME, 'data': url_for('static', filename='img/demo.jpg')})
                    return jsonify({'status': 'success', 'data': data})
                else:
                    raise NotImplemented

        class Page(WebPage):
            URL = '/webimg_test'

            def type_(self):
                return 'WebPage'

        Page.init_page(app=current_app, endpoint=cls.__name__ + '.test', on_post=on_post)

        with Page() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='200px')) as c1:
                    with c1.add_child(globals()[cls.__name__](parent=page, name=COMPONENT_NAME)) as test:
                        pass

        with page.render_post_w():
            test.render_for_post()

        html = page.render()
        return render_template_string(html)


class WebBtnToggle(WebComponentBootstrap):

    def toggle(self):
        '''
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={})
        self.add_context(context)
        '''
        params = {}
        return self.func_call(params)


class WebBtnGroup(WebComponentBootstrap):
    pass


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
                    with btng1.add_child(OODatePickerRange(test=True)) as dp1:
                        pass
        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)

    @classmethod
    def test_result(cls):
        r = request.form['test']
        return json.dumps({"status": "sucess"}), 201


class WebBtn(WebComponentBootstrap):

    @classmethod
    def on_post(cls):
        r = super().on_post()
        print('WebBtn.test_result, got request:{}'.format(r['data']))
        return jsonify({'status':'success', 'data':'test post_w success!'})

    @classmethod
    def test_result(cls):
        return cls.on_post()

    @classmethod
    def test_request(cls, methods=['GET']):
        with WebPage(test=True) as page:
            with page.add_child(WebBtn(styles={"border-top-left-radius": "10px"}, test=True)) as btn1:
                pass
            with page.add_child(WebBtn(value='Disable button')) as btn2:
                pass
            with page.add_child(WebBtn(value='Enable button')) as btn3:
                pass
            with page.add_child(WebBtn(value='Test custom function')) as btn4:
                pass
            with page.add_child(WebBtn(value='Test post_w function')) as post_btn:
                with post_btn.on_event_w('click'):
                    with LVar(parent=post_btn, var_name='data') as post_data:
                        post_data.add_script('"test_post";\n', indent=False)
                    with post_btn.post_w('"/test_WebBtn_result"', data=post_data):
                        post_btn.alert('"Test post success with result:"+data')
            with page.add_child(WebBtn(value='Test dict')) as dict_btn:
                pass
            with page.add_child(WebBtn(value='Test "is" method')) as is_btn:
                with is_btn.on_event_w('click'):
                    with LVar(parent=page, var_name='target') as target:
                        target.add_script("$(event.target)", indent=False)
                    with is_btn.if_w():
                        with is_btn.condition_w():
                            target.is_('button')
                    with is_btn.cmds_w():
                        target.alert('"is methods works!"')
            with page.add_child(WebBtn(value='Test nest if ')) as nest_if_btn:
                with nest_if_btn.on_event_w('click'):
                    with LVar(parent=page, var_name='target2') as target2:
                        target2.add_script("$(event.target)", indent=False)
                    with nest_if_btn.if_w():
                        with nest_if_btn.condition_w():
                            target2.is_('button')
                    with nest_if_btn.cmds_w():
                        with nest_if_btn.if_w():
                            with nest_if_btn.condition_w():
                                target2.equal(right='"test"', force_condition=True)
                            with nest_if_btn.cmds_w():
                                target2.alert('"target is test!"')

            # response click event of the button
        with btn1.on_event_w(event="click"):
            btn1.alert("'Button ' + $(event.currentTarget).attr('id') + ' is clicked!' ")

            # response change event of the button
        with btn1.on_event_w(event='change'):
            btn1.alert("'Button ' + $(event.currentTarget).attr('id') + ' is changed!' ")
            btn1.trigger_event(event='change')  # expect not any alert pop up

            # expect trigger change event, but jquery actually not, fixed in val()
        btn1.set_js(True)
        btn1.val('"新测试"')
        btn1.set_js(False)

        # Expect btn1 is disabled by clicking btn2
        with btn2.on_event_w('click'):
            btn1.disable(disable=True)

        # Expect btn1 is enabled by clicking btn3
        with btn3.on_event_w('click'):
            btn1.disable(disable=False)

        # Test custom function
        custom_func = [
            "alert('custom_func works!');\n",
        ]
        btn4.declare_custom_func('test_custom_func', fparams=['id'], fbody=custom_func)
        with btn4.on_event_w('click'):
            btn4.call_custom_func('test_custom_func', fparams={'id': '"{}"'.format(btn4.id())})

        with dict_btn.on_event_w('click'):
            with OODict(parent=page, dict={'key1': 'val1', 'key2': 'val2'}, var_name='test_dict') as dict:
                pass
            with dict.update_w(key='key_updated'):
                dict.add_script('"val_updated"', indent=False)
            dict_btn.alert('"Test dict: { key1:" + test_dict.key1 + ",key_updated: " + test_dict.key_updated + " }"')

        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)


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
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c1:
                    with c1.add_child(WebBtnDropdown(value='测试', select_options=[{'name': '测试1', 'href': '#'}, {'name': '测试2', 'href': '#'}])) as btn:
                        pass  # btn.clear(call=True)
                    with c1.add_child(WebBtnDropdown(value='测试2', select_options=[{'name': '测试3', 'href': '#'},
                                                                                  {'name': '测试4',
                                                                                   'href': '#'}])) as btn2:
                        pass
        # response to change event and pop up an alert
        '''
        with btn.on_event_w('change'):
            page.alert('"WebBtnDropdown " + $(event.currentTarget).attr("id") + " is changed!"')
            with LVar(parent=btn, var_name='text') as text:
                btn.val()
            with btn.if_w():
                with btn.condition_w():
                    text.equal('"测试2"')
                with btn.cmds_w():
                    page.alert('"Find 测试2"')
                    new_options = [{'name': 'test1', 'href': '#'}, {'name': 'test2', 'href': '#'}]
                    btn.set_options(options=new_options)

        # trigger the click a event
        with btn.on_event_w(event='click', filter='a'):
            page.alert('"WebBtnDropdown " + $(event.currentTarget).attr("id") + " click a event triggered!"')

        # trigger a click a event and expect an alert poping up
        # btn.trigger_event(event='click',filter='a')
        
        # set value of the dropdown button programingly, expecte poping up an alert of change event
        btn.set_js(True)
        btn.val('"新测试"')
        btn.set_js(False)
        '''

        # one drop button's action change another drop button value
        with btn.on_event_w('change'):
            with LVar(parent=btn, var_name='btn_val') as btn_value:
                btn.val()
            time_sel_opt = [{'name': '时间段', 'href': '#'},
                            {'name': '时间1', 'href': '#'},
                            {'name': '时间2', 'href': '#'}]
            btn2.set_options(time_sel_opt)
            btn2.val('"时间段"')

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


class OODatePickerBase:
    
    DAY_FORMAT_ZH = ("yyyy年 M月 d日", "%Y年 %m月 %d日 ")
    WEEK_FORMAT_ZH = ("yyyy'年' M'月' '第'W'周'", "")
    MONTH_FORMAT_ZH = ("yyyy年 M月", "%Y年 %m月")

    DAY_FORMAT_EN = ("yyyy M d", "%Y %m %d")
    WEEK_FORMAT_EN = ("yyyy M 'week':W", "")
    MONTH_FORMAT_EN = ("yyyy M", "%Y %m")

    @classmethod
    def DAY_DATETIME_STR(cls, lang, dt):
        format = None
        if lang == 'zh':
            format = cls.DAY_FORMAT_ZH[1]
        else:
            format = cls.DAY_FORMAT_EN[1]
        return dt.strftime(format)

    @classmethod
    def DAY_STR_STAMP(cls, lang, str):
        dt = None
        if lang == 'zh':
            dt = datetime.strptime(str, DAY_FORMAT_ZH[1])
        else:
            dt = datetime.strptime(str, DAY_FORMAT_EN[1])
        return int(dt.timestamp()) * 1000

    @classmethod
    def WEEK_DATETIME_STR(cls, lang, dt):
        if lang == 'zh':
            return "{}年 {}月 第{}周".format(dt.year, dt.month, day_2_week_number(dt))
        else:
            return "{} {} week:{}".format(dt.year, dt.month, day_2_week_number(dt))

    @classmethod
    def WEEK_STR_STAMP(cls, lang, str):
        dt = None
        if lang == 'zh':
            dt = datetime.strptime(str, cls.DAY_FORMAT_ZH[1])
        else:
            dt = datetime.strptime(str, cls.DAY_FORMAT_EN[1])
        return int(dt.timestamp()) * 1000

    @classmethod
    def MONTH_DATETIME_STR(cls, lang, dt):
        format = None
        if lang == 'zh':
            format = cls.MONTH_FORMAT_ZH[1]
        else:
            format = cls.MONTH_FORMAT_EN[1]
        return dt.strftime(format)

    @classmethod
    def MONTH_STR_STAMP(cls, lang, str):
        dt = None
        if lang == 'zh':
            dt = datetime.strptime(str, cls.MONTH_FORMAT_ZH[1])
        else:
            dt = datetime.strptime(str, cls.MONTH_FORMAT_EN[1])
        return int(dt.timestamp()) * 1000

    FORMATS = {
        'zh': {
            'day': {'format': DAY_FORMAT_ZH[0], 'str_func': 'DAY_DATETIME_STR', 'stamp_func': 'DAY_STR_STAMP'},
            'week': {'format': WEEK_FORMAT_ZH[0], 'str_func': 'WEEK_DATETIME_STR', 'stamp_func': 'WEEK_STR_STAMP'},
            'month': {'format': MONTH_FORMAT_ZH[0], 'str_func': 'MONTH_DATETIME_STR', 'stamp_func': 'MONTH_STR_STAMP'}
        },
        'en': {
            'day': {'format': DAY_FORMAT_EN[0], 'str_func': 'DAY_DATETIME_STR', 'stamp_func': 'DAY_STR_STAMP'},
            'week': {'format': WEEK_FORMAT_EN[0], 'str_func': 'WEEK_DATETIME_STR', 'stamp_func': 'WEEK_STR_STAMP'},
            'month': {'format': MONTH_FORMAT_EN[0], 'str_func': 'MONTH_DATETIME_STR', 'stamp_func': 'MONTH_STR_STAMP'}
        }
    }
    

class OODatePickerSimple(WebInputGroup, OODatePickerBase):

    def __init__(self, language='zh', value={'view':'week','start_date':datetime.datetime.today().strftime('%Y %m %d')}, views=['day','week','month'], place_holders=('开始', '结束'), **kwargs):
        kwargs['value'] = value
        kwargs['views'] = views
        kwargs['language'] = language
        kwargs['place_holders'] = place_holders
        super().__init__(**kwargs)

    def disable(self, disable, btn_only=False):
        params={'btn_only':btn_only, 'disable':disable}
        self.func_call(params)

    @classmethod
    def test_request(cls, methods=['GET']):
        # border_radius = {"tl": "10px", "tr": "20px", "bl": "30px", "br": "40px"}
        #
        def on_post():
            req = WebPage.on_post()
            if req['me'] == 'oodatepicker':
                print(req['me'])
                return jsonify({'status': 'success', 'data': 'null'})

        class Page(WebPage):
             URL = '/oodatepickersimple_test'

             @classmethod
             def type_(cls):
                return 'WebPage'

        Page.init_page(app=current_app, endpoint=cls.__name__+'.test', on_post=on_post)

        with Page() as page:
            with page.add_child(globals()[cls.__name__](value='week',views=['week'])) as test1:
                test1.set_js(True)
                test1.disable(btn_only=True, disable=True)
                test1.set_js(False)
            with page.add_child(globals()[cls.__name__](value='week',views=['week'])) as test2:
                test1.set_js(True)
                test2.disable(btn_only=True, disable=True)
                test1.set_js(False)
            with page.add_child(WebBr()) as br:
                pass
            with page.add_child(WebBtn(value='周测试')) as week_btn:
                pass
            with page.add_child(WebBtn(value='月测试')) as month_btn:
                pass
            with page.add_child(WebBtn(value='日测试')) as day_btn:
                pass

        with test1.on_event_w(event='change'):
            with LVar(parent=test1, var_name='date_data') as data:
                test1.val()
            #test1.alert("' Test1 changed: select:'+date_data.select+', date:'+date_data.date+', viewDate:'+date_data.viewDate")
            test2.val("date_data")

        with test2.on_event_w(event='change'):
            with LVar(parent=test1, var_name='date_data') as data:
                test2.val()
            #test2.alert("' Test2 changed: select:'+date_data.select+', date:'+date_data.date+', viewDate:'+date_data.viewDate")
            test1.val("date_data")

        with week_btn.on_event_w(event='click'):
            test1.val("{'select':'周', 'date': new Date}")

        with month_btn.on_event_w(event='click'):
            test1.val("{'select':'月', 'date': new Date}")

        with day_btn.on_event_w(event='click'):
            test1.val("{'select':'日', 'date': new Date}")

        with page.render_post_w():
            test1.render_for_post()
            test2.render_for_post()

        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)


class OODatePickerIcon(OODatePickerSimple):

    @classmethod
    def test_request(cls, methods=['GET']):
        class Page(WebPage):
            URL = '/oodatepickericon_test'

            @classmethod
            def type_(cls):
                return 'WebPage'

            @classmethod
            def on_post(cls):
                req = super().on_post()
                if req['me'] == 'oodatepicker':
                    print(req['me'])
                return jsonify({'status':'success', 'data':'null'})

        Page.init_page(app=current_app, endpoint='oodatepickericon', on_post=Page.on_post)

        with Page() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=["md8"],offset=['mdo2'])) as c1:
                    with page.add_child(WebHead1(value="Test OODatePickerIcon with week view")):
                        pass
            with page.add_child(WebBr()) as br1:
                pass
            with page.add_child(WebBr()) as br2:
                pass
            with page.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=["md8"], offset=['mdo2'])) as c2:
                    with page.add_child(globals()[cls.__name__](value='week')) as test1:
                        pass

        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)


class OODatePickerRange(OODatePickerSimple):

    def __init__(self, language='zh', value={'view':'week','start_date':datetime.datetime.today().strftime('%Y %m %d'),'end_date':datetime.datetime.today().strftime('%Y %m %d')}, views=['day','week','month'], place_holders=('开始', '结束'), **kwargs):
        kwargs['value'] = value
        kwargs['views'] = views
        kwargs['language'] = language
        kwargs['place_holders'] = place_holders
        super().__init__(**kwargs)

    @classmethod
    def test_request(cls, methods=['GET']):
        '''Create a testing page containing the component which is being tested'''

        #border_radius = {"tl": "10px", "tr": "20px", "bl": "30px", "br": "40px"}

        NAME1 = 'test1'
        NAME2 = 'test2'

        def on_post():
            req = WebPage.on_post()
            dt = None
            for r in req:
                if r['me'] == NAME1:
                    lang = r['data']['lang']
                    format = None
                    if r['data']['select'] == '周':
                        start = None if not r['data']['start_viewDate'] else r['data']['start_viewDate'].split('T')[0]
                        if start:
                            # USE cls FORMATS here
                            format = cls.FORMATS[lang]['week']['format']
                            dt = datetime.datetime.strptime(start, '%Y-%m-%d')
                    elif r['data']['select'] == '日':
                        start = None if not r['data']['start_date'] else r['data']['start_date']
                        if start:
                            if lang == 'zh':
                                format = cls.DAY_FORMAT_ZH[1]
                            else:
                                format = cls.DAY_FORMAT_EN[1]
                            dt = datetime.datetime.strptime(start, format)
                    else:
                        start = None if not r['data']['start_date'] else r['data']['start_date']
                        if start:
                            if lang == 'zh':
                                format = cls.MONTH_FORMAT_ZH[1]
                            else:
                                format = cls.MONTH_FORMAT_EN[1]
                            dt = datetime.datetime.strptime(start, format)

            return jsonify({'status': 'success', 'data': []})

        class Page(WebPage):
            URL = '/oodatepickerrange_test'

            @classmethod
            def type_(cls):
                return 'WebPage'

        #Page.init_page(app=current_app, endpoint='oodatepickerrange', on_post=Page.on_post)

        Page.init_page(app=current_app, endpoint=cls.__name__+'.test', on_post=on_post)

        with Page() as page:
            with page.add_child(globals()[cls.__name__](test=True, name=NAME1)) as test1:
                pass
            with page.add_child(globals()[cls.__name__](test=True, name=NAME2)) as test2:
                pass

        #process change event of OODatePicker test1, pops up alerts to show which widget triggered the change event
        # keep OODatePicker test2 the same

        with test1.on_event_w(event='change'):
            with LVar(parent=test1, var_name="test1_data") as test1_data:
                test1.val()
            test2.val(value='test1_data')

        with test2.on_event_w(event='change'):
            with LVar(parent=test2, var_name='test2_data') as test2_data:
                test2.val()
            test1.val(value='test2_data')

        #trigger change event by programming, expect an alert of change event poping up
        #test1.trigger_event(event='change')

        # Add the buttons to set values into datepicker 1 and expect poping up an alert of change event
        with page.add_child(WebBtn(value='测试:周清除')) as test_btn_week:
            pass
        with page.add_child(WebBtn(value="测试:月清除")) as test_btn_month:
            pass
        with page.add_child(WebBtn(value='测试:日清除')) as test_btn_day:
            pass
        with page.add_child(WebBtn(value='Disable Test1')) as disable_test1:
            pass
        with page.add_child(WebBtn(value='Enable Test1')) as enable_test1:
            pass
        with page.add_child(WebBtn(value='Disable test1 btn')) as disable_test1_btn:
            pass
        with page.add_child(WebBtn(value='Enable Test1 btn')) as enable_test1_btn:
            pass

        # set value into test1
        with test_btn_week.on_event_w(event="click"):
            test1.val("{'select':'周', 'start_date': new Date, 'start_viewDate': new Date, 'end_date': new Date, 'end_viewDate': new Date}")
        with test_btn_month.on_event_w(event="click"):
            test1.val("{'select':'月', 'start_date': new Date, 'start_viewDate': new Date, 'end_date': new Date, 'start_viewDate': new Date}")
        with test_btn_day.on_event_w(event="click"):
            test1.val("{'select':'日', 'start_date': new Date, 'start_viewDate': new Date, 'end_date': new Date, 'start_viewDate': new Date}")

        #disable/enable datepicker test1
        with disable_test1.on_event_w(event='click'):
            test1.disable(disable=True)
        with enable_test1.on_event_w('click'):
            test1.disable(disable=False)
        with disable_test1_btn.on_event_w(event='click'):
            test1.disable(btn_only=True,disable=True)
        with enable_test1_btn.on_event_w(event='click'):
            test1.disable(btn_only=True, disable=False)

        with page.render_post_w():
            test1.render_for_post()
            test2.render_for_post()

        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)


class WebSvg(WebComponentBootstrap):

    def id(self, _id=None):
        if not _id:
            if not hasattr(self, '_id') or not self._id:
                self._id = 'svg_' + str(uuid.uuid4()).split('-')[0]
            return self._id
        else:
            self._id = _id


class OOChartNVD3(WebSvg):

    OOCHART_CLASSES = {}
    OOCHART_CREATE_FUNC_NAME = 'oochart_create'

    @classmethod
    def CALL_CREATE_FUNC(cls,  svg, chart_type, chart_data, aobj, parent='null', duration=0, simple=False):
        params={'svg':svg, 'chart_type':chart_type, 'chart_data':chart_data, 'aobj_id': aobj.id(), 'parent':parent,
                'duration':duration, 'simple':simple}
        return aobj.class_func_call(cls=cls.__name__, params=params)

    @classmethod
    def test_request(cls, methods=['GET']):
        '''Create a testing page containing the component which is being tested'''

        '''
        TODO: Remove WebPageTest class and use WebPage(test=True)
        '''
        with WebPage() as page:
            with page.add_child(WebRow()) as r1:
                with page.add_child(WebColumn()) as c1:
                    with c1.add_child(globals()[cls.__name__](value='example_data', height='400px')) as test:
                        pass

            '''
            Test creating charts by global methods of class instead of object
            '''
            with page.add_child(WebRow()) as row2:
                with row2.add_child(WebColumn(width=['md8'],offset=['mdo2'])) as col2:
                    with col2.add_child(WebDiv(styles={'width': '200px', 'height': '150px'})) as div1:
                        with div1.add_child(WebDiv(styles={'width': '100px', 'height': '100px'})) as div2:
                            with LVar(parent=col2, var_name='$test_chart') as test_chart:
                                test_chart.add_script('$(document.createElementNS(d3.ns.prefix.svg, "svg")); \n',
                                                      indent=False)
                            #test_chart.add_script('$test_chart[0].setAttribute("viewBox","100,100,10000,10000");\n')
                            class_type = None
                            for k, v in OOChartNVD3.OOCHART_CLASSES.items():
                                if v == cls.__name__:
                                    class_type = k
                            OOChartNVD3.CALL_CREATE_FUNC(
                                svg='$test_chart[0]', chart_type=class_type, chart_data='example', aobj=test_chart,
                                parent='$("#{}")[0]'.format(div2.id()), simple=True
                            )
                            col2.add_script('$("#{}").append($test_chart);\n'.format(div2.id()))
            with page.add_child(WebBr()):
                pass
            with page.add_child(WebBr()):
                pass
            with page.add_child(WebBr()):
                pass
        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)


class OOChartLineFinder(OOChartNVD3):

    OOChartNVD3.OOCHART_CLASSES['linefinder'] = __qualname__


class OOChartPie(OOChartNVD3):

    OOChartNVD3.OOCHART_CLASSES['pie'] = __qualname__


class OOChartComulativeLine(OOChartNVD3):

    OOChartNVD3.OOCHART_CLASSES['cline'] = __qualname__


class OOChartLinePlusBar(OOChartNVD3):

    OOChartNVD3.OOCHART_CLASSES['lpbar'] = __qualname__


class OOChartHorizontalGroupedStackedBar(OOChartNVD3):

    OOChartNVD3.OOCHART_CLASSES['hgsbar'] = __qualname__


class OOChartDescreteBar(OOChartNVD3):

    OOChartNVD3.OOCHART_CLASSES['dbar'] = __qualname__


class OOChartStackedArea(OOChartNVD3):

    OOChartNVD3.OOCHART_CLASSES['stackedarea'] = __qualname__


class OOChartLine(OOChartNVD3):

    OOChartNVD3.OOCHART_CLASSES['line'] = __qualname__


class OOChartScatterBubble(OOChartNVD3):

    OOChartNVD3.OOCHART_CLASSES['sbubble'] = __qualname__


class OOChartMultiBar(OOChartNVD3):

    OOChartNVD3.OOCHART_CLASSES['mbar'] = __qualname__


class OOChartBullet(OOChartNVD3):

    OOChartNVD3.OOCHART_CLASSES['bullet'] = __qualname__


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

    RENDER_FUNC_NAME = 'oogselector_render'
    RENDER_FUNC_ARGS = ['that', 'url']

    VAL_BY_BTN_NAME = 'oogeneral_selector_val_by_btn'
    VAL_BY_BTN_PARAMS = ['btn_id']

    @staticmethod
    def data_format():
        return {
            'button': {'name': '', 'select':'', 'options': []},
            'option': {'name': '', 'href': '#'}
        }

    @classmethod
    def test_request(cls, methods=['GET']):
        '''Create a testing page containing the component which is being tested'''

        def on_post():
            req = WebPage.on_post()
            for r in req:
                if r['me'] == 'gs1' or r['me'] == 'gs2':
                    if 'data' not in r:
                        r['data'] = OOGeneralSelector._example_data()
                    for d in r['data']:
                        if not d['options']:
                            option1 = copy.deepcopy(OOGeneralSelector.data_format()['option'])
                            option1['name'] = d['name'] + '_option1'
                            option2 = copy.deepcopy(OOGeneralSelector.data_format()['option'])
                            option2['name'] = d['name'] + '_option2'
                            d['options'].append(option1)
                            d['options'].append(option2)

                            d['name'] = 'test00'
                            d['select'] = option1['name']

            return jsonify({'status': 'success', 'data': req})

        class Page(WebPage):
            URL = '/oogselector_test'

            @classmethod
            def type_(cls):
                return 'WebPage'

        Page.init_page(app=current_app, endpoint=cls.__name__+'.test', on_post=on_post)

        with Page() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c1:
                    with c1.add_child(globals()[cls.__name__](test=True, styles={'display': 'flex'}, name='gs1')) as gs1:
                        pass
            with page.add_child(WebBr()) as br:
                pass
            with page.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c2:
                    with c2.add_child(globals()[cls.__name__](test=True, styles={'display': 'flex'}, name='gs2')) as gs2:
                        pass

        # Test getting general selector value by its button id
        with gs1.on_event_w('change'):
            with LVar(parent=gs1, var_name='gs1_value') as gs1_value:
                gs1.val()
            gs2.val('gs1_value')
            #gs1.alert('"The general selector gs1\'s value:"+gs1_value')

        with gs2.on_event_w('change'):
            with LVar(parent=gs2, var_name='gs2_value') as gs2_value:
                gs2.val()
            gs1.val('gs2_value')
            #gs2.alert('"The general selector gs2\'s value:"+gs2_value')

        with page.render_post_w():
            gs1.render_for_post()
            gs2.render_for_post()

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


class OOBanner(WebDiv):

    def __init__(self, imgs=None, height="300px", interval=3000, **kwargs):
        kwargs['imgs'] = imgs
        kwargs['height'] = height
        kwargs['interval'] = interval
        super().__init__(**kwargs)


class OOCalendar(WebDiv):

    ME_PRE = 'oocalendar_buildin'
    LOAD_TEMPLATE_KEY = ME_PRE + '_loadtemplate_'
    TEMLATE_WEEK_KEY = ME_PRE + '_template_week'
    TEMPLATE_WEEK_DAYS_KEY = ME_PRE + '_template_week-days'
    TEMPLATE_DAY_KEY = ME_PRE + '_template_day'
    TEMPLATE_MONTH_KEY = ME_PRE + '_template_month'
    TEMPLATE_MONTH_DAY_KEY = ME_PRE + '_template_month-day'
    TEMPLATE_YEAR_KEY = ME_PRE + '_template_year'
    TEMPLATE_YEAR_MONTH_KEY = ME_PRE + '_template_year-month'
    TEMPLATE_EVENT_LIST_KEY = ME_PRE + '_template_events-list'
    LOAD_EVENTS_KEY = ME_PRE + '_load_event'

    VAL_FUNC_NAME = 'oocalendar_val'
    VAL_FUNC_ARGS = ['that', 'trigger_event=false']

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
        return [
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
    def on_post(cls,req):

        ret = req
        for r in req:
            if r['me'] == cls.LOAD_EVENTS_KEY:
                ret = cls._example_data()
            elif r['me'] == cls.TEMLATE_WEEK_KEY:
                ret = cls._week()
            elif r['me'] == cls.TEMPLATE_WEEK_DAYS_KEY:
                ret = cls._week_day()
            elif r['me'] == cls.TEMPLATE_DAY_KEY:
                ret = cls._day()
            elif r['me'] == cls.TEMPLATE_MONTH_KEY:
                ret = cls._month()
            elif r['me'] == cls.TEMPLATE_MONTH_DAY_KEY:
                ret = cls._month_day()
            elif r['me'] == cls.TEMPLATE_YEAR_KEY:
                ret = cls._year()
            elif r['me'] == cls.TEMPLATE_YEAR_MONTH_KEY:
                ret = cls._year_month()
            elif r['me'] == cls.TEMPLATE_EVENT_LIST_KEY:
                ret = cls._event_list()
        return ret

    @classmethod
    def test_request(cls, methods=['GET']):
        '''Create a testing page containing the component which is being tested'''

        NAME = 'calendar'

        def on_post():
            req = WebPage.on_post()
            ret = OOCalendar.on_post(req)
            return jsonify({'status':'success','data':ret})

        class Page(WebPage):
            URL = '/OOCalendar_test'

            def type_(self):
                return 'WebPage'

        Page.init_page(app=current_app, endpoint=cls.__name__ + '.test', on_post=on_post)

        with Page() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='200px')) as c1:
                    with c1.add_child(OOCalendarBar()) as bar:
                        pass
            with page.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=['md8'],offset=['mdo2'],
                                            styles={'margin-left':"20px",'margin-right':'20px'})) as c2:
                    with c2.add_child(globals()[cls.__name__]()) as calendar:
                        pass

        '''
        with page.render_post_w():
            calendar.render_for_post()
        '''

        html = page.render()
        return render_template_string(html)


class OOCalendarBar(WebDiv):
    pass


class WebTable(WebComponentBootstrap):

    '''
    WebTable generates a html table from a data including schema and records.
    schema leads to table heads and records lead to table body.
    The implementation of this class is different from other classes. The not all rendering of WebTable is on the
    server side, some render is on client side.

    HOW TO:
        Initial:
            set url
            prepare model and query
            call create_url_rule when initial app

    TODO: Change the members of model and query from class to object
    '''

    def __init__(self, value=None, head_classes=[],
                 body_classes=[], head_styles=None, body_styles=None, url=None, **kwargs):
        self._value = value
        kwargs['value'] = value
        super().__init__(**kwargs)
        WebTable._head_styles = head_styles
        WebTable._body_styles = body_styles
        WebTable._head_classes = head_classes
        WebTable._body_classes = body_classes

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
        if not hasattr(cls, '_body_styles') or not cls._body_styles:
            return ''

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
        if hasattr(cls,'_body_classes') and cls._body_classes:
            return ' '.join(cls._body_classes)
        else:
            return ''

    @classmethod
    def _head_classes_str(cls):
        if hasattr(cls, '_head_classes') and cls._head_classes:
            return ' '.join(cls._head_classes)
        else:
            return ''

    @classmethod
    def _example_data(cls, schema_only = False):
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

        schema = [
                {'name': '事件', 'style': 'width:30%', 'attr': ''},
                {'name': '审批', 'style': 'width:20%', 'attr': '', 'type':'checkbox'},
                {'name': '完成', 'style': '', 'attr': '', 'type':'checkbox'},
                {'name': '审核', 'style': '', 'attr': '', 'type':'checkbox'},
                {'name': '开始', 'style': '', 'attr': ''},
                {'name': '结束', 'style': '', 'attr': ''},
                {'name': '备份', 'style': '', 'attr': ''},
            ]
        if schema_only:
            return schema

        data = {
            'schema': schema,
            'records': []
        }
        for i in range(16):
            approve = True if random.randint(0, 1) else False
            done = True if random.randint(0, 1) else False
            check = True if random.randint(0, 1) else False

            start, end = randDatetimeRange()
            data['records'].append(
                (
                    {'data': _getStr(random.randint(3,6)), 'attr':'nowrap data-ootable-details="This is event name"'},
                    {'data': approve, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                    {'data': done, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                    {'data': check, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                    {'data': start, 'attr':'data-ootable-details="This is start date time"'},
                    {'data': end, 'attr':'data-ootable-details="This is end date time"'},
                    {'data': _getStr(random.randint(10,128)), 'attr':'data-ootable-details="This is details"'}
                )
            )

        return data

    @classmethod
    def _html(cls, data=None, head_class=None, head_style=None):

        if not data:
            _data = self.get_data()
        else:
            _data = data

        if not _data:
            return None

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
                #html.append('    <tr class="{}" style="{}">\n'.format(self._head_classes_str(), self._head_styles_str()))
                html.append(
                    '    <tr class="{}" style="{}">\n'.format(head_class, head_style))
                for th in tr:
                    html.append('        <th class="{}" style="{}" {}><div>{}</div></th>\n'.format(th['class'], th['style'], th['attr'], th['name']))
                html.append('    </tr>\n')

            columns = []
            _columns(matrix, 0, columns, max_cs)

            return columns

        html = []
        columns = []
        if 'schema' in _data and _data['schema']:
            html.append('<thead>\n')
            columns = _head(html, _data['schema'])
            html.append('</thead>\n')

        html.append('<tbody class="{}" style="{}">\n'.format(WebTable._body_classes_str(), WebTable._body_styles_str()))
        for tr in _data['records']:
            html.append('    <tr>\n')
            for i, d in enumerate(tr):
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

    '''
    @classmethod
    def on_post(cls):
        ret = Action.on_post()
        _request = ret['data']
        _data = {'html':''}
        if _request['data'] == 'webtable_render':
            table = globals()[cls.__name__](mytype=['striped', 'hover', 'borderless', 'responsive'])
            _data['html'] = table._html() #TODO: add current user get data into _html(data=current_user.get_data())
        return jsonify({'status':'success','data':_data})
    '''

    @classmethod
    def add_url_rule(cls, app, extend=[]):
        super().add_url_rule(app, extend)
        if extend:
            for e in extend:
                if e['view_func'] == cls.on_post:
                    return
        app.add_url_rule(rule=cls.HTML_URL, endpoint='{}_on_post'.format(cls.__name__), view_func=cls.on_post, methods=['POST']) #move this to extend for applying the custom on_post

    @classmethod
    def test_request(cls, methods=['GET']):

        #cls.add_url_rule(current_app)
        with WebPage() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'],height="400px")) as c1:
                    with c1.add_child(globals()[cls.__name__](mytype=['striped', 'hover', 'borderless', 'responsive'])) as test:
                        pass

        html = page.render()
        return render_template_string(html)


class OOTable(WebTable):

    SETTING = {}
    HTML_URL = '/ootable/ootable_html'

    RENDER_IMG_KEY = 'render_img'
    RENDER_CHART_KEY = 'render_chart'

    VAL_FUNC_NAME = 'ootable_val'
    VAL_FUNC_ARGS = ['that', 'data', 'trigger_event=false']

    RENDER_FUNC_NAME = 'ootable_rander'
    #RENDER_FUNC_ARGS = ['id', 'html', 'setting']
    RENDER_FUNC_ARGS = ['id', 'data']

    COLREORDER_FUNC_NAME = 'ootable_colreorder'
    COLREORDER_FUNC_ARGS = ['id', 'order']

    GET_ROW_DATA_FUNC_NAME = 'ootable_get_row_data'
    GET_ROW_DATA_FUNC_ARGS = ['that', 'data_attr="ootable-details"']

    ROW_CHILD_FUNC_NAME = 'ootable_row_child'
    ROW_CHILD_FUNC_ARGS = ['tr','data_attr=ootable-details']

    ROW_CHILD_FORMAT_FUNC_NAME = 'ootable_row_child_format'
    #ROW_CHILD_FORMAT_FUNC_ARGS = ['tr', 'data']
    ROW_CHILD_FORMAT_FUNC_ARGS = ['tr', 'data=ull']
    ROW_CHILD_FORMAT_FUNC_BODY = (
        '   var $this_tr = $(tr);\n',
        '   var tr_class = $this_tr.attr("class"); if(typeof tr_class == "undefined"){tr_class = ""};\n',
        '   var tr_style = $this_tr.attr("style"); if(typeof tr_style == "undefined"){tr_style = ""};\n',
        '   var this_td_data = data;\n',
        '   var next_tr = \'<tr class="<class>" style="<style>" >\'.replace("<class>", tr_class).replace("<style>", tr_style);\n',
        '   this_td_data.forEach(function(element,index){\n',
        '       let klass="";if(typeof element.klass != "undefined"){ klass = element.klass };\n',
        '       let style="";if(typeof element.style != "undefined"){ style = element.style };\n',
        '       let data="";if(typeof element.data != "undefined"){ data = element.data };\n',
        '       next_tr += \'<td class="!@#class!@#" style="!@#style!@# white-space:pre;background-color:Plum">!@#data!@#</td>\'.replace("!@#class!@#", klass).replace("!@#style!@#", style).replace("!@#data!@#", data)\n',
        '   });\n',
        '   next_tr += "</tr>";\n',
        '   return next_tr;\n',
    )

    CELL_RENDER_FUNC_NAME = 'ootable_cell_render'
    CELL_RENDER_FUNC_ARGS = ['data','type','row','meta']
    CELL_RENDER_FUNC_BODY = (
       "if(data.indexOf('!@#render_img!@#:')==0){\n".replace('!@#render_img!@#', RENDER_IMG_KEY),
       "    return \"<img width='100px' onload=webcomponent_draw_img(this,'60px') src='\"+data.substr('!@#render_img!@#:'.length)+\"'/>\";\n".replace('!@#render_img!@#',RENDER_IMG_KEY),
       "};\n"
       "return data;\n",
    )

    CREATED_CELL_RENDER_FUNC_NAME = 'ootable_created_cell_render'
    CREATED_CELL_RENDER_FUNC_ARGS = ['td','cellData','rowData','row','col']
    CREATED_CELL_RENDER_FUNC_BODY = (
       "if(cellData.indexOf('!@#render_chart!@#:')==0){\n".replace('!@#render_chart!@#', RENDER_CHART_KEY),
       "    let content = cellData.substr('!@#render_chart!@#:'.length);\n".replace('!@#render_chart!@#', RENDER_CHART_KEY),
       "    let chart_type = content.split(';')[0];\n",
       "    let chart_data = content.split(';')[1];\n",
       "    let $svg = $(document.createElementNS(d3.ns.prefix.svg, 'svg'));\n",
       "    let fn = window[chart_data];\n",
       "    $svg.css('width','100px');\n",
       "    $svg.css('height','60px');\n",
       "    {}($svg[0],chart_type,fn(),td,duration=0,simple=true);\n".format(OOChartNVD3.OOCHART_CREATE_FUNC_NAME),
       "    {}($svg[0],chart_type,fn(),td,duration=0,simple=true);\n".format(OOChartNVD3.OOCHART_CREATE_FUNC_NAME),
       "};\n",
    )

    TIMELY_EVENT_QUEUE = "ootable_timely_execute_queue"
    TIMEOUT_EVENT_QUEUE = 'ootable_timeout_execute_queue'

    class OOTableExampleData(ExampleData):

        def example_data_img(self):
            schema = [
                {'name': ''},
                {'name': ''},
                {'name': ''}
            ]
            records = []
            for _ in range(random.randint(6, 10)):
                records.append((
                    {'data': "!@#render_img!@#:".replace('!@#render_img!@#',self.RENDER_IMG_KEY) + url_for('static', filename='img/demo.jpg')},
                    {'data': _getStr(random.randint(3, 6))},
                    {'data': _getStr(random.randint(3, 6))}
                ))
            setting = {
                'scrollY': '200px',
                'scrollX': True,
                'scrollCollapse': True,
                'paging': False,
                'searching': False,
                'destroy': True,
                'colReorder': False,
                'columnDefs': []
            }
            return {'schema': schema, 'records': records, 'setting': setting}

        def example_data_chart(self):
            schema = [
                {'name': ''},
                {'name': ''},
                {'name': ''}
            ]
            records = []
            for _ in range(random.randint(2, 2)):
                records.append((
                    {'data': "!@#render_chart!@#:"+"mbar;oochart_multibar_example_data".replace('!@#render_chart!@#',self.RENDER_CHART_KEY)},
                    {'data': _getStr(random.randint(3, 6))},
                    {'data': _getStr(random.randint(3, 6))}
                ))
            setting = {
                'scrollY': '200px',
                'scrollX': True,
                'scrollCollapse': True,
                'paging': False,
                'searching': False,
                'destroy': True,
                'colReorder': False,
                'columnDefs': []
            }
            return {'schema': schema, 'records': records, 'setting': setting}

        def query(self, test="img"):
            if test == "img":
                return self.example_data_img()
            elif test == "chart":
                return self.example_data_chart()
            else:
                data =  WebTable._example_data()
                data['setting'] = {
                    'scrollY': '200px',
                    'scrollX': True,
                    'scrollCollapse': True,
                    'paging': False,
                    'searching': False,
                    'destroy': True,
                    'colReorder': False,
                    'columnDefs': []
                }
                return data
                raise NotImplementedError

    model = OOTableExampleData()
    query = {'example': True}

    def __init__(self, setting={}, **kwargs):
        if setting:
            OOTable.SETTING = setting
        else:
            OOTable.SETTING = self._example_setting()

        super().__init__(**kwargs)
        #self._html_url = html_url

    def col_reorder(self, order):
        params  = {'order': order}
        return self.func_call(params)

    def search(self, pattern):
        params = {'pattern': pattern}
        return self.func_call(params)

    def customer_search(self, search):
        params = {'search': search}
        return self.func_call(params)

    def columns_adjust(self):
        return self.func_call({})

    def draw(self):
        return self.func_call({})

    @classmethod
    def setting(cls, setting=None):
        if setting:
            cls.SETTING = setting
        else:
            return cls.SETTING

    @classmethod
    def _example_setting(cls):
        return {
                'scrollY': '500px',
                'scrollX': True,
                'scrollCollapse': True,
                'paging': True,
                'searching': True,
                'destroy':True,
                'colReorder': True
            }

    '''
    @classmethod
    def on_post(cls, data=None, methods=['GET','POST']):

        if request.method == 'GET':
            raise NotImplementedError
            return json.dumps({'html': html, 'setting': cls.setting()})
        elif request.method == 'POST': # rule for default value
            if not data:
                data = {'model':None,'value':None}
            if 'setting' not in data or not data['setting']:
                data['setting'] = cls.setting()
            table = OOTable(value=data)
            html = ''.join(table._html())
            return jsonify({'status':'success', 'data': {'html': html, 'setting': data['setting']}})
        else:
            raise NotImplementedError
    '''

    def get_data(self, setting_only=False):
        data = super().get_data()
        if not data:
            return None
        if setting_only:
            return data['setting']
        return {'schema': data['schema'], 'records': data['records']}

    def __enter__(self):
        ret = super().__enter__()
        #self.add_context_list(self._html())
        self.declare_custom_global_func(self.ROW_CHILD_FORMAT_FUNC_NAME, self.ROW_CHILD_FORMAT_FUNC_ARGS,
                                 self.ROW_CHILD_FORMAT_FUNC_BODY)
        self.declare_custom_global_func(self.CELL_RENDER_FUNC_NAME, self.CELL_RENDER_FUNC_ARGS, self.CELL_RENDER_FUNC_BODY)
        self.declare_custom_global_func(self.CREATED_CELL_RENDER_FUNC_NAME, self.CREATED_CELL_RENDER_FUNC_ARGS,
                                 self.CREATED_CELL_RENDER_FUNC_BODY)
        return self

    @classmethod
    def test_request(cls, methods=['GET', 'POST']):

        test_url = '/ootable_test'

        '''
        test_img_url = '/ootable_test_img'
        test_chart_url = '/ootable_test_chart'
        if request.method == 'POST':
            if test_img_url in request.url_rule.rule:
                table = OOTable(value={'model':cls.model,'query':{'test':'img'}})
                html = ''.join(table._html())
                setting = table.get_data(setting_only=True)
                return jsonify({'status': 'success', 'data': {'html': html, 'setting': setting}})
            if test_chart_url in request.url_rule.rule:
                table = OOTable(value={'model':cls.model,'query':{'test':'chart'}})
                html = ''.join(table._html())
                setting = table.get_data(setting_only=True)
                return jsonify({'status': 'success', 'data': {'html': html, 'setting': setting}})
        cls.add_url_rule(app=current_app)
        cls.add_url_rule(app=current_app, extend=[{'rule':test_img_url, 'view_func':cls.test_request, 'methods':['POST']}])
        cls.add_url_rule(app=current_app, extend=[{'rule': test_chart_url, 'view_func': cls.test_request, 'methods': ['POST']}])
        '''

        def on_post():
            ret = WebPage.on_post()
            for r in ret:
                if r['me'] == 'image_table':
                    # table = OOTable(value={'model': cls.model, 'query': {'test': 'img'}})
                    data = OOTable.model.query('img')
                    html = ''.join(OOTable._html(data=data))
                    # setting = table.get_data(setting_only=True)
                    r['data'] = {'html': html, 'setting': data['setting']}
                if r['me'] == 'chart_table':
                    data = OOTable.model.query('chart')
                    # table = OOTable(value={'model': cls.model, 'query': {'test': 'chart'}})
                    html = ''.join(OOTable._html(data=data))
                    # setting = OOTable.get_data(setting_only=True)
                    r['data'] = {'html': html, 'setting': data['setting']}
                if r['me'] == 'test':
                    data = OOTable.model.query("test")
                    html = ''.join(OOTable._html(data=data))
                    # setting = table.get_data(setting_only=True)
                    r['data'] = {'html': html, 'setting': data['setting']}
            return jsonify({'status': 'success', 'data': ret})

        class Page(WebPage):
            URL = test_url
            def type_(self):
                return 'WebPage'

        Page.init_page(app=current_app, endpoint=cls.__name__+'.test', on_post=on_post)

        with Page() as page:
            with page.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c2:
                    with c2.add_child(WebInput(value='')) as input:
                        pass

            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c1:
                    with c1.add_child(globals()[cls.__name__](value='test', mytype=['striped', 'hover', 'borderless', 'responsive'])) as test:
                        #test.render_func()
                        customer_search = []
                        customer_search.append('var filter = $("#{}").val();\n'.format(input.id()))
                        customer_search.append('if (! filter || data[0] === filter){\n')
                        customer_search.append('    return true;\n')
                        customer_search.append('}else{\n')
                        customer_search.append('    return false;\n')
                        customer_search.append('};\n')
                        test.customer_search(customer_search)

            '''
            with page.add_child(WebRow()) as r3:
                with r3.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as r3:
                    with r3.add_child(WebBtn(value='render')) as render_btn:
                        with render_btn.on_event_w('click'):
                            render_btn.alert('"rendering again"')
                            with LVar(parent=render_btn,var_name='post_data') as post_data:
                                post_data.add_script('{"data":"ootable_rander"}', indent=False)
                            with LVar(parent=render_btn, var_name='url') as url_data:
                                test.url()
                            with test.post_w(url='url',data='post_data'):
                                test.call_custom_func(
                                    fname=test.RENDER_FUNC_NAME,
                                    fparams={
                                        'id': '"{}"'.format(test.id()),
                                        'data': 'data',
                                    }
                                )
                    with r3.add_child(WebBtn(value='Reorder')) as reorder_btn:
                        with reorder_btn.on_event_w('click'):
                            reorder_btn.alert('"Reorder columns"')
                            test.call_custom_func(fname=test.COLREORDER_FUNC_NAME, fparams={'id':'"{}"'.format(test.id()), 'order':'[6,5,4,3,2,1,0]'})
            '''
            with page.add_child(WebBr()):
                pass

            with page.add_child(WebRow()) as r4:
                with r4.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c4:
                    with c4.add_child(OOTable(value='image_table',
                                              mytype=['striped', 'hover', 'borderless', 'responsive'])) as image_table:
                        pass
            with page.add_child(WebBr()):
                pass

            with page.add_child(WebRow()) as r5:
                with r5.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c5:
                    with c5.add_child(OOTable(value='chart_table',
                                              mytype=['striped', 'hover', 'borderless', 'responsive'],
                                              )) as chart_table:
                        pass
            with page.add_child(WebBr()):
                pass

        '''
        with test.on_event_w('timeout'):
            test.add_script('console.log("ootable on timeout event");\n')
            test.columns_adjust()

        with input.on_event_w('change'):
            page.alert('"searching ... "')
            test.draw()

        with test.on_event_w('click_row'):
            test.call_custom_func(fname=test.ROW_CHILD_FUNC_NAME, fparams={'tr': 'that'})
        '''

        with page.render_post_w():
            test.render_for_post()
            image_table.render_for_post()
            chart_table.render_for_post()

        with image_table.on_event_w('click_row'):
            image_table.alert('"Click_row!" + ootable_get_rowinfo(that)')

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

    HTML_URL = '/ootaggroup/ootaggroup_html'

    def __init__(self, value=[], col_num = 0, **kwargs):
        super().__init__(**kwargs)
        self._value = value
        if col_num:
            OOTagGroup.COL_NUM = col_num

    @classmethod
    def _example_setting(cls):
        return {
        'paging': False,
        'scrollY': '500px',
        'scrollX': True,
        'searching': True,
        'scrollCollapse': True,
    }

    @classmethod
    def _example_data(cls, schema_only = False):
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
        return data

    '''
    @classmethod
    def on_post(cls):
        ret = Action.on_post()
        _request = ret['data']
        _data = {'html': ''}
        if _request['data'] == 'webtable_render':
            table = OOTagGroup()
            _data['html'] = table._html()  # TODO: add current user get data into _html(data=current_user.get_data())
        return jsonify({'status': 'success', 'data': _data})
    '''

    @classmethod
    def test_request(cls, methods=['GET']):
        cls.add_url_rule(app=current_app)
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

    def __init__(self, parent, var_name, **kwargs):
        kwargs['parent'] = parent
        kwargs['var_name'] = var_name
        super().__init__(**kwargs)
        self._var_name = var_name

    def __repr__(self):
        return self._var_name


class LVar(Var):
    pass


class GVar(Var):

    @classmethod
    def test_request(cls, methods=['GET']):
        with WebPage(test=True) as page:
            with page.add_child(WebHead1(value='Test GVar and js values')) as head1:
                pass
            with page.add_child(WebHead3(value='var test = false;')) as head3:
                pass
            with page.add_child(GVar(parent=page, var_name='test')) as gv:
                gv.false
            with page.add_child(WebBtn(value='Test GVar assign')) as btn:
                pass

        with btn.on_event_w('click'):
            with gv.assign_w():
                gv.true
            btn.alert('"GVar value should be true, real:"+test')


class OOList(ListInf, WebComponentBootstrap):

    @contextmanager
    def append_w(self):
        params = {}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            print("Error: exception err:{}".format(err))
            raise Exception(err)
        finally:
            self._pop_current_context()

    @classmethod
    def test_request(cls, methods=['GET']):
        with WebPage() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c1:
                    with c1.add_child(WebBtn(value='test')) as btn1:
                        pass

        with btn1.on_event_w('click'):
            with LVar(parent=btn1) as data:
                with OOList(parent=data) as list_data:
                    with list_data.append():
                        btn1.val()
                    with list_data.append():
                        btn1.val()
            btn1.alert("data.join(' ')")

        html = page.render()
        return render_template_string(html)

    def __init__(self, parent, var_name=None, **kwargs):
        kwargs['parent'] = parent
        kwargs['var_name'] = var_name
        super().__init__(**kwargs)
        self._var_name = var_name

    def __repr__(self):
        return self._var_name


class OODict(DictInf, WebComponentBootstrap):

    def __init__(self, parent, var_name=None, **kwargs):
        kwargs['parent'] = parent
        kwargs['var_name'] = var_name
        super().__init__(**kwargs)
        self._var_name = var_name

    def __repr__(self):
        return self._var_name

    @contextmanager
    def update_w(self, key):
        params={'key':key}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

    @classmethod
    def test_request(cls, methods=['GET']):
        with WebPage(test=True) as page:
            with page.add_child(WebBtn(value='Test dict')) as btn1:
                pass
            with page.add_child(WebBtn(value='Test dict update')) as btn2:
                pass

        with btn1.on_event_w('click'):
            with OODict(parent=page, dict={'key1': 'val1', 'key2': 'val2'}, var_name='test_dict') as dict:
                pass
            btn1.alert('"Test dict: { key1:" + test_dict.key1 + "}"')

        with btn2.on_event_w("click"):
            with OODict(parent=page, dict={'key1': 'val1', 'key2': 'val2'}, var_name='test_dict_update') as dict_update:
                pass
            with dict_update.update_w(key='key2'):
                dict_update.add_script('"val_updated"', indent=False)
            btn2.alert('"Test dict update: { key2:" + test_dict_update.key2 + "}"')


        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)
