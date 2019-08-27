import abc

class BootstrapInf(metaclass=abc.ABCMeta):

    DEFAULT_URL='index'

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
    def add_child(self, child=None, id=None):
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


class ActionInf(metaclass=abc.ABCMeta):

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
    def on_click(self):
        pass

    @abc.abstractmethod
    def on_change(self):
        pass

    @abc.abstractmethod
    def on_ready(self):
        pass

    @abc.abstractmethod
    def post(self, url, data):
        pass

    '''
    @abc.abstractmethod
    def is_js_kw(self, scripts):
        pass
    '''
    
    @abc.abstractmethod
    def value(self, value):
        pass

class FormatInf(metaclass=abc.ABCMeta):

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


class CommandInf(metaclass=abc.ABCMeta):

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

