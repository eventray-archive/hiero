from hiero.views            import BaseController
from hiero.interfaces       import IHieroEntryClass
from hiero.schemas.blog     import EntryAdminSchema
from hiero.forms            import HieroForm
from horus.resources        import RootFactory
from hem.db                 import get_session
from pyramid.view           import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.orm.exc     import NoResultFound
from pyramid.i18n           import TranslationStringFactory
import colander
import deform
import logging

logger = logging.getLogger(__name__)

_ = TranslationStringFactory('hiero')

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
            , renderer='hiero:templates/admin/index.mako'
    )
    @view_config(
            route_name='hiero_admin_entry_index_paged'
            , renderer='hiero:templates/admin/index.mako'
    )
    def index(self):
        """ View that lists and pages all the entries for admins """
        page = int(self.request.matchdict.get('page', 1))

        query = self.Entry.get_all(self.request, page=page)

        return dict(entries=query.all())

    @view_config(
            route_name='hiero_admin_entry_create'
            , renderer='hiero:templates/admin/edit_entry.mako'
    )
    @view_config(
            route_name='hiero_admin_entry_edit'
            , renderer='hiero:templates/admin/edit_entry.mako'
    )
    def create(self):
        schema = EntryAdminSchema()
        schema = schema.bind(request=self.request)
        form = HieroForm(schema)

        if self.request.method == 'GET':
            if isinstance(self.request.context, RootFactory):
                return dict(form=form)
            else:
                return dict(
                    form=form,
                    appstruct = self.request.context.__json__()
                )
        else:
            try:
                controls = self.request.POST.items()
                captured = form.validate(controls)
            except deform.ValidationFailure, e:
                return dict(form=e, errors=e.error.children)


            if isinstance(self.request.context, RootFactory):
                entry = self.Entry()
            else:
                entry = self.request.context

            entry.title = captured['title']
            entry.owner_pk = captured['owner']
            entry.content = captured['content']
            entry.html_content = captured['content']
            entry.category_pk = captured['category']
            entry.series_pk = captured['series']
            entry.is_featured = captured['is_featured']
            entry.is_published = captured['is_published']
            entry.enable_comments = captured['enable_comments']
            entry.published_on = captured['published_on']

            if captured['slug']:
                entry.slug = captured['slug']

            self.session.add(entry)

            self.request.session.flash(_(u'The entry was created'), 'success')

            return HTTPFound(
                location=self.request.route_url('hiero_admin_entry_index')
            )


