from flask import Blueprint, render_template_string, jsonify, request, redirect, current_app
#from examples.example_project.pages.example import Example

bp_view = Blueprint('view', __name__)
VIEW_CONFIG = {'API_URL': 'http://localhost:8090', 'SECRET_KEY': 'educloud secret key'}

__all__ = ['index', 'VIEW_CONFIG']

from examples.example_project.pages.home import page_class as Home
import examples.example_project.pages.home as home

from examples.example_project.pages.example import page_class as Example

@bp_view.route('/')
def index():
    page = Home().render(app=current_app)
    return page
'''
@view.route('/example')
def example():
    page = Example().render()
    return page
'''
