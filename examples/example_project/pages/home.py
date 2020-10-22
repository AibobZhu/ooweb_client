from examples.example_project.pages.common_imports import *
from examples.example_project.pages import ExampleBasePage

'''
HEAD1='head1'

page = Page(name='owwwo_demo_home', url='/...', nav=None, title=None, container_class=None)

### Placing elements here ###

def place(self):
    with self.add_child(oocc.WebRow()) as r1:
        with r1.add_child(oocc.WebColumn(width=['md8'], offset=['mdo2'])) as c1:
            with c1.add_child(oocc.WebHead1(name=HEAD1)) as h1:
                pass

page.place = place

### End placing ###


### Creating events here ###

def default_events(self):
    with page.render_post_w():
        [element.render_for_post() for element in page.elements]
    
page.default_events = default_events

def event1(self):
    with self.elements[HEAD1].on_event_w('click'):
        with self.render_post_w():
            self.element[HEAD1].render_for_post()

page.events.append(event1)

### End creating events ###


### Creating action here ###

def action1(self, req):
    print("Processing req['me']:{}".format(req['me']))
    print("Got data: req['data']:{}".format(req['data']))
    self.width(req, '100px')
    
page.elements[HEAD1].action = action1

### End creating events ###

'''

page_name = 'owwwo_demo_home'

url_prefix = '/{}_post'.format(page_name)
HEAD_NAME = 'test_head'
INTRO_NAME = 'test_intro'
C1_NAME = 'c1_name'
C2_NAME = 'c2_name'

LANG = 'zh'

#model = ExampleData()

'''
def do_post(self):
    req_ = oocc.WebPage.on_post()

    for i, r in enumerate(req_):

        if r['me'] == HEAD_NAME:
            r['data'] = {'text': '<OwwwO> Demo'}

        elif r['me'] == INTRO_NAME:
            del r['data']['html']
            r['data']['text'] = 'This a demo website created with <OwwwO> framework.'

        elif r['me'] == C1_NAME:
            r['data']['remove_class'] = ['col-md-8', 'col-lg-8']
            r['data']['add_class'] = ['col-md-8', 'col-lg-8']

        elif r['me'] == C2_NAME:
            r['data']['remove_class'] = ['col-md-8', 'col-lg-8']
            r['data']['add_class'] = ['col-md-8', 'col-lg-8']

    return jsonify({'status': 'success', 'data': req_})
'''

class Page(ExampleBasePage):
    URL = url_prefix + '/on_post'

    def type_(self):
        return 'WebPage'


page = Page(page_name=page_name, url_prefix=url_prefix, endpoint=page_name,
                default_url='view.index', nav=ExampleBasePage.get_nav(current_user=current_user),
                value=ExampleBasePage.TITLE, container_classes='container')

def render(self, app):
    #Page.init_page(app=app, page_name=page_name, url_prefix=url_prefix, endpoint=page_name, on_post=on_post)
    if hasattr(page, 'rendered'):
        if page.rendered:
            return page.render()
    page.rendered = True
    def place(self):
        with self.add_child(oocc.WebRow()) as r1:
            with r1.add_child(oocc.WebColumn(name=C1_NAME, width=self._col_width, offset=page._col_offset)) as c1:
                with c1.add_child(oocc.WebHead3(parent=self, name=HEAD_NAME, value=HEAD_NAME)) as head:
                    pass
        with self.add_child(oocc.WebRow()) as r2:
            with r2.add_child(oocc.WebColumn(width=page._col_width, offset=page._col_offset)) as c2:
                with c2.add_child(oocc.WebHr()) as hr:
                    pass
        with self.add_child(oocc.WebRow()) as r3:
            with r3.add_child(oocc.WebColumn(name=C2_NAME, width=page._col_width, offset=page._col_offset)) as c3:
                with c3.add_child(oocc.WebLabel(parent=page, name=INTRO_NAME)) as intro:
                    pass

    page.place = types.MethodType(place, page)
    page.place()

    """
    Events
    """
    page.default_events()

    """
    Actions
    """
    def action1(self, req):
        req['data'] = {'text': '<OwwwO> Demo'}

    page.components[HEAD_NAME].action = types.MethodType(action1, page.components[HEAD_NAME])

    def action2(self, req):
        req['data'] = {'text': 'This a demo website created with <OwwwO> framework.' }
    page.components[INTRO_NAME].action = types.MethodType(action2, page.components[INTRO_NAME])

    return page.render()


page_class = type('Class_' + page_name, (object,), {
    'render': render
})
