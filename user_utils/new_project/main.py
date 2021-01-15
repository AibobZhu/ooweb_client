from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
#from flask_socketio import SocketIO
import pages

project_name = 'not set yet'


def create_app():
    app = Flask(project_name)
    AppConfig(app, 'config.py')
    Bootstrap(app)
    return app


app = create_app()
pages.register(app=app)
# run for developing
app.run(host='0.0.0.0', port=5000, debug=True)

# run for producting
#app.run(host='0.0.0.0', port=80)
