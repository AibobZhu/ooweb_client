from uml import Uml

dot = Uml(name='OwwwOClassAPI', comment='OwwwO class API')

'''
Default values: first get the default value of parameters, if None, try to get from config or theme, 
there should be a default builtin theme

The parameter of border is a dict, containing the keys 'width', 'radius'. 
The value of radius is a dict, containing the keys of 'top-left', 'top-right', 'bottom-right', 'bottom-left': 
example:
{ 
   width: '3px', 
   radius: 
       {'top-left': '3px', 'top-right':'3px', 'bottom':'3px', 'bottom': '3px'}
}

The value of color is a dict, containing the keys of 'background', 'containing', 'border', 
example:
color(background='red',
    containing='blue',
    border='green',
    font='yellow')
'''
dot.inf(name='AppearanceInf', methods=[
    'width', 'height', 'color', 'font', 'border', 'disable'
])

'''
pad(top='10px', bottom='3px', 'left'='4px', right='1px')
margin is same with pad
align(horizon='left'/'center'/'right', vertical='top'/'center'/'bottom')
'''
dot.inf(name='PositionInf', methods=[
    'pad', 'margin', 'align', 'offset'
])

'''
if attrs is given only one parameter and the type is dict, remove all attributes and reset with the parameter's value,
else if attrs is given parameters in **kwargs, just append attributes with the parameters, 
if a value in **kwarg passed in attrs is 'remove-me', then remove the attribute.
example:
attrs('data-value'='100', 'data-example': '200') # This set the 2 data attributes
attrs('data-value'='remove-me') # Remove attribute data-value
attrs('remove-all') # Remove all data attributes

if classes is given several parameters, then set the classes, if one of them begin with '-', then remove it, 
else if is given a '-', then remove all classes
example:
classes('class1','class2') # This set the classes
classes('-class1') # This remove class1
classes('-') # This remove all classes
'''
dot.inf(name='PropertyInf', methods=[
    'value', 'attrs', 'classes', 'styles'
])

dot.inf(name='EventInf', methods=[
    'on_event_w', 'render_post_w', 'render_for_post', 'trigger_event', 'sync', 'timeout_w'
])

dot.inf(name='CommandInf', methods=[
    'if_w', 'elif_w', 'else_w', 'for_w', 'equal',
    'is_js', 'set_js', 'is_condition', 'set_condition', 'condition_w', 'cmds_w',
    'declare_custom_func', 'declare_custom_global_func', 'call_custom_func'
])

dot.inf(name='ComponentInf', methods=[
    '__enter__', '__exit__', 'name', 'id',
    'children', 'add_child', 'remove_child', 'empty_children', 'parent', 'module', 'url',
    'render_content', 'context', 'add_context', 'add_context_indent', 'set_context', 'set_context_indent', 'get_context_indent',
    'add_scripts', 'replace_scripts', 'add_scripts_files', 'get_scripts_files', 'set_scripts_indent', 'get_scripts_indent',
    'add_styles', 'get_styles', 'add_styles_files', 'get_styles_files',
    'add_url_rule'
])

dot.inf(name='ActionInf')
dot.deri('ActionInf', 'AppearanceInf')
dot.deri('ActionInf', 'EventInf')
dot.deri('ActionInf', 'PositionInf')
dot.deri('ActionInf', 'PropertyInf')

dot.inf(name='FormatInf')
dot.deri('FormatInf', 'AppearanceInf')
dot.deri('FormatInf', 'PositionInf')
dot.deri('FormatInf', 'PropertyInf')

dot.klass(name='WebComponent', attrs=[
        '_id', '_name', '_context', '_scripts', '_script_indent', '_styles',
        '_children', '_parent', '_module', '_url'
    ],
    methods=[
        '__init__'
    ])
dot.impl('WebComponent', 'ComponentInf')

dot.klass(name='ClassTest', methods=[
    'events_trigger_for_class_test', 'events_action_for_class_test',
    'place_components_for_class_test', 'on_post_for_class_test'
    ], fontcolor='blue'
          )

dot.klass('WebComponentBootstrap')
dot.deri('WebComponentBootstrap', 'WebComponent')
dot.impl('WebComponentBootstrap', 'ActionInf')
dot.impl('WebComponentBootstrap', 'FormatInf')
dot.impl('WebComponentBootstrap', 'CommandInf')

dot.klass(name='WebPage')
dot.deri('WebPage','WebComponentBootstrap')

dot.klass(name='WebTable')
dot.deri('WebTable','WebComponentBootstrap')

dot.klass(name='WebBtnToggle', methods=['toggle_class', 'toggle'])
dot.deri('WebBtnToggle', 'WebComponentBootstrap')

dot.klass(name='WebImg')
dot.deri('WebImg','WebComponentBootstrap')

dot.klass(name='WebChart')
dot.deri('WebChart','WebComponentBootstrap')

dot.klass(name='Web...')
dot.deri('Web...', 'WebComponentBootstrap')

with dot.subgraph() as lev1:
    lev1.attr(rank='same')
    lev1.node('ComponentInf')
    lev1.node('EventInf')
    lev1.node('CommandInf')

with dot.subgraph() as lev2:
    lev2.attr(rank='same')
    lev2.node('ClassTest')
    lev2.node('WebComponent')

with dot.subgraph() as lev3:
    lev3.attr(rank='same')

with dot.subgraph() as lev4:
    lev4.attr(rank='same')
    lev4.node('WebComponentBootstrap')

with dot.subgraph() as lev5:
    lev5.attr(rank='same')
    lev5.node('WebPage')
    lev5.node('WebTable')
    lev5.node('WebBtnToggle')
    lev5.node('WebImg')
    lev5.node('WebChart')
    lev5.node('Web...')

dot.render('output/api_client.gv', view=True)
