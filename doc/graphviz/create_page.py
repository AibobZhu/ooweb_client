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
    name='register url',
    label='Define URL\l(page.url_prefix)\l',
    width=sub_module_width,
    color=sub_module_color)
page_name = flow.rect(
    name='page_name',
    label='Page Name\lpage.page_name\l',
    width=sub_module_width,
    color=sub_module_color
)
layout = flow.rect(
    name='Layout',
    label='Placements\l(page.place = place_func)\lLike placing components\l',
    width=module_width,
    color=module_color)
create_component = flow.rect(
    name='Create components',
    label='Create components\l(with page.add_child(WebComponent(...))) as com:\l...)',
    width=sub_module_width,
    color=sub_module_color)
add_events = flow.rect(
    name='Add events',
    label='Events\l(page.events.append(event_function))\lLike adding inputs\l',
    width=module_width,
    color=module_color
)
add_action = flow.rect(
    name='Add actions',
    label='Actions\l(page.components[NAME].action=a_action_func)\lLike connecting/routing components\l',
    width=module_width,
    color=module_color)

flow.flow_edge(tail='Start',head='Create page object')
flow.flow_edge(tail='Create page object', head='Layout')
flow.flow_edge(tail='Create page object', head='register url')
flow.flow_edge(tail='register url', head='Create page object')
flow.flow_edge(tail='register url', head='page_name')
flow.flow_edge(tail='page_name', head='register url')
flow.flow_edge(tail='Layout', head='Create components')
flow.flow_edge(tail='Create components', head='Layout')
flow.flow_edge(tail='Layout', head='Add events')
flow.flow_edge(tail='Add events', head='Add actions')
flow.flow_edge(tail='Add actions', head='End')

flow.render('output/create_page.gv', view=True)
