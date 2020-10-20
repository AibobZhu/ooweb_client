from examples.example_project.pages.common_imports import *
from examples.example_project.view import VIEW_CONFIG
from examples.example_project.pages import ExampleBasePage

page_name = 'owwwo_demo_example'
view = Blueprint(page_name, __name__)
view.config = VIEW_CONFIG

url_prefix = '/{}_post'.format(page_name)

BTN_SHOW_NAME = 'btn_show'
BTN_HIDE_NAME = 'btn_hide'

CHART_DIV_NAME = 'chart_div'
TABLE_DIV_NAME = 'table_div'
PIPE_NAME = 'pip'
MC_NAME = 'multi_columns'
TABLE_NAME = 'test_name'
RADIO_NAME = 'test_radio'
RADIO_ITEMS = [{'label': PIPE_NAME, 'checked':''},{'label': MC_NAME}]
LANG = 'zh'

# model = ExampleData()


def on_post():
    req_ = oocc.WebPage.on_post()
    show_chart = PIPE_NAME
    show_border = True
    for i, r in enumerate(req_):

        if r['me'] == RADIO_NAME:
            show_chart = r['data']

        elif r['me'] == BTN_SHOW_NAME:
            show_border = True

        elif r['me'] == BTN_HIDE_NAME:
            show_border = False

        elif r['me'] == PIPE_NAME:
            if show_chart == PIPE_NAME:
                r['data'] = {'data': oocc.OOChartPie.test_request_data(), 'style': {'visibility':'visible'}}
            else:
                r['data'] = {'data': oocc.OOChartPie.test_request_data(), 'style': {'visibility':'hidden'}}

        elif r['me'] == MC_NAME:
            if show_chart == MC_NAME:
                r['data'] = {'data': oocc.OOChartMultiBar.test_request_data(), 'style': {'visibility':'visible'}}
            else:
                r['data'] = {'data': oocc.OOChartMultiBar.test_request_data(), 'style': {'visibility':'hidden'}}

        elif r['me'] == TABLE_NAME:
            data = oocc.OOTable.model.query("test")
            html = ''.join(oocc.OOTable.html(data=data))
            # setting = table.get_data(setting_only=True)
            r['data'] = {'html': html, 'setting': data['setting'], 'add_class':['cell-border']}
            if show_border:
                r['data']['remove_class'] = ['borderless', 'table-borderless']
                r['data']['add_class'] = ['cell-border']
            else:
                r['data']['remove_class'] = ['cell-border']
                r['data']['add_class'] = ['borderless', 'table-borderless']


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
                with c1.add_child(oocc.WebBtnRadio(parent=page, name=RADIO_NAME, items=RADIO_ITEMS)) as radio:
                    pass
        with page.add_child(oocc.WebRow()) as r2:
            with r2.add_child(oocc.WebColumn(width=['md4', 'lg4'], offset=page._col_offset)) as c2_1:
                with c2_1.add_child(oocc.WebDiv()) as pip_div:
                    with pip_div.add_child(oocc.OOChartPie(height='500px', width='100%', name=PIPE_NAME)) as pip:
                        pass
            with r2.add_child(oocc.WebColumn(width=['md4', 'lg4'])) as c2_2:
                with c2_2.add_child(oocc.WebDiv()) as mc_div:
                    with mc_div.add_child(oocc.OOChartMultiBar(height='500px', width='100%', name=MC_NAME)) as mc:
                        pass
        with page.add_child(oocc.WebRow()) as r3:
            with r3.add_child(oocc.WebColumn(width=page._col_width, offset=page._col_offset)) as c3:
                with c3.add_child(oocc.OOTable(name=TABLE_NAME)) as table:
                    pass
        with page.add_child(oocc.WebRow()) as r4:
            with r4.add_child(oocc.WebColumn(width=page._col_width, offset=page._col_offset)) as c4:
                with c4.add_child(oocc.WebBtn(name=BTN_SHOW_NAME, value='Show table border')) as btn_show_border:
                    pass
                with c4.add_child(oocc.WebBtn(name=BTN_HIDE_NAME, value='Hide table border')) as btn_hide_border:
                    pass
        """
        Actions
        """
        with page.render_post_w():
            pip.render_for_post()
            mc.render_for_post()
            table.render_for_post()

        with radio.on_event_w('change'):
            with page.render_post_w():
                radio.render_for_post()
                pip.render_for_post()
                mc.render_for_post()

        with btn_show_border.on_event_w('click'):
            with page.render_post_w():
                btn_show_border.render_for_post()
                table.render_for_post()

        with btn_hide_border.on_event_w('click'):
            with page.render_post_w():
                btn_hide_border.render_for_post()
                table.render_for_post()

    return page.render()


page_class = type('Class_' + page_name, (ExampleBasePage,), {
    'render': render
})
