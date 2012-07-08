from hiero.views        import BaseController
from hiero.interfaces   import IHieroEntryClass
from hem.db             import get_session
from pyramid.view       import view_config
from sqlalchemy.orm.exc import NoResultFound
import logging

logger = logging.getLogger(__name__)

class EntryController(BaseController):
    @view_config(
            route_name='hiero_entry_index'
            , renderer='hiero:templates/blog_index.mako'
    )
    def index(self):
        """ View that lists and pages all the entries """
        page = self.request.matchdict.get('page', 1)

        query = self.Entry.get_all_active(self.request, page=page)
        return {'entries': query.all()}


    @view_config(
        route_name='hiero_entry_detail'
        , renderer='hiero:templates/entry_detail.mako'
    )
    def detail(self):
        """ View that is a detailed view of a single entry """
        slug = self.request.matchdict.get('slug', None)

        if slug:
            query = self.Entry.get_by_slug(self.request, slug)

            try:
                result = query.one()
                return dict(entry=result)
            except NoResultFound as exc:
                logger.debug('Could not find slug %s' % slug)
                raise

    @view_config(
        route_name='hiero_entry_edit'
        , renderer='hiero:templates/entry_edit.mako'
    )
    def edit(self):
        """ View that is for editing a single entry """
        slug = self.request.matchdict.get('slug', None)

        if slug:
            if self.request.method == 'GET':
                query = self.Entry.get_by_slug(self.request, slug)
                return {'entry': query.one()}
            elif self.request.method == 'POST':
                # valid entry post with colander
                pass


    @view_config(
        route_name='hiero_entry_search'
        , renderer='hiero:templates/detail.mako'
    )
    def search(self):
        """ View that allows you to search entries """
        pass

class AdminEntryController(BaseController):
    @view_config(
            route_name='hiero_admin_entry_index'
            , renderer='hiero:templates/blog_admin_index.mako'
    )
    def index(self):
        """ View that lists and pages all the entries for admins """
        page = self.request.matchdict.get('page', 1)

        query = self.Entry.get_all_active(self.request, page=page)
        return {'entries': query.all()}
