import os, datetime
from flask_sqlalchemy import SQLAlchemy
from flask import render_template_string, current_app


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
                    and (subclass.__name__.find('WebPage') < 0):
                cls._SUBCLASSES[subclass.__name__] = subclass
                cls.get_sub_classes(subclass)

        return cls._SUBCLASSES

    def __init__(self, test=False, client=False, **kwargs):
        super().__init__(**kwargs)
        self._test = test
        if self._test and not self._client and hasattr(self, 'test_init'):
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
        return '''alert('!@#class_name!@#');\n'''.replace('!@#class_name!@#', self.__class__.__name__)

    @classmethod
    def test_result(cls):
        '''sub class should overwr'''

        # return 'OK', 201
        raise NotImplementedError

    @classmethod
    def add_test_route(cls, app):
        url_request = 'test_' + cls.__name__ + '_request'
        app.add_url_rule('/' + url_request, endpoint=url_request, view_func=cls.test_request, methods=['GET', 'POST'])
        url_result = 'test_' + cls.__name__ + '_result'
        app.add_url_rule('/' + url_result, endpoint=url_result, view_func=cls.test_result, methods=['POST'])
        return {'test_request': url_request, 'test_result': url_result}

    @classmethod
    def test_init(cls):
        pass


class TestClient(Test):

    def __init__(self, test=False, **kwargs):
        super().__init__(**kwargs)
        self._test = test
        if self._test and self._client and hasattr(self, 'test_init'):
            self.test_init()


class TestPage(Test):
    _TEST_DB = 'test.db'

    def __init__(self, test=False, **kwargs):
        super().__init__(test=test, **kwargs)
        if test and not self._client:
            TestPage.test_init(self)

    def test_init(self):
        self._test_route_list = []
        self.create_app()

    def create_test_routes(self, app):
        '''
        Create a test url route and page link for each subclass, each page contains a test case in js. Finally create an index page of all tests
        TODO: may add this into a new interface of page
        '''

        nav_items = {'title': {'name': '测试所有类', 'action': None}, 'menu_list': []}
        subclasses = self.get_sub_classes(self._root_class)
        for name, klass in subclasses.items():
            test_urls = klass.add_test_route(app)
            nav_items['menu_list'].append({'name': name, 'action': test_urls['test_request']})

        self._nav_items = {**self._nav_items, **nav_items} if hasattr(self, '_nav_item') else nav_items

        @app.route('/')
        def index():
            '''
            nav_items = {'title': {'name': '测试所有类', 'action': None}, 'menu_list': []}
            subclasses = self.get_sub_classes(self._root_class)
            for name, klass in subclasses.items():
                test_urls = klass.add_test_route(app)
                nav_items['menu_list'].append({'name': name, 'action': test_urls['test_request']})

            self._nav_items = {**self._nav_items, **nav_items} if hasattr(self, '_nav_item') else nav_items
            '''
            return render_template_string(self.render())

    def create_app(self):
        '''create app, and all test urls'''

        from flask import Flask
        from flask_appconfig import AppConfig
        from flask_bootstrap import Bootstrap
        from flask_socketio import SocketIO

        app = Flask(__name__)
        AppConfig(app, 'default_config.py')
        Bootstrap(app)
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        timestamp = datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(basedir, self._TEST_DB + timestamp)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.socketio = SocketIO(app=app, debug=True)
        app.socketio = self.socketio
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
        self.app.run(host='0.0.0.0', port=5600, threaded=True)


class TestPageClient(TestClient, TestPage):

    def __init__(self, test=False, **kwargs):
        super().__init__(test=test, **kwargs)
        if test and self._client:
            TestPage.test_init(self)


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
        start_dt = date.today().replace(day=1, month=1).toordinal()
        end_dt = date.today().toordinal()
        return date.fromordinal(random.randint(start_dt, end_dt))

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
