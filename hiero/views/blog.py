from hiero.views                import BaseController
from hiero.schemas.blog         import EntryAdminSchema
from hiero.schemas.blog         import CategoryAdminSchema
from hiero.schemas.blog         import SeriesAdminSchema
from hiero.schemas.blog         import TagAdminSchema
from hiero.forms                import HieroForm
from hiero.formatters           import get_formatter
from horus.resources            import RootFactory
from pyramid.view               import view_config
from pyramid.view               import view_defaults
from pyramid.httpexceptions     import HTTPFound
from pyramid.httpexceptions     import HTTPNotFound
from sqlalchemy.orm.exc         import NoResultFound
from sqlalchemy.sql.expression  import func
from pyramid.i18n               import TranslationStringFactory
from datetime                   import datetime
import deform
import logging

logger = logging.getLogger(__name__)

_ = TranslationStringFactory('hiero')

def rss_content_type(info, request):
    request.response.content_type = 'application/rss+xml'

    return True

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
            , 'page': page
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
        category = self.session.query(self.Category).filter(slug == slug).one()

        return {
            'category': category
            , 'entries': query.all()
            , 'page': page
        }


    @view_config(
        route_name='hiero_entry_series'
        , renderer='hiero:templates/blog_index.mako'
    )
    def series_index(self):
        """ View that lists and pages all the entries 
        in a series 
        """
        page = int(self.request.matchdict.get('page', 1))
        slug = self.request.matchdict.get('slug')

        query = self.Entry.get_all_active(self.request, page=page)
        query = query.join(self.Series)
        query = query.filter(self.Slug.slug == slug)

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
                raise HTTPNotFound()


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
                appstruct = self.request.context.__json__(self.request,
                    convert_date=False)

                appstruct['tags'] = [str(t.id) for t in appstruct['tags']]

                return dict(
                    form=form,
                    appstruct=appstruct
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
            entry.owner_id = captured['owner']
            entry.content = captured['content']
            entry.markup = captured['markup']

            tags = self.session.query(self.Tag).all()

            saved_tags = []

            for tag in tags:
                if captured['tags']:
                    if str(tag.id) in captured['tags']:
                        saved_tags.append(tag)

            entry.tags = saved_tags

            formatter = get_formatter(captured['markup'])

            if formatter:
                entry.html_content = formatter(entry.content).get_html()
            else:
                entry.html_content = entry.content

            entry.category_id = captured['category']
            entry.series_id = captured['series']
            entry.is_featured = captured['is_featured']
            entry.is_published = captured['is_published']
            entry.enable_comments = captured['enable_comments']
            published_on = captured['published_on']
            entry.published_on = published_on.replace(tzinfo=None)


            if captured['slug']:
                entry.slug = captured['slug']

            self.session.add(entry)

            self.session.flush()

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
                    appstruct = self.request.context.__json__(self.request)
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
            route_name='hiero_admin_tag_index'
            , renderer='hiero:templates/admin/tag_index.mako'
    )
    @view_config(
            route_name='hiero_admin_tag_index_paged'
            , renderer='hiero:templates/admin/tag_index.mako'
    )
    def tag_index(self):
        page = int(self.request.matchdict.get('page', 1))

        query = self.Tag.get_all(self.request, page=page)

        return dict(tags=query.all())

    @view_config(
            route_name='hiero_admin_tag_create'
            , renderer='hiero:templates/admin/edit_tag.mako'
    )
    @view_config(
            route_name='hiero_admin_tag_edit'
            , renderer='hiero:templates/admin/edit_tag.mako'
    )
    def create_tag(self):
        schema = TagAdminSchema()
        schema = schema.bind(request=self.request)
        form = HieroForm(self.request, schema)

        if self.request.method == 'GET':
            if isinstance(self.request.context, RootFactory):
                return dict(form=form)
            else:
                return dict(
                    form=form,
                    appstruct = self.request.context.__json__(self.request)
                )
        else:
            try:
                controls = self.request.POST.items()
                captured = form.validate(controls)
            except deform.ValidationFailure, e:
                return dict(form=e, errors=e.error.children)


            if isinstance(self.request.context, RootFactory):
                tag = self.Tag()
            else:
                tag = self.request.context

            tag.title = captured['title']

            self.session.add(tag)

            self.request.session.flash(_(u'The tag was created'), 'success')

            return HTTPFound(
                location=self.request.route_url('hiero_admin_tag_index')
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
                    appstruct = self.request.context.__json__(self.request)
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

class RSSController(BaseController):
    def get_rss_data(self, entries):
        settings = self.request.registry.settings

        title = settings.get('hiero.rss_title', 'Set .ini, hiero.rss_title')
        description = settings.get('hiero.rss_description', '')
        link = settings.get('rss_link', self.request.host_url)
        lang = settings.get('rss_lang', 'en')
        copyright = settings.get('rss_copyright', '')
        ttl = settings.get('rss_ttl', 60)

        return {
            'title': title
            , 'description': description
            , 'link': link
            , 'language': lang
            , 'copyright': copyright
            , 'pub_date': datetime.utcnow()
            , 'last_build_date': datetime.utcnow()
            , 'ttl': ttl
            , 'entries': entries
        }

    @view_config(
        route_name='hiero_entry_rss'
        , renderer='hiero:templates/rss.mako'
        , custom_predicates = (rss_content_type,)
    )
    def rss(self):
        query = self.Entry.get_all_active(self.request)
        entries = query.all()

        return self.get_rss_data(entries)


    @view_config(
        route_name='hiero_entry_rss_category'
        , renderer='hiero:templates/rss.mako'
        , custom_predicates = (rss_content_type,)
    )
    def rss_category(self):
        category = func.lower(self.request.matchdict['category'])
        query = self.Entry.get_all_active(self.request)
        query = query.join(self.Category)
        query = query.filter(
            func.lower(self.Category.title) ==  category
        )
        entries = query.all()

        return self.get_rss_data(entries)

    @view_config(
        route_name='hiero_entry_rss_tag'
        , renderer='hiero:templates/rss.mako'
        , custom_predicates = (rss_content_type,)
    )
    def rss_tag(self):
        """
        SELECT entry_tag.title
        FROM entry 
        JOIN entry_tag_association on entry.id = entry_tag_association.entry_id 
        JOIN entry_tag on entry_tag.id = entry_tag_association.tag_id;
        """
        tag = func.lower(self.request.matchdict['tag'])
        query = self.Entry.get_all_active(self.request)
        query = query.join(self.EntryTag)
        query = query.join(
            self.Tag
            , self.EntryTag.tag_id == self.Tag.id
        )
        query = query.filter(
            func.lower(self.Tag.title) ==  tag
        )
        entries = query.all()

        return self.get_rss_data(entries)
