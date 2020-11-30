import os, datetime
from flask_sqlalchemy import SQLAlchemy
from flask import render_template_string, current_app, jsonify, url_for
import types
import copy
import pprint
import random
from share import randDatetimeRange, _getStr
import oocc_define as ooccd

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

        for subclass in root_class.__subclasses__():
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

    @classmethod
    def test_request(cls, methods=['GET']):
        # Create a testing page containing the component tested
        print('class {} test_request is called'.format(cls.__name__))
        if cls.CLASS_TEST_HTML:
            return cls.CLASS_TEST_HTML

        testing_cls_name = cls.testing_cls_name if hasattr(cls, 'testing_cls_name') else cls.__name__
        WebPage = cls._PAGE_CLASS
        page = WebPage(app=current_app, url='/test_' + cls.__name__ + '_request')
        page.testing_class = cls
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

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
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

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
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

        class TestPage(cls._PAGE_CLASS):
            def place_components_impl(self):
                page = self
                WebBtn = page._SUBCLASSES['WebBtn']['class']
                OODict = page._SUBCLASSES['OODict']['class']
                with page.add_child(WebBtn(value='Test dict', name='name1')) as btn1:
                    pass
                with page.add_child(WebBtn(value='Test dict update', name='name2')) as btn2:
                    pass

                with ooccd.MetisTransform.transform_w(component=self, vptr=ooccd.ACTION_MEMBER):
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

        page = TestPage(app=current_app, url='/test_'+cls.__name__+'_request')
        page.testing_class = cls
        html = page.render()

        cls.CLASS_TEST_HTML = render_template_string(html)
        return cls.CLASS_TEST_HTML

class WebBtnRadioTest(ClassTest):

    testing_cls_name = 'WebBtnRadio'

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
        page = self
        name = page.testing_class.testing_cls_name
        WebBtnRadio = page._SUBCLASSES['WebBtnRadio']['class']

        with page.add_child(WebBtnRadio(name=name, mytype=['inline'],
                                        items=[{'label': '测试1', 'checked': ''},
                                               {'label': '测试测试测试2'},
                                               {'label': '测试3'}])) as radio:
            pass

    @ooccd.MetisTransform(vptr=ooccd.RESPONSE_MEMBER)
    def events_action_for_class_test(self, req):
        print('Class testing, class {} got req:{}'.format(self.__class__.__name__, req['data']))
        req['data'] = {'oovalue': '测试3'}
        print('Class testing: testing for {} is setting "测试3" always'.format(self.__class__.__name__))

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        radio = page._components['WebBtnRadio']['obj']
        LVar = page._SUBCLASSES['LVar']['class']
        cls = radio.__class__

        with page.render_post_w():
            radio.render_for_post()

        with radio.on_event_w('change'):
            radio.alert('"Please checking on server side to find \'Class testing, class {} got: ...\''
                       ' And the radio buttons is set {} always by on_post function on server side"'.format(cls.__name__,
                       '测试3'))
            with LVar(parent=radio, var_name='click_val') as val:
                radio.val()
                radio.add_scripts('\n')
                radio.alert('"The clicked item is in oovalue : " + click_val.oovalue')
                with page.render_post_w():
                    radio.render_for_post()


class WebBtnGroupVerticalTest(ClassTest):

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        pass

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self, **kwargs):
        page = self
        this_class = page.testing_class
        WebBtnGroupVertical = page._SUBCLASSES['WebBtnGroupVertical']['class']
        WebBtnDropdown = page._SUBCLASSES['WebBtnDropdown']['class']

        with page.add_child(WebBtnGroupVertical(name=this_class.__name__)) as toolbar1:
            with toolbar1.add_child(WebBtnDropdown(value='WebBtnDropdown1')) as area1:
                pass
            with toolbar1.add_child(WebBtnDropdown(value='WebBtnDropdown2')) as area2:
                pass


class WebBtnDropdownTest(ClassTest):

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


class WebBtnTest(ClassTest):

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    def events_default_action(self, req):
        pass

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    def events_action_for_class_test(self, req):
        cls = self.__class__
        name_ = cls.__name__
        print('Class testing, class {} got req:{}'.format(name_, req))
        req['data'] = {'oovalue': name_ + ' from on_post'}

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        test_obj = page._components['WebBtn']['obj']
        WebBtn = page._SUBCLASSES['WebBtn']['class']

        with page.render_post_w():
            test_obj.render_for_post()
        with test_obj.on_event_w('click'):
            test_obj.alert('"Please check server side to find \'Class testing, class WebBtn got req: ... \'"')
            with page.render_post_w():
                test_obj.render_for_post()


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


class WebCheckboxTest(ClassTest):

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


class WebSelectTest(ClassTest):

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


class WebDatalistTest(ClassTest):

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


class OODatePickerSimpleTest(ClassTest):
    testing_cls_name = 'OODatePickerSimple'

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


class OODatePickerIconTest(ClassTest):
    testing_cls_name = 'OODatePickerIcon'

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


class OODatePickerRangeTest(ClassTest):
    testing_cls_name = 'OODatePickerRange'

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


class OOBannerTest(ClassTest):
    testing_cls_name = 'OOBanner'

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


class WebTabTest(ClassTest):

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


class OOTableTest(ClassTest):

    testing_cls_name = 'OOTable'
    testing_cls_name2 = 'OOTable2'
    testing_cls_name3 = 'OOTable3'

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
                                         cls.RENDER_IMG_KEY) + url_for('static', filename='img/demo.jpg')},
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
            return {'html': ''.join(cls.html({'schema': schema, 'records': records})), 'setting': setting}

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
                        '!@#render_chart!@#', cls.RENDER_CHART_KEY)},
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
            return {'html': ''.join(cls.html({'schema': schema, 'records': records})), 'setting': setting}

        if type == 'img':
            return example_data_img()
        elif type == 'chart':
            return example_data_chart()
        else:
            data = {'html': super().example_data(schema_only=schema_only)}
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

    @ooccd.MetisTransform(vptr=ooccd.FORMAT_MEMBER)
    @ooccd.RuntimeOnPage()
    def place_components_for_class_test(self):
        page = self
        testing_class = page.testing_class
        cls = page.testing_class

        WebRow = page._SUBCLASSES['WebRow']['class']
        WebColumn = page._SUBCLASSES['WebColumn']['class']
        WebBr = page._SUBCLASSES['WebBr']['class']

        with page.add_child(WebRow()) as r1:
            with r1.add_child(WebColumn(width=['md8'], offset=['mdo2'], height='400px')) as c1:
                with c1.add_child(testing_class(parent=page,
                                                mytype=['striped', 'hover', 'responsive'],
                                                name=testing_class.testing_cls_name,
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
                                                name=testing_class.testing_cls_name2,
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
                                                name=testing_class.testing_cls_name3,
                                                width='100%')) as test3:
                    pass

    @ooccd.MetisTransform(vptr=ooccd.ACTION_MEMBER)
    @ooccd.RuntimeOnPage()
    def events_trigger_for_class_test(self):
        page = self
        testing_cls_name = page.testing_class.testing_cls_name
        testing_cls_name2 = page.testing_class.testing_cls_name2
        testing_cls_name3 = page.testing_class.testing_cls_name3

        test = page._components[testing_cls_name]['obj']
        test2 = page._components[testing_cls_name2]['obj']
        test3 = page._components[testing_cls_name3]['obj']

        with page.render_post_w():
            test.render_for_post()
            test2.render_for_post()
            test3.render_for_post()

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
                print('Got OOTable request data: {}'.format(r['data']))
                r['data'] = self.example_data(type='img')
            elif r['me'] == self.testing_cls_name2:
                r['data'] = self.example_data(type='chart')
            elif r['me'] == self.testing_cls_name3:
                r['data'] = self.example_data(type=None)

        return jsonify({'status': 'success', 'data': req})


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


class OOChatServerTest(OOChatClientTest):

    testing_cls_name = 'oochatserver'

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
    class_objs = {}
    exclude_class_objs = ['OOCalendarBar', 'WebTabItem', 'WebTabContain', 'WebNav', 'WebOption', 'ServerChatNM']

    class ClassTestHomePage(PageClass):

        def type_(self):
            return 'WebPage'

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
                        url_request = 'test_' + name + '_request'
                        subclass['class']._PAGE_CLASS = PageClass
                        subclass['class']._PAGE_CLASS._TESTING_CLASS = subclass['class']
                        setattr(subclass['class'], 'RENDERED_HTML', None)
                        setattr(subclass['class'], 'CLASS_TEST_HTML', None)
                        app.add_url_rule('/' + url_request, endpoint=url_request,
                                         view_func=subclass['test_request'],
                                         methods=['GET', 'POST'])
                        url_result = 'test_' + name + '_result'
                        app.add_url_rule('/' + url_result,
                                         endpoint=url_result,
                                         view_func=subclass['test_result'],
                                         methods=['POST'])
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
                    self.add_scripts('location="/{}";'.format(class_obj['test_request_url']))

    test_page = ClassTestHomePage(app=current_app, nav_items=menu)
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
