from examples.example_project.pages.common_imports import *
from examples.example_project.view import VIEW_CONFIG
from examples.example_project.pages import ExampleBasePage, CustomPage

page_name = 'owwwo_demo'
view = Blueprint(page_name, __name__)
view.config = VIEW_CONFIG

url_prefix = '/{}_post'.format(page_name)
HEAD_NAME = 'test_head'

LANG = 'zh'

#model = ExampleData()


def on_post():
    req_ = oocc.WebPage.on_post()

    for i, r in enumerate(req_):

        if r['me'] == HEAD_NAME :
            pass

    return jsonify({'status': 'success', 'data': req_})


class Page(ExampleBasePage):
    URL = url_prefix + '/on_post'

    def type_(self):
        return 'WebPage'


def init_page(app):
    Page.init_page(app=app, blueprint=view, url_prefix=url_prefix, endpoint=page_name, on_post=on_post)


def render(self):

    page = Page(default_url='view.index', nav=CustomPage.get_nav(current_user=current_user), value=CustomPage.TITLE, container_classes='container')
    with page:
        page.sync(True)

        with page.add_child(oocc.WebRow()) as r1:
            with r1.add_child(oocc.WebColumn(width=['md8'], offset=['mdo2'], height='200px')) as c1:
                with c1.add_child(oocc.WebHead1(parent=page, value='This is OWWWO programming demo', name=HEAD_NAME)) as head:
                    pass

        """
        Actions
        """
        with page.render_post_w():
            head.render_for_post()


    return page.render()


page_class = type('Class_' + page_name, (CustomPage,), {
    'render': render
})
