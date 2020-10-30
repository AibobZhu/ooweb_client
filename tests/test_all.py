import sys
sys.path.append(".")
sys.path.append("..")
from test_class import create_app, test_home

from components_client import WebPage, WebComponentBootstrap

app = create_app()

def home():
    return test_home(app=app, PageClass=WebPage, RootClass=WebComponentBootstrap)

app.add_url_rule('/', endpoint='home', view_func=home, methods=['GET', 'POST'])
app.run(host='0.0.0.0', port=5000)
