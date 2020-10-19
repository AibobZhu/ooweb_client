from flask import Blueprint, render_template_string, jsonify, request, redirect
#from examples.example_project.pages.example import Example

view = Blueprint('view', __name__)
VIEW_CONFIG = {'API_URL': 'http://localhost:8090', 'SECRET_KEY': 'educloud secret key'}

__all__ = ['index', 'VIEW_CONFIG']

from examples.example_project.pages.home import page_class as Home

@view.route('/')
def index():
    page = Home().render()
    return page

'''
@view.route('/example')
def example():
    page = Example().render()
    return page
'''

