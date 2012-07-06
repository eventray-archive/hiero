def includeme(config):
    config.add_route('hiero_entry_index',   '/')
    config.add_route('hiero_entry_detail',   '/')
    config.add_route('get_pages',   '/pages') 
    config.add_route('get_page',    '/pages/{link_title}')
    config.add_route('edit_page',   '/pages/{link_title}/edit')
    config.add_route('add_page',    '/add_page')
    config.add_route('remove_page', '/pages/{link_title}/remove')
    config.include('pyramid_haml')
    config.scan()
