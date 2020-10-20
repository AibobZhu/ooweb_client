from examples.example_project.pages.common_imports import *
from examples.example_project.view import VIEW_CONFIG
from examples.example_project.pages import ExampleBasePage

page_name = 'owwwo_demo_home'
view = Blueprint(page_name, __name__)
view.config = VIEW_CONFIG

url_prefix = '/{}_post'.format(page_name)
HEAD_NAME = 'test_head'
INTRO_NAME = 'test_intro'

LANG = 'zh'

#model = ExampleData()


def on_post():
    req_ = oocc.WebPage.on_post()

    for i, r in enumerate(req_):

        if r['me'] == HEAD_NAME :
            r['data'] = {'text': '<OwwwO> Programming Demo'}

        elif r['me'] == INTRO_NAME:
            r['data'] = {'text': 'This a demo website created with <OwwwO> framework.'}

    return jsonify({'status': 'success', 'data': req_})


class Page(ExampleBasePage):
    URL = url_prefix + '/on_post'

    def type_(self):
        return 'WebPage'


def init_page(app):
    Page.init_page(app=app, blueprint=view, url_prefix=url_prefix, endpoint=page_name, on_post=on_post)


def render(self):

    page = Page(default_url='view.index', nav=ExampleBasePage.get_nav(current_user=current_user),
                value=ExampleBasePage.TITLE, container_classes='container')
    with page:
        page.sync(True)

        with page.add_child(oocc.WebRow()) as r1:
            with r1.add_child(oocc.WebColumn(width=page._col_width, offset=page._col_offset)) as c1:
                with c1.add_child(oocc.WebHead3(parent=page, name=HEAD_NAME)) as head:
                    pass
        with page.add_child(oocc.WebRow()) as r2:
            with r2.add_child(oocc.WebColumn(width=page._col_width, offset=page._col_offset)) as c2:
                with c2.add_child(oocc.WebHr()) as hr:
                    pass
        with page.add_child(oocc.WebRow()) as r3:
            with r3.add_child(oocc.WebColumn(width=page._col_width, offset=page._col_offset)) as c3:
                with c3.add_child(oocc.WebLabel(parent=page, name=INTRO_NAME)) as intro:
                    pass

        """
        Actions
        """
        with page.render_post_w():
            head.render_for_post()
            intro.render_for_post()

    return page.render()


page_class = type('Class_' + page_name, (ExampleBasePage,), {
    'render': render
})
