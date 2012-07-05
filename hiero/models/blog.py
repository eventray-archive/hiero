from hiero.models               import BaseModel
from hiero.models               import UserMixin
from hiero.models               import ENTRY_ASSOCIATION_TABLE_NAME
from hiero.models               import ENTRY_TAG_TABLE_NAME
from hiero.models               import ENTRY_TABLE_NAME
from hiero.models               import SERIES_TABLE_NAME
from hiero.models               import ENTRY_TAG_ASSOCIATION_TABLE_NAME
from horus.lib                  import pluralize

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
        return sa.Column(sa.Unicode(30), nullable=False, unique=True)

#    @declared_attr
#    def entries(self):
#        return sa.orm.relationship(
#            'Entry'
#            , secondary=ENTRY_TABLE_NAME
#            , passive_deletes=True
#            , passive_updates=True
#            , backref=pluralize(TagMixin.__tablename__)
#        )

class CategoryMixin(BaseModel):
    @declared_attr
    def title(self):
        """ Unique title for the category """
        return sa.Column(sa.Unicode(30), nullable=False, unique=True)

#    @declared_attr
#    def entries(self):
#        return sa.orm.relationship(
#            'Entry'
#            , secondary=ENTRY_TABLE_NAME
#            , passive_deletes=True
#            , passive_updates=True
#            , backref=pluralize(CategoryMixin.__tablename__)
#        )

# markup type
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
    def series_pk(self):
        return sa.Column(
            sa.Integer,
            sa.ForeignKey('%s.pk' % SERIES_TABLE_NAME)
        )

    @declared_attr
    def category_pk(self):
        return sa.Column(
            sa.Integer
            , sa.ForeignKey('%s.pk' % CategoryMixin.__tablename__)
        )

    @declared_attr
    def is_featured(self):
        """ Allows to pull entries to the top """
        return sa.Column(sa.Boolean, nullable=False)

    @declared_attr
    def is_published(self):
        """ Marks if the entry is a draft or ready to be displayed """
        return sa.Column(sa.Boolean, nullable=False)

    @declared_attr
    def enable_comments(self):
        """ If we should allow comments or not"""
        return sa.Column(sa.Boolean, nullable=False)

    @declared_attr
    def slug(self):
        """ Unique title for the entry """
        return sa.Column(sa.Unicode(30), nullable=False, unique=True)

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
        return sa.Column(sa.Unicode(30), nullable=False, unique=True)

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
        return sa.Column(sa.TIMESTAMP(timezone=False))

#    @declared_attr
#    def related_entries(self):
#        return sa.orm.relationship(
#            'Entry'
#            , secondary=ENTRY_ASSOCIATION_TABLE_NAME
#            , passive_deletes=True
#            , passive_updates=True
#            , backref=pluralize(ENTRY_TABLE_NAME)
#        )
#

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
        return sa.Column(sa.Unicode(30), nullable=False, unique=True)

    @declared_attr
    def description(self):
        return sa.Column(sa.UnicodeText())

#    @declared_attr
#    def entries(self):
#        """ relationship for entries belonging to this series """
#        return sa.orm.relationship(
#            'Entry'
#            , secondary=ENTRY_TABLE_NAME
#            , passive_deletes=True
#            , passive_updates=True
#            , backref=pluralize(SERIES_TABLE_NAME)
#        )
