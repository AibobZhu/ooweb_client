from interfaces import *

from flask import current_app
import uuid
import pprint
import inspect
from requests import post
from contextlib2 import contextmanager
from share import create_payload, extract_data, APIs
import sys

sys.setrecursionlimit(2000)

class Action(CommandInf, ActionInf):

    def if_(self):
        raise NotImplementedError

    def else_(self):
        raise NotImplementedError

    def for_(self):
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

    def condition(self):
        raise NotImplementedError

    def cmds(self):
        raise NotImplementedError

    def has_class(self, class_):
        raise NotImplementedError

    def add_class(self, class_):
        raise NotImplementedError

    def remove_class(self, class_):
        raise NotImplementedError

    def on_click(self):
        raise NotImplementedError

    def on_change(self):
        raise NotImplementedError

    def on_ready(self):
        raise NotImplementedError

    def post(self, url, data):
        raise NotImplementedError


class Format(BootstrapInf, FormatInf):

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


class WebComponent(ComponentInf, ClientInf):

    _context = None
    _cur_context_stack = []

    @classmethod
    def _set_context(cls, context):
        WebComponent._context = context
        WebComponent._cur_context_stack=[WebComponent._context]

    def _get_objcall_context(self, func, caller_id=None, params=None):
        return {
            'function': func,
            'caller_id': caller_id,
            'params': params
        }

    def __init__(self, **kwargs):

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

        context = self._get_objcall_context(func=self.type_(), params=kwargs)
        self.add_context(context)

    def __enter__(self):
        context = self._get_objcall_context(func='with', params={'obj_id':self.id()})
        context['sub_context'] = []
        self.add_context(context)
        self._push_current_context(context['sub_context'])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print('Error, tb:{}'.format(exc_tb))
        self._pop_current_context()
        return False

    def name(self, name=None):
        if not name:
            if not hasattr(self, '_name') or not self._name:
                self._name = self.__class__.__name__ + '-' + self.id()
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
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'child_id':child.id()})
        self.add_context(context)
        return child

    def parent(self, parent=None):
        raise NotImplementedError

    def module(self):
        raise NotImplementedError

    def type_(self):
        return self.__class__.__name__

    def url(self, url=None):
        raise NotImplementedError

    def render(self):
        print('WebPageClient.render:\n{}'.format(pprint.pformat(self.context())))
        #components = components_factory(self.context())
        payload = create_payload(self.context())
        #r = post(url='http://ec2-13-115-254-77.ap-northeast-1.compute.amazonaws.com:8089' + self._api, json=payload)
        r = post(url=self._api, json=payload)
        html = extract_data(r.json()['data'])
        return html

    def context(self):
        if self._parent:
            return self._parent.context()
        else:
            return self._context

    def add_context(self, cont):
        return self._add_context(cont)

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
        raise NotImplementedError

    def set_script_indent(self, indent):
        raise NotImplementedError

    def get_script_indent(self):
        raise NotImplementedError

    def styles(self):
        raise NotImplementedError

    def add_styles(self, styles):
        raise NotImplementedError

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
    def if_(self):
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

    @contextmanager
    def else_(self):
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

    @contextmanager
    def condition(self):
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

    @contextmanager
    def cmds(self):
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


class WebComponentBootstrap(WebComponent, Action, Format):

    def has_class(self, class_):
        raise NotImplementedError

    def is_width(self, width):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'width': width})
        context['sub_context'] = []
        self.add_context(context)

    def remove_width(self, width):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'width': width})
        context['sub_context'] = []
        self.add_context(context)

    def set_width(self, width):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'width': width})
        context['sub_context'] = []
        self.add_context(context)

    def value(self, value):
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={'value': value})
        context['sub_context'] = []
        self.add_context(context)

class WebPage(WebComponentBootstrap):

    def __init__(self, **kwargs):
        self._set_context([])
        super().__init__(**kwargs)
        self._api = current_app.config['API_URL'] + APIs['render'].format('v1.0')


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
        context = self._get_objcall_context(func=inspect.stack()[0][3], caller_id=self.id(), params={})
        self.add_context(context)


class WebBr(WebComponentBootstrap):
    pass

'''
[
    {
        'expression': {
            'type': 'create', 'param': {
                                        'class': 'WebPage', name: 'mypage', id: 0000, 'params': {
                                                                                                    value: '<OwwwO>'
                                                                                                }
                                        }
        }
    },
    {'expression': {'type': 'objcall', 'param': {'id': 098879087, 'function': 'add_child', 'params': {...}}}},
    {'expression': {'type': 'obj', 'param': {'id': 09987}}},
    {'expression': {'type': 'with', 'param': {'expression': {'type': 'obj', 'param': 0897786}, 'expressions': [
                                                                                                                    {},
                                                                                                                    {}
                                                                                                                ]
    }
]
'''

'''
with WebPage(name='mypage', value='<OwwwO>') as page:
    with page.add_child(WebRow()) as r1:
        with r1.add_child(WebColumn(width=['md6'], offset=['mdo3'], align=['horizon-center'])) as r1c1:
            with r1c1.add_child(WebHead1(value='&lt;OwwwO&gt; 	 Demo')) as h1:
                pass
    with page.add_child(WebRow(height='400px')) as r2:
        with r2.add_child(WebColumn(height='100%', width=['md2'], offset=['mdo3'])) as r2c1:
            with r2c1.add_child(WebField(value='左控件')) as r2c1fs:
                with r2c1fs.add_child(WebImg(value='img/burns.jpg', align=['horizon-center'])) as r2c1img:
                    pass
        with r2.add_child(WebColumn(height='100%', width=['md4'])) as r2c2:
            with r2c2.add_child(WebField(value='右控件')) as r2c2fs:
                with r2c2fs.add_child(WebImg(value='img/bobdylen.jpg', align=['horizon-center'])) as r2c2img:
                    pass
    with page.add_child(WebBr()):
        pass
    with page.add_child(WebRow()) as r3:
        with r3.add_child(WebColumn(width=['md6'], offset=['mdo3'], align=['horizon-center'])) as r3c1:
            with r3c1.add_child(WebBtnToggle(value='左2右4')) as r3c1btn:
                with r3c1btn.on_click():
                    r3c1btn.toggle()
                    with r3c1btn.if_():
                        with r3c1btn.condition():
                            r2c1.is_width('md2')
                        with r3c1btn.cmds():
                            r2c1.remove_width('md2')
                            r2c1.set_width('md4')
                            r2c2.remove_width('md4')
                            r2c2.set_width('md2')
                            r3c1btn.value('左4右2')
                    with r3c1btn.else_():
                        with r3c1btn.cmds():
                            r2c1.remove_width('md4')
                            r2c1.set_width('md2')
                            r2c2.remove_width('md2')
                            r2c2.set_width('md4')
                            r3c1btn.value('左2右4')
'''