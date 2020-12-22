import abc
from contextlib2 import contextmanager


class MetisInf(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_vptr(self):
        pass

    @abc.abstractmethod
    def set_vptr(self, vptr):
        pass

    @abc.abstractmethod
    def keep_vptr_ori(self):
        """
        Just for api mode, client need somewhere to keep the last vptr value for restore it when exit a with sentence
        """
        pass

    @abc.abstractmethod
    def restore_vptr_ori(self):
        """
        same with get_vptr_ori
        """
        pass


class AppearanceInf(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def width(self,  width=None):
        pass

    @abc.abstractmethod
    def height(self,  height=None):
        pass

    @abc.abstractmethod
    def color(self,  color=None):
        pass

    @abc.abstractmethod
    def font(self, font=None):
        pass

    @abc.abstractmethod
    def border(self, border=None):
        pass

    @abc.abstractmethod
    def icon(self, icon=None):
        pass

    @abc.abstractmethod
    def disable(self, disable=None):
        pass

    @abc.abstractmethod
    def display(self, display=None):
        pass


class PositionInf(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def pad(self,  pad=None):
        pass

    @abc.abstractmethod
    def margin(self, margin=None):
        pass

    @abc.abstractmethod
    def align(self, align=None):
        pass

    @abc.abstractmethod
    def offset(self, offset=None):
        pass


class PropertyInf(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def value(self, value=None):
        pass

    @abc.abstractmethod
    def attrs(self, attrs=None):
        pass

    @abc.abstractmethod
    def classes(self, classes=None):
        pass

    @abc.abstractmethod
    def styles(self, styles=None):
        pass


class EventInf(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    @contextmanager
    def on_event_w(self, event, filter='', propagation=None):
        '''Declare an execute_list, capture the event if not yet, push the following actions into the execute list'''
        pass

    @abc.abstractmethod
    def render_post_w(self, post_async=True):
        pass

    @abc.abstractmethod
    def render_for_post(self, trigger_event=False, return_parts=["all"]):
        pass

    @abc.abstractmethod
    def trigger_event(self, event, filter=''):
        pass

    @abc.abstractmethod
    def sync(self, sync=True):
        pass

    @abc.abstractmethod
    def timeout_w(self, time):
        pass


class BootstrapInf(metaclass=abc.ABCMeta):

    DEFAULT_URL='index'

    _SUBCLASSES = {}

    '''
    @abc.abstractmethod
    def get_sub_classes(cls):
        """
        Get all subclasses recursively
        """
        pass
    '''

    @abc.abstractmethod
    def create_default_nav_items(cls):
        pass

    @abc.abstractmethod
    def check_col_name(self, col):
        pass

    @abc.abstractmethod
    def check_align(self, align):
        pass

    @abc.abstractmethod
    def offset(self, offset=[]):
        pass

    @abc.abstractmethod
    def get_offset_name(self, offset):
        pass

    @abc.abstractmethod
    def _get_width_name(self, width):
        pass

    @abc.abstractmethod
    def base_context(self):
        pass

    @abc.abstractmethod
    def fix_cmd(self, cmd):
        pass

    @abc.abstractmethod
    def has_class(self, class_):
        pass

    @abc.abstractmethod
    def is_width(self, width):
        pass

    @abc.abstractmethod
    def set_width(self, width):
        pass

    @abc.abstractmethod
    def remove_width(self, width):
        pass

    @abc.abstractmethod
    def empty(self):
        pass


class ComponentInf(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __enter__(self):
        pass

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @abc.abstractmethod
    def name(self, name=None):
        pass

    @abc.abstractmethod
    def id(self, _id=None):
        pass

    @abc.abstractmethod
    def children(self, children=[]):
        pass

    @abc.abstractmethod
    def add_child(self, child=None, child_id=None, objs=None):
        pass

    @abc.abstractmethod
    def remove_child(self,child=None, child_id=None,objs=None):
        pass

    @abc.abstractmethod
    def empty_children(self):
        pass

    @abc.abstractmethod
    def parent(self, parent=None):
        pass

    @abc.abstractmethod
    def module(self):
        pass

    @abc.abstractmethod
    def url(self, url=None, js=True):
        pass

    @abc.abstractmethod
    def render_content(self):
        pass
    
    @abc.abstractmethod
    def context(self):
        pass

    @abc.abstractmethod
    def add_context(self, cont):
        pass

    @abc.abstractmethod
    def set_context(self, context):
        pass

    @abc.abstractmethod
    def add_context_indent(self, indent):
        pass

    @abc.abstractmethod
    def get_context_indent(self):
        pass

    @abc.abstractmethod
    def add_scripts(self, scripts, indent=True, place=None):
        pass

    @abc.abstractmethod
    def replace_scripts(self, stub, scripts):
        pass

    @abc.abstractmethod
    def add_scripts_files(self, files):
        pass

    @abc.abstractmethod
    def get_scripts_files(self):
        pass

    @abc.abstractmethod
    def set_scripts_indent(self, indent):
        pass

    @abc.abstractmethod
    def get_scripts_indent(self):
        pass

    @abc.abstractmethod
    def add_styles(self, styles):
        pass

    @abc.abstractmethod
    def get_styles(self):
        pass

    @abc.abstractmethod
    def add_styles_files(self, files):
        pass

    @abc.abstractmethod
    def get_styles_files(self):
        pass

    @classmethod
    @abc.abstractmethod
    def add_url_rule(cls, app, extend=[]):
        pass

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractmethod
    def is_js(self):
        pass

    @abc.abstractmethod
    def set_js(self, js):
        pass

    @abc.abstractmethod
    def is_condition(self):
        pass

    @abc.abstractmethod
    def set_condition(self, cond):
        pass


class CustomComponentInf(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def get_url(cls):
        pass

    @abc.abstractmethod
    def get_wc(self):
        pass

    @abc.abstractmethod
    def data_format(self, format=None):
        '''
        Define the data format, can be used by data creators like user class. Basically the format is a dict with blank values

        :param format: generally a dict
        :return:
        '''
        pass

    @classmethod
    @abc.abstractmethod
    def get_data(cls, model=None, query=None):
        '''
        Load data from user or model modules, and expect it in the correct format already,
            for the data should be created in the format defined by CustomToolbar.data_format

        :param model is the user or database model
        :param query is query conditions
        :return: the queried data from the model
        '''
        pass

    @abc.abstractmethod
    def create(self,parent):
        pass

    @classmethod
    @abc.abstractmethod
    def create_routes(cls, app):
        '''
        Create url routes to provide the backend data process methods

        :param app:
        :return:
        '''
        pass

    @classmethod
    @abc.abstractmethod
    def on_post(cls):
        '''
        Response the post request from itself post method. return data in the format of 
        {'status': , 'data': }
        :return: {'status': , 'data': }
        '''
        pass


class CommandInf(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def if_w(self):
        pass

    @abc.abstractmethod
    def elif_w(self):
        pass

    @abc.abstractmethod
    def else_w(self):
        pass

    @abc.abstractmethod
    def for_w(self):
        pass

    @abc.abstractmethod
    def equal(self,right, lef=None):
        pass

    @abc.abstractmethod
    def condition_w(self):
        pass

    @abc.abstractmethod
    def cmds_w(self):
        pass

    @abc.abstractmethod
    def declare_custom_func(self, fname='', fparams=[], fbody=[]):
        pass

    @abc.abstractmethod
    def declare_custom_global_func(self, fname, fparams=[], fbody=[]):
        pass

    @abc.abstractmethod
    def call_custom_func(self, fname='', fparams={}):
        pass


class ActionInf(EventInf, AppearanceInf, PositionInf, PropertyInf):

    '''
    All the interfaces about js operations

    TODO: add w_ head of all the function with decorated with contextmanager
    '''

    '''
    @abc.abstractmethod
    def val(self, value=''):
        pass

    @abc.abstractmethod
    def empty(self):
        pass

    @abc.abstractmethod
    def add_attrs(self, attrs):
        pass

    @abc.abstractmethod
    def remove_attrs(self, attrs):
        pass

    @classmethod
    @abc.abstractmethod
    def _example_data(cls):
        pass

    @abc.abstractmethod
    def false(self):
        pass

    @abc.abstractmethod
    def true(self):
        pass

    @abc.abstractmethod
    def null(self):
        pass

    @abc.abstractmethod
    def height(self, height=None):
        pass
    '''

'''
class ActionJqueryInf(ActionInf, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def empty(self):
        pass

    @abc.abstractmethod
    def is_(self):
        pass

    @abc.abstractmethod
    def data(self):
        pass

    @abc.abstractmethod
    def declare_event(self, event, use_clsname=False, selector=None, filter=''):
        pass

    @abc.abstractmethod
    def children(self, filter=''):
        pass

    @abc.abstractmethod
    def each_w(self):
        pass
'''

class FormatInf(AppearanceInf, PositionInf, PropertyInf):
    pass


class ClientInf(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def _add_context(cls, cont):
        pass

    @classmethod
    @abc.abstractmethod
    def _set_context(cls,context):
        pass

    @classmethod
    @abc.abstractmethod
    def _pop_current_context(cls,context):
        pass

    @classmethod
    @abc.abstractmethod
    def _push_current_context(cls, context):
        pass

    @abc.abstractmethod
    def _get_objcall_context(self, func, caller_id=None, parent_id=None, params=None, sub_context=[]):
        pass


class ListInf(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def append_w(self):
        pass


class DictInf(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update_w(self, dict):
        pass


class VarInf(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def equal(self):
        pass

    @abc.abstractmethod
    def assign_w(self):
        pass
