from hiero.models               import BaseModel
from hiero.models               import UserMixin
from hiero.models               import ENTRY_ASSOCIATION_TABLE_NAME
from hiero.models               import ENTRY_TAG_TABLE_NAME
from hiero.models               import ENTRY_TABLE_NAME
from hiero.models               import SERIES_TABLE_NAME
from hiero.models               import ENTRY_TAG_ASSOCIATION_TABLE_NAME
from hem.db                     import get_session
from hem.text                   import slugify
from hem.text                   import pluralize
from sqlalchemy.ext.declarative import declared_attr

import sqlalchemy as sa

class EntryAssociationMixin(BaseModel):
    @declared_attr
    def __tablename__(cls):
        return ENTRY_ASSOCIATION_TABLE_NAME

    @declared_attr
    def parent_entry_pk(self):
        return sa.Column(sa.Integer
                , sa.ForeignKey('%s.pk' % ENTRY_TABLE_NAME
                    , onupdate='CASCADE'
                    , ondelete='CASCADE'
                )
                , primary_key=True
        )

    @declared_attr
    def related_entry_pk(self):
        return sa.Column(sa.Integer
                , sa.ForeignKey('%s.pk' % ENTRY_TABLE_NAME
                    , onupdate='CASCADE'
                    , ondelete='CASCADE'
                )
                , primary_key=True
        )

class EntryTagMixin(BaseModel):
    @declared_attr
    def __tablename__(cls):
        return ENTRY_TAG_ASSOCIATION_TABLE_NAME

    @declared_attr
    def tag_pk(self):
        return sa.Column(sa.Integer
                , sa.ForeignKey('%s.pk' % ENTRY_TAG_TABLE_NAME
                    , onupdate='CASCADE'
                    , ondelete='CASCADE'
                )
                , primary_key=True
        )

    @declared_attr
    def entry_pk(self):
        return sa.Column(sa.Integer
                , sa.ForeignKey('%s.pk' % ENTRY_TABLE_NAME
                    , onupdate='CASCADE'
                    , ondelete='CASCADE'
                )
                , primary_key=True
        )

class TagMixin(BaseModel):
    @declared_attr
    def __tablename__(cls):
        return ENTRY_TAG_TABLE_NAME

    @declared_attr
    def title(self):
        """ Unique title for the tag """
        return sa.Column(sa.Unicode(128), nullable=False, unique=True)

class CategoryMixin(BaseModel):
    @declared_attr
    def title(self):
        """ Unique title for the category """
        return sa.Column(sa.Unicode(128), nullable=False, unique=True)

    @declared_attr
    def slug(self):
        """ Unique url for the category """
        def slug_title(context):
            title = context.current_parameters['title']

            if title:
                return slugify(title)
            else:
                #TODO: need to raise IntegrityError here
                pass

        return sa.Column(
            sa.Unicode(128)
            , nullable=False
            , unique=True
            , default=slug_title
        )

    @classmethod
    def get_by_slug(cls, request, slug):
        """Gets a category by its slug """
        session = get_session(request)

        return session.query(cls).filter(cls.slug == slug)


class EntryMixin(BaseModel):
    @declared_attr
    def __tablename__(cls):
        return ENTRY_TABLE_NAME

    @declared_attr
    def owner_pk(self):
        return sa.Column(
            sa.Integer
            , sa.ForeignKey('%s.pk' % UserMixin.__tablename__)
            , nullable=False
        )

    @declared_attr
    def owner(self):
        return sa.orm.relationship(
            'User'
            , backref=pluralize(ENTRY_TABLE_NAME)
        )

    @declared_attr
    def markup(self):
        """ The markup format"""
        return sa.Column(sa.Unicode(128))

    @declared_attr
    def series_pk(self):
        return sa.Column(
            sa.Integer,
            sa.ForeignKey('%s.pk' % SERIES_TABLE_NAME)
        )

    @declared_attr
    def series(self):
        return sa.orm.relationship(
            'Series'
            , backref=pluralize(ENTRY_TABLE_NAME)
        )

    @declared_attr
    def category_pk(self):
        return sa.Column(
            sa.Integer
            , sa.ForeignKey('%s.pk' % CategoryMixin.__tablename__)
        )

    @declared_attr
    def category(self):
        return sa.orm.relationship(
            'Category'
            , backref=pluralize(ENTRY_TABLE_NAME)
        )

    @declared_attr
    def is_featured(self):
        """ Allows to pull entries to the top """
        return sa.Column(
            sa.Boolean
            , nullable=False
            , default=False
            , server_default='false'
        )

    @declared_attr
    def is_published(self):
        """ Marks if the entry is a draft or ready to be displayed """
        return sa.Column(
            sa.Boolean
            , nullable=False
            , default=False
            , server_default='false'
        )

    @declared_attr
    def enable_comments(self):
        """ If we should allow comments or not"""
        return sa.Column(
            sa.Boolean
            , nullable=False
            , default=False
            , server_default='false'
        )

    @declared_attr
    def slug(self):
        """ Unique title for the entry """
        def slug_title(context):
            title = context.current_parameters['title']

            if title:
                return slugify(title)
            else:
                #TODO: need to raise IntegrityError here
                pass

        return sa.Column(
            sa.Unicode(128)
            , nullable=False
            , unique=True
            , default=slug_title
        )

    @declared_attr
    def content(self):
        """ The non-rendered content of the entry"""
        return sa.Column(sa.UnicodeText, nullable=False)

    @declared_attr
    def html_content(self):
        """ The HTML content of the entry"""
        return sa.Column(sa.UnicodeText, nullable=False)

    @declared_attr
    def title(self):
        """ Unique title for the entry """
        return sa.Column(sa.Unicode(128), nullable=False, unique=True)

    @declared_attr
    def created_on(self):
        """ Date the entry was created """
        return sa.Column(sa.TIMESTAMP(timezone=False),
            default=sa.sql.func.now(),
            server_default=sa.func.now()
        )

    @declared_attr
    def published_on(self):
        """ Date the entry was published """
        return sa.Column(sa.DateTime(timezone=False))

    @declared_attr
    def tags(self):
        return sa.orm.relationship(
            'Tag'
            , secondary=ENTRY_TAG_ASSOCIATION_TABLE_NAME
            , passive_deletes=True
            , passive_updates=True
            , backref=pluralize(ENTRY_TABLE_NAME)
        )


    @declared_attr
    def related_entries(self):
        return sa.orm.relationship(
            'Entry'
            , secondary=ENTRY_ASSOCIATION_TABLE_NAME
            , passive_deletes=True
            , passive_updates=True
            , primaryjoin='Entry.pk == EntryAssociation.parent_entry_pk'
            , secondaryjoin='Entry.pk == EntryAssociation.related_entry_pk'
        )

    @classmethod
    def get_all(cls, request, page=None, limit=None):
        session = get_session(request)

        query = session.query(cls)
        query = query.order_by(cls.published_on.desc())

        if limit:
            query = query.limit(limit)

        if page and limit:
            offset = (page - 1) * limit
            query = query.offset(offset)

        return query

    @classmethod
    def get_all_active(cls, request, page=1, limit=10):
        """Gets all active entries"""
        session = get_session(request)

        query = cls.get_all(request, page=page, limit=limit)
        query = query.from_self().filter(cls.is_published == True)

        return query

    @classmethod
    def get_by_slug(cls, request, slug):
        """Gets an entry by its slug """
        session = get_session(request)

        return session.query(cls).filter(cls.slug == slug)

class SeriesMixin(BaseModel):
    """ This represents a series of blog entries, such a 6 entry 
    series on debugging python
    """
    @declared_attr
    def __tablename__(cls):
        return SERIES_TABLE_NAME

    @declared_attr
    def title(self):
        """ Unique title for the series """
        return sa.Column(sa.Unicode(128), nullable=False, unique=True)

    @declared_attr
    def slug(self):
        """ Unique url readable title for the series """
        def slug_title(context):
            title = context.current_parameters['title']

            if title:
                return slugify(title)
            else:
                #TODO: need to raise IntegrityError here
                pass

        return sa.Column(
            sa.Unicode(128)
            , nullable=False
            , unique=True
            , default=slug_title
        )

    @declared_attr
    def description(self):
        return sa.Column(sa.UnicodeText())

    @classmethod
    def get_by_slug(cls, request, slug):
        """Gets all active entries"""
        session = get_session(request)

        return session.query(cls).filter(cls.slug == slug)
