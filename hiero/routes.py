from hiero.resources    import EntryFactory
from hiero.resources    import CategoryFactory
from hiero.resources    import SeriesFactory

def includeme(config):
    # non-admin routes
    config.add_route('hiero_entry_index',   '')
    config.add_route('hiero_entry_index_paged',   '/page/{page}')
    config.add_route('hiero_entry_detail',   '/detail/{slug}')
    config.add_route('hiero_entry_search',   '/search/{term}')
    config.add_route('hiero_entry_category',   '/category/{slug}')

    # admin routes
    config.add_route('hiero_admin_index',   '/admin')
    config.add_route('hiero_admin_entry_index_paged',   '/admin/entries/page/{page}')
    config.add_route('hiero_admin_entry_index',   '/admin/entries')
    config.add_route('hiero_admin_entry_create',   '/admin/entries/new')
    config.add_route('hiero_admin_entry_edit'
           , '/admin/entries/{slug}/edit'
           , factory=EntryFactory
           , traverse="/{slug}"
    )

    config.add_route('hiero_admin_category_index_paged',
            '/admin/categories/page/{page}')
    config.add_route('hiero_admin_category_index',   '/admin/categories')
    config.add_route('hiero_admin_category_create',   '/admin/categories/new')
    config.add_route('hiero_admin_category_edit'
           , '/admin/categories/{slug}/edit'
           , factory=CategoryFactory
           , traverse="/{slug}"
    )

    config.add_route('hiero_admin_series_index_paged',
            '/admin/series/page/{page}')
    config.add_route('hiero_admin_series_index',   '/admin/series')
    config.add_route('hiero_admin_series_create',   '/admin/series/new')
    config.add_route('hiero_admin_series_edit'
           , '/admin/series/{slug}/edit'
           , factory=SeriesFactory
           , traverse="/{slug}"
    )


    config.add_static_view('static/deform', 'deform:static')
    config.add_static_view('static', 'hiero:static')
