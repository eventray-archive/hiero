from hiero.resources    import EntryFactory

def includeme(config):
    config.add_route('hiero_entry_index',   '/')
    config.add_route('hiero_entry_index_paged',   '/page/{page}')
    config.add_route('hiero_admin_entry_index',   '/admin')
    config.add_route('hiero_admin_entry_index_paged',   '/admin/page/{page}')
    config.add_route('hiero_admin_entry_create',   '/admin/new_entry')
    config.add_route('hiero_admin_entry_edit'
           , '/admin/{slug}/edit'
           , factory=EntryFactory
           , traverse="/{slug}"
    )
    config.add_route('hiero_entry_detail',   '{slug}')
    config.add_route('hiero_entry_search',   '{term}')
