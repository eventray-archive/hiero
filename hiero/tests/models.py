from sqlalchemy.ext.declarative import declarative_base
from hiero.models               import GroupMixin
from hiero.models               import UserMixin
from hiero.models               import UserGroupMixin
from hiero.models               import ActivationMixin
from hiero.models               import BaseModel
from hiero.models.blog          import CategoryMixin
from hiero.models.blog          import EntryAssociationMixin
from hiero.models.blog          import EntryMixin
from hiero.models.blog          import EntryTagMixin
from hiero.models.blog          import TagMixin
from hiero.models.blog          import SeriesMixin

Base = declarative_base(cls=BaseModel)

class User(UserMixin, Base):
    pass

class Group(GroupMixin, Base):
    pass

class UserGroup(UserGroupMixin, Base):
    pass

class Activation(ActivationMixin, Base):
    pass

class EntryTag(EntryTagMixin, Base):
    pass

class Tag(TagMixin, Base):
    pass

class Category(CategoryMixin, Base):
    pass

class Entry(EntryMixin, Base):
    pass

class EntryAssociation(EntryAssociationMixin, Base):
    pass

class Series(SeriesMixin, Base):
    pass
