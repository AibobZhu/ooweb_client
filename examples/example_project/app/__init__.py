from flask import Flask
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_login import LoginManager

from examples.example_project.view import view
from examples.example_project.pages import home
import components_client as oocc

def create_app():

    app = Flask(__name__)
    AppConfig(app)
    Bootstrap(app)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config['WTF_CSRF_SECRET_KEY'] = 'mysecretkey1234567890'
    app.config['SECRET_KEY'] = 'mysecretkey1234567890'
    #login_manager = LoginManager()
    #login_manager.init_app(app)
    #login_manager.login_view = 'view.login'

    app.register_blueprint(view)
    home.init_page(app)
    #example.init_page(app)

    return app