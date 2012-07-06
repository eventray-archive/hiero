from hiero.interfaces   import IHieroEntryClass
from hem.config         import get_class_from_config

def includeme(config):
    settings = config.registry.settings

    if not config.registry.queryUtility(IHieroEntryClass):
        entry_class = get_class_from_config(settings, 'hiero.entry_class')
        config.registry.registerUtility(entry_class, IHieroEntryClass)

    config.add_route('hiero_entry_index',   '/')
    config.add_route('hiero_entry_detail',   '/')
    config.add_route('get_pages',   '/pages') 
    config.add_route('get_page',    '/pages/{link_title}')
    config.add_route('edit_page',   '/pages/{link_title}/edit')
    config.add_route('add_page',    '/add_page')
    config.add_route('remove_page', '/pages/{link_title}/remove')
    config.include('pyramid_haml')
    config.scan()

