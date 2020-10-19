import components_client as oocc
__all__ = ['ExampleBasePage']


class CustomPage:

    TITLE = 'OWWWO Demo'

    def __init__(self, name=None, c_wd=10, c_offset=0, **kwargs):
        self._c_wd = 'md' + str(c_wd)
        if c_offset:
            self._c_offset = c_offset
        else:
            self._c_offset = 'mdo' + str(int((12 - c_wd) / 2))
        if not name:
            self._name = self.__class__.__name__
        else:
            self._name = name

    @classmethod
    def create_routes(cls, app_bp, url=None, func=None, methods=[]):
        if not url:
            url = cls.__name__ + '_on_post'
        if not func:
            func = cls.on_post()
        if not methods:
            methods = ['GET', 'POST']
        app_bp.add_url_rule(url, func, methods)

    @classmethod
    def get_nav(cls, current_user):

        return {
            'title': {'name': 'OWWWO Demo', 'action': 'view.home'},
            #'menu_list': current_user.get_menus() if current_user and hasattr(current_user, 'get_menus') else [],
            'menu_list': ['test'],
            'login': {
                'site_name': 'OWWWO Demo',
                'is_login': True,
                #'login_name': current_user.name if current_user and hasattr(current_user, 'name') else '测试用户',
                'login_name': '测试用户',
                'login_href': 'view.login',
                'logout_href': 'view.logout'
            },
            'lang': 'zh'
        }

    def render(self, on_post=None):

        with oocc.WebPage(default_url='view.test', value=self.TITLE,
                          nav=self.NAV) as page:
            return page


class ExampleBasePage(oocc.WebPage):
    PAGE = None

    def __init__(self, default_url='view.index', nav_items=None, value=CustomPage.TITLE, **kwargs):
        kwargs['default_url'] = default_url
        '''
        if nav_items is None:
            nav_items = CustomPage.get_nav(current_user=current_user)
        kwargs['nav_items'] = nav_items
        kwargs['value'] = value
        '''
        super().__init__(**kwargs)

