from hiero.views        import BaseController
from hiero.interfaces   import IHieroEntryClass
from hem.db             import get_session
from pyramid.view       import view_config

class EntryController(BaseController):
    def __init__(self, request):
        self.request = request
        self.session = get_session(request)
        self.Entry = request.registry.getUtility(IHieroEntryClass)

    @view_config(
            route_name='hiero_entry_index'
            , renderer='hiero:templates/index.mkao'
    )
    def index(self):
        """ View that lists and pages all the entries """
        page = self.request.matchdict.get('page', 1)

        query = self.Entry.get_all_active(self.request, page=page)
        return {'entries': query.all()}

    @view_config(
        route_name='hiero_entry_detail'
        , renderer='hiero:templates/detail.mako'
    )
    def detail(self):
        """ View that is a detailed view of a single entry """
        slug = self.request.matchdict.get('slug', None)

        if slug:
            query = self.Entry.get_by_slug(self.request, slug)
            return {'entry': query.one()}

    @view_config(
        route_name='hiero_entry_search'
        , renderer='hiero:templates/detail.mako'
    )
    def search(self):
        """ View that allows you to search entries """
        pass
