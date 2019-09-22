import abc
from test_class import *

class BootstrapInf(MinXin, metaclass=abc.ABCMeta):

    DEFAULT_URL='index'

    _SUBCLASSES = {}

    @staticmethod
    def get_sub_classes(cls):
        """
        Get all subclasses recursively
        """

        for subclass in cls.__subclasses__():
            if (not (subclass.__name__) in cls._SUBCLASSES.keys()) and (subclass.__name__.find('Inf') < 0) \
                    and (subclass.__name__.find('WebPage') < 0) and (subclass.__name__.find('WebNav') < 0):
                cls._SUBCLASSES[subclass.__name__] = subclass
                cls.get_sub_classes(subclass)

        return cls._SUBCLASSES

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
    def get_width_name(self, width):
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


class ComponentInf(MinXin, metaclass=abc.ABCMeta):

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
    def add_child(self, child=None, id=None):
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
    def url(self, url=None):
        pass

    @abc.abstractmethod
    def type_(self):
        pass

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractmethod
    def context(self):
        pass

    @abc.abstractmethod
    def add_context(self, cont):
        pass

    @abc.abstractmethod
    def scripts(self):
        pass

    @abc.abstractmethod
    def add_scripts(self, scripts):
        pass

    @abc.abstractmethod
    def replace_scripts(self, stub, scripts):
        pass

    @abc.abstractmethod
    def add_script_files(self, files):
        pass

    @abc.abstractmethod
    def get_script_files(self):
        pass

    @abc.abstractmethod
    def set_script_indent(self, indent):
        pass

    @abc.abstractmethod
    def get_script_indent(self):
        pass

    @abc.abstractmethod
    def get_global_styles(self):
        pass

    @abc.abstractmethod
    def add_global_styles(self, styles):
        pass

    @abc.abstractmethod
    def add_style_files(self, files):
        pass

    @abc.abstractmethod
    def get_style_files(self):
        pass

    def data_format(self):
        raise NotImplementedError

    def default_data(self):
        raise NotImplementedError


class CustomComponentInf(MinXin, metaclass=abc.ABCMeta):

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

    @abc.abstractmethod
    def load_data(self, data=None):
        '''
        Load data from user or model modules, and expect it in the correct format already,
            for the data should be created in the format defined by CustomToolbar.data_format

        :param data:
        :return:
        '''
        pass

    @abc.abstractmethod
    def query_data(self, qeury):
        '''
        Let the user of custom complex controller query data in a format , like the endpoint to response post request
        :return: queried data
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


class ActionInf(MinXin, metaclass=abc.ABCMeta):

    '''
    All the interfaces about js operations

    TODO: add w_ head of all the function with decorated with contextmanager
    '''

    @abc.abstractmethod
    def has_class(self, class_):
        pass

    @abc.abstractmethod
    def add_class(self, class_):
        pass

    @abc.abstractmethod
    def remove_class(self, class_):
        pass

    @abc.abstractmethod
    def on_event_w(self,event):
        '''Declare an execute_list, capture the event if not yet, push the following actions into the execute list'''
        pass

    @abc.abstractmethod
    def trigger_event(self,event):
        '''Trigger the event on the element'''
        pass


    '''
    TODO: The following should be replaced with trigger_event, on_event
    '''
    '''
    @abc.abstractmethod
    def on_select(self):
        pass

    @abc.abstractmethod
    def select_declare(self):
        pass

    @abc.abstractmethod
    def on_click(self):
        pass

    @abc.abstractmethod
    def on_change(self):
    '''
    '''
        Define the action to process change event
        Normally, push function into the execution list

        :return:
    '''
    '''
        pass

    @abc.abstractmethod
    def on_change_event(self, filter=''):
    '''
    '''
        Declare the change event capture

        :return:
    '''
    '''
        pass

    @abc.abstractmethod
    def clear_declare(self):
        pass

    @abc.abstractmethod
    def event_declare(self, event, filter=''):
        pass

    @abc.abstractmethod
    def _execute_list_name(self, action_name):
        pass

    @abc.abstractmethod
    def execute_list_declare(self, action_name):
        pass

    @abc.abstractmethod

    def on_ready(self):
        pass
        
    @abc.abstractmethod
    def on_window_resize(self):
        pass
        
    '''
    '''
    TODO END
    '''

    @abc.abstractmethod
    def post(self, url, data, success):
        pass

    @staticmethod
    def on_post():
        raise NotImplementedError
    
    @abc.abstractmethod
    def val(self, value):
        pass


class FormatInf(MinXin, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def pad(self, pad=None):
        pass

    @abc.abstractmethod
    def margin(self, margin=None):
        pass

    @abc.abstractmethod
    def width(self, width=None):
        pass

    @abc.abstractmethod
    def height(self, height=None):
        pass

    @abc.abstractmethod
    def align(self, align=None):
        pass

    @abc.abstractmethod
    def value(self, value=None):
        pass

    @abc.abstractmethod
    def color(self, color=None):
        pass

    @abc.abstractmethod
    def font(self, font=None):
        pass

    @abc.abstractmethod
    def styles(self, style=None):
        pass
    
    @abc.abstractmethod
    def styles_str(self):
        pass

    @abc.abstractmethod
    def add_styles(self, styles):
        pass
    
    @abc.abstractmethod
    def remove_style(self, style):
        pass

    @abc.abstractmethod
    def atts(self, atts=None):
        pass

    @abc.abstractmethod
    def atts_str(self):
        pass

    @abc.abstractmethod
    def add_atts(self, atts):
        pass

    @abc.abstractmethod
    def remove_att(self, att):
        pass

    @abc.abstractmethod
    def classes(self, classes=None):
        pass

    @abc.abstractmethod
    def classes_str(self):
        pass

    @abc.abstractmethod
    def add_class(self, class_):
        pass

    @abc.abstractmethod
    def remove_class(self, class_):
        pass

    @abc.abstractmethod
    def border_radius(self, radius=None):
        '''
        Set the border radius
        :param radius: {'tl':1px, 'tr':2px, 'br':3px, 'bl':4px}
        :return:
        '''
        pass


class CommandInf(MinXin, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def if_(self):
        pass

    @abc.abstractmethod
    def else_(self):
        pass

    @abc.abstractmethod
    def for_(self):
        pass

    @abc.abstractmethod
    def var(self, value=None):
        pass

    @abc.abstractmethod
    def g_var(self, value=None):
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

    @abc.abstractmethod
    def condition(self):
        pass

    @abc.abstractmethod
    def cmds(self):
        pass


class ClientInf(MinXin, metaclass=abc.ABCMeta):

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

