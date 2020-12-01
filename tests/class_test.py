import sys
from flask import request
sys.path.append(".")
sys.path.append("..")
from test_class import create_app, test_home
from components_client import ClassTestPage, WebComponent, WebComponentBootstrap, ServerChatNM

app = create_app()

def home():
    base_url = request.base_url
    testing_classes = ClassTestPage.get_sub_classes(root_class=WebComponentBootstrap)
    testing_classes['ServerChatNM'] = {'class': ServerChatNM}
    return test_home(app=app, PageClass=ClassTestPage, testing_classes=testing_classes)

testing_classes = ClassTestPage.get_sub_classes(root_class=WebComponentBootstrap)
for name, tc in testing_classes.items():
    TestRequestPage = type(name+'_page', (ClassTestPage,), {})
    setattr(TestRequestPage, 'INSTANCES', set())
    setattr(TestRequestPage, 'testing_class', tc['class'])
    tc['class']._PAGE_CLASS = TestRequestPage
    url_rule = 'test_' + name + '_request'
    app.add_url_rule('/'+url_rule, endpoint=url_rule, view_func=tc['test_request'], methods=['GET', 'POST'])
    app.add_url_rule('/'+url_rule+'/on_post',
                     endpoint='test_'+name+'_on_post',
                     view_func=TestRequestPage.on_page_render,
                     methods=['POST'])

app.add_url_rule('/', endpoint='home', view_func=home, methods=['GET', 'POST'])
app.socketio.run(app=app, host='0.0.0.0', port=5000)
