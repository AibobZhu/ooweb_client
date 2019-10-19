import os, datetime
from flask_sqlalchemy import SQLAlchemy
from flask import render_template_string

class MinXin:

    def __init__(self, **kwargs):
        super().__init__()

class Test(MinXin):

    '''
    Page all the testing methods. The subclass inherited it
    '''
    _TEST_JS = ''

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

    def __init__(self, test=False, **kwargs):
        super().__init__(**kwargs)
        self._test = test
        if self._test and hasattr(self,'test_init'):
            self.test_init()

    def get_test_js(self):
        '''
        Post test result to url of class_name_test_result
        Sub class should overwrite this according its own condition if necessary
        '''

        '''
        test_js = self._TEST_JS
        return test_js
        '''

        url = ''
        return '''alert('!@#class_name!@#');\n'''.replace('!@#class_name!@#',self.__class__.__name__)

    @classmethod
    def test_result(cls):
        '''sub class should over'''

        #return 'OK', 201
        raise NotImplementedError

    @classmethod
    def add_test_route(cls, app):
        url_request = 'test_' + cls.__name__ + '_request'
        app.add_url_rule('/' + url_request, endpoint=url_request, view_func=cls.test_request)
        url_result = 'test_' + cls.__name__ + '_result'
        app.add_url_rule('/' + url_result, endpoint=url_result, view_func=cls.test_result, methods=['POST'])
        return {'test_request':url_request,'test_result':url_result}

    @classmethod
    def test_init(cls):
        pass


class TestPage(Test):

    _TEST_DB = 'test.db'

    def __init__(self, test=False, **kwargs):
        super().__init__(test=test, **kwargs)
        if test:
            TestPage.test_init(self)

    def test_init(self):
        self._test_route_list = []
        self.create_app()

    def create_test_routes(self, app):
        '''
        Create a test url route and page link for each subclass, each page contains a test case in js. Finally create an index page of all tests
        TODO: may add this into a new interface of page
        '''

        nav_items = {'menu_list':[]}
        subclasses = self.get_sub_classes(self._root_class)
        for name, klass in subclasses.items():
            test_urls = klass.add_test_route(app)
            nav_items['menu_list'].append({'name':name,'action':test_urls['test_request']})

        self._nav_items = {**self._nav_items, **nav_items} if hasattr(self, '_nav_item') else nav_items

        @app.route('/')
        def index():
            return render_template_string(self.render())

    def create_app(self):
        '''create app, and all test urls'''

        from flask import Flask
        from flask_appconfig import AppConfig
        from flask_bootstrap import Bootstrap

        app = Flask(__name__)
        AppConfig(app,'default_config.py')
        Bootstrap(app)
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        timestamp = datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(basedir, self._TEST_DB + timestamp)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.create_test_routes(app)
        self.app_client = app.test_client()
        self.app = app
        self.db = SQLAlchemy(app)
        self.db.drop_all()
        self.db.create_all()

        def week():
            print('week')



        return app

    def test_start(self):
        self.app.run(port=5600, threaded=True)

