from uml import Uml

dot = Uml(name='OwwwOClassAPI', comment='OwwwO class API')

dot.inf(name='FormatInf',methods=[
    'pad', 'margin', 'width', 'height', 'align',
    'value', 'color', 'font', 'styles', 'styles_str', 'add_styles', 'remove_styles',
    'atts', 'atts_str', 'add_atts', 'remove_atts', 'classes', 'classes_str', 'add_class', 'remove_class', 'border_radius'
])
dot.inf(name='ActionInf', methods=[
    'has_class', 'add_class', 'remove_class', 'on_click', 'on_change', 'on_ready', 'post'
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
dot.impl('Action', 'ActionInf')
dot.impl('Action', 'CommandInf')

dot.klass(name='ActionJquery')
dot.deri('ActionJquery','Action')

dot.klass(name='Format', attrs=[
                'UNITS', '_atts', '_classes', '_WIDTH', '_value'
            ],methods=[
                'check_hw'
            ]
)
dot.impl('Format', 'FormatInf')

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
dot.impl('WebComponentClient', 'ActionInf')
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
    lev1.node('ActionInf')
    lev1.node('CommandInf')
    lev1.node('FormatInf')

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
