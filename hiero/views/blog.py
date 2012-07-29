from hiero.views            import BaseController
from hiero.schemas.blog     import EntryAdminSchema
from hiero.schemas.blog     import CategoryAdminSchema
from hiero.schemas.blog     import SeriesAdminSchema
from hiero.forms            import HieroForm
from hiero.formatters       import get_formatter
from horus.resources        import RootFactory
from pyramid.view           import view_config
from pyramid.view           import view_defaults
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.orm.exc     import NoResultFound
from pyramid.i18n           import TranslationStringFactory
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

        return {
            'entries': query.all()
        }

    @view_config(
        route_name='hiero_entry_category'
        , renderer='hiero:templates/blog_index.mako'
    )
    def category_index(self):
        """ View that lists and pages all the entries 
        for a specific category 
        """
        page = int(self.request.matchdict.get('page', 1))
        slug = self.request.matchdict.get('slug')

        query = self.Entry.get_all_active(self.request, page=page)
        query = query.join(self.Category)
        query = query.filter(self.Category.slug == slug)

        return {
            'entries': query.all()
        }


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

@view_defaults(permission='group:admin')
class AdminEntryController(BaseController):
    @view_config(
        route_name='hiero_admin_index'
        , renderer='hiero:templates/admin/index.mako'
    )
    def index(self):
        return {}

    @view_config(
        route_name='hiero_admin_entry_index'
        , renderer='hiero:templates/admin/entry_index.mako'
    )
    @view_config(
        route_name='hiero_admin_entry_index_paged'
        , renderer='hiero:templates/admin/entry_index.mako'
    )
    def entry_index(self):
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
    def create_entry(self):
        schema = EntryAdminSchema()
        schema = schema.bind(request=self.request)
        form = HieroForm(self.request, schema)

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
            entry.markup = captured['markup']

            formatter = get_formatter(captured['markup'])

            if formatter:
                entry.html_content = formatter(entry.content).get_html()
            else:
                entry.html_content = entry.content

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

    @view_config(
            route_name='hiero_admin_category_index'
            , renderer='hiero:templates/admin/category_index.mako'
    )
    @view_config(
            route_name='hiero_admin_category_index_paged'
            , renderer='hiero:templates/admin/category_index.mako'
    )
    def category_index(self):
        page = int(self.request.matchdict.get('page', 1))

        query = self.Category.get_all(self.request, page=page)

        return dict(categories=query.all())

    @view_config(
            route_name='hiero_admin_category_create'
            , renderer='hiero:templates/admin/edit_category.mako'
    )
    @view_config(
            route_name='hiero_admin_category_edit'
            , renderer='hiero:templates/admin/edit_category.mako'
    )
    def create_category(self):
        schema = CategoryAdminSchema()
        schema = schema.bind(request=self.request)
        form = HieroForm(self.request, schema)

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
                category = self.Category()
            else:
                category = self.request.context

            category.title = captured['title']

            if captured['slug']:
                category.slug = captured['slug']

            self.session.add(category)

            self.request.session.flash(_(u'The category was created'), 'success')

            return HTTPFound(
                location=self.request.route_url('hiero_admin_category_index')
            )


    @view_config(
            route_name='hiero_admin_series_index'
            , renderer='hiero:templates/admin/series_index.mako'
    )
    @view_config(
            route_name='hiero_admin_series_index_paged'
            , renderer='hiero:templates/admin/series_index.mako'
    )
    def series_index(self):
        page = int(self.request.matchdict.get('page', 1))

        query = self.Series.get_all(self.request, page=page)

        return dict(series=query.all())

    @view_config(
            route_name='hiero_admin_series_create'
            , renderer='hiero:templates/admin/edit_series.mako'
    )
    @view_config(
            route_name='hiero_admin_series_edit'
            , renderer='hiero:templates/admin/edit_series.mako'
    )
    def create_series(self):
        schema = SeriesAdminSchema()
        schema = schema.bind(request=self.request)
        form = HieroForm(self.request, schema)

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
                series = self.Series()
            else:
                series = self.request.context

            series.title = captured['title']

            if captured['slug']:
                series.slug = captured['slug']

            self.session.add(series)

            self.request.session.flash(_(u'The series was created'), 'success')

            return HTTPFound(
                location=self.request.route_url('hiero_admin_series_index')
            )
