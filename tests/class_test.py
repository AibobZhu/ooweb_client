import sys
sys.path.append(".")
sys.path.append("..")
from test_class import create_app, test_home

from components_client import WebPage, WebComponent, WebComponentBootstrap, ServerChatNM

app = create_app()

def home():
    testing_classes = WebPage.get_sub_classes(root_class=WebComponentBootstrap)
    testing_classes['ServerChatNM'] = {'class': ServerChatNM}
    return test_home(app=app, PageClass=WebPage, testing_classes=testing_classes)

app.add_url_rule('/', endpoint='home', view_func=home, methods=['GET', 'POST'])
app.socketio.run(app=app, host='0.0.0.0', port=5000)
