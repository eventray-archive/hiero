from hiero.views        import BaseController
from hiero.interfaces   import IHieroEntryClass
from hiero.schemas.blog import EntryAdminSchema
from hiero.forms        import HieroForm
from hem.db             import get_session
from pyramid.view       import view_config
from sqlalchemy.orm.exc import NoResultFound
import colander
import deform
import logging

logger = logging.getLogger(__name__)

class EntryController(BaseController):
    @view_config(
            route_name='hiero_entry_index'
            , renderer='hiero:templates/blog_index.mako'
    )
    @view_config(
            route_name='hiero_entry_index_paged'
            , renderer='hiero:templates/blog_index.mako'
    )
    def index(self):
        """ View that lists and pages all the entries """
        page = int(self.request.matchdict.get('page', 1))

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
    @view_config(
            route_name='hiero_admin_entry_index_paged'
            , renderer='hiero:templates/blog_admin_index.mako'
    )
    def index(self):
        """ View that lists and pages all the entries for admins """
        page = int(self.request.matchdict.get('page', 1))

        query = self.Entry.get_all_active(self.request, page=page)

    @view_config(
            route_name='hiero_admin_entry_create'
            , renderer='hiero:templates/blog_admin_new_entry.mako'
    )
    def create(self):
        schema = EntryAdminSchema()
        schema = schema.bind(request=self.request)
        form = HieroForm(schema)

        if self.request.method == 'GET':
            return dict(form=form)
        else:
            try:
                controls = self.request.POST.items()
                captured = form.validate(controls)
            except deform.ValidationFailure, e:
                return dict(form=e, errors=e.error.children)
