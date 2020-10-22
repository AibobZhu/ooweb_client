from flask import Flask
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_login import LoginManager

from examples.example_project.view import bp_view
import examples.example_project.view as view
from examples.example_project.pages import home
from examples.example_project.pages import example
import components_client as oocc


def create_app():

    app = Flask(__name__)
    AppConfig(app)
    Bootstrap(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'view.login'

    @login_manager.user_loader
    def load_user(user_id):
        print("==>load_user user_id:{}".format(user_id))
        '''
        user = ExampleUser.get_record(id_=user_id)
        if user:
            return ExampleUser.create_user(user=user)
        else:
            return None
        '''
        return None

    app.register_blueprint(bp_view)
    home.page.init_api(app=app, page_name=home.page_name,
                       view_config=view.VIEW_CONFIG, url_prefix=home.url_prefix,
                       endpoint=home.page_name, on_post=home.page.do_post)
    #example.init_page(app)

    return app