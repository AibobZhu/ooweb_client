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
    'width', 'height', 'color', 'font', 'border'
])

'''
pad(top='10px', bottom='3px', 'left'='4px', right='1px')
margin is same with pad
align(horizon='left'/'center'/'right', vertical='top'/'center'/'bottom')
'''
dot.inf(name='PositionInf', methods=[
    'pad', 'margin', 'align'
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
    'on_event_w', 'render_post_w', 'render_for_post'
])

dot.inf(name='CommandInf', methods=[
    'if_', 'else_', 'for_', 'var', 'g_var',
    'is_js', 'set_js', 'is_condition', 'set_condition', 'condition', 'cmds'
])

dot.inf(name='ComponentInf', methods=[
    '__enter__', '__exit__', 'name', 'id', 'children', 'add_child', 'parent', 'module', 'type_', 'url', 'render',
    'context', 'add_context', 'scripts', 'add_scripts', 'set_script_indent', 'get_script_indent',
    'styles', 'add_styles'
])

dot.klass(name='Action',
          attrs=['_js', '_condition']
)
dot.impl('Action', 'EventInf')
dot.impl('Action', 'CommandInf')
dot.impl('Action', 'AppearanceInf')
dot.impl('Action', 'PositionInf')
dot.impl('Action', 'PropertyInf')

dot.klass(name='ActionJquery')
dot.deri('ActionJquery','Action')

dot.klass(name='Format', attrs=['UNITS', '_attrs', '_styles', '_classes', '_value',
                                '_width', '_height', '_color', '_font', '_border',
                                '_pad', '_margin', '_align',
                                ],
)
dot.impl('Format', 'AppearanceInf')
dot.impl('Format', 'PositionInf')
dot.impl('Format', 'PropertyInf')

dot.klass(name='FormatBootstrap', attrs=[
        'COL_NAME', 'COL_OFFSET_NAME', 'ALIGN', '-----------------------',
        '_ALIGN', '_WIDTH'
    ], methods=[
        'check_col_name', 'check_align', 'offset', 'get_width_name', 'get_offset_name'
    ])
dot.deri('FormatBootstrap','Format')

dot.klass(name='WebComponent', attrs=[
        '_id', '_name', '_context', '_scripts', '_script_indent', '_styles',
        '_children', '_parent', '_module', '_url'
    ],
    methods=[
        '__init__'
    ])
dot.impl('WebComponent', 'ComponentInf')

dot.klass(name='TestCase', methods=[
    'setUp', 'tearDown', 'test'
])
dot.klass('WebComponentBootstrap', methods=[
    'base_context', 'fix_cmd', 'has_class', 'add_class', 'remove_class',
    'is_width', 'remove_width', 'set_width'
])
dot.deri('WebComponentBootstrap', 'WebComponent')
dot.deri('WebComponentBootstrap', 'ActionJquery')
dot.deri('WebComponentBootstrap', 'FormatBootstrap')
dot.deri('WebComponentBootstrap', 'TestCase')

dot.klass('WebComponentClient')
dot.deri('WebComponentClient', 'WebComponent')
'''
dot.impl('WebComponentClient', 'CommandInf')
dot.impl('WebComponentClient', 'EventInf')
dot.impl('WebComponentClient', 'FormatInf')
'''

dot.klass(name='WebPage')
dot.deri('WebPage','WebComponentBootstrap')

dot.klass(name='WebPageClient')
dot.deri('WebPageClient','WebComponentClient')

dot.klass(name='WebTable')
dot.deri('WebTable','WebComponentBootstrap')

dot.klass(name='WebTableClient')
dot.deri('WebTableClient', 'WebComponentClient')

dot.klass(name='WebBtnToggle', methods=['toggle_class', 'toggle'])
dot.deri('WebBtnToggle', 'WebComponentBootstrap')

dot.klass(name='WebImg')
dot.deri('WebImg','WebComponentBootstrap')

dot.klass(name='WebImgClient')
dot.deri('WebImgClient', 'WebComponentClient')

dot.klass(name='WebChart')
dot.deri('WebChart','WebComponentBootstrap')

dot.klass(name='WebChartClient')
dot.deri('WebChartClient','WebComponentClient')

dot.klass(name='Web...')
dot.deri('Web...', 'WebComponentBootstrap')

dot.klass(name='Web...Client')
dot.deri('Web...Client', 'WebComponentClient')

with dot.subgraph() as lev1:
    lev1.attr(rank='same')
    lev1.node('ComponentInf')
    lev1.node('EventInf')
    lev1.node('CommandInf')

with dot.subgraph() as lev2:
    lev2.attr(rank='same')
    lev2.node('WebComponent')
    lev2.node('FormatBootstrap')
    lev2.node('ActionJquery')

with dot.subgraph() as lev3:
    lev3.attr(rank='same')
    lev3.node('WebComponentBootstrap')

with dot.subgraph() as lev4:
    lev4.attr(rank='same')
    lev4.node('WebComponentClient')

dot.render('output/api.gv', view=True)
