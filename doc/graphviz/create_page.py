from flow import Flow

module_width = '2.5'
module_color = 'blue'

sub_module_width = '2'
sub_module_color = 'skyblue'

flow = Flow(name='CreatePage', comment='Create page process', bt='TB')

start = flow.circle('Start')
end = flow.circle('End')

web_instance = flow.rect(
    name='Create page object',
    label='Instance WebPage',
    width=module_width,
    color=module_color)
register_url = flow.rect(
    name='register_url',
    label='Define URL\l(page.register_url)\l',
    width=module_width,
    color=module_color)
layout = flow.rect(
    name='Layout',
    label='Placement\l(Define page.render function)',
    width=module_width,
    color=module_color)
create_component = flow.rect(
    name='Create components',
    width=sub_module_width,
    color=sub_module_color)
add_action = flow.rect(
    name='Add action',
    label='Routing\l(page.register_action)\l',
    width=module_width,
    color=module_color)

flow.flow_edge(tail='Start',head='Create page object')
flow.flow_edge(tail='Create page object', head='register_url')
flow.flow_edge(tail='register_url', head='Layout')
flow.flow_edge(tail='Layout', head='Create components')
flow.flow_edge(tail='Create components', head='Layout')
flow.flow_edge(tail='Layout', head='Add action')
flow.flow_edge(tail='Add action', head='End')

flow.render('output/create_page.gv', view=True)
