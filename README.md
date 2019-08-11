# ooweb_client
- The client part of owwwo, it allows you to Object-Oriented develop your web pages in python, without the knowledge of html, css, js ... anymore in most instances.

# Run the example
## Ubuntu
- git clone https://github.com/AibobZhu/ooweb_client.git
- cd ooweb_client
- virtualenv venv3 --python=/usr/bin/python3
- source venv3/bin/activate
- pip install -r requirements.txt
- cd examples
- python example_app.py

## Windows
- Install and run Pycharm
- From Pycharm git clone https://github.com/AibobZhu/ooweb_client.git
- open exmaples\example_app.py and click the run icon

# TODO
- Add more html elements
- Add more examples
- Use flask_appconfig to setup application

# Note
- The ooweb_client code calls remote APIs to render the HTML page. The server URL of the remote APIs may change. If your code doesn't work due to it, please check the settings.py on github.
