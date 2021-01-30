import os, datetime
from flask_sqlalchemy import SQLAlchemy
from flask import render_template_string, current_app, jsonify, url_for
import types
import copy
import pprint
import random
from share import randDatetimeRange, _getStr
import oocc_define as ooccd
import pickle
from bs4 import BeautifulSoup

class MinXin:

    def __init__(self, **kwargs):
        super().__init__()


class ClassTest():

    _SUBCLASSES = {}
    _PAGE_CLASS = None
    RENDERED_HTML = None
    CLASS_TEST_HTML = None
    testing_class = None
    RUNTIME_ROOT_CLASS = None
    WIDTH = ['md6', 'lg6', 'sm10', 'xs10']
    OFFSET = ['mdo3', 'lgo3', 'smo1', 'xso1']

    ROW = 'row'

    def events_action_for_class_test(self, req):
        cls = self.__class__
        name_ = cls.__name__
        print('Class testing, class {} got req:{}'.format(name_, req))
        if not hasattr(cls, 'test_request_data') or not cls.test_request_data:
            req['data'] = {'val': name_ + '_testing from on_post', 'text': name_ + '_testing from on_post'}
        else:
            req['data'] = {'data': cls.test_request_data()}

    @classmethod
    def get_sub_classes(cls, root_class):
        """
        Get all subclasses recursively
        """
        all_subclasses = root_class.__subclasses__()
        for subclass in all_subclasses:
            if (not (subclass.__name__) in cls._SUBCLASSES.keys()) and \
                    (subclass.__name__.find('Inf') < 0) and \
                    (subclass.__name__.find('WebPage') < 0):
                cls._SUBCLASSES[subclass.__name__] = {'class': subclass,
                                                      'test_request': subclass.test_request,
                                                      'test_result': subclass.test_result}
                cls.get_sub_classes(subclass)
        return cls._SUBCLASSES

    def __init__(self, client=False, **kwargs):
        self.custom_test_init()

    def custom_test_init(self):
        """
        Do custom test initialization for a class if necessary
        """
        pass

    def get_test_js(self):
        """
        TODO: discard
        """

        url = ''
        return '''alert('!@#class_name!@#');\n'''.replace('!@#class_name!@#', self.__class__.__name__)

    @classmethod
    def test_result(cls):
        '''
        TODO: will discard
        '''
        raise NotImplementedError

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def class_testing(self):
        self.value('class testing ' + self.__class__.__name__ + ' from response')
        return

    @classmethod
    def test_request(cls, methods=['GET']):

        # Create a testing page containing the component tested
        print('class {} test_request is called'.format(cls.__name__))
        """
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        WebPage = cls._PAGE_CLASS
        page = WebPage(url='/test_'+cls.__name__+'_request',
                       value='class {} test'.format(cls.__name__))
        '''
        page.place_components = types.MethodType(cls.place_components_for_class_test, page)
        page.place_components()
        page.events_trigger = types.MethodType(cls.events_trigger_for_class_test, page)
        page.events_trigger()

        this_obj = page._components[testing_cls_name]['obj']
        this_obj.on_post_for_class_test = types.MethodType(this_obj.__class__.on_post_for_class_test, this_obj )
        page.init_on_post(app=current_app,
                          on_post=this_obj.on_post_for_class_test,
                          endpoint=cls.__name__ + '_test',
                          url='/' + cls.__name__ + '_test')
        '''
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        """
        Page = cls._PAGE_CLASS
        Page.testing_class = cls
        return Page.get_page(top_menu=None, rule='/test_'+cls.__name__+'_request',
                            name='class {} test'.format(cls.__name__), title='class {} test'.format(cls.__name__))


class GVarTest(ClassTest):

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):
            def place_components_impl(self):
                page = self
                WebHead1 = page._SUBCLASSES['WebHead1']['class']
                WebHead3 = page._SUBCLASSES['WebHead3']['class']
                GVar = page._SUBCLASSES['GVar']['class']
                WebBtn = page._SUBCLASSES['WebBtn']['class']
                with page.add_child(WebHead1(value='Test GVar and js values')) as head1:
                    pass
                with page.add_child(WebHead3(value='var test = false;')) as head3:
                    pass
                with page.add_child(GVar(parent=page, name='GVar', var_name='test', var_value='false')) as gv:
                    pass
                with page.add_child(WebBtn(value='Test GVar assign', name='TestBtn')) as btn:
                    pass

            def intro_events_impl(self):
                page = self
                btn = page._components['TestBtn']['obj']
                gv = page._components['GVar']['obj']
                with btn.on_event_w('click'):
                    with gv.assign_w():
                        gv.true()
                    btn.alert('"GVar value should be true, real:"+test')

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class OOListTest(ClassTest):

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self, **kwargs):
        page = self._page
        WebRow = page._SUBCLASSES['WebRow']['class']
        WebColumn = page._SUBCLASSES['WebColumn']['class']
        WebBtn = page._SUBCLASSES['WebBtn']['class']
        LVar = page._SUBCLASSES['LVar']['class']
        OOList = page._SUBCLASSES['OOList']['class']
        with page.add_child(WebRow()) as r1:
            with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c1:
                with c1.add_child(WebBtn(name='TestBtn', value='Test OOList')) as btn:
                    pass

        with ooccd.MetisTransform.transform_w(component=self, vptr=ooccd.ACTION_MEMBER):
            with btn.on_event_w('click'):
                with btn.add_child(LVar(parent=btn, name='lvar', var_name='data')) as data:
                    with data.add_child(OOList(parent=data, name='OOList')) as list_data:
                        with list_data.append_w():
                            list_data.add_scripts('"value1"', indent=False)
                        with list_data.append_w():
                            list_data.add_scripts('"value2"', indent=False)
                    list_data.add_scripts(';\n')
                    page.alert(
                        "'Testing is to append the text of the button to a list twice and print out the list: ' + data.join(' ')")

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        print('OOList.events_trigger_for_class_test')

    @classmethod
    def test_request(cls, methods=['GET ']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class TestPage(cls._PAGE_CLASS):

            def place_components_impl(self):
                page = self._page
                WebRow = page._SUBCLASSES['WebRow']['class']
                WebColumn = page._SUBCLASSES['WebColumn']['class']
                WebBtn = page._SUBCLASSES['WebBtn']['class']
                LVar = page._SUBCLASSES['LVar']['class']
                OOList = page._SUBCLASSES['OOList']['class']
                with page.add_child(WebRow()) as r1:
                    with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c1:
                        with c1.add_child(WebBtn(name='TestBtn', value='Test OOList')) as btn:
                            pass

                with ooccd.MetisTransform.transform_w(component=self, vptr=ooccd.ACTION_MEMBER):
                    with btn.on_event_w('click'):
                        with btn.add_child(LVar(parent=btn, name='lvar', var_name='data')) as data:
                            with data.add_child(OOList(parent=data, name='OOList')) as list_data:
                                with list_data.append_w():
                                    list_data.add_scripts('"value1"', indent=False)
                                with list_data.append_w():
                                    list_data.add_scripts('"value2"', indent=False)
                            list_data.add_scripts(';\n')
                            page.alert(
                                "'Testing is to append the text of the button to a list twice and print out the list: ' + data.join(' ')")

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class OODictTest(ClassTest):

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self, **kwargs):
        page = self
        WebBtn = page._SUBCLASSES['WebBtn']['class']
        OODict = page._SUBCLASSES['OODict']['class']
        with page.add_child(WebBtn(value='Test dict', name='name1')) as btn1:
            pass
        with page.add_child(WebBtn(value='Test dict update', name='name2')) as btn2:
            pass

        with ooccd.MetisTransform.transform_w(component=self, vptr=ooccd.ACTION_MEMBER):
            with btn1.on_event_w('click'):
                with btn1.add_child(OODict(parent=page, name='OODict', dict={'key1': '"val1"', 'key2': '"val2"'}, var_name='test_dict')) as dict:
                    pass
                btn1.alert('"Test dict: { key1:" + test_dict.key1 + "}"')

            with btn2.on_event_w("click"):
                with OODict(parent=page, dict={'key1': '"val1"', 'key2': '"val2"'}, var_name='test_dict_update') as dict_update:
                    pass
                with dict_update.update_w(key='key2'):
                    dict_update.add_scripts('"val_updated";\n', indent=False)
                btn2.alert('"Test dict update: { key2:" + test_dict_update.key2 + "}"')

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        pass

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def place_components_impl(self):
            page = self
            WebBtn = page._SUBCLASSES['WebBtn']['class']
            OODict = page._SUBCLASSES['OODict']['class']
            with page.add_child(WebBtn(value='Test dict', name='name1')) as btn1:
                pass
            with page.add_child(WebBtn(value='Test dict update', name='name2')) as btn2:
                pass

        def intro_events_impl(self):
            page = self
            OODict = self._SUBCLASSES['OODict']['class']

            btn1 = page._components['name1']['obj']
            btn2 = page._components['name2']['obj']

            with btn1.on_event_w('click'):
                with btn1.add_child(
                        OODict(parent=page, name='OODict', dict={'key1': '"val1"', 'key2': '"val2"'},
                               var_name='test_dict')) as dict:
                    pass
                btn1.alert('"Test dict: { key1:" + test_dict.key1 + "}"')

            with btn2.on_event_w("click"):
                with OODict(parent=page, dict={'key1': '"val1"', 'key2': '"val2"'},
                            var_name='test_dict_update') as dict_update:
                    pass
                with dict_update.update_w(key='key2'):
                    dict_update.add_scripts('"val_updated";\n', indent=False)
                btn2.alert('"Test dict update: { key2:" + test_dict_update.key2 + "}"')

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class WebATest(ClassTest):

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        TEST_OBJ = 'test_obj'

        def place_components_impl(self):
            page = self
            WebA = page._SUBCLASSES['WebA']['class']
            WebBtn = page._SUBCLASSES['WebBtn']['class']
            WebIcon = page._SUBCLASSES['WebIcon']['class']
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']

            with page.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=self.WIDTH,
                                            offset=self.OFFSET,
                                            align='horizon-center',
                                            height='80px',
                                            styles={'border':'solid 1px blue'})) as c22:
                    with c22.add_child(WebA()) as a21:
                        with a21.add_child(WebIcon(
                                                    align=['left'],
                                                    icon='arrow-left',
                                                   font={'size':'40px'},
                                                    margin={'top':'20px'})) as left_arrow2:
                            pass
                    with c22.add_child(WebA()) as a22:
                        with a22.add_child(WebBtn(value='Test', height='40px',
                                              margin={'top':'20px'})) as btn_22:
                            pass
                    with c22.add_child(WebA()) as a23:
                        with a23.add_child(WebIcon(align=['right'],
                                               icon='arrow-right',
                                                   font={'size':'60px'},
                                               margin={'top':'10px'})) as rightt_arrow2:
                            pass

        def intro_events_impl(self):
            pass

        def on_my_render_impl(self, req):
            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):
            SIDE_WIDTH = ['md1', 'lg1', 'xs1', 'sm1']
            CENTER_WIDTH = ['md4', 'lg4', 'xs4', 'sm4']

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))

        page = TestPage(app=current_app,
                        url='/test_' + cls.__name__ + '_request',
                        value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class WebIconTest(ClassTest):

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        TEST_OBJ = 'test_obj'

        def place_components_impl(self):
            page = self
            WebIcon = page._SUBCLASSES['WebIcon']['class']
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']

            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c1:
                    with c1.add_child(WebIcon(name=TEST_OBJ,
                                              icon='arrow-right',
                                              font={'size':'60px'},
                                              color={'color':'grey'})) as icon:
                        pass

        def intro_events_impl(self):
            pass

        def on_my_render_impl(self, req):
            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))

        page = TestPage(app=current_app,
                        url='/test_' + cls.__name__ + '_request',
                        value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML


class WebBtnRadioTest(ClassTest):

    testing_cls_name = 'WebBtnRadio'

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        TEST_OBJ = 'test_obj'

        DYN_BE_OBJ = 'test_be_obj'
        DYN_BE_VAL = 'test_be_val'
        DYN_BE_REF_BTN = 'dyn_be_ref_btn'
        DYN_BE_VAL_BTN = 'dyn_be_val_btn'

        def place_components_impl(self):
            page = self
            WebBtnRadio = page._SUBCLASSES['WebBtnRadio']['class']
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            WebHead5 = page._SUBCLASSES['WebHead5']['class']
            WebBtn = page._SUBCLASSES['WebBtn']['class']
            WebBr = page._SUBCLASSES['WebBr']['class']
            WebHead3 = page._SUBCLASSES['WebHead3']['class']

            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c1:
                    with c1.add_child(WebBtnRadio(name=TEST_OBJ,
                                                 mytype=['inline'],
                                                 items=[
                                                     {'label': '测试1', 'checked': ''},
                                                     {'label': '测试测试测试2'},
                                                     {'label': '测试3'}])) as radio:
                        pass

            with page.add_child(WebBr()):
                pass
            with page.add_child(WebRow()) as dyn_title_r:
                with dyn_title_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_title_c:
                    with dyn_title_c.add_child(WebHead3(value='Dynamically create radio on backend:')):
                        pass
            with page.add_child(WebRow()) as dyn_r:
                with dyn_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_c:
                    with dyn_c.add_child(WebBtnRadio(name=DYN_BE_OBJ, mytype=['inline'])) as dyn_radio:
                        pass
            with page.add_child(WebBr()):
                pass
            with page.add_child(WebRow()) as dyn_val_r:
                with dyn_val_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_val_c:
                    with dyn_val_c.add_child(WebHead5(name=DYN_BE_VAL)) as dyn_val:
                        pass
            with page.add_child(WebRow()) as dyn_btn_r:
                with dyn_btn_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_btn_c:
                    with dyn_btn_c.add_child(WebBtn(name=DYN_BE_VAL_BTN, value='Get value of radio')) as dyn_val_btn:
                        pass
                    with dyn_btn_c.add_child(WebBtn(name=DYN_BE_REF_BTN, value='Refresh radio')) as dyn_ref_btn:
                        pass

        def intro_events_impl(self):
            page = self
            radio = page._components[TEST_OBJ]['obj']
            LVar = page._SUBCLASSES['LVar']['class']
            cls = radio.__class__

            dyn_be_obj = page._components[DYN_BE_OBJ]['obj']
            dyn_be_val = page._components[DYN_BE_VAL]['obj']
            val_btn = page._components[DYN_BE_VAL_BTN]['obj']
            ref_btn = page._components[DYN_BE_REF_BTN]['obj']

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

            with dyn_be_obj.on_event_w('change'):
                dyn_be_obj.alert('"Clicked"')
                with page.render_post_w():
                    dyn_be_obj.render_for_post()

            with val_btn.on_event_w('click'):
                with page.render_post_w():
                    dyn_be_obj.render_for_post()
                    dyn_be_val.render_for_post()
            with ref_btn.on_event_w('click'):
                ref_btn.alert('"Refresh button click"')
                with page.render_post_w():
                    ref_btn.render_for_post()
                    dyn_be_obj.render_for_post()

        def on_my_render_impl(self, req):
            page = self

            testing_cls = page.testing_class
            testing_cls_name = testing_cls.__name__
            testing_obj = page._components[TEST_OBJ]['obj']

            dyn_be_value = None
            new_dyn_be_value = None
            new_dyn_be_value2 = {
                'children':
                    [
                        {'label': '2NewItem1', 'checked': True},
                        {'label': '2NewItem2'},
                        {'label': '2NewItem3'},
                    ],
                'mytype': ['inline'],

            }
            for r in req:
                if r['me'] == TEST_OBJ:
                    print('{} got request:{}'.format(testing_cls_name, pprint.pformat(r)))
                    testing_obj.request(req=r)
                    testing_obj.value(value='测试3')
                    r['data'] = testing_obj.response()['data']
                elif r['me'] == DYN_BE_OBJ:
                    dyn_be_obj = page._components[DYN_BE_OBJ]['obj']
                    print('{} got request:{}'.format(dyn_be_obj.name(), pprint.pformat(r)))
                    dyn_be_obj.request(req=r)
                    '''
                    dyn_be_value=dyn_be_obj._value_response(radio_cls=testing_cls,
                                        request_member=dyn_be_obj._vtable[ooccd.RESPONSE_MEMBER])
                    '''
                    dyn_be_value=dyn_be_obj.value()
                    if new_dyn_be_value:
                        '''
                        dyn_be_obj._value_response(radio_cls=dyn_be_obj.__class__,
                                                    request_member=dyn_be_obj._vtable[ooccd.RESPONSE_MEMBER],
                                                   value=new_dyn_be_value2)
                        '''
                        dyn_be_obj.value(value=new_dyn_be_value2)
                    r['data'] = dyn_be_obj.response()['data']
                elif r['me'] == DYN_BE_VAL:
                    dyn_val_obj = page._components[DYN_BE_VAL]['obj']
                    print('{} got request:{}'.format(dyn_val_obj.name(), pprint.pformat(r)))
                    dyn_val_obj.request(req=r)
                    info = 'selected:{}, \n\rchildren: {}'.format(dyn_be_value['selected'],
                                                              dyn_be_value['children'])
                    dyn_val_obj.value(info)
                    r['data'] = dyn_val_obj.response()['data']
                elif r['me'] == DYN_BE_REF_BTN:
                    new_dyn_be_value = {
                        'children':
                            [
                                {'label': 'NewItem1', 'checked': True},
                                {'label': 'NewItem2'},
                                {'label': 'NewItem3'},
                            ],
                        'mytype':['inline'],

                    }
            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))

        '''
        page = TestPage(app=current_app,
                        url='/test_' + cls.__name__ + '_request',
                        value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name,
                                      rule='/test_' + cls.__name__ + '_request',
                                      title=title_name,
                                      page_class=TestPage)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        cls._PAGE_CLASS.testing_class = cls
        TestPage.testing_class = cls
        return page_html


class WebBtnGroupTest(ClassTest):

    @classmethod
    def test_request(cls, methods=['GET']):

        # Create a testing page containing the component tested
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        TEST_OBJ_NORMAL='test_obj_normal'
        TEST_OBJ_VERTICAL='test_obj_vertical'
        TEST_OBJ_HORIZON_CKBX='test_obj_horizon_checkbox'
        TEST_OBJ4='test_obj4'
        GetValueBtn1 = 'getvalue_btn1'
        GetCkbxValueBtn = 'getcheckboxvalue_btn'
        ShowValue1 = 'show_value1'
        ShowCkbxValue = 'show_ckbx_value'
        ShowDynBEValue = 'show_backend_value'

        DYN_OBJ = 'dynamic_object'
        DYN_BTN = 'dynamic_btn'
        DYN_VALUE = 'dynamic_value'
        DYN_BE_OBJ = 'dynamic_beckend_object'

        DYN_BE_BTN = 'dynamic_beckend_btn'
        DYN_BE_VALUE = 'dynamic_beckend_value'
        DYN_BE_REFRESH_BTN = 'dynamic_beckend_refresh_btn'

        DYN_BE_RADIO_OBJ = 'dynamic_be_radio_obj'
        DYN_BE_RADIO_VAL_BTN = 'dyn_be_radio_val_btn'
        DYN_BE_RADIO_REF_BTN = 'dyn_be_radio_ref_btn'
        DYN_BE_RADIO_VALUE = 'dyn_be_radio_value'

        def place_components_impl(self):
            page = self
            this_class = page.testing_class
            WebCheckbox = page._SUBCLASSES['WebCheckbox']['class']
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            WebBr = page._SUBCLASSES['WebBr']['class']
            WebBtn = page._SUBCLASSES['WebBtn']['class']
            WebHead3 = page._SUBCLASSES['WebHead3']['class']
            WebHead5 = page._SUBCLASSES['WebHead5']['class']

            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c1:
                    with c1.add_child(WebHead3(value='WebBtnGroup() test:')):
                        pass
                    with c1.add_child(this_class(name=TEST_OBJ_NORMAL)) as test_obj1:
                        with test_obj1.add_child(WebBtn(value='TestBtn1')) as checkbox1:
                            pass
                        with test_obj1.add_child(WebBtn(value='TestBtn2')) as checkbox2:
                            pass
            with page.add_child(WebBr()):
                pass
            with page.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c2:
                    with c2.add_child(WebHead3(value='WebBtnGroup(mytype=["vertical"]) test:')):
                        pass
                    with c2.add_child(this_class(name=TEST_OBJ_VERTICAL, mytype=['vertical'])) as test_obj2:
                        with test_obj2.add_child(WebBtn(value='TestBtn3')) as checkbox3:
                            pass
                        with test_obj2.add_child(WebBtn(value='TestBtn4')) as checkbox4:
                            pass
            with page.add_child(WebBr()):
                pass
            with page.add_child(WebRow()) as r3:
                with r3.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c3:
                    with c3.add_child(WebHead3(value='WebBtnGroup() + WebCheckbox(mytype=["horizontal"]) test:')):
                        pass
                    with c3.add_child(this_class(name=TEST_OBJ_HORIZON_CKBX)) as test_obj3:
                        with test_obj3.add_child(WebCheckbox(value='TestCheckbox1',
                                                             mytype=['horizontal'],
                                                             checked=True)) as testcheckbox1:
                            pass
                        with test_obj3.add_child(WebCheckbox(value='TestCheckbox2',
                                                             mytype=['horizontal'])) as testcheckbox2:
                            pass

            with page.add_child(WebRow()) as r3_1:
                with r3_1.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c3_1:
                    with c3_1.add_child(WebBtn(name=GetValueBtn1, value='Get button group values')) as testbtn1:
                        pass
            with page.add_child(WebRow()) as r3_2:
                with r3_2.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c3_2:
                    with c3_2.add_child(WebHead5(name=ShowValue1)):
                        pass

            with page.add_child(WebBr()):
                pass
            with page.add_child(WebRow()) as r4:
                with r4.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c4:
                    with c4.add_child(WebHead3(value="WebBtnGroup() + "
                                                     "WebCheckbox() test:")):
                        pass
                    with c4.add_child(this_class(name=TEST_OBJ4)) as test_obj4:
                        with test_obj4.add_child(WebCheckbox(value='TestCheckbox3')) as testcheckbox3:
                            pass
                        with test_obj4.add_child(WebCheckbox(value='TestCheckbox4')) as testcheckbox4:
                            pass
            with page.add_child(WebRow()) as r5:
                with r5.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c5:
                    with c5.add_child(WebBtn(name=GetCkbxValueBtn, value='Get checkbox values')) as testbtn2:
                        pass
            with page.add_child(WebRow()) as r6:
                with r6.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c6:
                    with c6.add_child(WebHead5(name=ShowCkbxValue)):
                        pass

            with page.add_child(WebRow()) as dyn_title_r:
                with dyn_title_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_title_c:
                    with dyn_title_c.add_child(WebHead3(value='Dynamically create and add checkboxes in a WebBtnGroup:')):
                        pass

            with page.add_child(WebRow()) as dyn_r:
                with dyn_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_c:
                    with dyn_c.add_child(this_class(name=DYN_OBJ)) as dyn_obj:
                        dyn_checkboxes=['dynamic_checkbox1', 'dynamic_checkbox2', 'dynamic_checkbox3']
                        for dc in dyn_checkboxes:
                            with dyn_obj.add_child(WebCheckbox(name=dc, value=dc)):
                                pass

            with page.add_child(WebRow()) as dyn_btn_r:
                with dyn_btn_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_btn_c:
                    with dyn_btn_c.add_child(WebBtn(name=DYN_BTN, value='Get dynamic WebBtnGroup values')) as dyn_btn:
                        pass

            with page.add_child(WebRow()) as dyn_value_r:
                with dyn_value_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_value_c:
                    with dyn_value_c.add_child(WebHead5(name=DYN_VALUE)):
                        pass

            with page.add_child(WebBr()):
                pass
            with page.add_child(WebRow()) as dyn_backend_title_r:
                with dyn_backend_title_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_backend_title_c:
                    with dyn_backend_title_c.add_child(WebHead3(value='Dynamically create checkbox and button for button group on backend:')):
                        pass
            with page.add_child(WebRow()) as dyn_backend_r:
                with dyn_backend_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_backend_c:
                    with dyn_backend_c.add_child(this_class(name=DYN_BE_OBJ)) as dyn_be_obj:
                        pass

            with page.add_child(WebRow()) as dyn_backend_value_r:
                with dyn_backend_value_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_backend_value_c:
                    with dyn_backend_value_c.add_child(WebHead5(name=ShowDynBEValue)) as dyn_backend_value:
                        pass
            with page.add_child(WebBr()):
                pass
            with page.add_child(WebRow()) as dyn_backend_btn_r:
                with dyn_backend_btn_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_backend_btn_c:
                    with dyn_backend_btn_c.add_child(WebBtn(name=DYN_BE_BTN,
                                                            value='Get dynamic button group values')) as dyn_be_btn:
                        pass
                    with dyn_backend_btn_c.add_child(WebBtn(name=DYN_BE_REFRESH_BTN,
                                                            value='Dynamically refresh the button group on backend.')) \
                        as dyn_be_ref_btn:
                        pass

            with page.add_child(WebBr()):
                pass
            with page.add_child(WebRow()) as dyn_be_radio_r:
                with dyn_be_radio_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_be_radio_c:
                    with dyn_be_radio_c.add_child(WebHead3(value='Dynamic create radios for button group:')):
                        pass
            with page.add_child(WebRow()) as dyn_be_radio_r:
                with dyn_be_radio_r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as dyn_be_radio_c:
                    with dyn_be_radio_c.add_child(this_class(name=DYN_BE_RADIO_OBJ)) as dyn_be_radio_obj:
                        pass
            with page.add_child(WebBr()):
                pass
            with page.add_child(WebRow()) as dyn_be_radio_val_r:
                with dyn_be_radio_val_r.add_child(WebColumn(width=self.WIDTH,
                                                            offset=self.OFFSET)) as dyn_be_radio_val_c:
                    with dyn_be_radio_val_c.add_child(WebHead5(name=DYN_BE_RADIO_VALUE)) as dyn_be_radio_value:
                        pass
            with page.add_child(WebRow()) as dyn_be_radio_btn_r:
                with dyn_be_radio_btn_r.add_child(WebColumn(width=self.WIDTH,
                                                            offset=self.OFFSET)) as dyn_be_radio_btn_c:
                    with dyn_be_radio_btn_c.add_child(WebBtn(name=DYN_BE_RADIO_VAL_BTN,
                                                             value='Get values')) as dyn_be_radio_btn:
                        pass
                    with dyn_be_radio_btn_c.add_child(WebBtn(name=DYN_BE_RADIO_REF_BTN,
                                                             value='Refresh')) as dyn_be_radio_ref_btn:
                        pass

        def intro_events_impl(self):
            page = self
            test_obj_hor_ckbx = page._components[TEST_OBJ_HORIZON_CKBX]['obj']
            test_obj4 = page._components[TEST_OBJ4]['obj']
            dyn_obj = page._components[DYN_OBJ]['obj']
            dyn_be_obj = page._components[DYN_BE_OBJ]['obj']
            dyn_be_radio_obj = page._components[DYN_BE_RADIO_OBJ]['obj']

            getvalue_btn1 = page._components[GetValueBtn1]['obj']
            ckbx_value_btn = page._components[GetCkbxValueBtn]['obj']
            dyn_btn = page._components[DYN_BTN]['obj']
            dyn_be_btn = page._components[DYN_BE_BTN]['obj']
            dyn_be_ref_btn = page._components[DYN_BE_REFRESH_BTN]['obj']
            dyn_be_radio_ref_btn = page._components[DYN_BE_RADIO_REF_BTN]['obj']
            dyn_be_radio_val_btn = page._components[DYN_BE_RADIO_VAL_BTN]['obj']

            showvalue1 = page._components[ShowValue1]['obj']
            show_ckbx_value = page._components[ShowCkbxValue]['obj']
            show_dyn_value = page._components[DYN_VALUE]['obj']
            show_dyn_be_value = page._components[ShowDynBEValue]['obj']
            show_dyn_be_radio_value = page._components[DYN_BE_RADIO_VALUE]['obj']

            with getvalue_btn1.on_event_w('click'):
                with page.render_post_w():
                    test_obj_hor_ckbx.render_for_post()
                    showvalue1.render_for_post()
            with ckbx_value_btn.on_event_w('click'):
                with page.render_post_w():
                    test_obj4.render_for_post()
                    show_ckbx_value.render_for_post()
            with dyn_btn.on_event_w('click'):
                with page.render_post_w():
                    dyn_obj.render_for_post()
                    show_dyn_value.render_for_post()
            with dyn_be_btn.on_event_w('click'):
                with page.render_post_w():
                    dyn_be_obj.render_for_post()
                    show_dyn_be_value.render_for_post()
            with dyn_be_ref_btn.on_event_w('click'):
                with page.render_post_w():
                    dyn_be_ref_btn.render_for_post()
                    dyn_be_obj.render_for_post()

            with dyn_be_radio_ref_btn.on_event_w('click'):
                with page.render_post_w():
                    dyn_be_radio_ref_btn.render_for_post()
                    dyn_be_radio_obj.render_for_post()
            with dyn_be_radio_val_btn.on_event_w('click'):
                with page.render_post_w():
                    dyn_be_radio_obj.render_for_post()
                    show_dyn_be_radio_value.render_for_post()

        def on_my_render_impl(self, req):
            page = self

            testing_cls = page.testing_class
            testing_cls_name = testing_cls.__name__
            test3_value = ''
            test4_value = ''
            dyn_value = ''
            dyn_be_value = ''
            dyn_be_radio_val = ''
            new_dyn_be_value = None
            new_dyn_be_radio_val = None

            for r in req:
                if r['me'] == GetValueBtn1:
                    print('{} got request:{}'.format(GetValueBtn1, pprint.pformat(r)))
                elif r['me'] == GetCkbxValueBtn:
                    print('{} got request:{}'.format(GetCkbxValueBtn, pprint.pformat(r)))
                elif r['me'] == TEST_OBJ_HORIZON_CKBX:
                    print('{} got request:{}'.format(TEST_OBJ_HORIZON_CKBX, pprint.pformat(r)))
                    test_obj_ckbx = page._components[TEST_OBJ_HORIZON_CKBX]['obj']
                    test_obj_ckbx.request(req=r)
                    test3_value_=test_obj_ckbx.value()
                    for v in test3_value_:
                        if v['element_type'] == 'WebCheckbox':
                            test3_value += '{}:{},  '.format(v['label'],v['checked'])
                    test3_value = test3_value.rstrip()
                    test3_value = test3_value[:-1]
                elif r['me'] == TEST_OBJ4:
                    print('{} got reqeust:{}'.format(TEST_OBJ4, pprint.pformat(r)))
                    test_obj4 = page._components[TEST_OBJ4]['obj']
                    test_obj4.request(req=r)
                    test4_value_ = test_obj4.value()
                    for v in test4_value_:
                        if v['element_type'] == 'WebCheckbox':
                            test4_value += '{}:{},  '.format(v['label'],v['checked'])
                    test4_value = test4_value.rstrip()
                    test4_value = test4_value[:-1]
                elif r['me'] == ShowValue1:
                    print('{} got request:{}'.format(ShowValue1, pprint.pformat(r)))
                    showvalue_obj1 = page._components[ShowValue1]['obj']
                    showvalue_obj1.request(req=r)
                    showvalue_obj1.value(test3_value)
                    r['data'] = showvalue_obj1.response()['data']
                elif r['me'] == ShowCkbxValue:
                    print('{} got request:{}'.format(ShowCkbxValue, pprint.pformat(r)))
                    showvalue_obj2 = page._components[ShowCkbxValue]['obj']
                    showvalue_obj2.request(req=r)
                    showvalue_obj2.value(test4_value)
                    r['data'] = showvalue_obj2.response()['data']
                elif r['me'] == DYN_OBJ:
                    dyn_obj = page._components[DYN_OBJ]['obj']
                    print('{} got request:{}'.format(dyn_obj.name(), pprint.pformat(r)))
                    dyn_obj.request(req=r)
                    dyn_value = dyn_obj.value()
                elif r['me'] == DYN_VALUE:
                    dyn_value_obj = page._components[DYN_VALUE]['obj']
                    print('{} got request:{}'.format(dyn_value_obj.name(), pprint.pformat(r)))
                    dyn_value_obj.request(req=r)
                    if dyn_value:
                        dyn_value_obj.value(dyn_value)
                    r['data'] = dyn_value_obj.response()['data']
                elif r['me'] == DYN_BE_OBJ:
                    dyn_be_obj = page._components[DYN_BE_OBJ]['obj']
                    print('{} got request:{}'.format(dyn_be_obj.name(), pprint.pformat(r)))
                    dyn_be_obj.request(req=r)
                    dyn_be_value = dyn_be_obj.value()
                    if new_dyn_be_value:
                        dyn_be_obj.value(new_dyn_be_value)
                    r['data'] = dyn_be_obj.response()['data']
                elif r['me'] == ShowDynBEValue:
                    dyn_be_value_obj = page._components[ShowDynBEValue]['obj']
                    print('{} got request:{}'.format(dyn_be_value_obj.name(), pprint.pformat(r)))
                    dyn_be_value_obj.request(req=r)
                    value_info = 'VALUES: \n'
                    if dyn_be_value:
                        value_info += dyn_be_value
                        '''
                        
                        '''
                        value_info += '\n'
                        dyn_be_value_obj.value(value_info)
                    r['data'] = dyn_be_value_obj.response()['data']
                elif r['me'] == DYN_BE_REFRESH_BTN:
                    dyn_be_fre_btn = page._components[DYN_BE_REFRESH_BTN]['obj']
                    print('{} got request:{}'.format(dyn_be_fre_btn.name(), pprint.pformat(r)))
                    new_dyn_be_value = {'children': [
                                                        {
                                                            'element_type': 'WebCheckbox',
                                                            'value': 'checkbox1',
                                                            'checked': True
                                                        },
                                                        {
                                                            'element_type': 'WebCheckbox',
                                                            'value': 'checkbox2',
                                                            'checked': True
                                                        },
                                                        {
                                                            'element_type': 'WebBtn',
                                                            'value': 'button1',
                                                        }
                                                    ]
                                       }
                elif r['me'] == DYN_BE_RADIO_REF_BTN:
                    dyn_be_radio_ref_btn = page._components[DYN_BE_RADIO_REF_BTN]['obj']
                    print('{} got request:{}'.format(dyn_be_radio_ref_btn.name(), pprint.pformat(r)))
                    new_dyn_be_radio_val = \
                        {
                            'children':[
                                {
                                    'element_type':'WebBtnRadio',
                                    'items':[
                                                {
                                                    'element_type':'WebBtnRadio',
                                                    'label': 'Radio1',
                                                    'checked': True
                                                },
                                                {
                                                    'element_type': 'WebBtnRadio',
                                                    'label': 'Radio2',
                                                },
                                                {
                                                    'element_type': 'WebBtnRadio',
                                                    'label': 'Radio3'
                                                }
                                        ]
                                }
                            ]
                        }
                elif r['me'] == DYN_BE_RADIO_OBJ:
                    dyn_be_radio_obj = page._components[DYN_BE_RADIO_OBJ]['obj']
                    print('{} got request:{}'.format(dyn_be_radio_obj.name(), pprint.pformat(r)))
                    dyn_be_radio_obj.request(req=r)
                    dyn_be_radio_val = dyn_be_radio_obj.value()
                    if new_dyn_be_radio_val:
                        dyn_be_radio_obj.value(value=new_dyn_be_radio_val)
                    r['data'] = dyn_be_radio_obj.response()['data']
                elif r['me'] == DYN_BE_RADIO_VALUE:
                    dyn_be_radio_val_obj = page._components[DYN_BE_RADIO_VALUE]['obj']
                    print('{} got request:{}'.format(dyn_be_radio_val_obj.name(), pprint.pformat(r)))
                    dyn_be_radio_val_obj.request(req=r)
                    info = ''
                    if dyn_be_radio_val:
                        if 'children' in dyn_be_radio_val:
                            for child in dyn_be_radio_val['children']:
                                if child['element_type'] == 'WebBtnRadio':
                                    info += 'selected:'
                                    info += child['selected']
                                    if 'children' in child:
                                        info += ', children:{'
                                        for c in child['children']:
                                            info += 'label:'
                                            info += c['label']
                                            if 'checked' in c.keys():
                                                info += ',checked:'
                                                info += str(c['checked'])
                                            if child['children'].index(c) < len(child['children'])-1:
                                                info += ';'
                                        info +='}'
                    dyn_be_radio_val_obj.value(info)
                    r['data'] = dyn_be_radio_val_obj.response()['data']

            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request',
                        value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'test_'+cls.__name__
        page_html = TestPage.get_page(rule='/test_'+cls.__name__+'_request',
                                 name=title_name, title=title_name,top_menu=None)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class WebBtnDropdownTest(ClassTest):

    """
    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
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

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
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
    """
    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

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

        def on_my_render_impl(self, req):

            page = self
            if self.__class__.__name__ != 'WebPage':
                page = self._page
            testing_cls = page.testing_class
            testing_cls_name = testing_cls.__name__
            testing_obj = page._components[testing_cls_name]['obj']
            for r in req:
                if r['me'] == testing_cls_name:
                    print('{} got request:{}'.format(testing_obj.name(), pprint.pformat(r)))
            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl,self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl,self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl,self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html

'''
class WebBtnTest(ClassTest):

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))

        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def intro_events_impl(self):
            page = self
            testing_class = page.testing_class

            test_obj = page._components[testing_class.__name__]['obj']
            WebBtn = testing_class

            with page.render_post_w():
                test_obj.render_for_post()
            with test_obj.on_event_w('click'):
                test_obj.alert('"Please check server side to find \'Class testing, class WebBtn got req: ... \'"')
                with page.render_post_w():
                    test_obj.render_for_post()

        def on_my_events_impl(self, req):
            page = self._page
            testing_cls = page.testing_class
            testing_obj = self._components[testing_cls.__name__]['obj']
            for r in req:
                if r['me'] == testing_cls.__name__:
                    print('{} got request:{}'.format(testing_cls.__name__, pprint.pformat(r)))
                    testing_obj.request(r)
                    testing_obj.value('class {} testing'.format(testing_cls.__name__))
                    r['data'] = testing_obj.response()['data']

            return jsonify({'status':'success', 'data':req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))
                setattr(self, 'on_my_events_impl', types.MethodType(intro_events_impl, self))


        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request',
                        value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
'''

class WebInputTest(ClassTest):

    def class_test(self):
        return self.value(value='class {} from class test'.format(self.__class__.__name__))


class WebImgTest(ClassTest):

    def class_test(self):
        #req['data']['oovalue'] = url_for('static', filename='img/demo.jpg')
        return self.value(value={'oovalue':url_for('static', filename='img/demo.jpg')})


class WebSwitchTest(ClassTest):

    def class_test(self):
        return self.value(value={
            'checked': True,
            'onText': 'Display',
            'offText': 'Hide'
        })

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        TESTING_NAME = cls.__name__

        def intro_events_impl(self):
            page = self._page
            testing_obj = page._components[TESTING_NAME]['obj']
            row = page._components[self.ROW]['obj']
            hide_switch = page._components[self.HIDE_SWITCH]['obj']

            with testing_obj.on_event_w('switch'):
                testing_obj.alert('"switch state:"+state+", offColor will be changed to be warning on backend."')
                with page.render_post_w():
                    testing_obj.render_for_post()
            with hide_switch.on_event_w('switch'):
                row.toggle(state_name='state')

        def on_my_render_impl(self, req):
            page = self
            for r in req:
                if r['me'] == TESTING_NAME:
                    switch_obj = page._components[TESTING_NAME]['obj']
                    switch_obj.request(req=r)
                    switch_obj.value({
                        'onText': 'Display',
                        'offText': 'Hide',
                        'offColor': 'warning'
                    })
                    r['data'] = switch_obj.response()['data']
            return jsonify({'status':'success', 'data':req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request',
                        value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class WebBtnToggleTest(ClassTest):

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        test_obj = page._components['WebBtnToggle']['obj']
        with page.render_post_w():
            test_obj.render_for_post()
        with test_obj.on_event_w('click'):
            test_obj.alert('"Please check server side to find \'Class testing, class WebBtn got req: ... \'"')
            with page.render_post_w():
                test_obj.render_for_post()

'''
class WebBtnSwitchTest(ClassTest):

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def on_my_render_impl(self, req):
            page = self
            testing_class = page.testing_class
            test_obj = page._components[testing_class.__name__]['obj']
            for r in req:
                if r['me'] == testing_class.__name__:
                    print('{} got request:{}'.format(test_obj.name(), pprint.pformat(r)))
                    test_obj.request(req=r)
                    test_obj.check(checked=False)
                    r['data'] = test_obj.response()['data']
            return jsonify({'status': 'success', 'data': req})


        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                #setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))
                #setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))

        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request',
                        value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
'''


class WebCheckboxTest(ClassTest):

    '''
    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        test_obj = page._components['WebCheckbox']['obj']
        LVar = page._SUBCLASSES['LVar']['class']
        with test_obj.on_event_w('change'):
            with LVar(parent=self, var_name="data") as data:
                test_obj.val()
            test_obj.alert(' data + " clicked !"')
    '''

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def intro_events_impl(self):
            page = self
            test_class = page.testing_class
            test_obj = page._components[test_class.__name__]['obj']
            LVar = page._SUBCLASSES['LVar']['class']
            with test_obj.on_event_w('change'):
                with LVar(parent=self, var_name="data") as data:
                    test_obj.val()
                test_obj.alert(' data + " clicked! And the checkbox is unchecked by response always." ')
                with page.render_post_w():
                    test_obj.render_for_post()

        def on_my_render_impl(self, req):
            page = self
            testing_class = page.testing_class
            test_obj = page._components[testing_class.__name__]['obj']
            for r in req:
                if r['me'] == testing_class.__name__:
                    print('{} got request:{}'.format(test_obj.name(), pprint.pformat(r)))
                    test_obj.request(req=r)
                    print('{} got checked info:{}'.format(test_obj.label(), test_obj.check()))
                    test_obj.check(checked=False)
                    test_obj.label(label='Reset checkbox label by response')
                    r['data'] = test_obj.response()['data']
            return jsonify({'status': 'success', 'data':req})

        def place_components_impl(self):

            page = self

            testing_class = page.testing_class
            testing_cls_name = testing_class.__name__
            class_name = testing_class.__name__
            name_ = testing_cls_name

            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            default_width = ['md6', 'lg6']
            default_offset = ['mdo3', 'mdo3']
            page._url = '/test_' + testing_class.__name__ + '_request'
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=default_width, offset=default_offset, height='200px')) as c1:
                    with c1.add_child(testing_class(parent=c1,
                                                        name=name_,
                                                        value=name_,
                                                        icon='tag',
                                                        url='/' + testing_class.__name__ + '_test')) as test:
                        pass

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl,self))
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class WebSelectTest(ClassTest):

    '''
    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def events_action_for_class_test(self, req):
        print('Class testing, class {} got req:{}'.format(self.__class__.__name__, req['data']))
        req['data'] = {'options': [{'text': 'OptionResetByOnPost1'},
                                 {'text': 'OptionResetByOnPost2'},
                                 {'text': 'OptionResetByOnPost3', 'selected': 'true'}]}

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        test_obj = page._components['WebSelect']['obj']
        with page.render_post_w():
            test_obj.render_for_post()

        with test_obj.on_event_w('change'):
            test_obj.alert('"Testing works that \'OptionResetByOnPost3\' item is always slected."')
            with page.render_post_w():
                test_obj.render_for_post()

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
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
    '''

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def place_components_impl(self):
            page = self
            this_class = page.testing_class
            name_ = this_class.__name__
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=self.WIDTH,
                                            offset=self.OFFSET, height='200px')) as c1:
                    options = [{'text': 'option1'},
                               {'text': 'option2'},
                               {'selected': True, 'text': 'option3'}]
                    with c1.add_child(this_class(parent=page, name=name_, options=options)) as test:
                        pass

        def intro_events_impl(self):
            page = self
            testing_cls = page.testing_class
            test_obj = page._components[testing_cls.__name__]['obj']
            with page.render_post_w():
                test_obj.render_for_post()

            with test_obj.on_event_w('change'):
                test_obj.alert('"Testing works that \'OptionResetByOnPost3\' item is always slected."')
                with page.render_post_w():
                    test_obj.render_for_post()

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html

    def class_test(self):
        options = [
                    {'text': 'OptionResetByOnPost1'},
                    {'text': 'OptionResetByOnPost2'},
                    {'text': 'OptionResetByOnPost3', 'selected': 'true'}
                  ]

        response = self._vtable[ooccd.RESPONSE_MEMBER]._response
        if 'data' in response:
            response['data']['options'] = options
        else:
            response['data'] = {'options': options}


class WebDatalistTest(ClassTest):

    '''
    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
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

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        input = page._components['test_input']['obj']
        test_obj = page._components['WebDatalist']['obj']
        with page.render_post_w():
            test_obj.render_for_post()

        with input.on_event_w(event='keydown', filter=13):
            with page.render_post_w():
                test_obj.render_for_post()

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def events_action_for_class_test(self, req):
        print('Class testing, WebDatalist got req:{}'.format(req['data']))

        options = [{'text': 'OptionResetByOnPost1'},
                   {'text': 'OptionResetByOnPost2'},
                   {'text': 'OptionResetByOnPost3', 'selected': 'true'}]
        req['data'] = {'options': options}
    '''

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def place_components_impl(self):
            page = self
            this_class = page.testing_class
            TEST_ID = 'test_id'
            INPUT_NAME = 'test_input'
            name_ = this_class.__name__
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            WebInput = page._SUBCLASSES['WebInput']['class']
            with page.add_child(WebRow(name=self.ROW)) as r1:
                with r1.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET, height='200px')) as c1:
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

        def on_my_render_impl(self, req):
            page = self
            testing_obj = page._components['WebDatalist']['obj']
            for r in req:
                if r['me'] == 'WebDatalist':
                    print('{} got request:{}'.format(testing_obj.name(), pprint.pformat(r)))
                    testing_obj.request(r)
                    testing_obj.class_test()
                    r['data'] = testing_obj.response()['data']

            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl,self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl,self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl,self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class WebUlTest(ClassTest):

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
        page = self
        cls = page.testing_class
        name = cls.__name__
        item1 = 'item1'
        item2 = 'item2'
        item3 = 'item3'
        WebRow = page._SUBCLASSES['WebRow']['class']
        WebColumn = page._SUBCLASSES['WebColumn']['class']
        with page.add_child(WebRow()) as r1:
            with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='200px')) as c1:
                with c1.add_child(cls(parent=page, value="WebUl", name=name, ul_list=[
                    {'name': item1, 'href': '#' + item1, 'active': True},
                    {'name': item2, 'href': '#' + item2},
                    {'name': item3, 'href': '#' + item3}
                ])) as test:
                    pass

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def events_action_for_class_test(self, req):
        data  = '' if 'data' not in req else req['data']
        print('Class testing, class {} got req:{}'.format(self.__class__.__name__, data))
        req['data'] = {'oovalue': '{} Testing from event_action on server side'.format(self.__class__.__name__)}


class OOGeneralSelectorTest(ClassTest):
    testing_cls_name = 'OOGeneralSelector'

    '''
    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
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

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
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

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def events_action_for_class_test(self, req):
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
    '''

    @classmethod
    def test_request(cls, methods=['GET']):

        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

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

        def on_my_render_impl(self, req):
            page = self._page
            testing_cls = page.testing_class
            OOGeneralSelector = testing_cls
            testing_obj = page._components[testing_cls.__name__]['obj']
            for r in req:
                if r['me'] == testing_cls.__name__:
                    print('{} got request:{}'.format(testing_obj.name(), pprint.pformat(r)))
                    testing_obj.request(r)
                    response = testing_obj.response()
                    response['data'] = OOGeneralSelector._example_data()
                    for d in response['data']:
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
                    r['data'] = response['data']
            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl,self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl,self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl,self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class OODatePickerSimpleTest(ClassTest):
    testing_cls_name = 'OODatePickerSimple'

    '''
    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
        page = self
        this_class = page.testing_class
        name = this_class.__name__
        with page.add_child(
                this_class(name=name, radius={'tl': '8px', 'tr': '5px', 'br': '9px', 'bl': '5px'},
                                        width="500px")) as test1:
            pass

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        test_obj = self._components['OODatePickerSimple']['obj']

        with test_obj.on_event_w('switch'):
            with page.render_post_w():
                test_obj.render_for_post(trigger_event=False)

        with page.render_post_w():
            test_obj.render_for_post(trigger_event=False)

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def events_action_for_class_test(self, req):
        r = req
        lang = r['data']['lang']
        format_ = None
        cls = self.__class__
        if r['data']['select'] == '周':
            start = None if not r['data']['viewDate'] else r['data']['viewDate'].split('T')[0]
            if start:
                # USE cls FORMATS here
                print('OODatepickerSimple got week start: {}'.format(start))
                format_ = cls.FORMATS[lang]['week']['to_format']
                #dt = datetime.datetime.strptime(start, "%Y-%m-%d")
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
                    format_ = cls.DAY_FORMAT_ZH[1]
                else:
                    format_ = cls.DAY_FORMAT_EN[1]
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
                    format_ = cls.MONTH_FORMAT_ZH[1]
                else:
                    format_ = cls.MONTH_FORMAT_EN[1]
                try:
                    dt = datetime.datetime.strptime(start, format_).timestamp()
                except ValueError:
                    dt = datetime.datetime.today().timestamp()
            else:
                dt = datetime.datetime.today().timestamp()
            r['data']['date'] = int(dt)
    '''
    @classmethod
    def test_request(cls, methods=['GET']):
        # Create a testing page containing the component tested
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def place_components_impl(self):
            page = self
            this_class = page.testing_class
            name = this_class.__name__
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            with page.add_child(WebRow()) as r:
                with r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c:
                    with c.add_child(this_class(name=name, width="500px")) as test_obj:
                        pass

        def intro_events_impl(self):
            page = self
            test_obj = self._components['OODatePickerSimple']['obj']

            with test_obj.on_event_w('switch'):
                with page.render_post_w():
                    test_obj.render_for_post(trigger_event=False)

            with page.render_post_w():
                test_obj.render_for_post(trigger_event=False)

        def on_my_render_impl(self, req):
            page = self._page
            test_cls = page.testing_class
            testing_obj = page._components[test_cls.__name__]['obj']
            for r in req:
                if r['me'] == test_cls.__name__:
                    print('{} got request:{}'.format(testing_obj.name(), pprint.pformat(r)))
                    lang = r['data']['lang']
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
                req[req.index(r)] = r
            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class OODatePickerIconTest(ClassTest):
    testing_cls_name = 'OODatePickerIcon'

    '''
    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        test_obj = self._components['OODatePickerIcon']['obj']
        with page.render_post_w():
            test_obj.render_for_post()

        with test_obj.on_event_w('change'):
            with page.render_post_w():
                test_obj.render_for_post()

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def events_action_for_class_test(self, req):
        r = req
        cls = self.__class__
        if r['data']['date']:
            dt = cls.get_dates(_data=r['data'])
            print('OODatePickerIcon testing: got dates: {} ~ {}'.format(
                pprint.pformat(dt[0]), pprint.pformat(dt[1]))
            )
            cls.get_ret_stamp(r['data'])

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
        page = self
        WebRow = page._SUBCLASSES['WebRow']
        WebColumn = page._SUBCLASSES['WebColumn']
        
        this_class = page.testing_class
        testing_cls_name = this_class.testing_cls_name if hasattr(this_class, 'testing_cls_name') else \
            this_class.__name__
        name = testing_cls_name
        with page.add_child(WebRow()) as r:
            with r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c:
                with c.add_child(this_class(name=name)) as test:
                    pass
        with ooccd.MetisTransform.transform_w(component=test, vptr=ooccd.ACTION_MEMBER):
            test.call_custom_func(fname=test.start_func_name,
                              fparams={'that': '$("#{}")'.format(test.id()),
                                       'type': '"{}"'.format(test.VIEWS['week'])})
    '''

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def place_components_impl(self):
            page = self
            this_class = page.testing_class
            testing_cls_name = this_class.testing_cls_name if hasattr(this_class, 'testing_cls_name') else \
                this_class.__name__
            name = testing_cls_name
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            with page.add_child(WebRow()) as r:
                with r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c:
                    with c.add_child(this_class(name=name)) as test_obj:
                        pass

        def intro_events_impl(self):
            page = self
            test_obj = self._components['OODatePickerIcon']['obj']
            test_obj.call_custom_func(fname=test_obj.start_func_name,
                                  fparams={'that': '$("#{}")'.format(test_obj.id()),
                                           'type': '"{}"'.format(test_obj.VIEWS['week'])})
            with page.render_post_w():
                test_obj.render_for_post()

            with test_obj.on_event_w('change'):
                with page.render_post_w():
                    test_obj.render_for_post()

        def on_my_render_impl(self, req):
            page = self._page
            test_cls = page.testing_class
            testing_obj = page._components[test_cls.__name__]['obj']
            for r in req:
                if r['me'] == test_cls.__name__:
                    print('{} got request:{}'.format(testing_obj.name(), pprint.pformat(r)))
                    dt = cls.get_dates(_data=r['data'])
                    print('OODatePickerIcon testing: got dates: {} ~ {}'.format(
                        pprint.pformat(dt[0]), pprint.pformat(dt[1]))
                    )
                    cls.get_ret_stamp(r['data'])
                req[req.index(r)] = r
            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request',
                        value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class OODatePickerRangeTest(ClassTest):
    testing_cls_name = 'OODatePickerRange'

    '''
    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        this_obj = page._components[page.testing_class.testing_cls_name]['obj']
        this_class = this_obj.__class__

        with this_obj.on_event_w('change'):
            with page.render_post_w():
                this_obj.render_for_post()

        with page.render_post_w():
            this_obj.render_for_post()

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def events_action_for_class_test(self, req):
        page = self._page
        test_obj = self
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
    '''

    @classmethod
    def test_request(cls, methods=['GET']):

        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

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
                start = datetime.strptime('2020-1-1', '%Y-%m-%d')
            else:
                try:
                    start = test_obj.get_dt(type=r['data']['select'], dt_str=start, format=format)
                except ValueError:
                    start = datetime.strptime('2020-1-1', '%Y-%m-%d')

            end = None if not r['data']['end'] else r['data']['end']
            if not end:
                # end = None if not r['data']['end_viewDate'] else r['data']['end_viewDate'].split('T')[0]
                end = datetime.strptime('2020-12-31', '%Y-%m-%d')
            else:
                try:
                    end = test_obj.get_dt(type=r['data']['select'], dt_str=end, format=format)
                except ValueError:
                    end = datetime.strptime('2020-12-31', '%Y-%m-%d')

            r['data']['start'] = int(start.timestamp())
            r['data']['start_viewDate'] = start.strftime('%Y-%m-%dT')
            r['data']['end'] = int(end.timestamp())
            r['data']['end_viewDate'] = end.strftime("%Y-%m-%dT")

        def on_my_render_impl(self, req):
            page = self
            test_cls = page.testing_class
            test_obj = page._components[test_cls.__name__]['obj']
            for r in req:
                if r['me'] == test_cls.__name__:
                    print('{} got request:{}'.format(test_obj.name(), pprint.pformat(r)))
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
                    req[req.index(r)] = r
            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl,self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl,self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl,self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class OOBannerTest(ClassTest):
    testing_cls_name = 'OOBanner'

    def class_test(self):
        Page = self._PAGE_CLASS
        FormatBootstrap = Page._SUBCLASSES['FormatBootstrap']['class']
        banner = self._get_banner()
        new_html = render_template_string(FormatBootstrap.CAROUSEL_HTML, banner=banner)
        self.value({'html': new_html})

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def events_action_for_class_test(self, req):
        print('Class testing, class {} got req:{}'.format(self.__class__.__name__, req['data']))
        banner = self._get_banner()
        new_html = render_template_string(self.CAROUSEL_HTML,
                                          banner=banner)
        req['data']['html'] = new_html


class OOCalendarTest(ClassTest):

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
        page = self
        TITLE = 'title'
        this_class = page.testing_class
        NAME = this_class.testing_cls_name if hasattr(this_class, 'testing_cls_name') else this_class.__name__
        WebRow = page._SUBCLASSES['WebRow']['class']
        WebColumn = page._SUBCLASSES['WebColumn']['class']
        WebHead2 = page._SUBCLASSES['WebHead2']['class']
        OOCalendarBar = page._SUBCLASSES['OOCalendarBar']['class']
        WebBr = page._SUBCLASSES['WebBr']['class']
        with page.add_child(WebRow()) as r0:
            with r0.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c0:
                with c0.add_child(WebHead2(name=TITLE)) as title:
                    pass
        with page.add_child(WebRow()) as r1:
            with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c1:
                with c1.add_child(OOCalendarBar()) as bar:
                    pass
        with page.add_child(WebRow()) as r2:
            with r2.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c2:
                with c2.add_child(this_class(name=NAME,
                                             url='/test_' + this_class.__name__ + '_request')) as calendar:
                    pass
        with page.add_child(WebBr()):
            pass

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        title = page._components['title']['obj']
        testing_class = page.testing_class
        testing_name = testing_class.testing_cls_name if hasattr(testing_class, 'testing_cls_name') else \
            testing_class.__name__
        calendar = page._components[testing_name]['obj']

        with page.render_post_w():
            calendar.render_for_post()
            title.render_for_post()

        with calendar.on_event_w('change'):
            calendar.alert('"Calendar changed!"')
            with page.render_post_w():
                calendar.render_for_post()
                title.render_for_post()

    '''
    @classmethod
    def test_request(cls, methods=['GET']):
        # Create a testing page containing the component tested
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        class_name = cls.__name__

        PageClass = cls._PAGE_CLASS
        page = PageClass(app=current_app, url='/' + cls.__name__ + '_test')

        page.place_components = types.MethodType(
            cls.place_components_for_class_test, page)
        page.place_components(testing_class=cls)

        page.events_trigger = types.MethodType(PageClass.events_trigger_for_class_test, page)
        this_obj = page._components[class_name]
        this_obj.events_trigger = types.MethodType(this_obj.__class__.events_trigger_for_class_test, this_obj)

        page.init_on_post(app=current_app,
                          on_post=page._components[class_name].on_post_for_class_test,
                          endpoint=cls.__name__ + '_test',
                          url='/' + cls.__name__ + '_test')

        html = page.render()
        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
    '''

    '''
    @classmethod
    def test_request(cls, methods=['GET']):

        NAME = 'calendar'
        TITLE = 'title'

        def on_post():

            req_ = WebPage.on_post()
            title_ = '时间标题'
            for r in req_:
                if r['me'] == NAME:

                    start_ = datetime.fromtimestamp(int(r['data']['start']) / 1000)
                    end_ = datetime.fromtimestamp(int(r['data']['end']) / 1000)
                    title_ = r['data']['title']
                    view_ = r['data']['view']
                    r['data']['hierarchy'] = "test_hierarchy"

                elif r['me'] == TITLE:

                    r['data'] = {'text': title_}

                elif r['me'].find(components_client.OOCalendar.ME_PRE) == 0:

                    # Return data   directly, for the OOCalendar buildin requests,
                    #   needn't {'me':xxx, 'data':xxx} anymore

                    req_ = OOCalendar.on_post(r)['data']
                    break

            return jsonify({'status': 'success', 'data': req_})

        class Page(WebPage):

            URL = '/OOCalendar_test_post'

            def type_(self):
                return 'WebPage'

        Page.init_page(app=current_app, endpoint=cls.__name__ + '.test', on_post=on_post)

        with Page(app=current_app, on_post=on_post, on_post_endpoint=cls.__name__ + '_test') as page:
            with page.add_child(WebRow()) as r0:
                with r0.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c0:
                    with c0.add_child(WebHead2(name=TITLE)) as title:
                        pass
            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c1:
                    with c1.add_child(OOCalendarBar()) as bar:
                        pass
            with page.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=['md8'], offset=['mdo2'])) as c2:
                    with c2.add_child(globals()[cls.__name__](name=NAME)) as calendar:
                        pass
            with page.add_child(WebBr()):
                pass

        html = page.render()
        return render_template_string(html)
    '''
    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def on_post_for_class_test(self):
        NAME = self.testing_cls_name if hasattr(self, 'testing_cls_name') else self.__class__.__name__
        TITLE = 'title'
        WebPage = self._PAGE_CLASS
        req_ = None
        if hasattr(self._page, '_action'):
            req_ = self._page._action.on_post()
        else:
            req_ = self._page.on_post()
        title_ = '时间标题'
        OOCalendar = self.__class__
        for r in req_:
            if r['me'] == NAME:

                start_ = datetime.datetime.fromtimestamp(int(r['data']['start']) / 1000)
                end_ = datetime.datetime.fromtimestamp(int(r['data']['end']) / 1000)
                title_ = r['data']['title']
                view_ = r['data']['view']
                r['data']['hierarchy'] = "test_hierarchy"

            elif r['me'] == TITLE:

                r['data'] = {'text': title_}

            elif r['me'].find(OOCalendar.ME_PRE) == 0:

                # Return data   directly, for the OOCalendar buildin requests,
                #   needn't {'me':xxx, 'data':xxx} anymore

                req_ = OOCalendar.on_post_builtin(r)['data']
                break

        return jsonify({'status': 'success', 'data': req_})

    """
    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def place_components_impl(self):
            page = self
            this_class = page.testing_class
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            WebHead2 = page._SUBCLASSES['WebHead2']['class']
            OOCalendarBar = page._SUBCLASSES['OOCalendarBar']['class']
            WebBr = page._SUBCLASSES['WebBr']['class']

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

            # req_ = self.on_post()
            OOCalendar = self._SUBCLASSES['OOCalendar']['class']
            title_ = '时间标题'
            req_ = req
            for r in req_:
                if r['me'] == self.TestName:
                    print('{} got request:{}'.format(self.TestName, pprint.pformat(r)))
                    start_ = datetime.datetime.fromtimestamp(int(r['data']['start']) / 1000)
                    end_ = datetime.datetime.fromtimestamp(int(r['data']['end']) / 1000)
                    title_ = r['data']['title']
                    view_ = r['data']['view']
                    r['data']['hierarchy'] = "test_hierarchy"

                elif r['me'] == self.TestTitleName:
                    print('{} got request:{}'.format(self.TestTitleName, r))
                    r['data'] = {'text': title_}

                elif r['me'].find(OOCalendar.ME_PRE) == 0:
                    print('{} got request:{}'.format(OOCalendar.ME_PRE, r))
                    # Return data   directly, for the OOCalendar buildin requests,
                    #   needn't {'me':xxx, 'data':xxx} anymore

                    req_ = OOCalendar.on_post_builtin(r)['data']
                    break

            return jsonify({'status': 'success', 'data': req_})

        class TestPage(cls._PAGE_CLASS):

            TestName = 'OOCalendarTest'
            TestTitleName = 'OOCalendarTitleTest'
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl,self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl,self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl,self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html
    """

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def place_components_impl(self):
            page = self
            OOCalendar = page._SUBCLASSES['OOCalendar']['class']
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebBr = page._SUBCLASSES['WebBr']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            WebHead2 = page._SUBCLASSES['WebHead2']['class']
            OOCalendarBar = page._SUBCLASSES['OOCalendarBar']['class']

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
            page = self
            OOCalendar = page._SUBCLASSES['OOCalendar']['class']
            # req_ = self.on_post()
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

        class TestPage(cls._PAGE_CLASS):

            TestName = 'OOCalendarTest'
            TestTitleName = 'OOCalendarTitleTest'

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl,self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl,self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl,self))
        '''
        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class WebTabTest(ClassTest):

    '''
    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
        page = self
        testing_class = page.testing_class
        cls = testing_class
        tab_name = testing_class.testing_cls_name if hasattr(testing_class, 'testing_cls_name') else \
            testing_class.__name__
        tab_contain_name = 'tab_contain_test'
        tab_item1_name = 'tab_item1'
        tab_item2_name = 'tab_item2'
        tab_item3_name = 'tab_item3'
        tab_contain1_name = 'tab_contain1'
        tab_contain2_name = 'tab_contain2'
        tab_contain3_name = 'tab_contain3'
        WebRow = page._SUBCLASSES['WebRow']['class']
        WebColumn = page._SUBCLASSES['WebColumn']['class']
        WebTabContain = page._SUBCLASSES['WebTabContain']['class']
        WebTabItem = page._SUBCLASSES['WebTabItem']['class']
        WebHead3 = page._SUBCLASSES['WebHead3']['class']
        with page.add_child(WebRow()) as r1:
            with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='200px')) as c1:
                with c1.add_child(cls(parent=page, name=tab_name, ul_list=[
                    {'name': tab_item1_name, 'href': '#' + tab_item1_name},
                    {'name': tab_item2_name, 'href': '#' + tab_item2_name},
                    {'name': tab_item3_name, 'href': '#' + tab_item3_name, 'active': True},
                ])) as test:
                    pass
                with c1.add_child(WebTabContain(parent=page, name=tab_contain_name)) as contain:
                    with contain.add_child(WebTabItem(id=tab_item1_name, name=tab_item1_name)) as item1:
                        with item1.add_child(WebHead3(name=tab_contain1_name, value=tab_contain1_name)) as contain1:
                            pass
                    with contain.add_child(WebTabItem(id=tab_item2_name, name=tab_item2_name)) as item2:
                        with item2.add_child(WebHead3(name=tab_contain2_name, value=tab_contain2_name)) as contain2:
                            pass
                    with contain.add_child(
                            WebTabItem(id=tab_item3_name, name=tab_item3_name, ootype=['active'])) as item3:
                        with item3.add_child(WebHead3(name=tab_contain3_name, value=tab_contain3_name)) as contain3:
                            pass

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        tab_contain_name = 'tab_contain_test'
        tab_item1_name = 'tab_item1'
        tab_item2_name = 'tab_item2'
        tab_item3_name = 'tab_item3'
        tab_contain1_name = 'tab_contain1'
        tab_contain2_name = 'tab_contain2'
        tab_contain3_name = 'tab_contain3'

        page = self
        testing_class = page.testing_class
        testing_cls_name = page.testing_class.testing_cls_name if hasattr(testing_class, 'testing_cls_name') else \
            testing_class.__name__
        test = page._components[testing_cls_name]['obj']
        contain = page._components[tab_contain_name]['obj']

        with page.render_post_w():
            test.render_for_post()
            contain.render_for_post()

        with test.on_event_w(event='active_change'):
            with page.render_post_w():
                test.render_for_post()
                contain.render_for_post()

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def on_post_for_class_test(self):
        tab_name = self.testing_cls_name if hasattr(self, 'testing_cls_name') else self.__class__.__name__
        tab_contain_name = 'tab_contain_test'
        tab_item1_name = 'tab_item1'
        tab_item2_name = 'tab_item2'
        tab_item3_name = 'tab_item3'
        tab_contain1_name = 'tab_contain1'
        tab_contain2_name = 'tab_contain2'
        tab_contain3_name = 'tab_contain3'
        WebPage = self._PAGE_CLASS
        req = None
        if hasattr(self._page, '_action'):
            req = self._page._action.on_post()
        else:
            req = self._page.on_post()
        for r in req:
            if r['me'] == tab_name:
                print('Got tab active item: {}'.format(r['data']))
                r['data'] = tab_item2_name
            if r['me'] == tab_contain_name:
                print('Got tab contain active page: {}'.format(r['data']))
                r['data'] = tab_item2_name
        return jsonify({'status': 'success', 'data': req})
    '''

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def place_components_impl(self):
            page = self
            testing_class = page.testing_class
            cls = testing_class

            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            WebTabContain = page._SUBCLASSES['WebTabContain']['class']
            WebTabItem = page._SUBCLASSES['WebTabItem']['class']
            WebHead3 = page._SUBCLASSES['WebHead3']['class']
            WebBtn = page._SUBCLASSES['WebBtn']['class']

            with page.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md8','lg8'], offset=['mdo2','lgo2'], height='200px')) as c1:
                    with c1.add_child(cls(parent=page, name=self.tab_name, ul_list=[
                        {'name': self.tab_item1_name, 'href': '#' + self.tab_item1_name, 'active': True},
                        {'name': self.tab_item2_name, 'href': '#' + self.tab_item2_name},
                        {'name': self.tab_item3_name, 'href': '#' + self.tab_item3_name},
                    ])) as test:
                        pass
                    with c1.add_child(WebTabContain(parent=page, name=self.tab_contain_name)) as contain:
                        with contain.add_child(WebTabItem(
                                id=self.tab_item1_name,
                                name=self.tab_item1_name,
                                mytype=['active'])) as item1:
                            with item1.add_child(WebHead3(
                                    value=self.tab_contain1_name)) as contain1:
                                pass
                        with contain.add_child(WebTabItem(
                                id=self.tab_item2_name,
                                name=self.tab_item2_name)) as item2:
                            with item2.add_child(WebHead3(
                                    value=self.tab_contain2_name)) as contain2:
                                pass
                        with contain.add_child(WebTabItem(
                                id=self.tab_item3_name,
                                name=self.tab_item3_name)) as item3:
                            with item3.add_child(WebHead3(
                                    value=self.tab_contain3_name)) as contain3:
                                pass

            with page.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=['md8','lg8'], offset=['mdo2','lgo2'])) as c2:
                    with c2.add_child(WebBtn(name=self.DEL_BTN, value='Remove tab_item3')) as dyn_btn:
                        pass
                    with c2.add_child(WebBtn(name=self.ADD_BTN, value='Add head3 in item_item2')) as add_btn:
                        pass

        def intro_events_impl(self):

            page = self
            testing_class = page.testing_class

            test = page._components[self.tab_name]['obj']
            contain = page._components[self.tab_contain_name]['obj']
            del_btn = page._components[self.DEL_BTN]['obj']
            add_btn = page._components[self.ADD_BTN]['obj']

            with page.render_post_w():
                test.render_for_post(return_parts=['html'])
                contain.render_for_post(return_parts==['html'])

            with test.on_event_w(event='active_change'):
                with page.render_post_w():
                    test.render_for_post(return_parts=['html'])
                    contain.render_for_post(return_parts=['html'])

            with del_btn.on_event_w(event='click'):
                with page.render_post_w():
                    del_btn.render_for_post()
                    test.render_for_post(return_parts=['html'])
                    contain.render_for_post(return_parts=['html'])

            with add_btn.on_event_w(event='click'):
                with page.render_post_w():
                    add_btn.render_for_post()
                    test.render_for_post(return_parts=['html'])
                    contain.render_for_post(return_parts=['html'])

        def on_my_render_impl(self, req):
            page = self._page
            WebHead3 = page._SUBCLASSES['WebHead3']['class']
            WebTabItem = page._SUBCLASSES['WebTabItem']['class']
            del_btn = page._components[self.DEL_BTN]['obj']
            add_btn = page._components[self.ADD_BTN]['obj']
            dyn_update = False
            add_update = False
            for r in req:
                if r['me'] == self.tab_name:
                    #print('{} got tab active item: {}'.format(self.tab_name, pprint.pformat(r['data'])))
                    tab_obj = self._components[self.tab_name]['obj']
                    tab_obj.request(r)
                    if dyn_update:
                        tab_obj.remove_child(child_name=self.tab_item3_name)
                        new_html = tab_obj.render(children_only=True)['html']
                        tab_obj.html(new_html)
                    if add_update:
                        tab_obj.add_child(child={'name':self.tab_item4_name,
                                                  'href':self.tab_item4_name})
                        new_html = tab_obj.render(children_only=True)['html']
                        tab_obj.html(new_html)
                    #tab_obj.active_item(self.tab_item1_name)
                    r['data']=tab_obj.response()['data']

                elif r['me'] == self.tab_contain_name:
                    #print('{} got tab contain active page: {}'.format(self.tab_contain1_name, pprint.pformat(r['data'])))
                    tab_con_obj = page._components[self.tab_contain_name]['obj']
                    tab_con_obj.request(r)
                    if dyn_update:
                        tab_con_obj.remove_child(child_name=self.tab_item3_name)
                        children_html = tab_con_obj.render(children_only=True)['html']
                        tab_con_obj.html(children_html)
                    if add_update:
                        with tab_con_obj.add_child(WebTabItem(id=self.tab_item4_name,
                                                              name=self.tab_item4_name,)) as item4:
                            with item4.add_child(WebHead3(value=self.tab_contain4_name)) as contain4:
                                pass
                        children_html = tab_con_obj.render(children_only=True)['html']
                        tab_con_obj.html(children_html)
                    #tab_con_obj.active_item(self.tab_item1_name)
                    r['data']=tab_con_obj.response()['data']

                elif r['me'] == self.DEL_BTN:
                    print('Got {} request:{}'.format(self.DEL_BTN, r))
                    dyn_update = True

                elif r['me'] == self.ADD_BTN:
                    add_update = True

            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):

            tab_name = 'WebTabTest'
            tab_contain_name = 'tab_contain_test'
            tab_item1_name = 'tab_item1'
            tab_item2_name = 'tab_item2'
            tab_item3_name = 'tab_item3'
            tab_item4_name = 'tab_item4'
            tab_contain1_name = 'tab_contain1'
            tab_contain2_name = 'tab_contain2'
            tab_contain3_name = 'tab_contain3'
            tab_contain4_name = 'tab_contain4'

            DEL_BTN = 'del_btn'
            ADD_BTN = 'add_btn'

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl,self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl,self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl,self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request', value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class WebTableTest(ClassTest):

    testing_cls_name = 'WebTable'

    @classmethod
    def example_data(cls, schema_only=False):
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
                    {'data': _getStr(random.randint(3, 6)), 'attr': 'nowrap data-ootable-details="This is event name"'},
                    {'data': approve, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                    {'data': done, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                    {'data': check, 'attr': "disabled=\"disabled\"" if random.randint(0, 1) else ""},
                    {'data': start, 'attr': 'data-ootable-details="This is start date time"'},
                    {'data': end, 'attr': 'data-ootable-details="This is end date time"'},
                    {'data': _getStr(random.randint(10, 128)), 'attr': 'data-ootable-details="This is details"'}
                )
            )

        return ' '.join(cls.html(data))

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self, **kwargs):
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

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        testing_cls_name = page.testing_class.testing_cls_name
        test = page._components[testing_cls_name]['obj']

        with page.render_post_w():
            test.render_for_post()

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def on_post_for_class_test(self):

        WebPage = self._PAGE_CLASS
        test_obj = self._page._components[self.testing_cls_name]['obj']
        req = None
        if hasattr(self._page, '_action'):
            req = self._page._action.on_post()
        else:
            req = self._page.on_post()
        for r in req:
            if r['me'] == self.testing_cls_name:
                print('Got WebTable request data: {}'.format(r['data']))
                r['data'] = {'html': self.example_data()}

        return jsonify({'status': 'success', 'data': req})

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        Page = cls._PAGE_CLASS
        WebTable = Page._SUBCLASSES['WebTable']['class']

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

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))

        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class OOTableTest(ClassTest):

    testing_cls_name = 'OOTable'
    testing_cls_name2 = 'OOTable2'
    testing_cls_name3 = 'OOTable3'

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        WebTable = None
        for bc in cls.__bases__:
            if bc.__name__ == 'WebTable':
                WebTable = bc

        OOTable = cls

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
                WebRow = page._SUBCLASSES['WebRow']['class']
                WebColumn = page._SUBCLASSES['WebColumn']['class']
                WebBr = page._SUBCLASSES['WebBr']['class']

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

                for r in req:
                    if r['me'] == self.TEST_NAME1:
                        print('{} got request: {}'.format(self.TEST_NAME1, pprint.pformat(r)))
                        r['data'] = self.example_data(type='img')
                    elif r['me'] == self.TEST_NAME2:
                        print('{} got request:{}'.format(self.TEST_NAME2, pprint.pformat(r)))
                        r['data'] = self.example_data(type='chart')
                    elif r['me'] == self.TEST_NAME3:
                        print('{} got request:{}'.format(self.TEST_NAME3, pprint.pformat(r)))
                        r['data'] = self.example_data(type=None)

                return jsonify({'status': 'success', 'data': req})

        '''
        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class OOTagGroupTest(ClassTest):

    def example_setting(self):
        return {
            'paging': False,
            'scrollY': '500px',
            'scrollX': True,
            'searching': True,
            'scrollCollapse': True,
        }

    def example_data(self, schema_only=False):
        page = self._page
        WebCheckbox = page._SUBCLASSES['WebCheckbox']['class']
        OOTable = page._SUBCLASSES['OOTable']['class']

        data = {
            'schema': [],
            'records': []
        }

        for j in range(self.COL_NUM):
            data['schema'].append({"name": ""})

        for i in range(2):
            approve = True if random.randint(0, 1) else False
            done = True if random.randint(0, 1) else False
            check = True if random.randint(0, 1) else False

            start, end = randDatetimeRange()
            td = []
            for i in range(len(data['schema'])):
                with WebCheckbox(   page='no page',
                                    value=_getStr(random.randint(2, 5)),
                                    checked=True
                                 ) as locals()["wc" + str(i)]:
                    pass
                locals()['wc' + str(i)].set_api()
                wc_content = locals()['wc' + str(i)].render_content()
                td.append({"data": wc_content['content'], "attr": "nowrap"})
                del locals()['wc' + str(i)]
            data['records'].append(td)
        return {'html': OOTable.html(data), 'setting':self.example_setting()}

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        testing_btn = 'testing_btn'

        def place_components_impl(self):
            page = self
            testing_class = page.testing_class
            WebBtn = page._SUBCLASSES['WebBtn']['class']
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            WebBr = page._SUBCLASSES['WebBr']['class']

            with page.add_child(WebRow()) as r:
                with r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c:
                    with c.add_child(testing_class(name=testing_class.__name__)) as testing_obj:
                        pass
            with page.add_child(WebBr()):
                pass
            with page.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c2:
                    with c2.add_child(WebBtn(name=testing_btn, value='Get checked values')) as btn:
                        pass

        def intro_events_impl(self):
            page = self
            testing_cls = page.testing_class
            testing_obj = page._components[testing_cls.__name__]['obj']
            testing_btn_obj = page._components[testing_btn]['obj']
            LVar = page._SUBCLASSES['LVar']['class']

            with page.render_post_w():
                testing_obj.render_for_post()

            with testing_btn_obj.on_event_w('click'):
                with LVar(parent=page, var_name='data') as value:
                    testing_obj.value()
                testing_obj.alert('"All the checked tags: " + data.checked_values')
                testing_obj.alert('"The expect result: all the checkboxes should be refreshed"')
                with page.render_post_w():
                    testing_obj.render_for_post()

        def on_my_render_impl(self, req):
            page = self
            testing_class = page.testing_class
            testing_obj = page._components[testing_class.__name__]['obj']

            for r in req:
                if r['me'] == testing_class.__name__:
                    if 'checked_values' in r['data']:
                        print('{} got checked values: {}'.format(testing_obj.name(), r['data']['checked_values']))
                        r['data'] = {'html': testing_obj.example_data()['html'],
                                     'setting': testing_obj.example_setting()}

            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class OOChatClientTest(ClassTest):

    testing_cls_name = 'oochatclient'
    NAMESPACE = '/test_namespace'
    SERVER_DATA = 'server_data'

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
        page = self
        server_name = '客服1'
        testing_class = page.testing_class
        cls = page.testing_class
        testing_cls_name = testing_class.testing_cls_name if hasattr(testing_class, 'testing_cls_name') else \
            testing_class.__name__

        WebRow = page._SUBCLASSES['WebRow']['class']
        WebColumn = page._SUBCLASSES['WebColumn']['class']

        with page.add_child(WebRow()) as r1:
            with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='800px')) as c1:
                with c1.add_child(testing_class(  parent=page,
                                                  name=testing_cls_name,
                                                  socket_namespace=testing_class.NAMESPACE,
                                                  user_name='用户' + str(random.randint(1, 1000)),
                                                  server_name=server_name,
                                                  radius='20px 10px 10px 10px')) as chat_test:
                    pass

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self, **kwargs):
        pass

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def on_post_for_class_test(self):
        WebPage = self._PAGE_CLASS
        test_obj = self._page._components[self.testing_cls_name]['obj']

        BODY, INPUT, SEND_BTN = self.get_names(myname=self.testing_cls_name)

        req = None
        if hasattr(self._page, '_action'):
            req = self._page._action.on_post()
        else:
            req = self._page.on_post()

        for r in req:
            if r['me'] == self.testing_cls_name:
                req_me = r['data']
                server_message = None
                client_message = None
                for r_ in req_me:
                    if r_['me'] == self.SERVER_DATA:
                        print('Got request data from chat server: {}'.format(r_['data']))
                        server_message = r_['data']
                    elif r_['me'] == BODY:
                        print('Got data of panel body : {}'.format(r_['data']))
                        if 'style' not in r_['data']:
                            r_['data'] = {**r_['data'], **self.DEFAULT_BODY_STYLE}
                        else:
                            r_['data']['style'] = {'height': self.DEFAULT_BODY_STYLE['style']['height']}
                        if server_message:
                            self.body_process(body_data=r_['data'], message=server_message, me=test_obj.user_name)
                        if client_message:
                            self.body_process(body_data=r_['data'], message=client_message, me=test_obj.user_name)
                    elif r_['me'] == INPUT:
                        print('Got data of input : {}'.format(r_['data']))
                        val = r_['data']['val'] if 'val' in r_['data'] else ''
                        client_message = {'from': '我', 'data': {'message': val}, 'type': 'me'}
                    elif r_['me'] == SEND_BTN:
                        print('Got data of send btn : {}'.format(r_['data']))

        return jsonify({'status': 'success', 'data': req})

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def place_components_impl(self):
            page = self

            testing_class = page.testing_class
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']

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
                    print('{} got request:{}'.format('OOChatClient',pprint.pformat(r)))
                    req_me = r['data']
                    server_message = None
                    client_message = None
                    for r_ in req_me:
                        if r_['me'] == test_class.SERVER_DATA:
                            print('{} got request data from chat server: {}'.format(test_class.SERVER_DATA, r_['data']))
                            server_message = r_['data']
                        elif r_['me'] == BODY:
                            print('{} got data of panel body : {}'.format(BODY, r_['data']))
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
                            print('{} got data of input : {}'.format(INPUT, r_['data']))
                            val = r_['data']['val'] if 'val' in r_['data'] else ''
                            client_message = {'from': '我', 'data': {'message': val}, 'type': 'me'}
                        elif r_['me'] == SEND_BTN:
                            print('{} got data of send btn : {}'.format(SEND_BTN, r_['data']))

            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):
            SERVER_NAME = '客服1'

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
                setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl, self))

        '''
        page = TestPage(app=current_app, url='/test_' + cls.__name__ + '_request',
                        value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class OOChatServerTest(OOChatClientTest):

    testing_cls_name = 'oochatserver'

    '''
    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
        NAME = '客服1'

        page = self
        testing_class = page.testing_class
        testing_cls_name = testing_class.testing_cls_name if hasattr(testing_class, 'testing_cls_name') else \
            testing_class.__name__

        WebRow = page._SUBCLASSES['WebRow']['class']
        WebColumn = page._SUBCLASSES['WebColumn']['class']
        ServerChatNM = page._SUBCLASSES['ServerChatNM']['class']

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

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def on_post_for_class_test(self):
        req = None
        if hasattr(self._page, '_action'):
            req = self._page._action.on_post()
        else:
            req = self._page.on_post()

        return jsonify({'status': 'success', 'data': req})
    '''

    @classmethod
    def test_request(cls, methods=['GET']):
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        def place_components_impl(self):
            NAME = self.TestName

            page = self
            testing_class = page.testing_class
            testing_cls_name = testing_class.__name__
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            ServerChatNM = page._SUBCLASSES['ServerChatNM']['class']

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


        class TestPage(cls._PAGE_CLASS):
            TestName = '客服1'

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))

        '''
        page = TestPage(app=current_app,
                        url='/test_' + cls.__name__ + '_request',
                        value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


class OOChartNVD3Test(ClassTest):

    @classmethod
    def test_request(cls, methods=['GET']):

        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        '''
        def place_components_impl(self):
            page = self
            WebRow = page._SUBCLASSES['WebRow']['class']
            WebColumn = page._SUBCLASSES['WebColumn']['class']
            test_class = page.testing_class
            class_name = test_class.__name__

            with page.add_child(WebRow()) as r:
                with r.add_child(WebColumn(width=self.WIDTH, offset=self.OFFSET)) as c:
                    with c.add_child(test_class(
                            parent=page,
                            value=class_name,
                            name=class_name,
                            height='400px',
                            width='100%',
                            url='/' + test_class.__name__ + '_test')) as test:
                        pass
        '''

        def on_my_render_impl(self, req):

            page = self
            if self.__class__.__name__ != 'WebPage':
                page = self._page
            testing_cls = page.testing_class
            testing_cls_name = testing_cls.__name__
            testing_obj = page._components[testing_cls_name]['obj']
            hide_switch = 'no hide switch' if not hasattr(self, 'HIDE_SWITCH') else self.HIDE_SWITCH
            dis_switch = 'no disable switch' if not hasattr(self, 'DISABLE_SWITCH') else self.DISABLE_SWITCH
            hide = None
            disable = False
            for r in req:
                if r['me'] == testing_cls_name:
                    print('{} got request:{}'.format(testing_cls_name, pprint.pformat(r)))
                    testing_obj.request(req=r)
                    testing_obj.value({'data': cls.test_request_data(),
                                       'value': cls.test_request_data()})
                    r['data'] = testing_obj.response()['data']
                elif r['me'] == hide_switch:
                    hide_switch_obj = page._components[self.HIDE_SWITCH]['obj']
                    hide_switch_obj.request(r)
                    value = hide_switch_obj.value()
                    hide = value['onText'] if value['state'] else value['offText']
                elif r['me'] == dis_switch:
                    dis_switch = page._components[self.DISABLE_SWITCH]['obj']
                    dis_switch.request(r)
                    value = dis_switch.value()
                    disable = False if value['state'] else True
                elif r['me'] == self.ROW:
                    row = page._components[self.ROW]['obj']
                    row.request(req=r)
                    display = (hide != 'Hide')
                    row.value({'display': display})
                    r['data'] = row.response()['data']


            return jsonify({'status': 'success', 'data': req})

        class TestPage(cls._PAGE_CLASS):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                setattr(self, 'on_my_render_impl', types.MethodType(on_my_render_impl,self))

        '''
        page = TestPage(app=current_app,
                        url='/test_' + cls.__name__ + '_request',
                        value='class {} test'.format(cls.__name__))
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML
        '''
        title_name = 'class {} test'.format(cls.__name__)
        page_html = TestPage.get_page(top_menu=None, name=title_name, rule='/test_' + cls.__name__ + '_request',
                                      title=title_name)
        cls._PAGE_CLASS.RUNNING_INSTANCE = TestPage.RUNNING_INSTANCE
        return page_html


_TEST_DB = 'test.db'
def create_app():
    '''create app, and all test urls'''

    from flask import Flask
    from flask_appconfig import AppConfig
    from flask_bootstrap import Bootstrap
    from flask_socketio import SocketIO

    app = Flask(__name__)
    AppConfig(app, 'test_config.py')
    Bootstrap(app)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['TESTING'] = True
    timestamp = datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                            os.path.join(basedir, _TEST_DB + timestamp)
    app.socketio = SocketIO(app=app, debug=True)
    #self.create_test_routes(app)
    #self.app_client = app.test_client()
    app.db = SQLAlchemy(app)
    app.db.drop_all()
    app.db.create_all()

    return app

exclude_classes = ['OOCalendarBar',
                      'WebTabItem',
                      'WebTabContain',
                      'WebNav',
                      'WebOption',
                      'ServerChatNM',
                      'ClassTestPage',
                      'WebPage']


def test_home(app, PageClass, testing_classes):

    if hasattr(PageClass, 'TEST_HOME_HTML') and PageClass.TEST_HOME_HTML:
        return PageClass.TEST_HOME_HTML

    subclasses = testing_classes

    WebRow = subclasses['WebRow']['class']
    WebColumn = subclasses['WebColumn']['class']
    WebHead1 = subclasses['WebHead1']['class']
    WebHr = subclasses['WebHr']['class']
    WebBtn = subclasses['WebBtn']['class']
    menu = {
        'title': {'name': 'OwwwO', 'endpoint': 'home', 'href': '/'},
        'login': {
            'site_name': 'OwwwO',
            'is_login': False,
            'login_name': 'TestUser',
            'login_href': '/',
            'logout_href': '/'
        }
    }

    # class_objs = []

    class ClassTestHomePage(PageClass):

        def place_components_impl(self):
            with self.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md6', 'lg6'], offset=['mdo3', 'lgo3'])) as c1:
                    with c1.add_child(WebHead1(value='OWWWO Classes Testing')) as head:
                        pass
            with self.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=['md8', 'lg8'], offset=['mdo2', 'lgo2'])) as c2:
                    with c2.add_child(WebHr()) as hr:
                        pass
            with self.add_child(WebRow()) as r3:
                with r3.add_child(WebColumn(width=['md6', 'lg6'], offset=['mdo3', 'lgo3'])) as c3:
                    for name, subclass in subclasses.items():
                        url_request = '/test_' + name + '_request'
                        setattr(subclass['class'], 'RENDERED_HTML', None)
                        setattr(subclass['class'], 'CLASS_TEST_HTML', None)
                        if name == 'ServerChatNM':
                            print('find ServerChatNM')
                        if name not in self._components.keys():
                            if name not in exclude_classes:
                                with c3.add_child(WebBtn(name=name,
                                                     value=name,
                                                     width='265px',
                                                     styles={'margin-top': '10px', 'margin-left': '10px'})
                                              ) as btn:
                                    pass
                                self._components[name]['test_request_url'] = url_request
                        else:
                            raise RuntimeError('Find multiple objects with same name:{}'.format(name))

        def intro_events_impl(self):
            page = self
            class_objs = page._components
            for name, class_obj in class_objs.items():
                if name in exclude_classes or 'test_request_url' not in class_obj.keys():
                    continue
                with class_obj['obj'].on_event_w('click'):
                    self.add_scripts("location.href='{}';\n".format(class_obj['test_request_url']))

        def type_(self):
            return 'WebPage'

        """
        def place_components_impl(self):
            with self.add_child(WebRow()) as r1:
                with r1.add_child(WebColumn(width=['md6', 'lg6'], offset=['mdo3', 'lgo3'])) as c1:
                    with c1.add_child(WebHead1(value='OWWWO Classes Testing')) as head:
                        pass
            with self.add_child(WebRow()) as r2:
                with r2.add_child(WebColumn(width=['md8', 'lg8'], offset=['mdo2', 'lgo2'])) as c2:
                    with c2.add_child(WebHr()) as hr:
                        pass
            with self.add_child(WebRow()) as r3:
                with r3.add_child(WebColumn(width=['md6', 'lg6'], offset=['mdo3', 'lgo3'])) as c3:
                    for name, subclass in subclasses.items():
                        if name == 'ClassTestPage':
                            subclass['class']._PAGE_CLASS = PageClass
                            continue
                        if name in exclude_class_objs:
                            continue
                        url_request = '/test_' + name + '_request'
                        '''
                        TestRequestPage = type(name+'_page', (PageClass,), {})
                        setattr(TestRequestPage, 'INSTANCES', set())
                        subclass['class']._PAGE_CLASS = TestRequestPage
                        TestRequestPage.register(app=app,
                                                 route=url_request,
                                                 top_menu=menu,
                                                 view_func=subclass['test_request'])
                        subclass['class']._PAGE_CLASS._TESTING_CLASS = subclass['class']
                        '''
                        setattr(subclass['class'], 'RENDERED_HTML', None)
                        setattr(subclass['class'], 'CLASS_TEST_HTML', None)
                        '''
                        app.add_url_rule('/' + url_request, endpoint=url_request,
                                         view_func=subclass['test_request'],
                                         methods=['GET', 'POST'])
                        url_result = 'test_' + name + '_result'
                        app.add_url_rule('/' + url_result,
                                         endpoint=url_result,
                                         view_func=subclass['test_result'],
                                         methods=['POST'])
                        '''
                        with c3.add_child(WebBtn(name=name, value=name, width='265px',
                                                 styles={'margin-top': '10px', 'margin-left': '10px'})) as btn:

                            # class_objs.append({'obj': btn, 'name': name, 'test_request_url': url_request})
                            if name not in class_objs.keys():
                                class_objs[name] = {'obj': btn, 'test_request_url': url_request}
                            else:
                                raise RuntimeError('Find multiple objects with same name:{}'.format(name))
            '''
            if not hasattr(self, '_nav_items'):
                self._nav_items = {}
            '''
            self._components = class_objs
        

        def intro_events_impl(self):
            page = self
            class_objs = page._components
            for name, class_obj in class_objs.items():
                if name in exclude_class_objs:
                    continue
                with class_obj['obj'].on_event_w('click'):
                    self.add_scripts("location.href='{}';\n".format(class_obj['test_request_url']))
        """
        """
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            setattr(self, 'place_components_impl', types.MethodType(place_components_impl, self))
            setattr(self, 'intro_events_impl', types.MethodType(intro_events_impl, self))
        """

    test_page = ClassTestHomePage(app=current_app, nav_items=menu, value='<OwwwO> class test')
    test_page.socketio = app.socketio
    test_page.db = app.db

    html = test_page.render()
    PageClass.TEST_HOME_HTML = render_template_string(html)
    return PageClass.TEST_HOME_HTML


class ExampleData():
    LAST_NAME = [
        '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
        '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
        '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
        '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
        '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
        '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
        '熊', '纪', '舒', '屈', '项', '祝', '董', '梁'
    ]

    FIRST_NAME_FEMALE = [
        '蕊', '薇', '菁', '梦', '岚', '苑', '婕', '馨', '瑗', '琰', '韵', '融', '园', '艺',
        '咏', '卿', '聪', '澜', '纯', '爽', '琬', '茗', '羽', '希', '宁', '欣', '飘', '育',
        '滢', '馥', '筠', '柔', '竹', '霭', '凝', '晓', '欢', '霄', '伊', '亚', '宜', '可',
        '姬', '舒', '影', '荔', '枝', '思', '丽', '芬', '芳', '燕', '莺', '媛', '艳', '珊',
        '莎', '蓉', '眉', '君', '琴', '毓', '悦', '昭', '冰', '枫', '芸', '菲', '寒', '锦', '玲', '秋',
        '秀', '娟', '英', '华', '慧', '巧', '美', '娜', '静', '淑', '惠', '珠', '翠', '雅', '芝', '玉', '萍', '红', '月',
        '彩', '春', '菊', '兰', '凤', '洁', '梅', '琳', '素', '云', '莲', '真', '环', '雪', '荣', '爱', '妹', '霞', '香',
        '瑞', '凡', '佳', '嘉', '琼', '勤', '珍', '贞', '莉', '桂', '娣', '叶', '璧', '璐', '娅', '琦', '晶', '妍', '茜',
        '黛', '青', '倩', '婷', '姣', '婉', '娴', '瑾', '颖', '露', '瑶', '怡', '婵', '雁', '蓓', '纨', '仪', '荷', '丹'
    ]

    FIRST_NAME_MALE = [
        '梁', '栋', '维', '启', '克', '伦', '翔', '旭', '鹏', '泽', '晨', '辰', '士', '以', '建', '家', '致', '树', '炎',
        '盛', '雄', '琛', '钧', '冠', '策', '腾', '楠', '榕', '风', '航', '弘', '义', '兴', '良', '飞', '彬', '富', '和',
        '鸣', '朋', '斌', '行', '时', '泰', '博', '磊', '民', '友', '志', '清', '坚', '庆', '若', '德', '彪',
        '伟', '刚', '勇', '毅', '俊', '峰', '强', '军', '平', '保', '东', '文', '辉', '力', '明', '永', '健', '世', '广',
        '海', '山', '仁', '波', '宁', '福', '生', '龙', '元', '全', '国', '胜', '学', '祥', '才', '发', '武', '新', '利',
        '顺', '信', '子', '杰', '涛', '昌', '成', '康', '星', '光', '天', '达', '安', '岩', '中', '茂', '进', '林', '有',
        '诚', '先', '敬', '震', '振', '壮', '会', '思', '群', '豪', '心', '邦', '承', '乐', '绍', '功', '松', '善', '厚',
        '裕', '河', '哲', '江', '超', '浩', '亮', '政', '谦', '亨', '奇', '固', '之', '轮', '翰', '朗', '伯', '宏', '言'
    ]

    def query(self, query):
        return None

    def get_name(self, gender='男'):
        if gender == '男':
            first_name = random.choice(self.FIRST_NAME_MALE)
            if random.choice([True, False]):
                first_name = first_name + random.choice(self.FIRST_NAME_MALE)
            return random.choice(self.LAST_NAME) + first_name
        else:
            first_name = random.choice(self.FIRST_NAME_FEMALE)
            if random.choice([True, False]):
                first_name = first_name + random.choice(self.FIRST_NAME_FEMALE)
            return random.choice(self.LAST_NAME) + first_name

    def get_born_date(self):
        return datetime.datetime(year=random.randint(1980, 2000), month=random.randint(1, 12), day=random.randint(1, 28))

    def get_age(self, born):
        this_year = datetime.datetime.today().year
        return this_year - born.year

    def get_gender(self):
        return random.choice(['男', '女'])

    def get_a_day(self):
        start_dt = datetime.date.today().replace(day=1, month=1).toordinal()
        end_dt = datetime.date.today().toordinal()
        return datetime.date.fromordinal(random.randint(start_dt, end_dt))

    def example_data(self):
        raise NotImplementedError

    def get_example_data(self):
        example_data = None
        if not os.path.exists(self.example_data_file):
            example_data = self.example_data()
            with open(self.example_data_file, mode='wb') as example_file:
                pickle.dump(example_data, example_file)
        else:
            with open(self.example_data_file, mode='rb') as example_file:
                example_data = pickle.load(example_file)
        return example_data
