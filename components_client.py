#########################################
# Author         : Haibo Zhu             
# Email          : haibo.zhu@hotmail.com 
# created        : 2019-08-09 20:19 
# Last modified  : 2019-08-09 20:19
# Filename       : components_client.py
# Description    :                       
#########################################
import sys
sys.path.append(".")
import calendar
import datetime as dt
import inspect
import sys
import uuid

import dateutil.parser
from dateutil.relativedelta import relativedelta
import numpy as np
from flask import Blueprint, request
from interfaces import *
from requests import post
from share import create_payload, extract_data, APIs, _getStr, day_2_week_number
from test_class import *
import json
import oocc_define as ooccd

sys.setrecursionlimit(2000)


class Response(AppearanceInf, PositionInf, PropertyInf):

    def __init__(self, **kwargs):
        self._response = None

    # AppearanceInf
    def width(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))

    def height(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))

    def color(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))

    def font(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))

    def border(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))

    def disable(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))
    # End AppearanceInf

    # PositionInf
    def pad(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))

    def margin(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))

    def align(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))

    def offset(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))
    # End PositionInf

    # PropertyInf
    def value(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))

    def attrs(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))

    def classes(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))

    def styles(self, **kwargs):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} hasn't been implemented really!".format(c_name, f_name))
    # End PropertyInf

    def on_post(self):
        """
        The process function to response the post request from the WebComponent itself
        TODO: Query data by user model

        :return: jsonify({'status':'success','data': data})
        """
        data_j = request.form.get('data')
        if data_j:
            data = json.loads(request.form.get('data'))
            return data
        return []
        # return {"status": "sucess", 'data': data['data'], 'me':data['me']}


class ClientBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def id(self):
        pass

    @abc.abstractmethod
    def add_context(self, context):
        pass

    @abc.abstractmethod
    def _get_objcall_context(self, func, caller_id, params):
        pass

    def context_call(self, params):
        context = self._get_objcall_context(func='add_context', caller_id=self.id(), params=params)
        self.add_context(context)
        return context

    def func_call(self, params):
        context = self._get_objcall_context(
            func=inspect.stack()[1][3], caller_id=self.id(), params=params)
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


class Action(CommandInf, ActionInf):

    DRAW_IMG_FUNC_NAME = 'webcomponent_draw_img'
    DRAW_IMG_FUNC_ARG = ['img', 'height']


"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    @contextmanager
    def for_w(self):
        raise NotImplementedError

    def equal(self, right, left=None, force_condition=False):
        params = {'right': right, 'left': left, 'force_condition': force_condition}
        self.func_call(params=params)

    def is_js(self):
        raise NotImplementedError

    def set_js(self, js_):
        params = {'js_': js_}
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

    def declare_custom_func(self, fname='', fparams=[], fbody=[]):
        params = {'fname': fname, 'fparams': fparams, 'fbody': fbody}
        return self.func_call(params)

    def declare_custom_global_func(self, fname, fparams=[], fbody=[]):
        params = {'fname': fname, 'fparams': fparams, 'fbody': fbody}
        return self.func_call(params)

    def call_custom_func(self, fname='', fparams={}):
        params = {'fname': fname, 'fparams': fparams}
        return self.func_call(params)

    '''
    def is_(self, element_name):
        params = {'element_name': element_name}
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
    
    def has_class(self, class_):
        raise NotImplementedError

    def add_class(self, class_):
        params = {'class_': class_}
        return self.func_call(params)
    
    def remove_class(self, class_):
        params = {'class_': class_}
        return self.func_call(params)

    def add_attrs(self, attrs):
        params = {'attrs': attrs}
        return self.func_call(params)

    def remove_attrs(self, attrs):
        params = {'attrs', attrs}
        return self.func_call(params)
    '''

    @classmethod
    def on_post(cls):
        '''
        The process function to response the post request from the WebComponent itself
        TODO: Query data by user model

        :return: jsonify({'status':'success','data': data})
        '''
        data = json.loads(request.form.get('data'))
        if isinstance(data, list):
            all_is_str = True
            for d in data:
                if not isinstance(d, str):
                    all_is_str = False
            if all_is_str:
                data_a = [json.loads(d) for d in data]
                data = data_a
        return data
        # return {"status": "sucess", 'data': data, 'me': req['me']}

    '''
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
        data_ = data
        if not isinstance(data, str):
            data_ = '{}'.format(str(data))
        url_ = url
        if not isinstance(url, str):
            url_ = '"{}"'.format(str(url))
        params = {'url': str(url), 'data': data_, 'success': success}
        self.with_call(params)
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()
    '''

    def alert(self, message=''):
        params = {'message': message}
        return self.func_call(params)

    '''
    def execute_list_name(self, action_name):
        params = {'action_name': action_name}
        return self.func_call(params)
    '''

    @contextmanager
    def on_event_w(self, event, filter='', propagation=None):
        '''
        context = self._get_objcall_context(func='with', caller_id=self.id(),
                                            params={'function': inspect.stack()[0][3], 'params': {'event':event,'filter':filter}})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        '''
        params = {'event': event, 'filter': filter, 'propagation': propagation}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

    '''
    def stop_event(self, event, filter='', stop=False):
        params = {'event': event, 'filter': filter, 'stop': stop}
        self.func_call(params)
    '''

    def trigger_event(self, event):
        params = {'event': event}
        self.func_call(params)

    def val(self, value=None):
        if value:
            params = {'value': value}
        else:
            params = {}
        self.func_call(params)

    '''
    def empty(self):
        params = {}
        self.func_call(params)
    '''

    def _example_data(cls):
        raise NotImplementedError

    '''
    @property
    def true(self):
        params = {}
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
        params = {'event': event, 'use_clsname': use_clsname, 'selector': selector, 'filter': filter}
        return self.func_call(params)
    '''

    def sync(self, sync=True):
        params = {'sync': sync}
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

    @contextmanager
    def timeout_w(self, time=None):
        params = {'time': time}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            print('Error: exception err:{}'.format(err))
            raise Exception(err)
        finally:
            self._pop_current_context()

    def width(self, width=None):
        params = {'width': width}
        return self.func_call(params)

    def height(self, height=None):
        params = {'height': height}
        return self.func_call(params)

    def color(self, color=None):
        params = {'color': color}
        return self.func_call(params)

    def font(self, font=None):
        params = {'font': font}
        return self.func_call(params)

    def border(self, border=None):
        params = {'border': border}
        return self.func_call(params)

    def disable(self, disable):
        params = {'disable': disable}
        self.func_call(params)

    def value(self, value=None):
        params = {'value': value}
        return self.func_call(params)

    def attrs(self, attrs=None):
        params = {'attrs': attrs}
        return self.func_call(params)

    def classes(self, classes=None):
        params = {'classes': classes}
        return self.func_call(params)

    def styles(self, styles=None):
        params = {'styles': styles}
        return self.func_call(params)

    def pad(self, pad=None):
        params = {'pad': pad}
        return self.func_call(params)

    def margin(self, margin=None):
        params = {'margin': margin}
        return self.func_call(params)

    def align(self, align=None):
        params = {'align': align}
        return self.func_call(params)


class ActionJquery(Action):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    @contextmanager
    def for_w(self):
        raise NotImplementedError

    def equal(self, right, left=None, force_condition=False):
        params = {'right': right, 'left': left, 'force_condition': force_condition}
        self.func_call(params=params)

    def is_js(self):
        raise NotImplementedError

    def set_js(self, js_):
        params = {'js_': js_}
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

    def declare_custom_func(self, fname='', fparams=[], fbody=[]):
        params = {'fname': fname, 'fparams': fparams, 'fbody': fbody}
        return self.func_call(params)

    def declare_custom_global_func(self, fname, fparams=[], fbody=[]):
        params = {'fname': fname, 'fparams': fparams, 'fbody': fbody}
        return self.func_call(params)

    def call_custom_func(self, fname='', fparams={}):
        params = {'fname': fname, 'fparams': fparams}
        return self.func_call(params)

    '''
    def is_(self, element_name):
        params = {'element_name': element_name}
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

    def has_class(self, class_):
        raise NotImplementedError

    def add_class(self, class_):
        params = {'class_': class_}
        return self.func_call(params)

    def remove_class(self, class_):
        params = {'class_': class_}
        return self.func_call(params)

    def add_attrs(self, attrs):
        params = {'attrs': attrs}
        return self.func_call(params)

    def remove_attrs(self, attrs):
        params = {'attrs', attrs}
        return self.func_call(params)
    '''

    @classmethod
    def on_post(cls):
        '''
        The process function to response the post request from the WebComponent itself
        TODO: Query data by user model

        :return: jsonify({'status':'success','data': data})
        '''
        data = json.loads(request.form.get('data'))
        if isinstance(data, list):
            all_is_str = True
            for d in data:
                if not isinstance(d, str):
                    all_is_str = False
            if all_is_str:
                data_a = [json.loads(d) for d in data]
                data = data_a
        return data
        # return {"status": "sucess", 'data': data, 'me': req['me']}

    '''
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
        data_ = data
        if not isinstance(data, str):
            data_ = '{}'.format(str(data))
        url_ = url
        if not isinstance(url, str):
            url_ = '"{}"'.format(str(url))
        params = {'url': str(url), 'data': data_, 'success': success}
        self.with_call(params)
        try:
            yield
        except:
            pass
        finally:
            self._pop_current_context()
    '''

    '''
    def execute_list_name(self, action_name):
        params = {'action_name': action_name}
        return self.func_call(params)
    '''

    @contextmanager
    def on_event_w(self, event, filter='', propagation=None):
        params = {'event': event, 'filter': filter, 'propagation': propagation}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

    '''
    def stop_event(self, event, filter='', stop=False):
        params = {'event': event, 'filter': filter, 'stop': stop}
        self.func_call(params)
    '''

    def trigger_event(self, event):
        params = {'event': event}
        self.func_call(params)

    def val(self, value=None):
        if value:
            params = {'value': value}
        else:
            params = {}
        self.func_call(params)

    '''
    def empty(self):
        params = {}
        self.func_call(params)
    '''

    def _example_data(cls):
        raise NotImplementedError

    @classmethod
    def add_url_rule(cls, app, extend=[]):
        if extend:
            for e in extend:
                if 'endpoint' in e and e['endpoint'] and 'methods' in e and e['methods']:
                    app.add_url_rule(rule=e['rule'], endpoint=e['endpoint'], view_func=e['view_func'],
                                     methods=e['methods'])
                elif 'endpoint' in e and e['endpoint']:
                    app.add_url_rule(rule=e['rule'], endpoint=e['endpoint'], view_func=e['view_func'])
                elif 'methods' in e and e['methods']:
                    app.add_url_rule(rule=e['rule'], view_func=e['view_func'], methods=e['methods'])
                elif not 'rule' in e or not e['rule'] or not 'view_func' in e or not e['view_func']:
                    raise RuntimeError('add_url_rule extend should have "rule" and "view_func"')
                else:
                    url = e['rule']
                    app.add_url_rule(rule=url, view_func=e['view_func'])

    '''
    @property
    def true(self):
        params = {}
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
        params = {'event': event, 'use_clsname': use_clsname, 'selector': selector, 'filter': filter}
        return self.func_call(params)
    '''

    def sync(self, sync=True):
        params = {'sync': sync}
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

    @contextmanager
    def timeout_w(self, time=None):
        params = {'time': time}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            print('Error: exception err:{}'.format(err))
            raise Exception(err)
        finally:
            self._pop_current_context()

    def width(self, width=None):
        params = {'width': width}
        return self.func_call(params)

    def height(self, height=None):
        params = {'height': height}
        return self.func_call(params)

    def color(self, color=None):
        params = {'color': color}
        return self.func_call(params)

    def font(self, font=None):
        params = {'font': font}
        return self.func_call(params)

    def border(self, border=None):
        params = {'border': border}
        return self.func_call(params)

    def disable(self, disable):
        params = {'disable': disable}
        self.func_call(params)

    def value(self, value=None):
        params = {'value': value}
        return self.func_call(params)

    def attr(self, attr=None):
        params = {'attr': attr}
        return self.func_call(params)

    def classes(self, classes=None):
        params = {'classes': classes}
        return self.func_call(params)

    def styles(self, styles=None):
        params = {'styles': styles}
        return self.func_call(params)

    def pad(self, pad=None):
        params = {'pad': pad}
        return self.func_call(params)

    def margin(self, margin=None):
        params = {'margin': margin}
        return self.func_call(params)

    def align(self, align=None):
        params = {'align': align}
        return self.func_call(params)


class Format(FormatInf):

    # Position
    def pad(self, pad=None):
        params = {'pad': pad}
        return  self.func_call(params=params)

    def margin(self, margin=None):
        params = {'margin': margin}
        return self.func_call(params=params)

    def align(self, align=None):
        params = {'align': align}
        return self.func_call(params=params)
    # End position

    # Appearance
    def width(self, width=None):
        params = {'width': width}
        return self.func_call(params=params)

    def height(self, height=None):
        params = {'height': height}
        return self.func_call(params=params)

    def color(self, color=None):
        params = {'color': color}
        return self.func_call(params=params)

    def font(self, font=None):
        params = {'font': font}
        return self.func_call(params=params)

    def border(self, border=None):
        params = {'border': border}
        return self.func_call(params)

    def disable(self, disable=None):
        params = {'disable': disable}
        return self.func_call(params)
    # End appearance

    # Property
    def value(self, value=None):
        raise NotImplementedError

    def attrs(self, attrs=None):
        raise NotImplementedError

    '''
    def attrs_str(self):
        raise NotImplementedError

    def add_attrs(self, att):
        raise NotImplementedError

    def remove_att(self, att):
        raise NotImplementedError
    '''

    def classes(self, classes=None):
        raise NotImplementedError

    '''
    def classes_str(self):
        raise NotImplementedError

    def add_class(self, class_):
        params = {'class_': class_}
        return self.func_call(params=params)

    def remove_class(self, class_):
        params = {'class_': class_}
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
    '''

    def styles(self, style=None):
        raise NotImplementedError

    '''
    def styles_str(self):
        raise NotImplementedError

    def border_radius(self, radius=None):
        params = {'radius': radius}
        self.func_call(params)
    '''
    #End property


class FormatBootstrap(Format):

    '''
    @staticmethod
    def get_sub_classes(cls):

        for subclass in cls.__subclasses__():
            if (not (subclass.__name__) in cls._SUBCLASSES.keys()) and (subclass.__name__.find('Inf') < 0) \
                    and (subclass.__name__.find('WebPage') < 0) and (subclass.__name__.find('WebNav') < 0):
                cls._SUBCLASSES[subclass.__name__] = subclass
                cls.get_sub_classes(subclass)

        return cls._SUBCLASSES
    '''

    @classmethod
    def create_default_nav_items(cls):
        menu = {
            'title': {'name': 'OwwwO', 'action': cls.DEFAULT_URL},
            'menu_list': [
                {'name': 'test menu 1', 'action': cls.DEFAULT_URL},
                {'name': 'test menu 2', 'action': cls.DEFAULT_URL}
            ],
            'login': {
                'site_name': 'OwwwO',
                'is_login': False,
                'login_name': 'TestUser',
                'login_href': cls.DEFAULT_URL,
                'logout_href': cls.DEFAULT_URL
            }
        }
        return menu
"""


class WebComponent(ComponentInf, ClientBase):


    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    '''
    _context = None
    _cur_context_stack = []

    # ComponentInf

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
        assert (child)
        assert (not child_id)
        assert (not objs)
        self._children.add(child)
        child._parent = self
        assert(self._page)
        assert(isinstance(self._page, WebPage))
        child._page = self._page
        if child.name() not in self._page._components.keys():
            self._page._components[child.name()] = {'obj': child}

        params = {'child_id': child.id()}
        self.func_call(params)
        return child

    def remove_child(self, child=None, child_id=None, objs=None):
        pass

    def empty_children(self):
        self._children.clear()

    def parent(self, parent=None):
        raise NotImplementedError

    def module(self):
        raise NotImplementedError

    def url(self, url=None, js=True):

        if not js:
            if not url:
                if self._parent:
                    return self._parent.url(js=js)
                else:
                    return self._url
            else:
                self._url = url
                return url
        else:
            params = {'url': url, 'js': js}
            self.func_call(params)

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
            'scripts': rdata['scripts'],
            'script_files': rdata['script_files'],
            'styles': rdata['styles'],
            'styles_files': rdata['style_files']
        }

    def context(self):
        if self._parent:
            return self._parent.context()
        else:
            return self._context

    def add_context(self, cont):
        return self._add_context(cont)

    def add_context_indent(self, indent):
        raise NotImplementedError

    def get_context_indent(self):
        raise NotImplementedError

    def add_scripts(self, scripts, indent=True, place=None):
        raise NotImplementedError

    def replace_scripts(self, stub, scripts):
        raise NotImplementedError

    def add_scripts_files(self, files):
        raise NotImplementedError

    def get_scripts_files(self):
        raise NotImplementedError

    def set_scripts_indent(self, indent):
        raise NotImplementedError

    def get_scripts_indent(self):
        raise NotImplementedError

    def add_styles(self, styles):
        raise NotImplementedError

    def get_styles(self):
        raise NotImplementedError

    def add_styles_files(self, files):
        raise NotImplementedError

    def get_styles_files(self):
        raise NotImplementedError

    @classmethod
    def add_url_rule(cls, app, extend=[]):
        if extend:
            for e in extend:
                if 'endpoint' in e and e['endpoint'] and 'methods' in e and e['methods']:
                    app.add_url_rule(rule=e['rule'], endpoint=e['endpoint'], view_func=e['view_func'],
                                     methods=e['methods'])
                elif 'endpoint' in e and e['endpoint']:
                    app.add_url_rule(rule=e['rule'], endpoint=e['endpoint'], view_func=e['view_func'])
                elif 'methods' in e and e['methods']:
                    app.add_url_rule(rule=e['rule'], view_func=e['view_func'], methods=e['methods'])
                elif not 'rule' in e or not e['rule'] or not 'view_func' in e or not e['view_func']:
                    raise RuntimeError('add_url_rule extend should have "rule" and "view_func"')
                else:
                    url = e['rule']
                    app.add_url_rule(rule=url, view_func=e['view_func'])

    def render(self):
        raise RuntimeError('{}.render should be removed, for only page need render for now.'.
                           format(self.__class__.__name__))
        '''
        render and return a complete page information in html
        :return:
        '''
        # components = components_factory(self.context())
        payload = create_payload(self.context())
        # print('WebPage::render api:{}'.format(self._ap_i))
        r = post(url=self._api, json=payload)
        html = extract_data(r.json()['data'])
        return render_template_string(html)

    def is_js(self):
        raise NotImplementedError

    def set_js(self, js):
        raise NotImplementedError

    def is_condition(self):
        raise NotImplementedError

    def set_condition(self, cond):
        raise NotImplementedError

    @classmethod
    def _add_context(cls, cont):
        if len(cls._cur_context_stack) == 0:
            cls._cur_context_stack.append([])
        cls._cur_context_stack[-1].append(cont)

        return cls._cur_context_stack[-1]

    @classmethod
    def set_context(cls, context):
        WebComponent._context = context
        WebComponent._cur_context_stack = [WebComponent._context]

    # End ComponentInf

    # My methods

    def _get_objcall_context(self, func, caller_id=None, params=None, sub_context=[]):
        """
        Convert an object call to context

        :param func: function name
        :param caller_id: caller id
        :param params: parameters in dict
        :param sub_context: sub context
        :return: context in dict
        """

        def convert_param_obj(params):
            if isinstance(params, str):
                print("error: params is instance of _str")
            for k, v in params.items():
                if k == 'params':
                    convert_param_obj(v)
                if isinstance(v, WebComponent):
                    params[k] = {'obj_id': v.id()}

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
                print("error: params is instance of _str")
            for k, v in params.items():
                if k == 'params':
                    convert_param_obj(v)
                if isinstance(v, WebComponent):
                    params[k] = {'obj_id': v.id()}

        convert_param_obj(params)
        return {
            'function': 'classmethod:' + cls + '.' + func,
            'params': params,
            'sub_context': sub_context
        }

    def __init__(self, test=False, client=True, **kwargs):
        self._client = client
        kwargs['client'] = client
        super().__init__(**kwargs)
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

        '''
        if page:
            assert(isinstance(page, WebPage))
        elif isinstance(self, WebPage):
            page = self
        else:
            wrapper_frame = sys._getframe(2)
            page = wrapper_frame.f_locals['current_page']
        assert(page)
        self._page = page
        '''

        page = None
        if 'page' in kwargs and kwargs['page']:
            page = kwargs['page']
            assert (isinstance(page, WebPage))
        elif isinstance(self, WebPage):
            page = self
        else:
            stack = inspect.stack()
            wrapper_index = 0
            ROP_find = False
            for level in stack:
                if level.function.find('ROP_wrapped_function') >= 0:
                    ROP_find = True
                    break
                wrapper_index += 1
            if ROP_find:
                wrapper_frame = sys._getframe(wrapper_index)
                page = wrapper_frame.f_locals['current_page']
            else:
                raise RuntimeError("Not able to find page in stack, "
                                   "may add RuntimeOnPage someware ahead of this class:{} is instanced".
                                   format(self.__class__.__name__))
        assert (page)
        self._page = page
        kwargs['page_id'] = page.id()

        self._children = set()
        if 'children' in kwargs:
            self._children = kwargs['children']

        kwargs['name'] = self.name()
        kwargs['id'] = self.id()
        if hasattr(self, '_nav_items'):
            kwargs['nav'] = self._nav_items
        if self.__class__.__name__.find("WebPage") != 0:
            kwargs['test'] = test
        else:
            kwargs['test'] = False

        if hasattr(self, '_value') and 'value' not in kwargs:
            kwargs['value'] = self._value

        context = self._get_objcall_context(func=self.type_(), params=kwargs)
        # self._mycont = self.add_context(context)
        self._mycont = [context]
        self.add_context(context)
        self._components = None

    def set_api(self):
        if hasattr(self, "app") and self.app:
            self._api = self.app.config['API_URL'] + APIs['render'].format('v1.0')
        else:
            if current_app:
                self._api = current_app.config['API_URL'] + APIs['render'].format('v1.0')

    def type_(self):
        return self.__class__.__name__

    @classmethod
    def _push_current_context(cls, cont):
        cls._cur_context_stack.append(cont)

    @classmethod
    def _pop_current_context(cls):
        cls._cur_context_stack.pop()

    def true(self):
        params = {}
        return self.func_call(params)

    def false(self):
        params = {}
        return self.func_call(params)

    def null(self):
        params = {}
        return self.func_call(params)

    # End my methods

    '''
    def add_style_files(self, files):
        raise NotImplementedError
    '''

    '''
    def add_script(self, scripts, indent=True, place=None):
        params = {'scripts': scripts, 'indent': indent, "place": place}
        return self.func_call(params)

    def add_script_files(self, files):
        params = {'files': files}
        return self.func_call(params)

    def get_script_files(self):
        raise NotImplementedError

    def set_script_indent(self, indent):
        params = {'indent': indent}
        return self.func_call(params)

    def get_script_indent(self):
        raise NotImplementedError
    '''

    '''
    def get_style_files(self):
        raise NotImplementedError
    '''

    '''
    def url_for(self, context):
        pass
    '''

    '''
    def add_context_list(self, context_list, indent=True):
        self.context_call(params={'context': ''.join(context_list)})
    '''

    '''
    def add_script_list(self, script_list):
        raise NotImplementedError
    '''

    '''
    def remove_context(self, cont):
        self._remove_context(cont)

    @classmethod
    def _remove_context(cls, cont=None):
        if not cont:
            del cls._cur_context_stack[-1]
        else:
            for i, v in enumerate(cls._cur_context_stack):
                if v == cont:
                    del cls._cur_context_stack[i]
    '''

    '''
    def scripts(self):
        raise NotImplementedError
    '''

    '''
    def add_script_list(self, script_list, indent=True, place=None):
        
        params = {'script_list': script_list, 'indent': indent, 'place': place}
        return self.func_call(params)

    def styles(self):
        raise NotImplementedError
        
    @contextmanager
    def cmds(self):
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
    '''

    '''
    @classmethod
    def test_request(cls, methods=['GET']):
        
        with WebPage() as page:
            with page.add_child(globals()[cls.__name__](test=True)) as test:
                pass
        html = page.render()
        print(pprint.pformat(html))
        return render_template_string(html)
    '''

    '''
    @contextmanager
    def var_w(self, name='data'):
       
        params = {'name': name}
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
        if hasattr(self, '_value') and 'model' in self._value:
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
        
    def events_default_action(self, req):
        pass
    '''

    '''
    def has_class(self, class_):
        raise NotImplementedError

    def is_width(self, width):

        params = {'width': width}
        return self.func_call(params)

    def remove_width(self, width):

        params = {'width': width}
        return self.func_call(params)

    def set_width(self, width):
        params = {'width': width}
        return self.func_call(params)

    def value(self, value):
        params = {'value': value}
        return self.func_call(params)

    def val(self, value=''):
        params = {'value': value}
        return self.func_call(params)


    def is_js_kw(self):
        pass

    def test_init(self):
        if (not hasattr(self, '_value')) or (not self._value):
            self._value = self.__class__.__name__ + 'Test'

    def action(self, req):
        print('Got request')
        if req:
            print('     req["me"]:{}'.format(req['me']))

    '''

    BASE_VAL_FUNC_NAME = 'ooweb_base_val'
    BASE_VAL_FUNC_PARAMS = ['that', 'data=null', 'trigger_event=false', 'return_parts=["all"]']

    VAL_FUNC_NAME = 'ooweb_val'
    VAL_FUNC_PARAMS = BASE_VAL_FUNC_PARAMS


class WebComponentBootstrap(WebComponent,
                            EventInf, AppearanceInf, PositionInf, PropertyInf,
                            CommandInf,
                            ClassTest, ClientBase):

    ACTION_MEMBER = ooccd.ACTION_MEMBER
    FORMAT_MEMBER = ooccd.FORMAT_MEMBER
    RESPONSE_MEMBER = ooccd.RESPONSE_MEMBER

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        '''
        self._derive_event_members(**kwargs)
        self._format = FormatBootstrap(**kwargs)
        self._action = ActionJquery(component=self, **kwargs)
        self._format = FormatBootstrap(component=self, **kwargs)
        self._derive_format_members(**kwargs)
        self._derive_action_members(**kwargs)
        '''

    # EventInf

    @contextmanager
    def on_event_w(self, event, filter='', propagation=None):
        params = {'event': event, 'filter': filter, 'propagation': propagation}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

    @contextmanager
    def render_post_w(self, post_async=True):
        params = {'post_async': post_async}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

    def render_for_post(self, trigger_event=False, return_parts=["all"]):
        params = {'trigger_event': trigger_event, 'return_parts': return_parts}
        return self.func_call(params)

    def trigger_event(self, event):
        params = {'event': event}
        return self.func_call(params=params)
    
    def sync(self, sync=True):
        params = {'sync': sync}
        return self.func_call(params=params)
    
    def timeout_w(self, time):
        params = {'time': time}
        return self.func_call(params=params)

    # End EventInf

    # Appearance members
    def width(self, width=None):
        params = {'width':width}
        return self.func_call(params=params)

    def height(self, height=None):
        params = {'height':height}
        return self.func_call(params=params)

    def color(self, color=None):
        params = {'color':color}
        return self.func_call(params=params)

    def font(self, font=None):
        params = {'font':font}
        return self.func_call(params=params)

    def border(self, border=None):
        params = {'border':border}
        return self.func_call(params=params)

    def disable(self, disable=None):
        params = {'disable': disable}
        return self.func_call(params=params)
    # End appearance

    # Position
    def pad(self, pad=None):
        params = {'pad': pad}
        return self.func_call(params=params)

    def margin(self, margin=None):
        params = {'margin':margin}
        return self.func_call(params=params)

    def align(self, align=None):
        params = {'align': align}
        return self.func_call(params=params)

    def offset(self, offset=None):
        params = {'offset': offset}
        return self.func_call(params=params)
    # End position

    # Property.
    def value(self, value=None):
        params = {'value': value}
        return self.func_call(params=params)

    def attrs(self, attrs=None):
        params = {'attrs': attrs}
        return self.func_call(params=params)

    def classes(self, classes=None):
        params = {'classes': classes}
        return self.func_call(params=params)

    def styles(self, styles=None):
        params = {'styles': styles}
        return self.func_call(params=params)
    # End property

    # CommandInf
    def call_custom_func(self, fname='', fparams={}):
        params = {'fname': fname, 'fparams': fparams}
        return self.func_call(params=params)

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

    @contextmanager
    def for_w(self):
        params = {}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

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

    def declare_custom_func(self, fname='', fparams=[], fbody=[]):
        params = {'fname': fname, 'fparams': fparams, 'fbody': fbody}
        return self.func_call(params=params)

    def declare_custom_global_func(self, fname, fparams=[], fbody=[]):
        params = { 'fname': fname, 'fparams': fparams, 'fbody': fbody}
        return self.func_call(params=params)

    def equal(self):
        params = {}
        return self.func_call(params=params)

    def is_condition(self):
        params = {}
        return self.func_call(params=params)

    def is_js(self):
        params = {}
        return self.func_call(params=params)

    def set_condition(self, cond):
        params = {'cond': cond}
        return self.func_call(params=params)

    def set_js(self, js):
        params = {'js': js}
        return self.func_call(params=params)
    # End CommandInf

    # ComponentInf
    def add_context_indent(self, indent):
        params = {'indent': indent}
        return self.func_call(params=params)

    def add_scripts(self, scripts, indent=True, place=None):
        params = {'scripts': scripts, 'indent': indent, 'place': place}
        return self.func_call(params=params)

    def set_scripts_indent(self, indent):
        params = {'indent': indent}
        return self.func_call(params=params)

    def add_scripts_files(self, files):
        params = {'files': files}
        return self.func_call(params=params)

    def get_scripts_files(self):
        params = {}
        return self.func_call(params=params)

    def get_scripts_indent(self):
        params = {}
        return self.func_call(params=params)

    def add_styles_files(self, files):
        params = {'files': files}
        return self.func_call(params=params)

    def get_styles_files(self):
        params = {}
        return self.func_call(params=params)

    def get_context_indent(self):
        params = {}
        return self.func_call(params=params)
    # End ComponentInf

    # Other functions
    def alert(self, message):
        params = {'message': message}
        return self.func_call(params=params)

    def val(self, value=None):
        params = {'value': value}
        return self.func_call(params=params)

    @classmethod
    def check_width_format(cls, width):
        if width[-1:] != '%' and width[-2:] != 'px' and width != 'auto':
            return False
        return True

    @classmethod
    def check_height_format(cls, height):
        if height[-1:] != '%' and height[-2:] != 'px' and height != 'auto':
            return False
        else:
            return True
    # End other functions


from dominate import tags
from flask_nav import Nav
from flask_nav.elements import *
from flask_bootstrap.nav import BootstrapRenderer, sha1


"""
class WebNav(WebComponentBootstrap):
    BASE_TEMPLATE = \
        '''
          {% extends 'bootstrap/base.html' %}

          {% block styles %}
            {{ super() }}

{% if style_files %}
{{ style_files | safe }}
{% endif %}

{% if styles %}
{{ styles | safe}}
{% endif %}

          {% endblock %}

          {% block scripts %}
            {{ super() }}

{% if script_files %}
{{ script_files | safe }}
{% endif %}

            <script>

{% if global_scripts %}
{{ global_scripts | safe}} 
{% endif %}            

                $(function(){

{% if scripts %}
{{ scripts | safe}}
{% endif %}

                })
            </script>
          {% endblock %}

          {% block navbar %}

{% if nav %}
{{ nav.top.render() }}
{% endif %}

          {% endblock %}

    '''

    class NavView(View):

        def get_url(self):
            if self.url_for_kwargs:
                params = ',' + str(**self.url_for_kwargs)
            else:
                params = ''
            ret = "{{ url_for('" + self.endpoint + "'" + params + ")}}" if self.endpoint else '/'

            return ret

    class ExtendedNavbar(NavigationItem):

        def __init__(self, title, root_class='navbar navbar-default', items=[], right_items=[]):
            self.title = title
            self.root_class = root_class
            self.items = items
            self.right_items = right_items

    class CustomBootstrapRenderer(BootstrapRenderer):

        def visit_ExtendedNavbar(self, node):
            node_id = self.id or sha1(str(id(node)).encode()).hexdigest()

            root = tags.nav() if self.html5 else tags.div(role='navigation')
            root['class'] = node.root_class

            cont = root.add(tags.div(_class='container-fluid'))

            # collapse button
            header = cont.add(tags.div(_class='navbar-header'))
            btn = header.add(tags.button())
            btn['type'] = 'button'
            btn['class'] = 'navbar-toggle collapsed'
            btn['data-toggle'] = 'collapse'
            btn['data-target'] = '#' + node_id
            btn['aria-expanded'] = 'false'
            btn['aria-controls'] = 'navbar'

            btn.add(tags.span('Toggle navigation', _class='sr-only'))
            btn.add(tags.span(_class='icon-bar'))
            btn.add(tags.span(_class='icon-bar'))
            btn.add(tags.span(_class='icon-bar'))

            # title may also have a 'get_url()' method, in which case we render
            # a brand-link
            if node.title is not None:
                if hasattr(node.title, 'get_url'):
                    header.add(tags.a(node.title.text, _class='navbar-brand', href=node.title.get_url()))
                else:
                    header.add(tags.span(node.title, _class='navbar-brand'))

            bar = cont.add(tags.div(_class='navbar-collapse collapse', id=node_id))
            bar_list = bar.add(tags.ul(_class='nav navbar-nav'))
            for item in node.items:
                bar_list.add(self.visit(item))

            if node.right_items:
                right_bar_list = bar.add(tags.ul(_class='nav navbar-nav navbar-right'))
                for item in node.right_items:
                    right_bar_list.add(self.visit(item))

            return root

    def init_custom_nav_render(self, app):
        app.extensions['nav_renderers']['bootstrap'] = (__name__, 'WebNav.CustomBootstrapRenderer')
        app.extensions['nav_renderers'][None] = (__name__, 'WebNav.CustomBootstrapRenderer')

    def base_navbar(self):
        '''
        self._nav_items = {
            'title':{'name':'OwwwO','action':'test'},
            'menu_list': [
                {'subgroup':{
                                'name': 'xxx',
                                'menu_list': [
                                    {'name': 'xxx', 'action': 'xxx'},
                                    {'name': 'xxx', 'action': 'xxx'},
                                ]
                            }
                },
                {'name': 'xxx', 'action': 'xxx'},
                ...
            }
        }

        :return: WebNav.ExtendedNavbar
        '''

        items = []

        for item in self._nav_items['menu_list']:
            k1 = list(item.keys())[0]
            v1 = list(item.values())[0]
            if k1 == 'subgroup':
                sg_items = []
                for menu in v1['menu_list']:
                    sg_items.append(WebNav.NavView(menu['name'], menu['action']))
                items.append(Subgroup(v1['name'], sg_items))
            elif k1 == 'name':
                items.append(WebNav.NavView(v1, item['action']))

        return WebNav.ExtendedNavbar(
            title=WebNav.NavView(self._nav_items['title']['name'], self._nav_items['title']['action']),
            items=items
        )

    def top_navbar(self):
        top_bar = self.base_navbar()
        if 'login' in self._nav_items.keys():
            if self._nav_items['login']['is_login']:
                top_bar.right_items = (
                    Subgroup(
                        self._nav_items['login']['login_name'],
                        WebNav.NavView('退出', self._nav_items['login']['logout_href'])
                    ),
                )
            else:
                top_bar.right_items = (
                    WebNav.NavView(u'登录', self._nav_items['login']['login_href']),
                )
        return top_bar

    def __init__(self, nav_items=None):

        if not hasattr(self, '_nav_items'):
            self._nav_items = {}

        if nav_items:
            self._nav_items = {**self._nav_items, **nav_items}
        else:
            self._nav_items = self.create_default_nav_items()

        self._top_bar = 'top'
        self._nav = Nav()
        self._nav.register_element(self._top_bar, self.top_navbar)
        if current_app:
            self._nav.init_app(current_app)
            self.init_custom_nav_render(current_app)

    def render(self):
        return
        pass

    @classmethod
    def html(cls, nav_items=None):
        '''
        render with nav items and return html string

        :param nav_items: nav items in list
        :return: html string
        '''
        if nav_items is None:
            nav_items = {}
        nav = WebNav(nav_items=nav_items)
        return render_template_string(
            source=cls.BASE_TEMPLATE,
        )
"""


class WebPage(WebComponentBootstrap):

    PAGE = None

    INSTANCES = set()

    '''
    Create an unique instance of page, which add a rule for on_post, and register current page view in app
    '''

    @classmethod
    def on_post(cls):
        '''
        The process function to response the post request from the WebComponent itself
        TODO: Query data by user model

        :return: jsonify({'status':'success','data': data})
        '''
        data_j = request.form.get('data')
        if data_j:
            data = json.loads(request.form.get('data'))
            return data
        return []

    '''
    @classmethod
    def get_page(cls, app):
        """
        if not cls.PAGE:
            cls.PAGE = Page(default_url='view.index', nav=CustomPage.NAV, value=CustomPage.TITLE, app=view)
            app.register_blueprint(blueprint=view, url_prefix=url_prefix)
            print('app.run, app.url_map:{}'.format(pprint.pformat(app.url_map)))
            print('app.run, app.view_functions:{}'.format(pprint.pformat(app.view_functions)))
        return cls.PAGE
        """
        raise NotImplemented
    '''

    '''
    def init_custom_nav_render(self, app):
        app.extensions['nav_renderers']['bootstrap'] = (__name__, 'WebNav.CustomBootstrapRenderer')
        app.extensions['nav_renderers'][None] = (__name__, 'WebNav.CustomBootstrapRenderer')

    def top_navbar(self):
        top_bar = self.base_navbar()
        if 'login' in self._nav_items.keys():
            if self._nav_items['login']['is_login']:
                top_bar.right_items = (
                    Subgroup(
                        self._nav_items['login']['login_name'],
                        WebNav.NavView('退出', self._nav_items['login']['logout_href'])
                    ),
                )
            else:
                top_bar.right_items = (
                    WebNav.NavView(u'登录', self._nav_items['login']['login_href']),
                )
        return top_bar
    '''

    @classmethod
    def on_page_render(cls):
        req = cls.on_post()
        ret = req
        assert(len(cls.INSTANCES))
        for ins in cls.INSTANCES:
            ret = ins.on_my_render(req=req)
        return ret

    @classmethod
    def register(cls, app, rule, top_menu, end_point=None, view_func=None):

        def get_page(top_menu=top_menu, rule=rule):
            page = cls(nav_items=top_menu, url=rule)
            html = page.render()
            return render_template_string(html)

        view_func_ = get_page
        if view_func:
            view_func_ = view_func

        end_point_ = '{}_route'.format(cls.__name__)
        if end_point:
            end_point_ = end_point

        end_point_on_ = end_point_ + '_on_page_render'
        app.add_url_rule(rule=rule, endpoint=end_point_, view_func=view_func_, methods=['GET', 'POST'])
        app.add_url_rule(rule=rule+'/on_post', endpoint=end_point_on_, view_func=cls.on_page_render, methods=['POST'])


    def type_(self):
        return 'WebPage'

    def __init__(self, app=None, url_prefix=None, **kwargs):
        self.set_context([])
        self._root_class = WebComponentBootstrap
        if 'url' in kwargs:
            self._url = kwargs['url']
        else:
            self._url = url_prefix if url_prefix else '/page_url_not_set'
            kwargs['url'] = self._url

        if app:
            self.app = app
        if not hasattr(self, 'app'):
            self.app = current_app
        super().__init__(**kwargs)
        self.set_api()

        def place(self):
            raise RuntimeError(
                "Error: instance {} of WebPage hasn't implemented 'place' member function yet!".format(self.name())
            )
        self.place = types.MethodType(place, self)
        self._components = {}
        self.rendered = False
        self.__class__.INSTANCES.add(self)

    def __del__(self):
        self.__class__.INSTANCES.remove(self)
        super().__del__()

    '''
    def do_post(self):
        req_ = self.on_post()

        for i, r in enumerate(req_):
            for name in self._components.keys():
                if name == r['me']:
                    self._components[name].action(req=r)

        return jsonify({'status': 'success', 'data': req_})
    '''

    def init_api(self,
                 app,page_name=None, view_config=None, url_prefix=None, endpoint=None, on_post=None):

        if not self.app:
            self.app = app
        if not hasattr(self, '_api') or not self._api:
            self.set_api()

        page_name_ = self.page_name if not page_name else page_name
        view_config_ = self.view_config if not view_config else view_config
        url_prefix_ = self.url_prefix if not url_prefix else url_prefix
        endpoint_ = page_name_ if not endpoint else endpoint
        on_post_ = self.on_post if not on_post else on_post

        view = Blueprint(page_name_, __name__)
        view.config = view_config_
        try:
            if view:
                self.add_url_rule(app=view, extend=[
                                                        {
                                                            'rule': '/on_post',
                                                            'endpoint': endpoint_,
                                                            'view_func': on_post_,
                                                            'methods': ['POST']
                                                        }
                                                    ]
                                  )
                app.register_blueprint(blueprint=view, url_prefix=url_prefix_)
            else:
                self.add_url_rule(app, extend=[
                                                {
                                                    'rule': url_prefix_,
                                                    'endpoint': endpoint_,
                                                    'view_func': on_post_,
                                                    'methods': ['POST']
                                                },
                                              ]
                                  )

        except AssertionError:
            print("Add url rule error!")

    '''
    def init_page(self, app,
                  page_name=None, view_config=None, url_prefix=None, endpoint=None, on_post=None):

        view = Blueprint(page_name, __name__)
        view.config = view_config

        try:
            if view:
                self.add_url_rule(app=view, extend=[
                    {'rule': '/on_post', 'endpoint': endpoint, 'view_func': on_post, 'methods': ['POST']}])
                app.register_blueprint(blueprint=view, url_prefix=url_prefix)
            else:
                cls.add_url_rule(app, extend=[
                    {'rule': self.url_prefix, 'endpoint': endpoint, 'view_func': on_post, 'methods': ['POST']}])

        except AssertionError:
            print("Add url rule error!")
    '''

    def place_components_impl(self):
        pass

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components(self):
        self.place_components_impl()

    def on_my_render_impl(self, req):
        '''
        page = self
        name = self.name()
        for r in req:
            if r['me'] == name:
                self.process_events(req=r)
        '''
        return req

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def on_my_render(self, req):
        return self.on_my_render_impl(req)

    def process_events_impl(self, req):
        pass

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def process_events(self, req):
        self.process_events_impl(req=req)

    def intro_events_impl(self):
        pass

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def intro_events(self):
        self.intro_events_impl()

    def render(self, app=None, on_post=None, endpoint=None, url=None):

        if hasattr(self, '_rendered_html') and self._rendered_html:
           return self._rendered_html

        self.place_components()
        self.intro_events()

        '''
        app_ = app if app else current_app
        on_post_ = on_post if on_post else self.on_page_render
        endpoint_ = endpoint if endpoint else self.name()+'_on_post'
        url_ = url if url else self._url
        self.init_on_page_render(app=app_,
                                 on_post=on_post_,
                                 endpoint=endpoint_,
                                 url=url_)
        '''

        payload = create_payload(self.context())
        r = post(url=self._api, json=payload)
        html = extract_data(r.json()['data'])

        self._rendered_html = render_template_string(html)
        return self._rendered_html

    def default_events(self):
        with self.render_post_w():
            [element.render_for_post() for element in self._components.values()]

    def init_on_page_render(self, app, on_post=None, blueprint=None, blueprint_url_prefix=None, endpoint='', url=''):

        on_post_ = on_post if on_post else self.on_post
        url_ = None
        if url:
            if not self._url or self._url == '/page_url_not_set':
                self._url = url
            else:
                print('Warning: the page {} has set url already!'.format(self.name()))
        else:
            assert self._url and self._url != '/page_url_not_set'
        url_ = self._url

        try:
            if blueprint:
                self.add_url_rule(app=blueprint, extend=[
                    {'rule': url_ + '/on_post',
                     'endpoint': endpoint,
                     'view_func': on_post_,
                     'methods': ['POST']}])
                app.register_blueprint(blueprint=blueprint, url_prefix=blueprint_url_prefix)
            else:
                self.add_url_rule(app=app, extend=[
                    {'rule': url_ + '/on_post',
                     'endpoint': endpoint,
                     'view_func': on_post_,
                     'methods': ['POST']}])
        except Exception as e:
            print("Add url rule error:{}!".format(e))

    def events_trigger(self):
        print('WebPage.events_trigger')
        '''
        with self.render_post_w():
            for name, component in self._components.items():
                component.render_for_post()
        '''

    def add_context_indent(self, indent=None):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} shouldn't been implemented on client side!".format(c_name, f_name))

    '''
    def add_scripts(self, scripts=None):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} shouldn't been implemented on client side!".format(c_name, f_name))
    '''

    def add_scripts_files(self, script_files):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} shouldn't been implemented on client side!".format(c_name, f_name))

    def add_styles_files(self, style_files):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} shouldn't been implemented on client side!".format(c_name, f_name))

    def get_context_indent(self):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} shouldn't been implemented on client side!".format(c_name, f_name))

    def get_scripts_files(self):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} shouldn't been implemented on client side!".format(c_name, f_name))

    def get_scripts_indent(self):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} shouldn't been implemented on client side!".format(c_name, f_name))

    def get_styles_files(self):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} shouldn't been implemented on client side!".format(c_name, f_name))

    def offset(self, offset):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} shouldn't been implemented on client side!".format(c_name, f_name))

    def set_scripts_indent(self, indent):
        c_name = self.__class__.__name__
        f_name = inspect.currentframe().f_code.co_name
        raise NotImplementedError("{}.{} shouldn't been implemented on client side!".format(c_name, f_name))

    def get_vptr(self):
        params = {}
        return self.func_call(params=params)

    def set_vptr(self, vptr):
        params = {'vptr': vptr}
        return self.func_call(params=params)

    def keep_vptr_ori(self):
        params = {}
        return self.func_call(params=params)

    def restore_vptr_ori(self):
        params = {}
        return self.func_call(params=params)


class ClassTestPage(WebPage):

    def place_components_impl(self):

        page = self

        testing_class = page.testing_class
        testing_cls_name = testing_class.__name__
        # testing_cls_name = testing_class.testing_cls_name if hasattr(testing_class, 'testing_cls_name') else testing_class.__name__
        class_name = testing_class.__name__
        name_ = testing_cls_name

        WebRow = page._SUBCLASSES['WebRow']['class']
        WebColumn = page._SUBCLASSES['WebColumn']['class']
        default_width = ['md6', 'lg6']
        default_offset = ['mdo3', 'mdo3']
        page._url = '/test_' + testing_class.__name__ + '_requesft'
        with page.add_child(WebRow()) as r1:
            with r1.add_child(WebColumn(width=default_width, offset=default_offset, height='200px')) as c1:
                if class_name.find('OOChart') == 0:
                    with c1.add_child(testing_class(
                            parent=page, value=class_name, name=name_, height='400px', width='100%',
                            url='/' + testing_class.__name__ + '_test')) as test:
                        pass
                else:
                    with c1.add_child(testing_class(parent=c1,
                                                    name=name_,
                                                    value=name_,
                                                    url='/' + testing_class.__name__ + '_test')) as test:
                        pass

    def intro_events_impl(self):

        page = self._page
        if (not hasattr(self, '_PAGE_CLASS')) or \
                (hasattr(self, '_PAGE_CLASS') and
                 self._PAGE_CLASS is None):
            page = self

        with page.render_post_w():
            for name, component in page._components.items():
                component['obj'].render_for_post()

        return

    def process_events_impl(self, req):
        cls = self.__class__
        name_ = req['me']
        print('Class testing, class {} got req:{}'.format(name_, req))
        if not hasattr(cls, 'test_request_data') or not cls.test_request_data:
            req['data'] = {'val': name_ + '_testing from on_post', 'text': name_ + '_testing from on_post'}
        else:
            req['data'] = {'data': cls.test_request_data(), 'attrs':'align:'}

    def on_my_render_impl(self, req):
        page = self
        if self.__class__.__name__ != 'WebPage':
            page = self._page
        testing_cls_name = page.testing_class.__name__
        for r in req:
            if r['me'] == testing_cls_name:
                self.process_events(req=r)

        return jsonify({'status': 'success', 'data': req})


class WebA(WebComponentBootstrap):
    pass


class WebRow(WebComponentBootstrap):
    pass


class WebColumn(WebComponentBootstrap):
    pass


class WebHead1(WebComponentBootstrap):
    VAL_FUNC_NAME = 'webhead_val'


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
    VAL_FUNC_NAME = 'webfield_val'
    VAL_FUNC_PARAMS = WebComponentBootstrap.BASE_VAL_FUNC_PARAMS


class WebImg(WebComponentBootstrap):

    VAL_FUNC_NAME = "web_img_val"
    VAL_FUNC_PARAMS = ['that', 'data']

    def __init__(self, value=None, **kwargs):

        if value:
            kwargs['value'] = value
        super().__init__(**kwargs)

    @classmethod
    def test_request(cls, methods=['GET']):
        # Create a testing page containing the component tested
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):
            def process_events_impl(self, req):
                req['data']['oovalue'] = url_for('static', filename='img/demo.jpg')

        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class WebBtnToggle(WebBtnToggleTest, WebComponentBootstrap):

    def toggle(self):
        '''
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={})
        self.add_context(context)
        '''
        params = {}
        return self.func_call(params)


class WebBtnGroup(WebComponentBootstrap):
    pass


class WebBtnGroupVertical(WebBtnGroupVerticalTest, WebComponentBootstrap):
    pass


class WebBtnToolbar(WebComponentBootstrap):

    '''
    @classmethod
    def test_request(cls, methods=['GET']):

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
    '''

    @classmethod
    def test_result(cls):
        r = request.form['test']
        return json.dumps({"status": "sucess"}), 201


class WebBtn(WebBtnTest, WebComponentBootstrap):
    pass
    '''
    @classmethod
    def on_post(cls):
        r = super().on_post()
        print('WebBtn.test_result, got request:{}'.format(r['data']))
        return jsonify({'status': 'success', 'data': 'test post_w success!'})

    @classmethod
    def test_result(cls):
        return cls.on_post()
    '''


class WebBtnRadio(WebBtnRadioTest, WebBtnGroup):

    VAL_FUNC_NAME = 'radio_val'
    VAL_FUNC_ARGS = ['that', 'data=null']

    '''
    @classmethod
    def test_request(cls, methods=['GET']):
        return super().test_request(methods=methods)
    '''

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def place_components_impl(self):
                page = self
                name = page.testing_class.testing_cls_name
                WebBtnRadio = page._SUBCLASSES['WebBtnRadio']['class']

                with page.add_child(WebBtnRadio(name=name, mytype=['inline'],
                                                items=[{'label': '测试1', 'checked': ''},
                                                       {'label': '测试测试测试2'},
                                                       {'label': '测试3'}])) as radio:
                    pass

            def process_events_impl(self, req):
                print('Class testing, class {} got req:{}'.format(self.__class__.__name__, req['data']))
                req['data'] = {'oovalue': '测试3'}
                print('Class testing: testing for {} is setting "测试3" always'.format(self.__class__.__name__))

            def intro_events_impl(self):
                page = self
                radio = page._components['WebBtnRadio']['obj']
                LVar = page._SUBCLASSES['LVar']['class']
                cls = radio.__class__

                with page.render_post_w():
                    radio.render_for_post()

                with radio.on_event_w('change'):
                    radio.alert('"Please checking on server side to find \'Class testing, class {} got: ...\''
                                ' And the radio buttons is set {} always by on_post function on server side"'.format(
                        cls.__name__,
                        '测试3'))
                    with LVar(parent=radio, var_name='click_val') as val:
                        radio.val()
                        radio.add_scripts('\n')
                        radio.alert('"The clicked item is in oovalue : " + click_val.oovalue')
                        with page.render_post_w():
                            radio.render_for_post()

        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class WebBtnDropdown(WebBtnDropdownTest, WebBtn):

    def set_options(self, options=None):
        params = {'options': options}
        self.func_call(params)

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def place_components_impl(self):
                page = self
                this_class = page.testing_class
                WebBtnDropdown = page._SUBCLASSES['WebBtnDropdown']['class']
                WebBtn = page._SUBCLASSES['WebBtn']['class']
                name = this_class.__name__

                with page.add_child(WebBtnDropdown(value='测试', name=name, select_options=[{'name': '测试1', 'href': '#'},
                                                                                          {'name': '测试2',
                                                                                           'href': '#'}])) as btn:
                    pass  # btn.clear(call=True)
                with page.add_child(WebBtn(value="Disable drop button", name='DisableBtn')) as disable_btn:
                    '''
                    with disable_btn.on_event_w('click'):
                        btn.disable(True)
                    '''
                    pass
                with page.add_child(WebBtn(value='Enable drop button', name='EnableBtn')) as enable_btn:
                    '''
                    with enable_btn.on_event_w('click'):
                        btn.disable(False)
                    '''
                    pass
                with page.add_child(WebBtn(value='Change options', name='ChangeBtn')) as change_btn:
                    '''
                    with change_btn.on_event_w('click'):
                        options = [{'name': 'op1', 'href': '#'}]
                        btn.set_options(options=options)
                        btn.val('"新菜单"')
                    '''
                    pass

            def intro_events_impl(self):
                page = self
                LVar = page._SUBCLASSES['LVar']['class']
                test_obj = page._components['WebBtnDropdown']['obj']
                disable_btn = page._components['DisableBtn']['obj']
                enable_btn = page._components['EnableBtn']['obj']
                change_btn = page._components['ChangeBtn']['obj']

                with disable_btn.on_event_w('click'):
                    test_obj.disable(disable=True)

                with enable_btn.on_event_w('click'):
                    test_obj.disable(disable=False)

                with change_btn.on_event_w('click'):
                    options = [{'name': 'op1, changed by change button', 'href': '#'}]
                    test_obj.set_options(options=options)
                    test_obj.val('"menu items/options are changed by change button"')

                with test_obj.on_event_w('selected'):
                    with LVar(parent=test_obj, var_name='data') as data:
                        test_obj.val()
                    test_obj.alert('"The dropdown button is selected, '
                                   'this alert dialog should pop up after the dropdown button select finish,'
                                   'new menu text is :"+data')

        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class WebQuickForm(WebComponentBootstrap):
    """
    QuickForm packages FlaskForm
    """

    PAGE_TEMPLATE = """
{% extends 'bootstrap/base.html' %}
{% import "bootstrap/utils.html" as util %} 

{% block title %}{{ title_name }}{% endblock %}

{% block head %}
  {{ super() }}
{% endblock %}

{% block navbar %}
  {% if nav %}
  {{ nav.top.render() }}
  {% endif %}
{% endblock %}

{% block content %}
    {{ super() }}
    {% block flash %}
      {{util.flashed_messages(dismissible=True)}}	
    {% endblock %}
    {% block modal %}
    <div class="modal fade" id="events-modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div Class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
            <h3 class="modal-title">Event</h3>
          </div>
          <div class="modal-body" style="height: 400px">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>  <!-- model -->
    {% endblock %}
    <div class="container">
        <br>
        <br>
        <div class="jumbotron">
          <h3>请登录</h3>
          <p>
            {% import "bootstrap/wtf.html" as wtf %}
            {{ wtf.quick_form(form) }}
          </p>
        </div>
    </div>
{% endblock %}

            """


class WebFormGroup(WebComponentBootstrap):
    pass


class WebInputGroup(WebComponentBootstrap):
    pass


class WebInput(WebComponentBootstrap):

    VAL_FUNC_NAME = 'webinput_val'


class WebInputGroup(WebComponentBootstrap):
    pass


class WebFormInline(WebComponentBootstrap):
    pass


class WebSelect(WebComponentBootstrap):

    VAL_FUNC_NAME = 'webselect_val'
    VAL_FUNC_PARAMS = WebComponentBootstrap.VAL_FUNC_PARAMS

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def place_components_impl(self):
                page = self
                this_class = page.testing_class
                name_ = this_class.__name__
                WebRow = page._SUBCLASSES['WebRow']['class']
                WebColumn = page._SUBCLASSES['WebColumn']['class']
                with page.add_child(WebRow()) as r1:
                    with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='200px')) as c1:
                        options = [{'text': 'option1'},
                                   {'text': 'option2'},
                                   {'selected': True, 'text': 'option3'}]
                        with c1.add_child(this_class(parent=page, name=name_, options=options)) as test:
                            pass

            def intro_events_impl(self):
                page = self
                test_obj = page._components['WebSelect']['obj']
                with page.render_post_w():
                    test_obj.render_for_post()

                with test_obj.on_event_w('change'):
                    test_obj.alert('"Testing works that \'OptionResetByOnPost3\' item is always slected."')
                    with page.render_post_w():
                        test_obj.render_for_post()

            def process_events_impl(self, req):
                print('Class testing, class {} got req:{}'.format(self.__class__.__name__, req['data']))
                req['data'] = {'options': [{'text': 'OptionResetByOnPost1'},
                                           {'text': 'OptionResetByOnPost2'},
                                           {'text': 'OptionResetByOnPost3', 'selected': 'true'}]}

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class WebSelect2(WebSelect):

    VAL_FUNC_NAME = 'webselect2_val'


class WebSpan(WebComponentBootstrap):
    pass


class WebB(WebComponentBootstrap):
    pass


class WebBr(WebComponentBootstrap):
    pass


class WebHr(WebComponentBootstrap):
    pass


class WebUl(WebUlTest, WebComponentBootstrap):
    VAL_FUNC_NAME = 'webul_val'


class WebDatalist(WebDatalistTest, WebSelect):

    VAL_FUNC_NAME = 'webdatalist_val'

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def place_components_impl(self):
                page = self
                this_class = page.testing_class
                TEST_ID = 'test_id'
                INPUT_NAME = 'test_input'
                name_ = this_class.__name__
                WebRow = page._SUBCLASSES['WebRow']['class']
                WebColumn = page._SUBCLASSES['WebColumn']['class']
                WebInput = page._SUBCLASSES['WebInput']['class']
                with page.add_child(WebRow()) as r1:
                    with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='200px')) as c1:
                        with c1.add_child(WebInput(name=INPUT_NAME, attrs={'list': '{}'.format(TEST_ID)})) as input:
                            options = [{'text': 'option1'},
                                       {'text': 'option2'},
                                       {'selected': True, 'text': 'option3'}]
                            with input.add_child(
                                    this_class(parent=page, name=name_, id=TEST_ID, options=options)) as test:
                                pass

            def intro_events_impl(self):
                page = self
                input = page._components['test_input']['obj']
                test_obj = page._components['WebDatalist']['obj']
                with page.render_post_w():
                    test_obj.render_for_post()

            def process_events_impl(self, req):
                print('Class testing, WebDatalist got req:{}'.format(req['data']))

                options = [{'text': 'OptionResetByOnPost1'},
                           {'text': 'OptionResetByOnPost2'},
                           {'text': 'OptionResetByOnPost3', 'selected': 'true'}]
                req['data'] = {'options': options}


        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class WebDiv(WebComponentBootstrap):

    VAL_FUNC_NAME = 'webdiv_val'


class WebLabel(WebDiv):
    VAL_FUNC_NAME = 'weblabel_val'


class WebCheckbox(WebSpan):

    VAL_FUNC_NAME = 'webcheckbox_val'

    def check(self, checked=True):
        params = {'checked': checked}
        self.func_call(params)

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def intro_events_impl(self):
                page = self
                test_obj = page._components['WebCheckbox']['obj']
                LVar = page._SUBCLASSES['LVar']['class']
                with test_obj.on_event_w('change'):
                    with LVar(parent=self, var_name="data") as data:
                        test_obj.val()
                    test_obj.alert(' data + " clicked !"')

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class OODatePickerBase:
    
    VIEWS = {'week': '周', 'month': '月', 'day': '日'}
    
    DAY_FORMAT_ZH = ("yyyy年 M月 d日", "%Y年 %m月 %d日")
    WEEK_FORMAT_ZH = ("yyyy'年 第'w'周'", "%Y年 第%W周:%w")
    MONTH_FORMAT_ZH = ("yyyy年 M月", "%Y年 %m月")

    DAY_FORMAT_EN = ("yyyy M d", "%Y %m %d")
    WEEK_FORMAT_EN = ("'Week of 'yyyy:w", "Week of %Y:%W:%w")
    MONTH_FORMAT_EN = ("yyyy M", "%Y %m")

    start_func_name = "OODatePickerStart"
    start_func_params = ["that", "type"]

    @classmethod
    def DAY_DT_STR(cls, lang, _dt):
        format_ = None
        if lang == 'zh':
            format_ = cls.DAY_FORMAT_ZH[1]
        else:
            format_ = cls.DAY_FORMAT_EN[1]
        return _dt.strftime(format_)

    @classmethod
    def DAY_STR_DT(cls, _lang, _str):
        dt_ = None
        if _lang == 'zh':
            dt_ = dt.datetime.strptime(_str, cls.DAY_FORMAT_ZH[1])
        else:
            dt_ = dt.datetime.strptime(_str, cls.DAY_FORMAT_EN[1])
        return dt_

    @classmethod
    def DAY_STR_STAMP(cls, lang, _str):
        dt = cls.DAY_STR_DT(_lang=lang, _str=_str)
        return int(dt.timestamp()) * 1000

    @classmethod
    def WEEK_DATETIME_STR(cls, lang, _dt):
        if lang == 'zh':
            return "{}年 {}月 第{}周".format(_dt.year, _dt.month, day_2_week_number(_dt))
        else:
            return "{} {} week:{}".format(_dt.year, _dt.month, day_2_week_number(_dt))

    @classmethod
    def WEEK_STR_DT(cls, _lang, _str):
        
        format_ = cls.WEEK_FORMAT_EN[1]
        is_view = False
        if _lang == 'zh':
            format_ = cls.WEEK_FORMAT_ZH[1]
            if _str.find('周') < 0:
                is_view = True
        elif _lang == 'en':
            format_ = cls.WEEK_FORMAT_EN[1]
            if _str.find('Week') < 0:
                is_view = True

        ret = None
        if not is_view:
            print('WEEK_STR_DT got string:{}, format:{}'.format(_str, format_))
            mon = dt.datetime.strptime(_str + ':1', format_)  # week starts at monday
            sun = dt.datetime.strptime(_str + ':6', format_) + dt.timedelta(days=1) # week end at sunday
            ret = [mon + dt.timedelta(days=-7), sun + dt.timedelta(days=-7)]
        else:
            view_date = dateutil.parser.parse(_str)
            mon = view_date - relativedelta(days=view_date.weekday())
            sun = view_date + relativedelta(days=6-view_date.weekday())
            ret = [mon, sun]

        return ret

    @classmethod
    def WEEK_STR_STAMP(cls, lang, _str):
        dt = cls.WEEK_STR_DT(_lang=lang, _str=_str)
        return int(dt.timestamp()) * 1000

    @classmethod
    def MONTH_DATETIME_STR(cls, lang, _dt):
        format_ = cls.MONTH_FORMAT_EN[1]
        if lang == 'zh':
            format_ = cls.MONTH_FORMAT_ZH[1]
        year = _dt.year
        month = _dt.month
        last_day = calendar.monthrange(year, month)[1]
        first_dt = dt.datetime.strptime('{}-{}-1'.format(year, month), '%Y-%m-%d')
        last_dt = dt.datetime.strptime('{}-{}-{}'.format(year, month, last_day), '%Y-%m-%d')
        return [first_dt.strftime(format_ + '-1'), last_dt.strftime(format_ + '-' + str(last_day))]

    @classmethod
    def MONTH_STR_DT(cls, _lang, _str):
        
        format = cls.MONTH_FORMAT_EN[1]
        if _lang == 'zh':
            format = cls.MONTH_FORMAT_ZH[1]

        dt_ = dt.datetime.strptime(_str, format)
        year = dt_.year
        month = dt_.month
        last_day = calendar.monthrange(year, month)[1]
        first_dt = dt.datetime.strptime('{}-{}-1'.format(year, month), '%Y-%m-%d')
        last_dt = dt.datetime.strptime('{}-{}-{}'.format(year, month, last_day), '%Y-%m-%d')
        return [first_dt, last_dt]

    @classmethod
    def MONTH_STR_STAMP(cls, lang, _str):
        dt = cls.MONTH_STR_DT(_lang=lang, _str=_str)
        return int(dt.timestamp()) * 1000

    FORMATS = {
        'zh': {
            'day': {'to_format': DAY_FORMAT_ZH[0], 'from_format': DAY_FORMAT_ZH[1], 'str_func': 'DAY_DT_STR',
                    'stamp_func': 'DAY_STR_STAMP'},
            'week': {'to_format': WEEK_FORMAT_ZH[0], 'from_format': WEEK_FORMAT_ZH[1], 'str_func': 'WEEK_DATETIME_STR',
                     'stamp_func': 'WEEK_STR_STAMP'},
            'month': {'to_format': MONTH_FORMAT_ZH[0], 'from_format': MONTH_FORMAT_ZH[1],
                      'str_func': 'MONTH_DATETIME_STR', 'stamp_func': 'MONTH_STR_STAMP'}
        },
        'en': {
            'day': {'to_format': DAY_FORMAT_EN[0], 'from_format': DAY_FORMAT_EN[1], 'str_func': 'DAY_DT_STR',
                    'stamp_func': 'DAY_STR_STAMP'},
            'week': {'to_format': WEEK_FORMAT_EN[0], 'from_format': WEEK_FORMAT_EN[1], 'str_func': 'WEEK_DATETIME_STR',
                     'stamp_func': 'WEEK_STR_STAMP'},
            'month': {'to_format': MONTH_FORMAT_EN[0], 'from_format': MONTH_FORMAT_EN[1],
                      'str_func': 'MONTH_DATETIME_STR', 'stamp_func': 'MONTH_STR_STAMP'}
        }
    }

    @classmethod
    def get_dt(cls, type, dt_str, format):
        if type == 'week' or type == '周':
            return datetime.datetime.strptime(dt_str+':1', format) - relativedelta(days=7)
        return datetime.datetime.strptime(dt_str, format)


class OODatePickerSimple(WebInputGroup, OODatePickerBase):

    def __init__(self, language='zh', value={'view': 'week',
                                             'start': dt.datetime.today().strftime('%Y %m %d')},
                 views=['day', 'week', 'month'], place_holders=('开始', '结束'), **kwargs):
        kwargs['value'] = value
        kwargs['views'] = views
        kwargs['language'] = language
        kwargs['place_holders'] = place_holders
        super().__init__(**kwargs)

    def disable(self, disable, btn_only=False):
        params = {'btn_only': btn_only, 'disable': disable}
        self.func_call(params)


    @classmethod
    def test_request(cls, methods=['GET']):
        # Create a testing page containing the component tested
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def place_components_impl(self):
                page = self
                this_class = page.testing_class
                name = this_class.__name__
                with page.add_child(
                        this_class(name=name, radius={'tl': '8px', 'tr': '5px', 'br': '9px', 'bl': '5px'},
                                   width="500px")) as test1:
                    pass

            def intro_events_impl(self):
                page = self
                test_obj = self._components['OODatePickerSimple']['obj']

                with test_obj.on_event_w('switch'):
                    with page.render_post_w():
                        test_obj.render_for_post(trigger_event=False)

                with page.render_post_w():
                    test_obj.render_for_post(trigger_event=False)

            def process_events_impl(self, req):
                r = req
                lang = r['data']['lang']
                format_ = None
                test_cls = OODatePickerSimple
                if r['data']['select'] == '周':
                    start = None if not r['data']['viewDate'] else r['data']['viewDate'].split('T')[0]
                    if start:
                        # USE cls FORMATS here
                        print('OODatepickerSimple got week start: {}'.format(start))
                        format_ = test_cls.FORMATS[lang]['week']['to_format']
                        # dt = datetime.datetime.strptime(start, "%Y-%m-%d")
                        try:
                            dt = datetime.datetime.strptime(start, format_)
                        except ValueError:
                            dt = datetime.datetime.today()
                        dt = dt.timestamp()
                    else:
                        dt = datetime.datetime.today().timestamp()
                    r['data']['date'] = int(dt)
                elif r['data']['select'] == '日':
                    start = None if not r['data']['date'] else r['data']['date']
                    if start:
                        if lang == 'zh':
                            format_ = test_cls.DAY_FORMAT_ZH[1]
                        else:
                            format_ = test_cls.DAY_FORMAT_EN[1]
                        try:
                            dt = datetime.datetime.strptime(start, format_).timestamp()
                        except ValueError:
                            dt = datetime.datetime.today().timestamp()
                    else:
                        dt = datetime.datetime.today().timestamp()
                    r['data']['date'] = int(dt)
                else:
                    start = None if not r['data']['date'] else r['data']['date']
                    if start:
                        if lang == 'zh':
                            format_ = test_cls.MONTH_FORMAT_ZH[1]
                        else:
                            format_ = test_cls.MONTH_FORMAT_EN[1]
                        try:
                            dt = datetime.datetime.strptime(start, format_).timestamp()
                        except ValueError:
                            dt = datetime.datetime.today().timestamp()
                    else:
                        dt = datetime.datetime.today().timestamp()
                    r['data']['date'] = int(dt)

        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class OODialog(WebDiv):

    BODY_HTML = """
        <div class="row">
        <div class="col-md-8  col-md-offset-1">
        {% import "bootstrap/wtf.html" as wtf %}
        {{ wtf.quick_form(form) }}
        </div>
        </div>
    """


class OODatePickerIcon(OODatePickerIconTest, OODatePickerSimple):

    @classmethod
    def get_dates(cls, _data):

        if not _data:
            return None

        lang_ = _data['lang']
        format_ = None
        dt_range_ = []

        if _data['view'] == 5:

            # week mode
            '''
            start = None if not _data['viewDate'] else _data['viewDate'].split('T00')[0]
            if start:
                format_ = cls.FORMATS[lang_]['week']['to_format']
                dt_ = datetime.strptime(start, '%Y-%m-%d')
            '''
            if _data['date']:
                dt_range_ = cls.WEEK_STR_DT(_lang=lang_, _str=_data['date'])
            elif _data['viewDate']:
                dt_range_ = cls.WEEK_STR_DT(_lang=lang_, _str=_data['viewDate'])
            # end week mode

        elif _data['view'] == 0:

            # day mode
            '''
            start = None if not _data['date'] else _data['date']
            if start:
                if lang_ == 'zh':
                    format_ = cls.DAY_FORMAT_ZH[1]
                else:
                    format_ = cls.DAY_FORMAT_EN[1]
                dt_ = datetime.strptime(start, format_)
            '''
            dt_ = cls.DAY_STR_DT(_lang=lang_, _str=_data['date'])
            dt_range_.append(dt_)
            dt_range_.append(None)
            # end day mode

        elif _data['view'] == 1:

            # month mode
            '''
            start = None if not _data['date'] else _data['date']
            if start:
                if lang_ == 'zh':
                    format_ = cls.MONTH_FORMAT_ZH[1]
                else:
                    format_ = cls.MONTH_FORMAT_EN[1]
                dt_ = datetime.strptime(start, format_)
            '''
            dt_range_ = cls.MONTH_STR_DT(_lang=lang_, _str=_data['date'])
            # end month mode

        return dt_range_

    @classmethod
    def get_ret_stamp(cls, _data):

        lang = _data['lang']
        format_ = None
        if _data['view'] == 5:
            start = None if not _data['viewDate'] else _data['viewDate'].split('T')[0]
            if start:
                # USE cls FORMATS here
                format_ = cls.FORMATS[lang]['week']['to_format']
                dt_ = dt.datetime.strptime(start, "%Y-%m-%d")
                dt_ = dt_.timestamp()
            else:
                dt_ = dt.datetime.today().timestamp()
            _data['date'] = int(dt_)
        elif _data['view'] == 0:
            start = None if not _data['date'] else _data['date']
            if start:
                if lang == 'zh':
                    format_ = cls.DAY_FORMAT_ZH[1]
                else:
                    format_ = cls.DAY_FORMAT_EN[1]
                dt_ = dt.datetime.strptime(start, format_).timestamp()
            else:
                dt_ = dt.datetime.today().timestamp()
            _data['date'] = int(dt_)
        else:
            start = None if not _data['date'] else _data['date']
            if start:
                if lang == 'zh':
                    format_ = cls.MONTH_FORMAT_ZH[1]
                else:
                    format_ = cls.MONTH_FORMAT_EN[1]
                dt_ = dt.datetime.strptime(start, format_).timestamp()
            else:
                dt_ = dt.datetime.today().timestamp()
            _data['date'] = int(dt_)

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def place_components_impl(self):
                page = self
                this_class = page.testing_class
                testing_cls_name = this_class.testing_cls_name if hasattr(this_class, 'testing_cls_name') else \
                    this_class.__name__
                name = testing_cls_name
                with page.add_child(this_class(name=name)) as test:
                    pass
                with ooccd.MetisTransform.transform_w(component=test, vptr=ooccd.ACTION_MEMBER):
                    test.call_custom_func(fname=test.start_func_name,
                                          fparams={'that': '$("#{}")'.format(test.id()),
                                                   'type': '"{}"'.format(test.VIEWS['week'])})
            def intro_events_impl(self):
                page = self
                test_obj = self._components['OODatePickerIcon']['obj']
                with page.render_post_w():
                    test_obj.render_for_post()

                with test_obj.on_event_w('change'):
                    with page.render_post_w():
                        test_obj.render_for_post()

            def process_events_impl(self, req):
                r = req
                cls = self.__class__
                if r['data']['date']:
                    dt = cls.get_dates(_data=r['data'])
                    print('OODatePickerIcon testing: got dates: {} ~ {}'.format(
                        pprint.pformat(dt[0]), pprint.pformat(dt[1]))
                    )
                    cls.get_ret_stamp(r['data'])

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class OODatePickerRange(OODatePickerSimple):

    def __init__(self, language='zh',
                 value={'view': 'week', 'start': dt.datetime.today().strftime('%Y %m %d'),
                        'end': dt.datetime.today().strftime('%Y %m %d')}, views=['day', 'week', 'month'],
                 place_holders=('开始', '结束'), **kwargs):
        kwargs['value'] = value
        kwargs['views'] = views
        kwargs['language'] = language
        kwargs['place_holders'] = place_holders
        super().__init__(**kwargs)

    @classmethod
    def test_request(cls, methods=['GET']):

        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def place_components_impl(self):
                page = self

                testing_class = page.testing_class
                testing_cls_name = testing_class.__name__
                # testing_cls_name = testing_class.testing_cls_name if hasattr(testing_class, 'testing_cls_name') else testing_class.__name__
                class_name = testing_class.__name__
                name_ = testing_cls_name

                WebRow = page._SUBCLASSES['WebRow']['class']
                WebColumn = page._SUBCLASSES['WebColumn']['class']
                default_width = ['md6', 'lg6']
                default_offset = ['mdo3', 'mdo3']
                page._url = '/test_' + testing_class.__name__ + '_request'
                with page.add_child(WebRow()) as r1:
                    with r1.add_child(WebColumn(width=default_width, offset=default_offset, height='200px')) as c1:
                        if class_name.find('OOChart') == 0:
                            with c1.add_child(testing_class(
                                    parent=page, value=class_name, name=name_, height='400px', width='100%'
                            )) as test:
                                pass
                        else:
                            with c1.add_child(testing_class(parent=c1,
                                                            name=name_,
                                                            url='/' + testing_class.__name__ + '_test')) as test:
                                pass

            def intro_events_impl(self):
                page = self
                this_obj = page._components['OODatePickerRange']['obj']

                with this_obj.on_event_w('change'):
                    with page.render_post_w():
                        this_obj.render_for_post()

                with page.render_post_w():
                    this_obj.render_for_post()

            def process_events_impl(self, req):
                page = self
                test_obj = page._components['OODatePickerRange']['obj']
                r = req
                cls = test_obj.__class__

                lang = r['data']['lang']
                format = None
                start = None
                end = None
                if r['data']['select'] == '周':
                    format = cls.FORMATS[lang]['week']['from_format']
                elif r['data']['select'] == '日':
                    format = cls.FORMATS[lang]['day']['from_format']
                else:
                    format = cls.FORMATS[lang]['month']['from_format']

                start = None if not r['data']['start'] else r['data']['start']
                if not start:
                    # start = None if not r['data']['start_viewDate'] else r['data']['start_viewDate'].split('T')[0]
                    start = datetime.datetime.strptime('2020-1-1', '%Y-%m-%d')
                else:
                    try:
                        start = test_obj.get_dt(type=r['data']['select'], dt_str=start, format=format)
                    except ValueError:
                        start = datetime.datetime.strptime('2020-1-1', '%Y-%m-%d')

                end = None if not r['data']['end'] else r['data']['end']
                if not end:
                    # end = None if not r['data']['end_viewDate'] else r['data']['end_viewDate'].split('T')[0]
                    end = datetime.datetime.strptime('2020-12-31', '%Y-%m-%d')
                else:
                    try:
                        end = test_obj.get_dt(type=r['data']['select'], dt_str=end, format=format)
                    except ValueError:
                        end = datetime.datetime.strptime('2020-12-31', '%Y-%m-%d')

                r['data']['start'] = int(start.timestamp())
                r['data']['start_viewDate'] = start.strftime('%Y-%m-%dT')
                r['data']['end'] = int(end.timestamp())
                r['data']['end_viewDate'] = end.strftime("%Y-%m-%dT")

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class WebSvg(WebComponentBootstrap):

    def id(self, _id=None):
        if not _id:
            if not hasattr(self, '_id') or not self._id:
                self._id = 'svg_' + str(uuid.uuid4()).split('-')[0]
            return self._id
        else:
            self._id = _id


class OOChatClient(OOChatClientTest, WebComponentBootstrap):

    VAL_FUNC_NAME = 'oochatclient_val'
    INIT_FUNC_NAME = 'oochatclient_init'

    DEFAULT_BODY_STYLE = {'style': {'height': '600px'}}
    DEFAULT_ME_MESSAGE_STYLE = {'class': 'me pull-right', 'style': ('font-size: 10px; '
                                                         'background-colour: rgb(244, 66, 155); '
                                                         'border-right: 3px solid #f4429b !important; '
                                                         'font-size: 14px;margin: -4px;'
                                                         'border-right: 3px solid #60DF88 !important;'
                                                         'padding: 5px;background-color: rgb(239, 255, 241);'
                                                         )}
    DEFAULT_YOU_MESSAGE_STYLE = {'class': 'you pull-left', 'style': ('font-size: 14px;margin: -4px;'
                                                                     'border-left: 3px solid rgb(255, 112, 0);'
                                                                     'padding: 5px;'
                                                                     'padding-left: 10px;'
                                                                     'background-color: rgb(247, 247, 214);')}

    OOCHAT_BODY = 'oochat_body_'
    OOCHAT_SEND_INPUT = 'oochat_send_input_'
    OOCHAT_SEND_BTN = 'oochat_send_btn_'

    MSG_EVENT_SERVER = 'to_client'
    MSG_EVENT_SERVER_SVR = 'to_server_svr'
    MSG_EVENT_CLIENT_SVR = 'to_client_svr'
    MSG_OPEN_ROOM_SERVER = 'open_room_s2s'

    FEEDBACK_EVENT = 'feedback_event'

    MSG_OPEN_ROOM = 'open_room'

    @classmethod
    def get_names(cls, myname):
        body_name = cls.OOCHAT_BODY + myname
        send_input_name = cls.OOCHAT_SEND_INPUT + myname
        send_btn_name = cls.OOCHAT_SEND_BTN + myname
        return body_name, send_input_name, send_btn_name

    '''
    @classmethod
    def test_request(cls, methods=['GET']):

        NAMESPACE = '/test_namespace'
        SERVER_DATA = 'server_data'
        NAME = 'test'
        USER_NAME = '用户' + str(random.randint(1, 100))
        BODY, INPUT, SEND_BTN = OOChatClient.get_names(myname=NAME)

        class Page(WebPage):
            URL = '/OOChatClient_test'

            def type_(self):
                return 'WebPage'

        def on_post():
            req = WebPage.on_post()

            OOChatClient.on_post(req=req, myname=NAME)
            server_message = None
            client_message = None
            for r in req:
                if r['me'] == SERVER_DATA:
                    print('Got message of "message from server" : {}'.format(r['data']))
                    server_message = r['data']
                elif r['me'] == BODY:
                    print('Got data of panel body : {}'.format(r['data']))
                    if 'style' not in r['data']:
                        r['data'] = {**r['data'], **cls.DEFAULT_BODY_STYLE}
                    else:
                        r['data']['style']['height'] = cls.DEFAULT_BODY_STYLE['height']
                    if server_message:
                        OOChatClient.body_process(body_data=r['data'], message=server_message, me=USER_NAME)
                    if client_message:
                        OOChatClient.body_process(body_data=r['data'], message=client_message, me=USER_NAME)
                elif r['me'] == INPUT:
                    print('Got data of input : {}'.format(r['data']))
                    client_message = {'from': '我', 'data': {'message': r['data']['val']}, 'type': 'me'}
                elif r['me'] == SEND_BTN:
                    print('Got data of send btn : {}'.format(r['data']))

            return jsonify({'status': 'success', 'data': req})

        Page.init_page(app=current_app, endpoint=cls.__name__ + '.test', on_post=on_post)

        with Page() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='200px')) as c1:
                    with c1.add_child(globals()[cls.__name__](parent=page, name=NAME, socket_namespace=NAMESPACE,
                                                              user_name=USER_NAME,
                                                              radius='10px 10px 10px 10px')) as chat_test:
                        pass

        html = page.render()
        return render_template_string(html)
    '''

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):
            SERVER_NAME = '客服1'

            def place_components_impl(self):
                page = self

                testing_class = OOChatClient
                testing_cls_name = testing_class.__name__

                with page.add_child(WebRow()) as r1:
                    with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='800px')) as c1:
                        with c1.add_child(testing_class(parent=page,
                                                        name=testing_cls_name,
                                                        socket_namespace=testing_class.NAMESPACE,
                                                        user_name='用户' + str(random.randint(1, 1000)),
                                                        server_name=self.SERVER_NAME,
                                                        radius='20px 10px 10px 10px')) as chat_test:
                            pass

            def intro_events_impl(self):
                pass

            def on_my_render_impl(self, req):
                test_obj = self._page._components['OOChatClient']['obj']
                test_class = test_obj.__class__

                BODY, INPUT, SEND_BTN = self.get_names('OOChatClient')

                '''
                req = None
                if hasattr(self._page, '_action'):
                    req = self._page._action.on_post()
                else:
                    req = self._page.on_post()
                '''

                for r in req:
                    if r['me'] == 'OOChatClient':
                        req_me = r['data']
                        server_message = None
                        client_message = None
                        for r_ in req_me:
                            if r_['me'] == test_class.SERVER_DATA:
                                print('Got request data from chat server: {}'.format(r_['data']))
                                server_message = r_['data']
                            elif r_['me'] == BODY:
                                print('Got data of panel body : {}'.format(r_['data']))
                                if 'style' not in r_['data']:
                                    r_['data'] = {**r_['data'], **test_class.DEFAULT_BODY_STYLE}
                                else:
                                    r_['data']['style'] = {'height': test_obj.DEFAULT_BODY_STYLE['style']['height']}
                                if server_message:
                                    test_obj.body_process(body_data=r_['data'], message=server_message,
                                                      me=test_obj.user_name)
                                if client_message:
                                    test_obj.body_process(body_data=r_['data'], message=client_message,
                                                      me=test_obj.user_name)
                            elif r_['me'] == INPUT:
                                print('Got data of input : {}'.format(r_['data']))
                                val = r_['data']['val'] if 'val' in r_['data'] else ''
                                client_message = {'from': '我', 'data': {'message': val}, 'type': 'me'}
                            elif r_['me'] == SEND_BTN:
                                print('Got data of send btn : {}'.format(r_['data']))

                return jsonify({'status': 'success', 'data': req})

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


from flask_socketio import *


class OOWebChatNM(Namespace):

    def on_connect(self):
        print('OOWwebChat.on_connect!')
        '''
        global thread
        clients.append(request.sid)
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
        '''

    def on_register(self, message):
        '''
        # Register user to the lists
        users[message['user']] = request.sid

        # Append user to object, so we know the chat state between two users
        all_chat[message['user']] = []

        # Broadcast that there is user is connected
        emit('user_response', {
            'type': 'connect',
            'message': '{0} is connected to the server'.format(message['user']),
            'data': {
                'users': users,
                'rooms': room_lists,
            },
        }, broadcast=True)
        '''
        print('OOWebChat.on_register!')

    def on_private_message(self, message):
        '''
        user = get_username(request.sid)
        # if there is no chat state between two users, append to the object
        if message['user'] not in all_chat[user]:
            emit('message_response', {
                'type': 'private',
                'message': '',
                'data': {
                    'user': message['user'],
                },
            })
            all_chat[user].append(message['user'])
        '''
        print('OOWebChat.on_private_message!')

    '''
    def on_private_send(self, message):

        user = get_username(request.sid)
        # if there is no chat state between two users, open new chat
        if user not in all_chat[message['friend']]:
            all_chat[message['friend']].append(user)
            emit('message_response', {
                'type': 'new_private',
                'message': '',
                'data': {
                    'user': user
                }
            }, room=users[message['friend']])

        # send the message to the other
        private_act = 'pm'

        # if type is disconnect, will send all disconnected user message
        if 'act' in message:
            private_act = 'disconnect'
        emit('message_response', {
            'type': 'private_message',
            'act': private_act,
            'data': {
                'text': message['text'],
                'from': user,
            }
        }, room=users[message['friend']])


    def on_room_send(self, message):
        user = get_username(request.sid)

        # because room id from the html start with rooms_ then get room name
        temp_room_name = message['friend'].split('_')
        room_name = '_'.join(temp_room_name[1:len(temp_room_name)])
        emit('message_response', {
            'type': 'room_message',
            'data': {
                'text': message['text'],
                'room': room_name,
                'from': user,
            }
        }, room=room_name)
    '''

    def on_close_chat(self, message):
        '''
        user = get_username(request.sid)
        if message['user'] in all_chat[user]:
            emit('message_response', {
                'type': 'private_close',
                'message': '',
                'data': {
                    'user': message['user']
                }
            })
            all_chat[user].remove(message['user'])
        '''
        print('OOWebChat.on_close_chat!')

    def on_create_room(self, message):
        '''
        # If the room is not exist, append new room to rooms object, also set the admin and initial user
        if message['room'] not in room_lists:
            room_lists[message['room']] = {}
            user = get_username(request.sid)
            room_lists[message['room']]['admin'] = user
            room_lists[message['room']]['users'] = [user]
            join_room(message['room'])
            emit('feed_response', {
                'type': 'rooms',
                'message': '{0} created room {1}'.format(room_lists[message['room']]['admin'], message['room']),
                'data': room_lists
            }, broadcast=True)

            emit('message_response', {
                'type': 'open_room',
                'data': {
                    'room': message['room'],
                },
            })
        else:
            emit('feed_response', {
                'type': 'feed',
                'message': 'Room is exist, please use another room',
                'data': False,
            })
        '''
        print('OOWebChat.on_create_room!')

    '''
    def on_get_room_users(self, message):
        if message['room'] in room_lists:
            emit('feed_response', {
                'type': 'room_users',
                'message': '',
                'data': room_lists[message['room']]['users'],
                'rooms': room_lists,
            })
    '''

    def on_join_room(self, message):
        '''
        if message['room'] in room_lists:
            user = get_username(request.sid)
            if user in room_lists[message['room']]['users']:
                emit('feed_response', {
                    'type': 'feed',
                    'message': 'You have already joined the room',
                    'data': False
                })
            else:
                # join room
                join_room(message['room'])
                # append to room users array
                room_lists[message['room']]['users'].append(user)

                # tell the existing users that there is new user joining the room
                emit('feed_response', {
                    'type': 'new_joined_users',
                    'message': '{0} joined room {1}'.format(user, message['room']),
                    'data': room_lists[message['room']]['users'],
                    'room': message['room'],
                    'user_action': user,
                    'welcome_message': '{0} join the room'.format(user),
                }, room=message['room'])

                # Append to news feed that there is user joining the room
                emit('feed_response', {
                    'type': 'rooms',
                    'message': '',
                    'data': room_lists
                }, broadcast=True)

                # tell the frontend that this is the message for joining the room
                # open chat with id rooms_roomName
                emit('message_response', {
                    'type': 'open_room',
                    'data': {
                        'room': message['room'],
                    },
                })
        '''
        print('OOWebChat.on_join_room!')

    def on_close_room(self, message):
        '''
        user = get_username(request.sid)
        temp_room_name = message['room'].split('_')
        room_name = '_'.join(temp_room_name[1:len(temp_room_name)])

        # if admin, close the room
        if user == room_lists[room_name]['admin']:
            # broadcast to users in the room
            emit('message_response', {
                'type': 'room_feed',
                'data': {
                    'text': '{0} (Admin) is closing the room'.format(user),
                    'room': room_name,
                    'from': user,
                }
            }, room=room_name)

            # update room user list
            emit('feed_response', {
                'type': 'update_room_users',
                'message': '',
                'data': room_lists[room_name]['users'],
                'room': room_name,
                'user_action': user,
                'act': 'close',
            }, broadcast=True)

            # close room
            close_room(room_name)
            # remove room from list
            room_lists.pop(room_name)

            # send message to feed
            emit('feed_response', {
                'type': 'rooms',
                'message': '{0} is closing room {1}'.format(user, room_name),
                'data': room_lists
            }, broadcast=True)
        else:
            # if not admin, leave room
            # broadcast to users in room
            emit('message_response', {
                'type': 'room_feed',
                'data': {
                    'text': '{0} is leaving the room'.format(user),
                    'room': room_name,
                    'from': user,
                }
            }, room=room_name)

            # update room user list
            emit('feed_response', {
                'type': 'update_room_users',
                'message': '',
                'data': room_lists[room_name]['users'],
                'room': room_name,
                'user_action': user,
                'act': 'leave',
            }, room=room_name)

            # leave room
            leave_room(room_name)
            # remove user from room
            room_lists[room_name]['users'].remove(user)

            # broadcast to users in room that there is user leaving the room
            emit('feed_response', {
                'type': 'rooms',
                'message': '{0} is leaving room {1}'.format(user, room_name),
                'data': room_lists
            }, broadcast=True)
        '''
        print('OOWebChat.on_close_room!')

    def on_disconnect(self):
        '''
        if request.sid in clients:
            # remove sid from clients
            clients.remove(request.sid)
            user = get_username(request.sid)
            # if user is exist
            if user:
                all_rooms = [i for i in
                             room_lists]  # create temporary array, so it won't affect the rooms list when it changes
                for room in all_rooms:
                    # if user is admin in a room or user exist in a room, call close room function, logic handled by the function
                    if room_lists[room]['admin'] == user or user in room_lists[room]['users']:
                        self.on_close_room({
                            'room': 'rooms_{0}'.format(room)
                        })

                # broadcast to all chat friend that the user is disconnecting
                for friend in all_chat[user]:
                    self.on_private_send({
                        'friend': friend,
                        'text': '{0} is offline'.format(user),
                        'act': 'disconnect',
                    })

                # remove user chat state
                all_chat.pop(user)

                # remove from users list
                users.pop(user)

                # append to news feed
                emit('user_response', {
                    'type': 'connect',
                    'message': '{0} is disconnected from the server'.format(user),
                    'data': {
                        'users': users,
                        'rooms': room_lists,
                    },
                }, broadcast=True)

        print('Client disconnected {}'.format(request.sid))
        '''
        print('OOWebChat.on_disconnect!')

    def on_my_ping(self):
        emit('my_pong')

    '''
    def on_message_from_client(self, message):
        print('oowebchatnm.on_message_from_client, message:{}'.format(message))
        emit(OOChatServer.MSG_EVENT_SERVER, {'message': 'Message received!',
                                             'from': '客服',
                                             'to': message['from']})
    '''


class ServerChatNM(OOWebChatNM):

    def __init__(self, server_obj, socket_namespace='test_socket_namespace'):
        super().__init__(namespace=socket_namespace)
        self.server_obj = server_obj

    def on_to_server(self, data):
        print('ServerChatNM.on_to_server, got message:{}'.format(data))
        emit(OOChatServer.MSG_EVENT_SERVER_SVR, {'message': data['message'],
                                                 'from': data['from'],
                                                 'to': data['to']},
             broadcast=True)

    def on_to_client(self, data):
        print('ServerChatNM.on_to_client, got message:{}'.format(data))
        emit(OOChatServer.MSG_EVENT_CLIENT_SVR, {'message': data['message'],
                                                 'from': data['from'],
                                                 'to': data['to']},
             broadcast=True)

    def on_open_room(self, data):
        print('ServerChatNM.on_to_server, got message:{}'.format(data))
        emit(OOChatServer.MSG_OPEN_ROOM_SERVER, {'from': data['from'],
                                                 'to': data['to']}, broadcast=True)

    def on_test(self, data):
        print('Got test event:{}'.format(data))


class OOChatServer(OOChatServerTest, OOChatClient):

    VAL_FUNC_NAME = 'oochatserver_val'

    '''
    @classmethod
    def test_request(cls, methods=['GET']):
        NAMESPACE = '/test_namespace'
        SERVER_DATA = 'server_data'
        NAME = '客服'
        USER_NAME = '客服'
        PANEL_NAME = 'chat'

        class Page(WebPage):
            URL = '/OOChatServer_test'

            def type_(self):
                return 'WebPage'

        def on_post():
            req = WebPage.on_post()

            return jsonify({'status': 'success', 'data': req})

        Page.init_page(app=current_app, endpoint=cls.__name__ + '.test', on_post=on_post)

        with Page() as page:
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn()) as c1:
                    with c1.add_child(globals()[cls.__name__](parent=page, name=NAME,
                                                              user_name=USER_NAME, socket_namespace=NAMESPACE,
                                                              radius='10px 10px 10px 10px')) as chat_test:
                        pass
        current_app.socketio.on_namespace(ServerChatNM(server_obj=None, socket_namespace=NAMESPACE))
        html = page.render()
        return render_template_string(html)
    '''

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            TestName = '客服1'

            def place_components_impl(self):
                NAME = self.TestName

                page = self
                testing_class = OOChatServer
                testing_cls_name = testing_class.__name__

                with page.add_child(WebRow()) as r1:
                    with r1.add_child(WebColumn()) as c1:
                        with c1.add_child(testing_class(parent=page,
                                                        name=testing_cls_name,
                                                        user_name=NAME,
                                                        socket_namespace=testing_class.NAMESPACE,
                                                        radius='10px 10px 10px 10px')) as chat_test:
                            pass

                current_app.socketio.on_namespace(ServerChatNM(server_obj=None,
                                                               socket_namespace=testing_class.NAMESPACE))

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class OOChartNVD3(WebSvg):

    OOCHART_CLASSES = {}
    OOCHART_CREATE_FUNC_NAME = 'oochart_create'

    @classmethod
    def stream_waves(cls, n, m):

        def map_func(i):
            def map_func_(j):
                x = 20 * j / m - i / 3
                return 2 * x * (-.5 * x)

            return list(map(cls.stream_index, list(map(map_func_, range(m)))))

        return list(map(map_func, range(n)))

    @classmethod
    def stream_index(cls, args):
        return {'x': args[0], 'y': max(0, -args[1])}

    @classmethod
    def stream_layers(cls, n, m, o=None):

        def bump(a):
            x = 1 / (.1 + random.random())
            y = 2 * random.random() - .5
            z = 10 / (.1 + random.random())
            for i in range(int(m)):
                w = (i / m - y) * z
                a[i] += x * (-w * w)

        def map_func(x):
            a = []
            for i in range(int(m)):
                a.append(o + o * random.random())
            for j in range(5):
                bump(a)
            return list(map(cls.stream_index, enumerate(a)))

        return list(map(map_func, range(n)))

    @classmethod
    def CALL_CREATE_FUNC(cls, svg, chart_type, chart_data, aobj, parent='null', duration=0, simple=False):
        params = {'svg': svg, 'chart_type': chart_type, 'chart_data': chart_data, 'aobj_id': aobj.id(),
                  'parent': parent,
                  'duration': duration, 'simple': simple}
        return aobj.class_func_call(cls=cls.__name__, params=params)

    @classmethod
    def test_request(cls, methods=['GET']):

        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def process_events_impl(self, req):
                test_obj = None
                test_class = None
                for name, obj in self._components.items():
                    if name.find('OOChart') == 0:
                        test_obj = obj['obj']
                        test_class = test_obj.__class__
                name_ = req['me']
                print('Class testing, class {} got req:{}'.format(name_, req))
                assert(hasattr(test_class, 'test_request_data') and test_class.test_request_data)
                req['data'] = {'data': cls.test_request_data()}


        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class OOChartLineFinder(OOChartNVD3):
    OOChartNVD3.OOCHART_CLASSES['linefinder'] = __qualname__

    @classmethod
    def test_request_data(cls):
        return 'linefinder'


class OOChartPie(OOChartNVD3):
    OOChartNVD3.OOCHART_CLASSES['pie'] = __qualname__

    @classmethod
    def test_request_data(cls):
        return [
            {
                "label": "One",
                "value": 29.765957771107
            },
            {
                "label": "Two",
                "value": 15
            },
            {
                "label": "Three",
                "value": 32.807804682612
            },

        ]


class OOChartComulativeLine(OOChartNVD3):
    OOChartNVD3.OOCHART_CLASSES['cline'] = __qualname__

    @classmethod
    def test_request_data(cls):
        return [
            {
                "key": "Series 1",
                "values": [[1025409600000, 0], [1028088000000, -6.3382185140371], [1030766400000, -5.9507873460847],
                           [1033358400000, -11.569146943813], [1036040400000, -5.4767332317425],
                           [1038632400000, 0.50794682203014], [1041310800000, -5.5310285460542],
                           [1043989200000, -5.7838296963382], [1046408400000, -7.3249341615649],
                           [1049086800000, -6.7078630712489], [1051675200000, 0.44227126150934],
                           [1054353600000, 7.2481659343222], [1056945600000, 9.2512381306992],
                           [1059624000000, 11.341210982529], [1062302400000, 14.734820409020],
                           [1064894400000, 12.387148007542], [1067576400000, 18.436471461827],
                           [1070168400000, 19.830742266977], [1072846800000, 22.643205829887],
                           [1075525200000, 26.743156781239], [1078030800000, 29.597478802228],
                           [1080709200000, 30.831697585341], [1083297600000, 28.054068024708],
                           [1085976000000, 29.294079423832], [1088568000000, 30.269264061274],
                           [1091246400000, 24.934526898906], [1093924800000, 24.265982759406],
                           [1096516800000, 27.217794897473], [1099195200000, 30.802601992077],
                           [1101790800000, 36.331003758254], [1104469200000, 43.142498700060],
                           [1107147600000, 40.558263931958], [1109566800000, 42.543622385800],
                           [1112245200000, 41.683584710331], [1114833600000, 36.375367302328],
                           [1117512000000, 40.719688980730], [1120104000000, 43.897963036919],
                           [1122782400000, 49.797033975368], [1125460800000, 47.085993935989],
                           [1128052800000, 46.601972859745], [1130734800000, 41.567784572762],
                           [1133326800000, 47.296923737245], [1136005200000, 47.642969612080],
                           [1138683600000, 50.781515820954], [1141102800000, 52.600229204305],
                           [1143781200000, 55.599684490628], [1146369600000, 57.920388436633],
                           [1149048000000, 53.503593218971], [1151640000000, 53.522973979964],
                           [1154318400000, 49.846822298548], [1156996800000, 54.721341614650],
                           [1159588800000, 58.186236223191], [1162270800000, 63.908065540997],
                           [1164862800000, 69.767285129367], [1167541200000, 72.534013373592],
                           [1170219600000, 77.991819436573], [1172638800000, 78.143584404990],
                           [1175313600000, 83.702398665233], [1177905600000, 91.140859312418],
                           [1180584000000, 98.590960607028], [1183176000000, 96.245634754228],
                           [1185854400000, 92.326364432615], [1188532800000, 97.068765332230],
                           [1191124800000, 105.81025556260], [1193803200000, 114.38348777791],
                           [1196398800000, 103.59604949810], [1199077200000, 101.72488429307],
                           [1201755600000, 89.840147735028], [1204261200000, 86.963597532664],
                           [1206936000000, 84.075505208491], [1209528000000, 93.170105645831],
                           [1212206400000, 103.62838083121], [1214798400000, 87.458241365091],
                           [1217476800000, 85.808374141319], [1220155200000, 93.158054469193],
                           [1222747200000, 65.973252382360], [1225425600000, 44.580686638224],
                           [1228021200000, 36.418977140128], [1230699600000, 38.727678144761],
                           [1233378000000, 36.692674173387], [1235797200000, 30.033022809480],
                           [1238472000000, 36.707532162718], [1241064000000, 52.191457688389],
                           [1243742400000, 56.357883979735], [1246334400000, 57.629002180305],
                           [1249012800000, 66.650985790166], [1251691200000, 70.839243432186],
                           [1254283200000, 78.731998491499], [1256961600000, 72.375528540349],
                           [1259557200000, 81.738387881630], [1262235600000, 87.539792394232],
                           [1264914000000, 84.320762662273], [1267333200000, 90.621278391889],
                           [1270008000000, 102.47144881651], [1272600000000, 102.79320353429],
                           [1275278400000, 90.529736050479], [1277870400000, 76.580859994531],
                           [1280548800000, 86.548979376972], [1283227200000, 81.879653334089],
                           [1285819200000, 101.72550015956], [1288497600000, 107.97964852260],
                           [1291093200000, 106.16240630785], [1293771600000, 114.84268599533],
                           [1296450000000, 121.60793322282], [1298869200000, 133.41437346605],
                           [1301544000000, 125.46646042904], [1304136000000, 129.76784954301],
                           [1306814400000, 128.15798861044], [1309406400000, 121.92388706072],
                           [1312084800000, 116.70036100870], [1314763200000, 88.367701837033],
                           [1317355200000, 59.159665765725], [1320033600000, 79.793568139753],
                           [1322629200000, 75.903834028417], [1325307600000, 72.704218209157],
                           [1327986000000, 84.936990804097], [1330491600000, 93.388148670744]]
            },
            {
                "key": "Series 2",
                "values": [[1025409600000, 0], [1028088000000, 0], [1030766400000, 0], [1033358400000, 0],
                           [1036040400000, 0], [1038632400000, 0], [1041310800000, 0], [1043989200000, 0],
                           [1046408400000, 0], [1049086800000, 0], [1051675200000, 0], [1054353600000, 0],
                           [1056945600000, 0], [1059624000000, 0], [1062302400000, 0], [1064894400000, 0],
                           [1067576400000, 0], [1070168400000, 0], [1072846800000, 0],
                           [1075525200000, -0.049184266875945], [1078030800000, -0.10757569491991],
                           [1080709200000, -0.075601531307242], [1083297600000, -0.061245277988149],
                           [1085976000000, -0.068227316401169], [1088568000000, -0.11242758058502],
                           [1091246400000, -0.074848439408270], [1093924800000, -0.11465623676497],
                           [1096516800000, -0.24370633342416], [1099195200000, -0.21523268478893],
                           [1101790800000, -0.37859370911822], [1104469200000, -0.41932884345151],
                           [1107147600000, -0.45393735984802], [1109566800000, -0.50868179522598],
                           [1112245200000, -0.48164396881207], [1114833600000, -0.41605962887194],
                           [1117512000000, -0.48490348490240], [1120104000000, -0.55071036101311],
                           [1122782400000, -0.67489170505394], [1125460800000, -0.74978070939342],
                           [1128052800000, -0.86395050745343], [1130734800000, -0.78524898506764],
                           [1133326800000, -0.99800440950854], [1136005200000, -1.1177951153878],
                           [1138683600000, -1.4119975432964], [1141102800000, -1.2409959736465],
                           [1143781200000, -1.3088936375431], [1146369600000, -1.5495785469683],
                           [1149048000000, -1.1563414981293], [1151640000000, -0.87192471725994],
                           [1154318400000, -0.84073995183442], [1156996800000, -0.88761892867370],
                           [1159588800000, -0.81748513917485], [1162270800000, -1.2874081041274],
                           [1164862800000, -1.9234702981339], [1167541200000, -1.8377768147648],
                           [1170219600000, -2.7107654031830], [1172638800000, -2.6493268125418],
                           [1175313600000, -3.0814553134551], [1177905600000, -3.8509837783574],
                           [1180584000000, -5.2919167850718], [1183176000000, -5.2297750650773],
                           [1185854400000, -3.9335668501451], [1188532800000, -2.3695525190114],
                           [1191124800000, -2.3084243151854], [1193803200000, -3.0753680726738],
                           [1196398800000, -2.2346609938962], [1199077200000, -3.0598810361615],
                           [1201755600000, -1.8410154270386], [1204261200000, -1.6479442038620],
                           [1206936000000, -1.9293858622780], [1209528000000, -3.0769590460943],
                           [1212206400000, -4.2423933501421], [1214798400000, -2.6951491617768],
                           [1217476800000, -2.8981825939957], [1220155200000, -2.9662727940324],
                           [1222747200000, 0.21556750497498], [1225425600000, 2.6784995167088],
                           [1228021200000, 4.1296711248958], [1230699600000, 3.7311068218734],
                           [1233378000000, 4.7695330866954], [1235797200000, 5.1919133040990],
                           [1238472000000, 4.1025856045660], [1241064000000, 2.8498939666225],
                           [1243742400000, 2.8106017222851], [1246334400000, 2.8456526669963],
                           [1249012800000, 0.65563070754298], [1251691200000, -0.30022343874633],
                           [1254283200000, -1.1600358228964], [1256961600000, -0.26674408835052],
                           [1259557200000, -1.4693389757812], [1262235600000, -2.7855421590594],
                           [1264914000000, -1.2668244065703], [1267333200000, -2.5537804115548],
                           [1270008000000, -4.9144552474502], [1272600000000, -6.0484408234831],
                           [1275278400000, -3.3834349033750], [1277870400000, -0.46752826932523],
                           [1280548800000, -1.8030186027963], [1283227200000, -0.99623230097881],
                           [1285819200000, -3.3475370235594], [1288497600000, -3.8187026520342],
                           [1291093200000, -4.2354146250353], [1293771600000, -5.6795404292885],
                           [1296450000000, -6.2928665328172], [1298869200000, -6.8549277434419],
                           [1301544000000, -6.9925308360918], [1304136000000, -8.3216548655839],
                           [1306814400000, -7.7682867271435], [1309406400000, -6.9244213301058],
                           [1312084800000, -5.7407624451404], [1314763200000, -2.1813149077927],
                           [1317355200000, 2.9407596325999], [1320033600000, -1.1130607112134],
                           [1322629200000, -2.0274822307752], [1325307600000, -1.8372559072154],
                           [1327986000000, -4.0732815531148], [1330491600000, -6.4417038470291]]
            },
            {
                "key": "Series 3",
                "values": [[1025409600000, 0], [1028088000000, -6.3382185140371], [1030766400000, -5.9507873460847],
                           [1033358400000, -11.569146943813], [1036040400000, -5.4767332317425],
                           [1038632400000, 0.50794682203014], [1041310800000, -5.5310285460542],
                           [1043989200000, -5.7838296963382], [1046408400000, -7.3249341615649],
                           [1049086800000, -6.7078630712489], [1051675200000, 0.44227126150934],
                           [1054353600000, 7.2481659343222], [1056945600000, 9.2512381306992],
                           [1059624000000, 11.341210982529], [1062302400000, 14.734820409020],
                           [1064894400000, 12.387148007542], [1067576400000, 18.436471461827],
                           [1070168400000, 19.830742266977], [1072846800000, 22.643205829887],
                           [1075525200000, 26.693972514363], [1078030800000, 29.489903107308],
                           [1080709200000, 30.756096054034], [1083297600000, 27.992822746720],
                           [1085976000000, 29.225852107431], [1088568000000, 30.156836480689],
                           [1091246400000, 24.859678459498], [1093924800000, 24.151326522641],
                           [1096516800000, 26.974088564049], [1099195200000, 30.587369307288],
                           [1101790800000, 35.952410049136], [1104469200000, 42.723169856608],
                           [1107147600000, 40.104326572110], [1109566800000, 42.034940590574],
                           [1112245200000, 41.201940741519], [1114833600000, 35.959307673456],
                           [1117512000000, 40.234785495828], [1120104000000, 43.347252675906],
                           [1122782400000, 49.122142270314], [1125460800000, 46.336213226596],
                           [1128052800000, 45.738022352292], [1130734800000, 40.782535587694],
                           [1133326800000, 46.298919327736], [1136005200000, 46.525174496692],
                           [1138683600000, 49.369518277658], [1141102800000, 51.359233230659],
                           [1143781200000, 54.290790853085], [1146369600000, 56.370809889665],
                           [1149048000000, 52.347251720842], [1151640000000, 52.651049262704],
                           [1154318400000, 49.006082346714], [1156996800000, 53.833722685976],
                           [1159588800000, 57.368751084016], [1162270800000, 62.620657436870],
                           [1164862800000, 67.843814831233], [1167541200000, 70.696236558827],
                           [1170219600000, 75.281054033390], [1172638800000, 75.494257592448],
                           [1175313600000, 80.620943351778], [1177905600000, 87.289875534061],
                           [1180584000000, 93.299043821956], [1183176000000, 91.015859689151],
                           [1185854400000, 88.392797582470], [1188532800000, 94.699212813219],
                           [1191124800000, 103.50183124741], [1193803200000, 111.30811970524],
                           [1196398800000, 101.36138850420], [1199077200000, 98.665003256909],
                           [1201755600000, 87.999132307989], [1204261200000, 85.315653328802],
                           [1206936000000, 82.146119346213], [1209528000000, 90.093146599737],
                           [1212206400000, 99.385987481068], [1214798400000, 84.763092203314],
                           [1217476800000, 82.910191547323], [1220155200000, 90.191781675161],
                           [1222747200000, 66.188819887335], [1225425600000, 47.259186154933],
                           [1228021200000, 40.548648265024], [1230699600000, 42.458784966634],
                           [1233378000000, 41.462207260082], [1235797200000, 35.224936113579],
                           [1238472000000, 40.810117767284], [1241064000000, 55.041351655012],
                           [1243742400000, 59.168485702020], [1246334400000, 60.474654847301],
                           [1249012800000, 67.306616497709], [1251691200000, 70.539019993440],
                           [1254283200000, 77.571962668603], [1256961600000, 72.108784451998],
                           [1259557200000, 80.269048905849], [1262235600000, 84.754250235173],
                           [1264914000000, 83.053938255703], [1267333200000, 88.067497980334],
                           [1270008000000, 97.556993569060], [1272600000000, 96.744762710807],
                           [1275278400000, 87.146301147104], [1277870400000, 76.113331725206],
                           [1280548800000, 84.745960774176], [1283227200000, 80.883421033110],
                           [1285819200000, 98.377963136001], [1288497600000, 104.16094587057],
                           [1291093200000, 101.92699168281], [1293771600000, 109.16314556604],
                           [1296450000000, 115.31506669000], [1298869200000, 126.55944572261],
                           [1301544000000, 118.47392959295], [1304136000000, 121.44619467743],
                           [1306814400000, 120.38970188330], [1309406400000, 114.99946573061],
                           [1312084800000, 110.95959856356], [1314763200000, 86.186386929240],
                           [1317355200000, 62.100425398325], [1320033600000, 78.680507428540],
                           [1322629200000, 73.876351797642], [1325307600000, 70.866962301942],
                           [1327986000000, 80.863709250982], [1330491600000, 86.946444823715]]
            },
            {
                "key": "Series 4",
                "values": [[1025409600000, -7.0674410638835], [1028088000000, -14.663359292964],
                           [1030766400000, -14.104393060540], [1033358400000, -23.114477037218],
                           [1036040400000, -16.774256687841], [1038632400000, -11.902028464000],
                           [1041310800000, -16.883038668422], [1043989200000, -19.104223676831],
                           [1046408400000, -20.420523282736], [1049086800000, -19.660555051587],
                           [1051675200000, -13.106911231646], [1054353600000, -8.2448460302143],
                           [1056945600000, -7.0313058730976], [1059624000000, -5.1485118700389],
                           [1062302400000, -3.0011028761469], [1064894400000, -4.1367265281467],
                           [1067576400000, 1.5425209565025], [1070168400000, 2.7673533607299],
                           [1072846800000, 7.7077114755360], [1075525200000, 9.7565015112434],
                           [1078030800000, 11.396888609473], [1080709200000, 10.013964745578],
                           [1083297600000, 8.0558890950562], [1085976000000, 9.6081966657458],
                           [1088568000000, 11.918590426432], [1091246400000, 7.9945345523982],
                           [1093924800000, 8.3201276776796], [1096516800000, 9.8283954846342],
                           [1099195200000, 11.527125859650], [1101790800000, 16.413657596527],
                           [1104469200000, 20.393798297928], [1107147600000, 17.456308413907],
                           [1109566800000, 20.087778400999], [1112245200000, 17.988336990817],
                           [1114833600000, 15.378490151331], [1117512000000, 19.474322935730],
                           [1120104000000, 20.013851070354], [1122782400000, 24.749943726975],
                           [1125460800000, 23.558710274826], [1128052800000, 24.558915040889],
                           [1130734800000, 22.355860488034], [1133326800000, 27.138026265756],
                           [1136005200000, 27.202220808591], [1138683600000, 31.219437344964],
                           [1141102800000, 31.392355525125], [1143781200000, 33.373099232542],
                           [1146369600000, 35.095277582309], [1149048000000, 30.923356507615],
                           [1151640000000, 31.083717332561], [1154318400000, 31.290690671561],
                           [1156996800000, 34.247769216679], [1159588800000, 37.411073177620],
                           [1162270800000, 42.079177096411], [1164862800000, 44.978191659648],
                           [1167541200000, 46.713271025310], [1170219600000, 49.203892437699],
                           [1172638800000, 46.684723471826], [1175313600000, 48.385458973500],
                           [1177905600000, 54.660197840305], [1180584000000, 60.311838415602],
                           [1183176000000, 57.583282204682], [1185854400000, 52.425398898751],
                           [1188532800000, 54.663538086985], [1191124800000, 60.181844325224],
                           [1193803200000, 62.877219773621], [1196398800000, 55.760611512951],
                           [1199077200000, 54.735280367784], [1201755600000, 45.495912959474],
                           [1204261200000, 40.934919015876], [1206936000000, 40.303777633187],
                           [1209528000000, 47.403740368773], [1212206400000, 49.951960898839],
                           [1214798400000, 37.534590035098], [1217476800000, 36.405758293321],
                           [1220155200000, 38.545373001858], [1222747200000, 26.106358664455],
                           [1225425600000, 4.2658006768744], [1228021200000, -3.5517839867557],
                           [1230699600000, -2.0878920761513], [1233378000000, -10.408879093829],
                           [1235797200000, -19.924242196038], [1238472000000, -12.906491912782],
                           [1241064000000, -3.9774866468346], [1243742400000, 1.0319171601402],
                           [1246334400000, 1.3109350357718], [1249012800000, 9.1668309061935],
                           [1251691200000, 13.121178985954], [1254283200000, 17.578680237511],
                           [1256961600000, 14.971294355085], [1259557200000, 21.551327027338],
                           [1262235600000, 24.592328423819], [1264914000000, 20.158087829555],
                           [1267333200000, 24.135661929185], [1270008000000, 31.815205405903],
                           [1272600000000, 34.389524768466], [1275278400000, 23.785555857522],
                           [1277870400000, 17.082756649072], [1280548800000, 25.248007727100],
                           [1283227200000, 19.415179069165], [1285819200000, 30.413636349327],
                           [1288497600000, 35.357952964550], [1291093200000, 35.886413535859],
                           [1293771600000, 45.003601951959], [1296450000000, 48.274893564020],
                           [1298869200000, 53.562864914648], [1301544000000, 54.108274337412],
                           [1304136000000, 58.618190111927], [1306814400000, 56.806793965598],
                           [1309406400000, 54.135477252994], [1312084800000, 50.735258942442],
                           [1314763200000, 42.208170945813], [1317355200000, 31.617916826724],
                           [1320033600000, 46.492005006737], [1322629200000, 46.203116922145],
                           [1325307600000, 47.541427643137], [1327986000000, 54.518998440993],
                           [1330491600000, 61.099720234693]]
            }
        ]


class OOChartLinePlusBar(OOChartNVD3):
    OOChartNVD3.OOCHART_CLASSES['lpbar'] = __qualname__

    @classmethod
    def test_request_data(cls):
        return [
            {
                "key": "Quantity",
                "bar": True,
                "values": [[1136005200000, 1271000.0], [1138683600000, 1271000.0], [1141102800000, 1271000.0],
                           [1143781200000, 0], [1146369600000, 0], [1149048000000, 0], [1151640000000, 0],
                           [1154318400000, 0], [1156996800000, 0], [1159588800000, 3899486.0],
                           [1162270800000, 3899486.0], [1164862800000, 3899486.0], [1167541200000, 3564700.0],
                           [1170219600000, 3564700.0], [1172638800000, 3564700.0], [1175313600000, 2648493.0],
                           [1177905600000, 2648493.0], [1180584000000, 2648493.0], [1183176000000, 2522993.0],
                           [1185854400000, 2522993.0], [1188532800000, 2522993.0], [1191124800000, 2906501.0],
                           [1193803200000, 2906501.0], [1196398800000, 2906501.0], [1199077200000, 2206761.0],
                           [1201755600000, 2206761.0], [1204261200000, 2206761.0], [1206936000000, 2287726.0],
                           [1209528000000, 2287726.0], [1212206400000, 2287726.0], [1214798400000, 2732646.0],
                           [1217476800000, 2732646.0], [1220155200000, 2732646.0], [1222747200000, 2599196.0],
                           [1225425600000, 2599196.0], [1228021200000, 2599196.0], [1230699600000, 1924387.0],
                           [1233378000000, 1924387.0], [1235797200000, 1924387.0], [1238472000000, 1756311.0],
                           [1241064000000, 1756311.0], [1243742400000, 1756311.0], [1246334400000, 1743470.0],
                           [1249012800000, 1743470.0], [1251691200000, 1743470.0], [1254283200000, 1519010.0],
                           [1256961600000, 1519010.0], [1259557200000, 1519010.0], [1262235600000, 1591444.0],
                           [1264914000000, 1591444.0], [1267333200000, 1591444.0], [1270008000000, 1543784.0],
                           [1272600000000, 1543784.0], [1275278400000, 1543784.0], [1277870400000, 1309915.0],
                           [1280548800000, 1309915.0], [1283227200000, 1309915.0], [1285819200000, 1331875.0],
                           [1288497600000, 1331875.0], [1291093200000, 1331875.0], [1293771600000, 1331875.0],
                           [1296450000000, 1154695.0], [1298869200000, 1154695.0], [1301544000000, 1194025.0],
                           [1304136000000, 1194025.0], [1306814400000, 1194025.0], [1309406400000, 1194025.0],
                           [1312084800000, 1194025.0], [1314763200000, 1244525.0], [1317355200000, 475000.0],
                           [1320033600000, 475000.0], [1322629200000, 475000.0], [1325307600000, 690033.0],
                           [1327986000000, 690033.0], [1330491600000, 690033.0], [1333166400000, 514733.0],
                           [1335758400000, 514733.0]]
            },
            {
                "key": "Price",
                "values": [[1136005200000, 71.89], [1138683600000, 75.51], [1141102800000, 68.49],
                           [1143781200000, 62.72], [1146369600000, 70.39], [1149048000000, 59.77],
                           [1151640000000, 57.27], [1154318400000, 67.96], [1156996800000, 67.85],
                           [1159588800000, 76.98], [1162270800000, 81.08], [1164862800000, 91.66],
                           [1167541200000, 84.84], [1170219600000, 85.73], [1172638800000, 84.61],
                           [1175313600000, 92.91], [1177905600000, 99.8], [1180584000000, 121.191],
                           [1183176000000, 122.04], [1185854400000, 131.76], [1188532800000, 138.48],
                           [1191124800000, 153.47], [1193803200000, 189.95], [1196398800000, 182.22],
                           [1199077200000, 198.08], [1201755600000, 135.36], [1204261200000, 125.02],
                           [1206936000000, 143.5], [1209528000000, 173.95], [1212206400000, 188.75],
                           [1214798400000, 167.44], [1217476800000, 158.95], [1220155200000, 169.53],
                           [1222747200000, 113.66], [1225425600000, 107.59], [1228021200000, 92.67],
                           [1230699600000, 85.35], [1233378000000, 90.13], [1235797200000, 89.31],
                           [1238472000000, 105.12], [1241064000000, 125.83], [1243742400000, 135.81],
                           [1246334400000, 142.43], [1249012800000, 163.39], [1251691200000, 168.21],
                           [1254283200000, 185.35], [1256961600000, 188.5], [1259557200000, 199.91],
                           [1262235600000, 210.732], [1264914000000, 192.063], [1267333200000, 204.62],
                           [1270008000000, 235.0], [1272600000000, 261.09], [1275278400000, 256.88],
                           [1277870400000, 251.53], [1280548800000, 257.25], [1283227200000, 243.1],
                           [1285819200000, 283.75], [1288497600000, 300.98], [1291093200000, 311.15],
                           [1293771600000, 322.56], [1296450000000, 339.32], [1298869200000, 353.21],
                           [1301544000000, 348.5075], [1304136000000, 350.13], [1306814400000, 347.83],
                           [1309406400000, 335.67], [1312084800000, 390.48], [1314763200000, 384.83],
                           [1317355200000, 381.32], [1320033600000, 404.78], [1322629200000, 382.2],
                           [1325307600000, 405.0], [1327986000000, 456.48], [1330491600000, 542.44],
                           [1333166400000, 599.55], [1335758400000, 583.98]]
            }
        ]


class OOChartHorizontalGroupedStackedBar(OOChartNVD3):
    OOChartNVD3.OOCHART_CLASSES['hgsbar'] = __qualname__

    @classmethod
    def test_request_data(cls):
        return [
            {
                "key": "Series1",
                "color": "#d62728",
                "values": [
                    {
                        "label": "Group A",
                        "value": -1.8746444827653
                    },
                    {
                        "label": "Group B",
                        "value": -8.0961543492239
                    },
                    {
                        "label": "Group C",
                        "value": -0.57072943117674
                    },
                    {
                        "label": "Group D",
                        "value": -2.4174010336624
                    },
                    {
                        "label": "Group E",
                        "value": -0.72009071426284
                    },
                    {
                        "label": "Group F",
                        "value": -0.77154485523777
                    },
                    {
                        "label": "Group G",
                        "value": -0.90152097798131
                    },
                    {
                        "label": "Group H",
                        "value": -0.91445417330854
                    },
                    {
                        "label": "Group I",
                        "value": -0.055746319141851
                    }
                ]
            },
            {
                "key": "Series2",
                "color": "#1f77b4",
                "values": [
                    {
                        "label": "Group A",
                        "value": 25.307646510375
                    },
                    {
                        "label": "Group B",
                        "value": 16.756779544553
                    },
                    {
                        "label": "Group C",
                        "value": 18.451534877007
                    },
                    {
                        "label": "Group D",
                        "value": 8.6142352811805
                    },
                    {
                        "label": "Group E",
                        "value": 7.8082472075876
                    },
                    {
                        "label": "Group F",
                        "value": 5.259101026956
                    },
                    {
                        "label": "Group G",
                        "value": 0.30947953487127
                    },
                    {
                        "label": "Group H",
                        "value": 0
                    },
                    {
                        "label": "Group I",
                        "value": 0
                    }
                ]
            }
        ]


class OOChartDescreteBar(OOChartNVD3):
    OOChartNVD3.OOCHART_CLASSES['dbar'] = __qualname__

    @classmethod
    def test_request_data(cls):
        return [
            {
                'key': "Cumulative Return",
                'values': [
                    {
                        "label": "A",
                        "value": -29.765957771107
                    },
                    {
                        "label": "B",
                        "value": 0
                    },
                    {
                        "label": "C",
                        "value": 32.807804682612
                    },
                    {
                        "label": "D",
                        "value": 196.45946739256
                    },
                    {
                        "label": "E",
                        "value": 0.19434030906893
                    },
                    {
                        "label": "F",
                        "value": -98.079782601442
                    },
                    {
                        "label": "G",
                        "value": -13.925743130903
                    },
                    {
                        "label": "H",
                        "value": -5.1387322875705
                    }
                ]
            }
        ]


class OOChartStackedArea(OOChartNVD3):
    OOChartNVD3.OOCHART_CLASSES['stackedarea'] = __qualname__

    @classmethod
    def test_request_data(cls):
        return [
            {
                "key": "North America",
                "values": [[1025409600000, 23.041422681023], [1028088000000, 19.854291255832],
                           [1030766400000, 21.02286281168], [1033358400000, 22.093608385173],
                           [1036040400000, 25.108079299458], [1038632400000, 26.982389242348],
                           [1041310800000, 19.828984957662], [1043989200000, 19.914055036294],
                           [1046408400000, 19.436150539916], [1049086800000, 21.558650338602],
                           [1051675200000, 24.395594061773], [1054353600000, 24.747089309384],
                           [1056945600000, 23.491755498807], [1059624000000, 23.376634878164],
                           [1062302400000, 24.581223154533], [1064894400000, 24.922476843538],
                           [1067576400000, 27.357712939042], [1070168400000, 26.503020572593],
                           [1072846800000, 26.658901244878], [1075525200000, 27.065704156445],
                           [1078030800000, 28.735320452588], [1080709200000, 31.572277846319],
                           [1083297600000, 30.932161503638], [1085976000000, 31.627029785554],
                           [1088568000000, 28.728743674232], [1091246400000, 26.858365172675],
                           [1093924800000, 27.279922830032], [1096516800000, 34.408301211324],
                           [1099195200000, 34.794362930439], [1101790800000, 35.609978198951],
                           [1104469200000, 33.574394968037], [1107147600000, 31.979405070598],
                           [1109566800000, 31.19009040297], [1112245200000, 31.083933968994],
                           [1114833600000, 29.668971113185], [1117512000000, 31.490638014379],
                           [1120104000000, 31.818617451128], [1122782400000, 32.960314008183],
                           [1125460800000, 31.313383196209], [1128052800000, 33.125486081852],
                           [1130734800000, 32.791805509149], [1133326800000, 33.506038030366],
                           [1136005200000, 26.96501697216], [1138683600000, 27.38478809681],
                           [1141102800000, 27.371377218209], [1143781200000, 26.309915460827],
                           [1146369600000, 26.425199957518], [1149048000000, 26.823411519396],
                           [1151640000000, 23.850443591587], [1154318400000, 23.158355444054],
                           [1156996800000, 22.998689393695], [1159588800000, 27.9771285113],
                           [1162270800000, 29.073672469719], [1164862800000, 28.587640408904],
                           [1167541200000, 22.788453687637], [1170219600000, 22.429199073597],
                           [1172638800000, 22.324103271052], [1175313600000, 17.558388444187],
                           [1177905600000, 16.769518096208], [1180584000000, 16.214738201301],
                           [1183176000000, 18.729632971229], [1185854400000, 18.814523318847],
                           [1188532800000, 19.789986451358], [1191124800000, 17.070049054933],
                           [1193803200000, 16.121349575716], [1196398800000, 15.141659430091],
                           [1199077200000, 17.175388025297], [1201755600000, 17.286592443522],
                           [1204261200000, 16.323141626568], [1206936000000, 19.231263773952],
                           [1209528000000, 18.446256391095], [1212206400000, 17.822632399764],
                           [1214798400000, 15.53936647598], [1217476800000, 15.255131790217],
                           [1220155200000, 15.660963922592], [1222747200000, 13.254482273698],
                           [1225425600000, 11.920796202299], [1228021200000, 12.122809090924],
                           [1230699600000, 15.691026271393], [1233378000000, 14.720881635107],
                           [1235797200000, 15.387939360044], [1238472000000, 13.765436672228],
                           [1241064000000, 14.631445864799], [1243742400000, 14.292446536221],
                           [1246334400000, 16.170071367017], [1249012800000, 15.948135554337],
                           [1251691200000, 16.612872685134], [1254283200000, 18.778338719091],
                           [1256961600000, 16.756026065421], [1259557200000, 19.385804443146],
                           [1262235600000, 22.950590240168], [1264914000000, 23.61159018141],
                           [1267333200000, 25.708586989581], [1270008000000, 26.883915999885],
                           [1272600000000, 25.893486687065], [1275278400000, 24.678914263176],
                           [1277870400000, 25.937275793024], [1280548800000, 29.461381693838],
                           [1283227200000, 27.357322961861], [1285819200000, 29.057235285673],
                           [1288497600000, 28.549434189386], [1291093200000, 28.506352379724],
                           [1293771600000, 29.449241421598], [1296450000000, 25.796838168807],
                           [1298869200000, 28.740145449188], [1301544000000, 22.091744141872],
                           [1304136000000, 25.07966254541], [1306814400000, 23.674906973064],
                           [1309406400000, 23.418002742929], [1312084800000, 23.24364413887],
                           [1314763200000, 31.591854066817], [1317355200000, 31.497112374114],
                           [1320033600000, 26.67238082043], [1322629200000, 27.297080015495],
                           [1325307600000, 20.174315530051], [1327986000000, 19.631084213898],
                           [1330491600000, 20.366462219461], [1333166400000, 19.284784434185],
                           [1335758400000, 19.157810257624]]
            },

            {
                "key": "Africa",
                "values": [[1025409600000, 7.9356392949025], [1028088000000, 7.4514668527298],
                           [1030766400000, 7.9085410566608], [1033358400000, 5.8996782364764],
                           [1036040400000, 6.0591869346923], [1038632400000, 5.9667815800451],
                           [1041310800000, 8.65528925664], [1043989200000, 8.7690763386254],
                           [1046408400000, 8.6386160387453], [1049086800000, 5.9895557449743],
                           [1051675200000, 6.3840324338159], [1054353600000, 6.5196511461441],
                           [1056945600000, 7.0738618553114], [1059624000000, 6.5745957367133],
                           [1062302400000, 6.4658359184444], [1064894400000, 2.7622758754954],
                           [1067576400000, 2.9794782986241], [1070168400000, 2.8735432712019],
                           [1072846800000, 1.6344817513645], [1075525200000, 1.5869248754883],
                           [1078030800000, 1.7172279157246], [1080709200000, 1.9649927409867],
                           [1083297600000, 2.0261695079196], [1085976000000, 2.0541261923929],
                           [1088568000000, 3.9466318927569], [1091246400000, 3.7826770946089],
                           [1093924800000, 3.9543021004028], [1096516800000, 3.8309891064711],
                           [1099195200000, 3.6340958946166], [1101790800000, 3.5289755762525],
                           [1104469200000, 5.702378559857], [1107147600000, 5.6539569019223],
                           [1109566800000, 5.5449506370392], [1112245200000, 4.7579993280677],
                           [1114833600000, 4.4816139372906], [1117512000000, 4.5965558568606],
                           [1120104000000, 4.3747066116976], [1122782400000, 4.4588822917087],
                           [1125460800000, 4.4460351848286], [1128052800000, 3.7989113035136],
                           [1130734800000, 3.7743883140088], [1133326800000, 3.7727852823828],
                           [1136005200000, 7.2968111448895], [1138683600000, 7.2800122043237],
                           [1141102800000, 7.1187787503354], [1143781200000, 8.351887016482],
                           [1146369600000, 8.4156698763993], [1149048000000, 8.1673298604231],
                           [1151640000000, 5.5132447126042], [1154318400000, 6.1152537710599],
                           [1156996800000, 6.076765091942], [1159588800000, 4.6304473798646],
                           [1162270800000, 4.6301068469402], [1164862800000, 4.3466656309389],
                           [1167541200000, 6.830104897003], [1170219600000, 7.241633040029],
                           [1172638800000, 7.1432372054153], [1175313600000, 10.608942063374],
                           [1177905600000, 10.914964549494], [1180584000000, 10.933223880565],
                           [1183176000000, 8.3457524851265], [1185854400000, 8.1078413081882],
                           [1188532800000, 8.2697185922474], [1191124800000, 8.4742436475968],
                           [1193803200000, 8.4994601179319], [1196398800000, 8.7387319683243],
                           [1199077200000, 6.8829183612895], [1201755600000, 6.984133637885],
                           [1204261200000, 7.0860136043287], [1206936000000, 4.3961787956053],
                           [1209528000000, 3.8699674365231], [1212206400000, 3.6928925238305],
                           [1214798400000, 6.7571718894253], [1217476800000, 6.4367313362344],
                           [1220155200000, 6.4048441521454], [1222747200000, 5.4643833239669],
                           [1225425600000, 5.3150786833374], [1228021200000, 5.3011272612576],
                           [1230699600000, 4.1203601430809], [1233378000000, 4.0881783200525],
                           [1235797200000, 4.1928665957189], [1238472000000, 7.0249415663205],
                           [1241064000000, 7.006530880769], [1243742400000, 6.994835633224],
                           [1246334400000, 6.1220222336254], [1249012800000, 6.1177436137653],
                           [1251691200000, 6.1413396231981], [1254283200000, 4.8046006145874],
                           [1256961600000, 4.6647600660544], [1259557200000, 4.544865006255],
                           [1262235600000, 6.0488249316539], [1264914000000, 6.3188669540206],
                           [1267333200000, 6.5873958262306], [1270008000000, 6.2281189839578],
                           [1272600000000, 5.8948915746059], [1275278400000, 5.5967320482214],
                           [1277870400000, 0.99784432084837], [1280548800000, 1.0950794175359],
                           [1283227200000, 0.94479734407491], [1285819200000, 1.222093988688],
                           [1288497600000, 1.335093106856], [1291093200000, 1.3302565104985],
                           [1293771600000, 1.340824670897], [1296450000000, 0], [1298869200000, 0], [1301544000000, 0],
                           [1304136000000, 0], [1306814400000, 0], [1309406400000, 0], [1312084800000, 0],
                           [1314763200000, 0], [1317355200000, 4.4583692315], [1320033600000, 3.6493043348059],
                           [1322629200000, 3.8610064091761], [1325307600000, 5.5144800685202],
                           [1327986000000, 5.1750695220791], [1330491600000, 5.6710066952691],
                           [1333166400000, 5.5611890039181], [1335758400000, 5.5979368839939]]
            },

            {
                "key": "South America",
                "values": [[1025409600000, 7.9149900245423], [1028088000000, 7.0899888751059],
                           [1030766400000, 7.5996132380614], [1033358400000, 8.2741174301034],
                           [1036040400000, 9.3564460833513], [1038632400000, 9.7066786059904],
                           [1041310800000, 10.213363052343], [1043989200000, 10.285809585273],
                           [1046408400000, 10.222053149228], [1049086800000, 8.6188592137975],
                           [1051675200000, 9.3335447543566], [1054353600000, 8.9312402186628],
                           [1056945600000, 8.1895089343658], [1059624000000, 8.260622135079],
                           [1062302400000, 7.7700786851364], [1064894400000, 7.9907428771318],
                           [1067576400000, 8.7769091865606], [1070168400000, 8.4855077060661],
                           [1072846800000, 9.6277203033655], [1075525200000, 9.9685913452624],
                           [1078030800000, 10.615085181759], [1080709200000, 9.2902488079646],
                           [1083297600000, 8.8610439830061], [1085976000000, 9.1075344931229],
                           [1088568000000, 9.9156737639203], [1091246400000, 9.7826003238782],
                           [1093924800000, 10.55403610555], [1096516800000, 10.926900264097],
                           [1099195200000, 10.903144818736], [1101790800000, 10.862890389067],
                           [1104469200000, 10.64604998964], [1107147600000, 10.042790814087],
                           [1109566800000, 9.7173391591038], [1112245200000, 9.6122415755443],
                           [1114833600000, 9.4337921146562], [1117512000000, 9.814827171183],
                           [1120104000000, 12.059260396788], [1122782400000, 12.139649903873],
                           [1125460800000, 12.281290663822], [1128052800000, 8.8037085409056],
                           [1130734800000, 8.6300618239176], [1133326800000, 9.1225708491432],
                           [1136005200000, 12.988124170836], [1138683600000, 13.356778764353],
                           [1141102800000, 13.611196863271], [1143781200000, 6.8959030061189],
                           [1146369600000, 6.9939633271353], [1149048000000, 6.7241510257676],
                           [1151640000000, 5.5611293669517], [1154318400000, 5.6086488714041],
                           [1156996800000, 5.4962849907033], [1159588800000, 6.9193153169278],
                           [1162270800000, 7.0016334389778], [1164862800000, 6.7865422443273],
                           [1167541200000, 9.0006454225383], [1170219600000, 9.2233916171431],
                           [1172638800000, 8.8929316009479], [1175313600000, 10.345937520404],
                           [1177905600000, 10.075914677026], [1180584000000, 10.089006188111],
                           [1183176000000, 10.598330295008], [1185854400000, 9.9689546533009],
                           [1188532800000, 9.7740580198146], [1191124800000, 10.558483060626],
                           [1193803200000, 9.9314651823603], [1196398800000, 9.3997715873769],
                           [1199077200000, 8.4086493387262], [1201755600000, 8.9698309085926],
                           [1204261200000, 8.2778357995396], [1206936000000, 8.8585045600123],
                           [1209528000000, 8.7013756413322], [1212206400000, 7.7933605469443],
                           [1214798400000, 7.0236183483064], [1217476800000, 6.9873088186829],
                           [1220155200000, 6.8031713070097], [1222747200000, 6.6869531315723],
                           [1225425600000, 6.138256993963], [1228021200000, 5.6434994016354],
                           [1230699600000, 5.495220262512], [1233378000000, 4.6885326869846],
                           [1235797200000, 4.4524349883438], [1238472000000, 5.6766520778185],
                           [1241064000000, 5.7675774480752], [1243742400000, 5.7882863168337],
                           [1246334400000, 7.2666010034924], [1249012800000, 7.5191821322261],
                           [1251691200000, 7.849651451445], [1254283200000, 10.383992037985],
                           [1256961600000, 9.0653691861818], [1259557200000, 9.6705248324159],
                           [1262235600000, 10.856380561349], [1264914000000, 11.27452370892],
                           [1267333200000, 11.754156529088], [1270008000000, 8.2870811422455],
                           [1272600000000, 8.0210264360699], [1275278400000, 7.5375074474865],
                           [1277870400000, 8.3419527338039], [1280548800000, 9.4197471818443],
                           [1283227200000, 8.7321733185797], [1285819200000, 9.6627062648126],
                           [1288497600000, 10.187962234548], [1291093200000, 9.8144201733476],
                           [1293771600000, 10.275723361712], [1296450000000, 16.796066079353],
                           [1298869200000, 17.543254984075], [1301544000000, 16.673660675083],
                           [1304136000000, 17.963944353609], [1306814400000, 16.63774086721],
                           [1309406400000, 15.84857094609], [1312084800000, 14.767303362181],
                           [1314763200000, 24.778452182433], [1317355200000, 18.370353229999],
                           [1320033600000, 15.253137429099], [1322629200000, 14.989600840649],
                           [1325307600000, 16.052539160125], [1327986000000, 16.424390322793],
                           [1330491600000, 17.884020741104], [1333166400000, 18.372698836036],
                           [1335758400000, 18.315881576096]]
            },

            {
                "key": "Asia",
                "values": [[1025409600000, 13.153938631352], [1028088000000, 12.456410521864],
                           [1030766400000, 12.537048663919], [1033358400000, 13.947386398309],
                           [1036040400000, 14.421680682568], [1038632400000, 14.143238262286],
                           [1041310800000, 12.229635347478], [1043989200000, 12.508479916948],
                           [1046408400000, 12.155368409526], [1049086800000, 13.335455563994],
                           [1051675200000, 12.888210138167], [1054353600000, 12.842092790511],
                           [1056945600000, 12.513816474199], [1059624000000, 12.21453674494],
                           [1062302400000, 11.750848343935], [1064894400000, 10.526579636787],
                           [1067576400000, 10.873596086087], [1070168400000, 11.019967131519],
                           [1072846800000, 11.235789380602], [1075525200000, 11.859910850657],
                           [1078030800000, 12.531031616536], [1080709200000, 11.360451067019],
                           [1083297600000, 11.456244780202], [1085976000000, 11.436991407309],
                           [1088568000000, 11.638595744327], [1091246400000, 11.190418301469],
                           [1093924800000, 11.835608007589], [1096516800000, 11.540980244475],
                           [1099195200000, 10.958762325687], [1101790800000, 10.885791159509],
                           [1104469200000, 13.605810720109], [1107147600000, 13.128978067437],
                           [1109566800000, 13.119012086882], [1112245200000, 13.003706129783],
                           [1114833600000, 13.326996807689], [1117512000000, 13.547947991743],
                           [1120104000000, 12.807959646616], [1122782400000, 12.931763821068],
                           [1125460800000, 12.795359993008], [1128052800000, 9.6998935538319],
                           [1130734800000, 9.3473740089131], [1133326800000, 9.36902067716],
                           [1136005200000, 14.258619539875], [1138683600000, 14.21241095603],
                           [1141102800000, 13.973193618249], [1143781200000, 15.218233920664],
                           [1146369600000, 14.382109727451], [1149048000000, 13.894310878491],
                           [1151640000000, 15.593086090031], [1154318400000, 16.244839695189],
                           [1156996800000, 16.017088850647], [1159588800000, 14.183951830057],
                           [1162270800000, 14.148523245696], [1164862800000, 13.424326059971],
                           [1167541200000, 12.974450435754], [1170219600000, 13.232470418021],
                           [1172638800000, 13.318762655574], [1175313600000, 15.961407746104],
                           [1177905600000, 16.287714639805], [1180584000000, 16.24659058389],
                           [1183176000000, 17.564505594808], [1185854400000, 17.872725373164],
                           [1188532800000, 18.018998508756], [1191124800000, 15.584518016602],
                           [1193803200000, 15.480850647182], [1196398800000, 15.699120036985],
                           [1199077200000, 19.184281817226], [1201755600000, 19.691226605205],
                           [1204261200000, 18.982314051293], [1206936000000, 18.707820309008],
                           [1209528000000, 17.459630929759], [1212206400000, 16.500616076782],
                           [1214798400000, 18.086324003978], [1217476800000, 18.929464156259],
                           [1220155200000, 18.233728682084], [1222747200000, 16.315776297325],
                           [1225425600000, 14.632892190251], [1228021200000, 14.667835024479],
                           [1230699600000, 13.946993947309], [1233378000000, 14.394304684398],
                           [1235797200000, 13.724462792967], [1238472000000, 10.930879035807],
                           [1241064000000, 9.8339915513708], [1243742400000, 10.053858541872],
                           [1246334400000, 11.786998438286], [1249012800000, 11.780994901769],
                           [1251691200000, 11.305889670277], [1254283200000, 10.918452290083],
                           [1256961600000, 9.6811395055706], [1259557200000, 10.971529744038],
                           [1262235600000, 13.330210480209], [1264914000000, 14.592637568961],
                           [1267333200000, 14.605329141157], [1270008000000, 13.936853794037],
                           [1272600000000, 12.189480759072], [1275278400000, 11.676151385046],
                           [1277870400000, 13.058852800018], [1280548800000, 13.62891543203],
                           [1283227200000, 13.811107569918], [1285819200000, 13.786494560786],
                           [1288497600000, 14.045162857531], [1291093200000, 13.697412447286],
                           [1293771600000, 13.677681376221], [1296450000000, 19.96151186453],
                           [1298869200000, 21.049198298156], [1301544000000, 22.687631094009],
                           [1304136000000, 25.469010617433], [1306814400000, 24.88379943712],
                           [1309406400000, 24.203843814249], [1312084800000, 22.138760964036],
                           [1314763200000, 16.034636966228], [1317355200000, 15.394958944555],
                           [1320033600000, 12.62564246197], [1322629200000, 12.973735699739],
                           [1325307600000, 15.78601833615], [1327986000000, 15.227368020134],
                           [1330491600000, 15.899752650733], [1333166400000, 15.661317319168],
                           [1335758400000, 15.359891177281]]
            },

            {
                "key": "Europe",
                "values": [[1025409600000, 9.3433263069351], [1028088000000, 8.4583069475546],
                           [1030766400000, 8.0342398154196], [1033358400000, 8.1538966876572],
                           [1036040400000, 10.743604786849], [1038632400000, 12.349366155851],
                           [1041310800000, 10.742682503899], [1043989200000, 11.360983869935],
                           [1046408400000, 11.441336039535], [1049086800000, 10.897508791837],
                           [1051675200000, 11.469101547709], [1054353600000, 12.086311476742],
                           [1056945600000, 8.0697180773504], [1059624000000, 8.2004392233445],
                           [1062302400000, 8.4566434900643], [1064894400000, 7.9565760979059],
                           [1067576400000, 9.3764619255827], [1070168400000, 9.0747664160538],
                           [1072846800000, 10.508939004673], [1075525200000, 10.69936754483],
                           [1078030800000, 10.681562399145], [1080709200000, 13.184786109406],
                           [1083297600000, 12.668213052351], [1085976000000, 13.430509403986],
                           [1088568000000, 12.393086349213], [1091246400000, 11.942374044842],
                           [1093924800000, 12.062227685742], [1096516800000, 11.969974363623],
                           [1099195200000, 12.14374574055], [1101790800000, 12.69422821995],
                           [1104469200000, 9.1235211044692], [1107147600000, 8.758211757584],
                           [1109566800000, 8.8072309258443], [1112245200000, 11.687595946835],
                           [1114833600000, 11.079723082664], [1117512000000, 12.049712896076],
                           [1120104000000, 10.725319428684], [1122782400000, 10.844849996286],
                           [1125460800000, 10.833535488461], [1128052800000, 17.180932407865],
                           [1130734800000, 15.894764896516], [1133326800000, 16.412751299498],
                           [1136005200000, 12.573569093402], [1138683600000, 13.242301508051],
                           [1141102800000, 12.863536342041], [1143781200000, 21.034044171629],
                           [1146369600000, 21.419084618802], [1149048000000, 21.142678863692],
                           [1151640000000, 26.56848967753], [1154318400000, 24.839144939906],
                           [1156996800000, 25.456187462166], [1159588800000, 26.350164502825],
                           [1162270800000, 26.478333205189], [1164862800000, 26.425979547846],
                           [1167541200000, 28.191461582256], [1170219600000, 28.930307448808],
                           [1172638800000, 29.521413891117], [1175313600000, 28.188285966466],
                           [1177905600000, 27.704619625831], [1180584000000, 27.49086242483],
                           [1183176000000, 28.770679721286], [1185854400000, 29.06048067145],
                           [1188532800000, 28.240998844973], [1191124800000, 33.004893194128],
                           [1193803200000, 34.075180359928], [1196398800000, 32.548560664834],
                           [1199077200000, 30.629727432729], [1201755600000, 28.642858788159],
                           [1204261200000, 27.973575227843], [1206936000000, 27.393351882726],
                           [1209528000000, 28.476095288522], [1212206400000, 29.29667866426],
                           [1214798400000, 29.222333802896], [1217476800000, 28.092966093842],
                           [1220155200000, 28.107159262922], [1222747200000, 25.482974832099],
                           [1225425600000, 21.208115993834], [1228021200000, 20.295043095268],
                           [1230699600000, 15.925754618402], [1233378000000, 17.162864628346],
                           [1235797200000, 17.084345773174], [1238472000000, 22.24600710228],
                           [1241064000000, 24.530543998508], [1243742400000, 25.084184918241],
                           [1246334400000, 16.606166527359], [1249012800000, 17.239620011628],
                           [1251691200000, 17.336739127379], [1254283200000, 25.478492475754],
                           [1256961600000, 23.017152085244], [1259557200000, 25.617745423684],
                           [1262235600000, 24.061133998641], [1264914000000, 23.223933318646],
                           [1267333200000, 24.425887263936], [1270008000000, 35.501471156693],
                           [1272600000000, 33.775013878675], [1275278400000, 30.417993630285],
                           [1277870400000, 30.023598978467], [1280548800000, 33.327519522436],
                           [1283227200000, 31.963388450372], [1285819200000, 30.49896723209],
                           [1288497600000, 32.403696817913], [1291093200000, 31.47736071922],
                           [1293771600000, 31.53259666241], [1296450000000, 41.760282761548],
                           [1298869200000, 45.605771243237], [1301544000000, 39.986557966215],
                           [1304136000000, 43.84633051005], [1306814400000, 39.857316881858],
                           [1309406400000, 37.675127768207], [1312084800000, 35.775077970313],
                           [1314763200000, 48.631009702578], [1317355200000, 42.830831754505],
                           [1320033600000, 35.611502589362], [1322629200000, 35.320136981738],
                           [1325307600000, 31.564136901516], [1327986000000, 32.074407502433],
                           [1330491600000, 35.053013769977], [1333166400000, 33.873085184128],
                           [1335758400000, 32.321039427046]]
            },

            {
                "key": "Australia",
                "values": [[1025409600000, 5.1162447683392], [1028088000000, 4.2022848306513],
                           [1030766400000, 4.3543715758736], [1033358400000, 5.4641223667245],
                           [1036040400000, 6.0041275884577], [1038632400000, 6.6050520064486],
                           [1041310800000, 5.0154059912793], [1043989200000, 5.1835708554647],
                           [1046408400000, 5.1142682006164], [1049086800000, 5.0271381717695],
                           [1051675200000, 5.3437782653456], [1054353600000, 5.2105844515767],
                           [1056945600000, 6.552565997799], [1059624000000, 6.9873363581831],
                           [1062302400000, 7.010986789097], [1064894400000, 4.4254242025515],
                           [1067576400000, 4.9613848042174], [1070168400000, 4.8854920484764],
                           [1072846800000, 4.0441111794228], [1075525200000, 4.0219596813179],
                           [1078030800000, 4.3065749225355], [1080709200000, 3.9148434915404],
                           [1083297600000, 3.8659430654512], [1085976000000, 3.9572824600686],
                           [1088568000000, 4.7372190641522], [1091246400000, 4.6871476374455],
                           [1093924800000, 5.0398702564196], [1096516800000, 5.5221787544964],
                           [1099195200000, 5.424646299798], [1101790800000, 5.9240223067349],
                           [1104469200000, 5.9936860983601], [1107147600000, 5.8499523215019],
                           [1109566800000, 6.4149040329325], [1112245200000, 6.4547895561969],
                           [1114833600000, 5.9385382611161], [1117512000000, 6.0486751030592],
                           [1120104000000, 5.23108613838], [1122782400000, 5.5857797121029],
                           [1125460800000, 5.3454665096987], [1128052800000, 5.0439154120119],
                           [1130734800000, 5.054634702913], [1133326800000, 5.3819451380848],
                           [1136005200000, 5.2638869269803], [1138683600000, 5.5806167415681],
                           [1141102800000, 5.4539047069985], [1143781200000, 7.6728842432362],
                           [1146369600000, 7.719946716654], [1149048000000, 8.0144619912942],
                           [1151640000000, 7.942223133434], [1154318400000, 8.3998279827444],
                           [1156996800000, 8.532324572605], [1159588800000, 4.7324285199763],
                           [1162270800000, 4.7402397487697], [1164862800000, 4.9042069355168],
                           [1167541200000, 5.9583963430882], [1170219600000, 6.3693899239171],
                           [1172638800000, 6.261153903813], [1175313600000, 5.3443942184584],
                           [1177905600000, 5.4932111235361], [1180584000000, 5.5747393101109],
                           [1183176000000, 5.3833633060013], [1185854400000, 5.5125898831832],
                           [1188532800000, 5.8116112661327], [1191124800000, 4.3962296939996],
                           [1193803200000, 4.6967663605521], [1196398800000, 4.7963004350914],
                           [1199077200000, 4.1817985183351], [1201755600000, 4.3797643870182],
                           [1204261200000, 4.6966642197965], [1206936000000, 4.3609995132565],
                           [1209528000000, 4.4736290996496], [1212206400000, 4.3749762738128],
                           [1214798400000, 3.3274661194507], [1217476800000, 3.0316184691337],
                           [1220155200000, 2.5718140204728], [1222747200000, 2.7034994044603],
                           [1225425600000, 2.2033786591364], [1228021200000, 1.9850621240805], [1230699600000, 0],
                           [1233378000000, 0], [1235797200000, 0], [1238472000000, 0], [1241064000000, 0],
                           [1243742400000, 0], [1246334400000, 0], [1249012800000, 0], [1251691200000, 0],
                           [1254283200000, 0.44495950017788], [1256961600000, 0.33945469262483],
                           [1259557200000, 0.38348269455195], [1262235600000, 0], [1264914000000, 0],
                           [1267333200000, 0], [1270008000000, 0], [1272600000000, 0], [1275278400000, 0],
                           [1277870400000, 0], [1280548800000, 0], [1283227200000, 0], [1285819200000, 0],
                           [1288497600000, 0], [1291093200000, 0], [1293771600000, 0],
                           [1296450000000, 0.52216435716176], [1298869200000, 0.59275786698454], [1301544000000, 0],
                           [1304136000000, 0], [1306814400000, 0], [1309406400000, 0], [1312084800000, 0],
                           [1314763200000, 0], [1317355200000, 0], [1320033600000, 0], [1322629200000, 0],
                           [1325307600000, 0], [1327986000000, 0], [1330491600000, 0], [1333166400000, 0],
                           [1335758400000, 0]]
            },

            {
                "key": "Antarctica",
                "values": [[1025409600000, 1.3503144674343], [1028088000000, 1.2232741112434],
                           [1030766400000, 1.3930470790784], [1033358400000, 1.2631275030593],
                           [1036040400000, 1.5842699103708], [1038632400000, 1.9546996043116],
                           [1041310800000, 0.8504048300986], [1043989200000, 0.85340686311353],
                           [1046408400000, 0.843061357391], [1049086800000, 2.119846992476],
                           [1051675200000, 2.5285382124858], [1054353600000, 2.5056570712835],
                           [1056945600000, 2.5212789901005], [1059624000000, 2.6192011642534],
                           [1062302400000, 2.5382187823805], [1064894400000, 2.3393223047168],
                           [1067576400000, 2.491219888698], [1070168400000, 2.497555874906],
                           [1072846800000, 1.734018115546], [1075525200000, 1.9307268299646],
                           [1078030800000, 2.2261679836799], [1080709200000, 1.7608893704206],
                           [1083297600000, 1.6242690616808], [1085976000000, 1.7161663801295],
                           [1088568000000, 1.7183554537038], [1091246400000, 1.7179780759145],
                           [1093924800000, 1.7314274801784], [1096516800000, 1.2596883356752],
                           [1099195200000, 1.381177053009], [1101790800000, 1.4408819615814],
                           [1104469200000, 3.4743581836444], [1107147600000, 3.3603749903192],
                           [1109566800000, 3.5350883257893], [1112245200000, 3.0949644237828],
                           [1114833600000, 3.0796455899995], [1117512000000, 3.3441247640644],
                           [1120104000000, 4.0947643978168], [1122782400000, 4.4072631274052],
                           [1125460800000, 4.4870979780825], [1128052800000, 4.8404549457934],
                           [1130734800000, 4.8293016233697], [1133326800000, 5.2238093263952],
                           [1136005200000, 3.382306337815], [1138683600000, 3.7056975170243],
                           [1141102800000, 3.7561118692318], [1143781200000, 2.861913700854],
                           [1146369600000, 2.9933744103381], [1149048000000, 2.7127537218463],
                           [1151640000000, 3.1195497076283], [1154318400000, 3.4066964004508],
                           [1156996800000, 3.3754571113569], [1159588800000, 2.2965579982924],
                           [1162270800000, 2.4486818633018], [1164862800000, 2.4002308848517],
                           [1167541200000, 1.9649579750349], [1170219600000, 1.9385263638056],
                           [1172638800000, 1.9128975336387], [1175313600000, 2.3412869836298],
                           [1177905600000, 2.4337870351445], [1180584000000, 2.62179703171],
                           [1183176000000, 3.2642864957929], [1185854400000, 3.3200396223709],
                           [1188532800000, 3.3934212707572], [1191124800000, 4.2822327088179],
                           [1193803200000, 4.1474964228541], [1196398800000, 4.1477082879801],
                           [1199077200000, 5.2947122916128], [1201755600000, 5.2919843508028],
                           [1204261200000, 5.198978305031], [1206936000000, 3.5603057673513],
                           [1209528000000, 3.3009087690692], [1212206400000, 3.1784852603792],
                           [1214798400000, 4.5889503538868], [1217476800000, 4.401779617494],
                           [1220155200000, 4.2208301828278], [1222747200000, 3.89396671475],
                           [1225425600000, 3.0423832241354], [1228021200000, 3.135520611578],
                           [1230699600000, 1.9631418164089], [1233378000000, 1.8963543874958],
                           [1235797200000, 1.8266636017025], [1238472000000, 0.93136635895188],
                           [1241064000000, 0.92737801918888], [1243742400000, 0.97591889805002],
                           [1246334400000, 2.6841193805515], [1249012800000, 2.5664341140531],
                           [1251691200000, 2.3887523699873], [1254283200000, 1.1737801663681],
                           [1256961600000, 1.0953582317281], [1259557200000, 1.2495674976653],
                           [1262235600000, 0.36607452464754], [1264914000000, 0.3548719047291],
                           [1267333200000, 0.36769242398939], [1270008000000, 0], [1272600000000, 0],
                           [1275278400000, 0], [1277870400000, 0], [1280548800000, 0], [1283227200000, 0],
                           [1285819200000, 0.85450741275337], [1288497600000, 0.91360317921637],
                           [1291093200000, 0.89647678692269], [1293771600000, 0.87800687192639], [1296450000000, 0],
                           [1298869200000, 0], [1301544000000, 0.43668720882994], [1304136000000, 0.4756523602692],
                           [1306814400000, 0.46947368328469], [1309406400000, 0.45138896152316],
                           [1312084800000, 0.43828726648117], [1314763200000, 2.0820861395316],
                           [1317355200000, 0.9364411075395], [1320033600000, 0.60583907839773],
                           [1322629200000, 0.61096950747437], [1325307600000, 0], [1327986000000, 0],
                           [1330491600000, 0], [1333166400000, 0], [1335758400000, 0]]
            }

        ]


class OOChartLine(OOChartNVD3):
    OOChartNVD3.OOCHART_CLASSES['line'] = __qualname__

    @classmethod
    def test_request_data(cls):
        return 'line'


class OOChartScatterBubble(OOChartNVD3):
    OOChartNVD3.OOCHART_CLASSES['sbubble'] = __qualname__

    @classmethod
    def test_request_data(cls):

        groups = 4
        points = 40
        data = []
        shapes = ['circle', 'cross', 'triangle-up', 'triangle-down', 'diamond', 'square']
        random_ = np.random.normal

        for i in range(groups):
            data.append({
                'key': 'Group ' + str(i),
                'values': []
            })

            for j in range(points):
                data[i]['values'].append({
                    'x': random_(),
                    'y': random_(),
                    'size': random.random()
                })

        return data


class OOChartMultiBar(OOChartNVD3):
    OOChartNVD3.OOCHART_CLASSES['mbar'] = __qualname__

    @classmethod
    def example_data(cls):

        '''
        data = []
        for stream in range(random.randint(2, 5)):
            data.append({
                'key': 'stream' + str(stream),
                'values': []
            })
            for value in range(random.randint(40, 100)):
                data[-1]['values'].append({
                    'x': str(value),
                    'y': random.random()
                })
        return data
        '''
        ls_data = cls.stream_layers(3, 10+random.random()*100, .1)
        data = [{'key': 'stream'+str(i), 'values': data} for i, data in enumerate(ls_data)]
        return data


    @classmethod
    def test_request_data(cls):
        return cls.example_data()


class OOChartBullet(OOChartNVD3):
    OOChartNVD3.OOCHART_CLASSES['bullet'] = __qualname__

    @classmethod
    def test_request_data(cls):
        return {
          "title": "Revenue",
          "subtitle": "US$, in thousands",
          "ranges": [150,225,300],
          "measures": [220],
          "markers": [250]
        }


class OOGeneralSelector(OOGeneralSelectorTest, WebBtnGroup):
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
            'button': {'name': '', 'select': '', 'options': []},
            'option': {'name': '', 'href': '#'}
        }

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

    @classmethod
    def test_request(cls, methods=['GET']):

        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def place_components_impl(self):
                page = self
                testing_class = page.testing_class
                WebRow = page._SUBCLASSES['WebRow']['class']
                WebColumn = page._SUBCLASSES['WebColumn']['class']
                WebBr = page._SUBCLASSES['WebBr']['class']
                WebBtn = page._SUBCLASSES['WebBtn']['class']

                with page.add_child(WebRow()) as r1:
                    with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c1:
                        with c1.add_child(
                                testing_class(styles={'display': 'flex'},
                                              name=testing_class.testing_cls_name)) as gs1:
                            pass
                with page.add_child(WebBr()) as br1:
                    pass

                with page.add_child(WebRow()) as r3:
                    with r3.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c3:
                        with c3.add_child(WebBtn(value='select值', name='test_btn')) as val_btn:
                            pass

            def intro_events_impl(self):
                page = self
                gs1 = page._components['OOGeneralSelector']['obj']
                val_btn = page._components['test_btn']['obj']
                LVar = page._SUBCLASSES['LVar']['class']

                with gs1.on_event_w('change'):
                    page.alert('"Please check console output on server side, should find \'Got gselector menu:xxx\'"')
                    with page.render_post_w():
                        gs1.render_for_post()

                # Test getting select values of OOGeneralSelector
                with val_btn.on_event_w('click'):
                    with LVar(parent=gs1, var_name='gs1_value') as gs1_val:
                        gs1.val()
                    gs1.alert(
                        'gs1_value[0].select + " " + gs1_value[1].select + " " + gs1_value[2].select + " " + gs1_value[3].select')

                with page.render_post_w():
                    gs1.render_for_post()

            def process_events_impl(self,req):
                page = self._page
                OOGeneralSelector = page._SUBCLASSES['OOGeneralSelector']['class']
                r = req
                if 'data' not in r:
                    r['data'] = OOGeneralSelector._example_data()
                for d in r['data']:
                    if not d['options']:
                        option1 = copy.deepcopy(OOGeneralSelector.data_format()['option'])
                        option1['name'] = d['name'] + '_option1' if 'name' in d else d['select'] + 'option1'
                        option2 = copy.deepcopy(OOGeneralSelector.data_format()['option'])
                        option2['name'] = d['name'] + '_option2' if 'name' in d else d['select'] + 'option1'
                        d['options'].append(option1)
                        d['options'].append(option2)

                        d['name'] = option1['name']
                        d['select'] = option1['name']
                    else:
                        print('Got gselector menu:{}'.format(d['select']))

        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class OOBanner(OOBannerTest, WebDiv):

    CAROUSEL_HTML = '''
                <ol class="carousel-indicators">
                  {% for _ in banner.imgs %}
                    {% if loop.index == 1 %}
                      <li data-target="#{{banner.id | safe}}" data-slide-to="{{loop.counter | safe}}" class="active"></li>
                    {% else %}
                      <li data-target="#{{banner.id | safe}}" data-slide-to="{{loop.counter | safe}}"></li>
                    {% endif %}
                  {% endfor %}
                </ol>
                <div class="carousel-inner" >
                  {% for img in banner.imgs %}
                    {% if loop.index == 1 %}
                      <div class="item active">
                    {% else %}
                      <div class="item">
                    {% endif %}
                        <a href='{{img.url | safe}}'>
                          <img src="{{url_for('static',filename=img.file) | safe}}" alt="" onload={{banner.draw_img}}(this,"{{banner.height}}")>
                        </a>
                        <div class='carousel-caption'>
                          <h4 class='alpha'>
                            <a style='color:white;' href="{{img.url}}">{{img.title | safe}}</a>
                          </h4>
                        </div>
                      </div>
                  {% endfor %}
                </div>
                <a class="left carousel-control" href="#{{banner.id}}" role="button" data-slide="prev">
                  <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></spa n>
                  <span class="sr-only">Previous</span>
                </a>
                <a class="right carousel-control" href="#{{banner.id | safe}}" role="button" data-slide="next">
                  <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
                  <span class="sr-only">Next</span>
                </a>
        '''

    VAL_FUNC_NAME = 'oobanner_val'

    def __init__(self, imgs=None, height="300px", interval=3000, **kwargs):
        kwargs['imgs'] = imgs
        kwargs['height'] = height
        kwargs['interval'] = interval
        super().__init__(**kwargs)

    def _get_banner(self):
        imgs = [
                {'file': 'img/carousel_demo1.jpg', 'title': '', 'href': '#'},
                {'file': 'img/carousel_demo2.jpg', 'title': '', 'href': '#'},
                {'file': 'img/carousel_demo3.jpg', 'title': '', 'href': '#'},
            ]

        height = '400px' if not hasattr(self, '_height') else self._height

        return {'id': self.id(), 'imgs': imgs, 'draw_img': self.DRAW_IMG_FUNC_NAME, 'height': height}

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def process_events_impl(self, req):
                print('Class testing, class {} got req:{}'.format(self.__class__.__name__, req['data']))
                banner = self._get_banner()
                new_html = render_template_string(self.CAROUSEL_HTML,
                                                  banner=banner)
                req['data']['html'] = new_html

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class OOCalendar(OOCalendarTest, WebDiv):

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
    VAL_FUNC_ARGS = ['that', 'data=null','trigger_event=false']

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
            _from = dt.datetime.fromtimestamp(float(_from) / 1000.0)
        _to = request.args.get('to')
        if _to:
            _to = dt.datetime.fromtimestamp(float(_to) / 1000.0)
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
        super().add_url_rule(app, extend)
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
    def load_events(cls):
        return cls._example_data()

    @classmethod
    def on_post(cls, r):

        ret = None
        if r['me'] == cls.LOAD_EVENTS_KEY:
            """
            The extra info like hierarchy, set by page.on_post.CALENDAR_NAME, like 
            r['data']['hierarchy'] = hierarchy, and get the extra data info here, by
            hierarchy = '' if not r['data']['extra'] else r['data']['extra']
            """
            test = '' if not r['data']['extra'] else r['data']['extra']
            print('OOCalendar.on_post.LOAD_EVENTS, test:' + test)

            ret = cls.load_events()

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
    def on_post_builtin(cls, r):

        if r['me'] == cls.LOAD_EVENTS_KEY:
            test = '' if not r['data']['extra'] else r['data']['extra']
            print('OOCalendar.on_post.LOAD_EVENTS, test:' + test)
            r['data'] = cls._example_data()
        elif r['me'] == cls.TEMLATE_WEEK_KEY:
            r['data'] = cls._week()
        elif r['me'] == cls.TEMPLATE_WEEK_DAYS_KEY:
            r['data'] = cls._week_day()
        elif r['me'] == cls.TEMPLATE_DAY_KEY:
            r['data'] = cls._day()
        elif r['me'] == cls.TEMPLATE_MONTH_KEY:
            r['data'] = cls._month()
        elif r['me'] == cls.TEMPLATE_MONTH_DAY_KEY:
            r['data'] = cls._month_day()
        elif r['me'] == cls.TEMPLATE_YEAR_KEY:
            r['data'] = cls._year()
        elif r['me'] == cls.TEMPLATE_YEAR_MONTH_KEY:
            r['data'] = cls._year_month()
        elif r['me'] == cls.TEMPLATE_EVENT_LIST_KEY:
            r['data'] = cls._event_list()

        return r

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            TestName = 'OOCalendarTest'
            TestTitleName = 'OOCalendarTitleTest'

            def place_components_impl(self):
                page = self
                this_class = OOCalendar
                with page.add_child(WebRow()) as r0:
                    with r0.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c0:
                        with c0.add_child(WebHead2(name=self.TestTitleName)) as title:
                            pass
                with page.add_child(WebRow()) as r1:
                    with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c1:
                        with c1.add_child(OOCalendarBar()) as bar:
                            pass
                with page.add_child(WebRow()) as r2:
                    with r2.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c2:
                        with c2.add_child(this_class(name=self.TestName,
                                                     url='/test_' + this_class.__name__ + '_request')) as calendar:
                            pass
                with page.add_child(WebBr()):
                    pass

            def intro_events_impl(self):
                page = self
                title = page._components[self.TestTitleName]['obj']
                calendar = page._components[self.TestName]['obj']

                with page.render_post_w():
                    calendar.render_for_post()
                    title.render_for_post()

                with calendar.on_event_w('change'):
                    calendar.alert('"Calendar changed!"')
                    with page.render_post_w():
                        calendar.render_for_post()
                        title.render_for_post()

            def on_my_render_impl(self, req):

                #req_ = self.on_post()
                req_ = req

                title_ = '时间标题'
                for r in req_:
                    if r['me'] == self.TestName:

                        start_ = datetime.datetime.fromtimestamp(int(r['data']['start']) / 1000)
                        end_ = datetime.datetime.fromtimestamp(int(r['data']['end']) / 1000)
                        title_ = r['data']['title']
                        view_ = r['data']['view']
                        r['data']['hierarchy'] = "test_hierarchy"

                    elif r['me'] == self.TestTitleName:

                        r['data'] = {'text': title_}

                    elif r['me'].find(OOCalendar.ME_PRE) == 0:

                        # Return data   directly, for the OOCalendar buildin requests,
                        #   needn't {'me':xxx, 'data':xxx} anymore

                        req_ = OOCalendar.on_post_builtin(r)['data']
                        break

                return jsonify({'status': 'success', 'data': req_})

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class OOCalendarBar(WebDiv):
    pass


class WebTabItem(WebDiv):
    pass


class WebTab(WebUl):

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            tab_name = 'WebTabTest'
            tab_contain_name = 'tab_contain_test'
            tab_item1_name = 'tab_item1'
            tab_item2_name = 'tab_item2'
            tab_item3_name = 'tab_item3'
            tab_contain1_name = 'tab_contain1'
            tab_contain2_name = 'tab_contain2'
            tab_contain3_name = 'tab_contain3'

            def place_components_impl(self):
                page = self
                testing_class = WebTab
                cls = testing_class

                WebRow = page._SUBCLASSES['WebRow']['class']
                WebColumn = page._SUBCLASSES['WebColumn']['class']
                WebTabContain = page._SUBCLASSES['WebTabContain']['class']
                WebTabItem = page._SUBCLASSES['WebTabItem']['class']
                WebHead3 = page._SUBCLASSES['WebHead3']['class']
                with page.add_child(WebRow()) as r1:
                    with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='200px')) as c1:
                        with c1.add_child(cls(parent=page, name=self.tab_name, ul_list=[
                            {'name': self.tab_item1_name, 'href': '#' + self.tab_item1_name},
                            {'name': self.tab_item2_name, 'href': '#' + self.tab_item2_name},
                            {'name': self.tab_item3_name, 'href': '#' + self.tab_item3_name, 'active': True},
                        ])) as test:
                            pass
                        with c1.add_child(WebTabContain(parent=page, name=self.tab_contain_name)) as contain:
                            with contain.add_child(WebTabItem(id=self.tab_item1_name, name=self.tab_item1_name)) as item1:
                                with item1.add_child(
                                        WebHead3(name=self.tab_contain1_name, value=self.tab_contain1_name)) as contain1:
                                    pass
                            with contain.add_child(WebTabItem(id=self.tab_item2_name, name=self.tab_item2_name)) as item2:
                                with item2.add_child(
                                        WebHead3(name=self.tab_contain2_name, value=self.tab_contain2_name)) as contain2:
                                    pass
                            with contain.add_child(
                                    WebTabItem(id=self.tab_item3_name, name=self.tab_item3_name, ootype=['active'])) as item3:
                                with item3.add_child(
                                        WebHead3(name=self.tab_contain3_name, value=self.tab_contain3_name)) as contain3:
                                    pass

            def intro_events_impl(self):

                page = self
                testing_class = WebTab
                '''
                testing_cls_name = page.testing_class.testing_cls_name if hasattr(testing_class, 'testing_cls_name') else \
                    testing_class.__name__
                '''
                test = page._components[self.tab_name]['obj']
                contain = page._components[self.tab_contain_name]['obj']

                with page.render_post_w():
                    test.render_for_post()
                    contain.render_for_post()

                with test.on_event_w(event='active_change'):
                    with page.render_post_w():
                        test.render_for_post()
                        contain.render_for_post()

            def on_my_render_impl(self, req):

                '''
                req = None
                if hasattr(self._page, '_action'):
                    req = self._page._action.on_post()
                else:
                    req = self._page.on_post()
                '''

                for r in req:
                    if r['me'] == self.tab_name:
                        print('Got tab active item: {}'.format(r['data']))
                        r['data'] = self.tab_item2_name
                    if r['me'] == self.tab_contain_name:
                        print('Got tab contain active page: {}'.format(r['data']))
                        r['data'] = self.tab_item2_name
                return jsonify({'status': 'success', 'data': req})

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class WebTabContain(WebDiv):
    pass


class WebTable(WebTableTest, WebComponentBootstrap):
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

    VAL_FUNC_NAME = 'webtable_val'
    VAL_FUNC_ARGS = ['that', 'data=null', 'trigger_event=false']

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
        if hasattr(cls, '_body_classes') and cls._body_classes:
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
    def html(cls, data=None, head_class=None, head_style=None):

        if not data:
            return None
        else:
            _data = data

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

            return colspan, sub_max_levels + 1

        def _head_rowspan(head, max_levels):

            if 'subhead' not in head or not head['subhead']:
                if max_levels > 1:
                    if 'attr' not in head:
                        head['attr'] = ''
                    head['attr'] = head['attr'] + ' rowspan="{}" '.format(max_levels)
                return
            else:
                assert (max_levels > 1)
                for sh in head['subhead']:
                    _head_rowspan(sh, max_levels - 1)

        def _head_matrix(head, matrix, index):
            attr = head['attr'] if 'attr' in head else ''
            style = head['style'] if 'style' in head else ''
            type = head['type'] if 'type' in head else ''
            classes = head['class'] if 'class' in head else ''
            if len(matrix) <= index:
                for i in range(len(matrix), index + 1):
                    matrix.append([])
            if matrix[index]:
                matrix[index].append(
                    {'name': head['name'], 'class': classes, 'attr': attr, 'style': style, 'type': type})
            else:
                matrix[index] = [{'name': head['name'], 'class': classes, 'attr': attr, 'style': style, 'type': type}]
            if 'subhead' in head and head['subhead']:
                if len(matrix) <= index + 1:
                    matrix.append([])
                for sh in head['subhead']:
                    _head_matrix(sh, matrix, index + 1)

        def _columns(matrix, matrix_index, columns, max_cs):
            columns_count = 0
            for th in matrix[matrix_index]:
                if th['attr'].find('colspan') >= 0:
                    th_attr = th['attr'].split(' ')
                    for attr in th_attr:
                        if attr.find('colspan') >= 0:
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
                _head_rowspan(h, max_level)

            matrix = []
            for h in schema:
                _head_matrix(h, matrix, 0)

            for tr in matrix:
                # html.append('    <tr class="{}" style="{}">\n'.format(self._head_classes_str(), self._head_styles_str()))
                html.append(
                    '    <tr class="{}" style="{}">\n'.format(head_class, head_style))
                for th in tr:
                    html.append(
                        '        <th class="{}" style="{}" {}><div>{}</div></th>\n'.format(th['class'], th['style'],
                                                                                           th['attr'], th['name']))
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
                data_ = d['data'] if 'data' in d and d['data'] else ''
                if columns and 'type' in columns[i] and columns[i]['type']:
                    if columns[i]['type'].find('checkbox') == 0:
                        if data_:
                            td = '        <input type="checkbox" checked="checked" class="{}" style="{}" {}>'.format(classes, style, attr)
                        else:
                            td = '        <input type="checkbox" class="{}" style="{}" {}>'.format(classes, style, attr)
                    else:
                        raise NotImplementedError
                else:
                    td = data_
                html.append('<td class="{}" style="{}" {} >{}</td>'.format(classes, style, attr, td))
            html.append('    </tr>\n')
        html.append('</tbody>\n')

        return html

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            @classmethod
            def example_data(cls, tbl_cls=WebTable, schema_only=False):
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

                cols = [
                    {'name': '事件', 'style': 'width:30%', 'attr': ''},
                    {'name': '审批', 'style': 'width:20%', 'attr': '', 'type': 'checkbox'},
                    {'name': '完成', 'style': '', 'attr': '', 'type': 'checkbox'},
                    {'name': '审核', 'style': '', 'attr': '', 'type': 'checkbox'},
                    {'name': '开始', 'style': '', 'attr': ''},
                    {'name': '结束', 'style': '', 'attr': ''},
                    {'name': '备份', 'style': '', 'attr': ''},
                ]

                schema = [
                    {'name': '标题', 'class': 'text-center', 'subhead': cols}
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
                            {'data': _getStr(random.randint(3, 6)),
                             'attr': 'nowrap data-ootable-details="This is event name"'},
                            {'data': approve, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                            {'data': done, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                            {'data': check, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                            {'data': start, 'attr': 'data-ootable-details="This is start date time"'},
                            {'data': end, 'attr': 'data-ootable-details="This is end date time"'},
                            {'data': _getStr(random.randint(10, 128)), 'attr': 'data-ootable-details="This is details"'}
                        )
                    )

                return ' '.join(tbl_cls.html(data))

            def place_components_impl(self):
                page = self

                testing_class = page.testing_class
                cls = page.testing_class

                WebRow = page._SUBCLASSES['WebRow']['class']
                WebColumn = page._SUBCLASSES['WebColumn']['class']
                WebTable = page._SUBCLASSES['WebTable']['class']
                with page.add_child(WebRow()) as r1:
                    with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='400px')) as c1:
                        with c1.add_child(WebTable(parent=page, name=testing_class.testing_cls_name)) as test:
                            pass

            def intro_events_impl(self):
                page = self
                testing_cls_name = page.testing_class.testing_cls_name
                test = page._components[testing_cls_name]['obj']

                with page.render_post_w():
                    test.render_for_post()

            def on_my_render_impl(self, req):
                WebPage = self._PAGE_CLASS
                test_obj = self._page._components['WebTable']['obj']
                '''
                req = None
                if hasattr(self._page, '_action'):
                    req = self._page._action.on_post()
                else:
                    req = self._page.on_post()
                '''
                for r in req:
                    if r['me'] == 'WebTable':
                        print('Got WebTable request data: {}'.format(r['data']))
                        r['data'] = {'html': self.example_data()}

                return jsonify({'status': 'success', 'data': req})

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class OOTable(OOTableTest, WebTable):

    SETTING = {}
    HTML_URL = '/ootable/ootable_html'

    RENDER_IMG_KEY = 'render_img'
    RENDER_CHART_KEY = 'render_chart'

    VAL_FUNC_NAME = 'ootable_val'
    VAL_FUNC_ARGS = ['that', 'data', 'trigger_event=false']

    RENDER_FUNC_NAME = 'ootable_rander'
    # RENDER_FUNC_ARGS = ['id', 'html', 'setting']
    RENDER_FUNC_ARGS = ['id', 'data']

    COLREORDER_FUNC_NAME = 'ootable_colreorder'
    COLREORDER_FUNC_ARGS = ['id', 'order']

    GET_ROW_DATA_FUNC_NAME = 'ootable_get_row_data'
    GET_ROW_DATA_FUNC_ARGS = ['that', 'data_attr="ootable-details"']

    ON_CLICK_ROW_FUNC_NAME = 'on_click_row'
    ON_CLICK_ROW_FUNC_ARGS = ['that', 'data']
    ON_CLICK_ROW_FUNC_BODY = (
        "\n",
    )

    ROW_INFO_FUNC_NAME = 'ootable_row_info'
    ROW_INFO_FUNC_ARGS = ['those', 'data=null']

    ROW_CHILD_FUNC_NAME = 'ootable_row_child'
    ROW_CHILD_FUNC_ARGS = ['tr', 'table_id', 'data_attr="ootable-details"']

    ROW_CHILD_FORMAT_FUNC_NAME = 'ootable_row_child_format'
    # ROW_CHILD_FORMAT_FUNC_ARGS = ['tr', 'data']
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

    ON_EXPAND_ROW_FUNC_NAME = 'on_expand_row'
    ON_EXPAND_ROW_FUNC_ARGS = ['index', 'row', '$detail']
    ON_EXPAND_ROW_FUNC_BODY = (
        "alert('on_expand_row_name!');\n",
    )

    CELL_RENDER_FUNC_NAME = 'ootable_cell_render'
    CELL_RENDER_FUNC_ARGS = ['data', 'type', 'row', 'meta']
    CELL_RENDER_FUNC_BODY = (
        "if(data.indexOf('!@#render_img!@#:')==0){\n".replace('!@#render_img!@#', RENDER_IMG_KEY),
        "    return \"<img width='100px' onload=webcomponent_draw_img(this,'60px') src='\"+data.substr('!@#render_img!@#:'.length)+\"'/>\";\n".replace(
            '!@#render_img!@#', RENDER_IMG_KEY),
        "};\n"
        "return data;\n",
    )

    CREATED_CELL_RENDER_FUNC_NAME = 'ootable_created_cell_render'
    CREATED_CELL_RENDER_FUNC_ARGS = ['td', 'cellData', 'rowData', 'row', 'col']
    CREATED_CELL_RENDER_FUNC_BODY = (
        "if(cellData.indexOf('!@#render_chart!@#:')==0){\n".replace('!@#render_chart!@#', RENDER_CHART_KEY),
        "    let content = cellData.substr('!@#render_chart!@#:'.length);\n".replace('!@#render_chart!@#',
                                                                                     RENDER_CHART_KEY),
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
                    {'data': "!@#render_img!@#:".\
                        replace('!@#render_img!@#', OOTable.RENDER_IMG_KEY) + url_for('static', filename='img/demo.jpg')},
                    {'data': _getStr(random.randint(3, 6))},
                    {'data': _getStr(random.randint(3, 6))}
                ))
            setting = {
                'scrollY': '500px',
                'scrollX': True,
                'scrollCollapse': True,
                'paging': False,
                'searching': False,
                'destroy': True,
                'colReorder': False,
                'columnDefs': [],
            }
            return {'schema': schema, 'records': records, 'setting': setting}

        def example_data_chart(self):
            schema = [
                {'name': ''},
                {'name': ''},
                {'name': ''}
            ]
            records = []
            for _ in range(10):
                records.append((
                    {'data': ("!@#render_chart!@#:" + "mbar;oochart_multibar_example_data").replace(
                        '!@#render_chart!@#', OOTable.RENDER_CHART_KEY)},
                    {'data': _getStr(random.randint(3, 6))},
                    {'data': _getStr(random.randint(3, 6))}
                ))
            setting = {
                'scrollY': '400px',
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
                data = WebTable._example_data()
                data['setting'] = {
                    'scrollY': '600px',
                    'scrollX': True,
                    'scrollCollapse': True,
                    'paging': False,
                    'searching': False,
                    'destroy': True,
                    'colReorder': False,
                    'columnDefs': [],
                    'border': True
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
        # self._html_url = html_url

    def col_reorder(self, order):
        params = {'order': order}
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
            'destroy': True,
            'colReorder': True
        }

    def get_data(self, setting_only=False):
        data = super().get_data()
        if not data:
            return None
        if setting_only:
            return data['setting']
        return {'schema': data['schema'], 'records': data['records']}

    def row_render_for_post(self, trigger_event=False):
        params = {'trigger_event': trigger_event}
        return self.func_call(params)

    def __enter__(self):
        ret = super().__enter__()

        with ooccd.MetisTransform.transform_w(self, ooccd.ACTION_MEMBER):
            self.declare_custom_global_func(self.ROW_CHILD_FORMAT_FUNC_NAME, self.ROW_CHILD_FORMAT_FUNC_ARGS,
                                            self.ROW_CHILD_FORMAT_FUNC_BODY)
            self.declare_custom_global_func(self.CELL_RENDER_FUNC_NAME, self.CELL_RENDER_FUNC_ARGS,
                                            self.CELL_RENDER_FUNC_BODY)
            self.declare_custom_global_func(self.CREATED_CELL_RENDER_FUNC_NAME, self.CREATED_CELL_RENDER_FUNC_ARGS,
                                            self.CREATED_CELL_RENDER_FUNC_BODY)
            self.declare_custom_global_func(fname=self.ON_CLICK_ROW_FUNC_NAME, fparams=self.ON_CLICK_ROW_FUNC_ARGS, fbody=self.ON_CLICK_ROW_FUNC_BODY)

        return self

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            TEST_NAME1 = 'test_table_1'
            TEST_NAME2 = 'test_table_2'
            TEST_NAME3 = 'test_table_3'

            @classmethod
            def example_data_old(cls, tbl_cls=WebTable, schema_only=False):
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

                cols = [
                    {'name': '事件', 'style': 'width:30%', 'attr': ''},
                    {'name': '审批', 'style': 'width:20%', 'attr': '', 'type': 'checkbox'},
                    {'name': '完成', 'style': '', 'attr': '', 'type': 'checkbox'},
                    {'name': '审核', 'style': '', 'attr': '', 'type': 'checkbox'},
                    {'name': '开始', 'style': '', 'attr': ''},
                    {'name': '结束', 'style': '', 'attr': ''},
                    {'name': '备份', 'style': '', 'attr': ''},
                ]

                schema = [
                    {'name': '标题', 'class': 'text-center', 'subhead': cols}
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
                            {'data': _getStr(random.randint(3, 6)),
                             'attr': 'nowrap data-ootable-details="This is event name"'},
                            {'data': approve, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                            {'data': done, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                            {'data': check, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                            {'data': start, 'attr': 'data-ootable-details="This is start date time"'},
                            {'data': end, 'attr': 'data-ootable-details="This is end date time"'},
                            {'data': _getStr(random.randint(10, 128)), 'attr': 'data-ootable-details="This is details"'}
                        )
                    )

                return ' '.join(tbl_cls.html(data))

            @classmethod
            def example_data(cls, type=None, schema_only=False):

                def example_data_img():
                    schema = [
                        {'name': ''},
                        {'name': ''},
                        {'name': ''}
                    ]
                    records = []
                    for _ in range(random.randint(6, 10)):
                        records.append((
                            {'data': "!@#render_img!@#:". \
                                         replace('!@#render_img!@#',
                                                 OOTable.RENDER_IMG_KEY) + url_for('static', filename='img/demo.jpg')},
                            {'data': _getStr(random.randint(3, 6))},
                            {'data': _getStr(random.randint(3, 6))}
                        ))
                    setting = {
                        'scrollY': '400px',
                        'scrollX': True,
                        'scrollCollapse': True,
                        'paging': False,
                        'searching': False,
                        'destroy': True,
                        'colReorder': False,
                        'columnDefs': [],
                    }
                    return {'html': ''.join(OOTable.html({'schema': schema, 'records': records})), 'setting': setting}

                def example_data_chart():
                    schema = [
                        {'name': ''},
                        {'name': ''},
                        {'name': ''}
                    ]
                    records = []
                    for _ in range(10):
                        records.append((
                            {'data': ("!@#render_chart!@#:" + "mbar;oochart_multibar_example_data").replace(
                                '!@#render_chart!@#', OOTable.RENDER_CHART_KEY)},
                            {'data': _getStr(random.randint(3, 6))},
                            {'data': _getStr(random.randint(3, 6))}
                        ))
                    setting = {
                        'scrollY': '400px',
                        'scrollX': True,
                        'scrollCollapse': True,
                        'paging': False,
                        'searching': False,
                        'destroy': True,
                        'colReorder': False,
                        'columnDefs': []
                    }
                    return {'html': ''.join(OOTable.html({'schema': schema, 'records': records})), 'setting': setting}

                if type == 'img':
                    return example_data_img()
                elif type == 'chart':
                    return example_data_chart()
                else:
                    data = {'html': cls.example_data_old(schema_only=schema_only)}
                    data['setting'] = {
                        'scrollY': '400px',
                        'scrollX': True,
                        'scrollCollapse': True,
                        'paging': False,
                        'searching': False,
                        'destroy': True,
                        'colReorder': False,
                        'columnDefs': [],
                        'border': True
                    }
                    return data

            def place_components_impl(self):
                page = self
                testing_class = OOTable

                with page.add_child(WebRow()) as r1:
                    with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='400px')) as c1:
                        with c1.add_child(testing_class(parent=page,
                                                        mytype=['striped', 'hover', 'responsive'],
                                                        name=self.TEST_NAME1,
                                                        width='100%')) as test1:
                            pass

                with page.add_child(WebBr()):
                    pass
                with page.add_child(WebBr()):
                    pass
                with page.add_child(WebRow()) as r2:
                    with r2.add_child(WebColumn(width=['md8'],
                                                offset=['mdo2'], height='400px')) as c2:
                        with c2.add_child(testing_class(parent=page,
                                                        mytype=['striped', 'hover', 'responsive'],
                                                        name=self.TEST_NAME2,
                                                        width='100%')) as test2:
                            pass

                with page.add_child(WebBr()):
                    pass
                with page.add_child(WebBr()):
                    pass
                with page.add_child(WebRow()) as r3:
                    with r3.add_child(WebColumn(width=['md8'],
                                                offset=['mdo2'], height='400px')) as c3:
                        with c3.add_child(testing_class(parent=page,
                                                        mytype=['striped', 'hover', 'responsive'],
                                                        name=self.TEST_NAME3,
                                                        width='100%')) as test3:
                            pass

            def intro_events_impl(self):
                page = self

                test = page._components[self.TEST_NAME1]['obj']
                test2 = page._components[self.TEST_NAME2]['obj']
                test3 = page._components[self.TEST_NAME3]['obj']

                with page.render_post_w():
                    test.render_for_post()
                    test2.render_for_post()
                    test3.render_for_post()

            def on_my_render_impl(self, req):
                '''
                req = None
                if hasattr(self._page, '_action'):
                    req = self._page._action.on_post()
                else:
                    req = self._page.on_post()
                '''
                for r in req:
                    if r['me'] == self.TEST_NAME1:
                        print('Got OOTable request data: {}'.format(r['data']))
                        r['data'] = self.example_data(type='img')
                    elif r['me'] == self.TEST_NAME2:
                        r['data'] = self.example_data(type='chart')
                    elif r['me'] == self.TEST_NAME3:
                        r['data'] = self.example_data(type=None)

                return jsonify({'status': 'success', 'data': req})

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


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

    def __init__(self, value=[], col_num=0, **kwargs):
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
    def _example_data(cls, schema_only=False):
        data = {
            'schema': [],
            'records': []
        }

        for j in range(cls.COL_NUM):
            data['schema'].append({"name": ""})

        for i in range(2):
            approve = True if random.randint(0, 1) else False
            done = True if random.randint(0, 1) else False
            check = True if random.randint(0, 1) else False

            start, end = randDatetimeRange()
            td = []
            for i in range(len(data['schema'])):
                with WebCheckbox(value=_getStr(random.randint(2, 5))) as locals()["wc" + str(i)]:
                    pass
                locals()['wc' + str(i)].set_api()
                wc_content = locals()['wc' + str(i)].render_content()
                td.append({"data": wc_content['content'], "attr": "nowrap"})
                del locals()['wc' + str(i)]
            data['records'].append(td)
        return data

    def val(self, val={}):
        params = {'value': val}
        return self.func_call(params=params)

    def check(self, check=True):
        params = {'check': check}
        return self.func_call(params)


class Var(WebComponentBootstrap):

    VAL_FUNC_NAME = 'var_val'

    def __init__(self, parent, var_name='data', **kwargs):
        kwargs['parent'] = parent
        kwargs['var_name'] = var_name
        super().__init__(**kwargs)
        self._var_name = var_name

    def __repr__(self):
        return self._var_name

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


class LVar(Var):
    pass


class GVar(GVarTest, Var):
    pass


class OOList(OOListTest, ListInf, WebComponentBootstrap):

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

    def __init__(self, parent, var_name=None, **kwargs):
        kwargs['parent'] = parent
        kwargs['var_name'] = var_name
        super().__init__(**kwargs)
        self._var_name = var_name

    def __repr__(self):
        return self._var_name


class OODict(OODictTest, DictInf, WebComponentBootstrap):

    def __init__(self, parent, var_name=None, **kwargs):
        kwargs['parent'] = parent
        kwargs['var_name'] = var_name
        super().__init__(**kwargs)
        self._var_name = var_name

    def __repr__(self):
        return self._var_name

    @contextmanager
    def update_w(self, key):
        params = {'key': key}
        self.with_call(params)
        try:
            yield
        except Exception as err:
            raise Exception(err)
        finally:
            self._pop_current_context()

    '''
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
    '''
