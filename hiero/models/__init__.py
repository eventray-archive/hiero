from horus.lib                  import pluralize
from sqlalchemy.ext.declarative import declared_attr

import horus.models
import sqlalchemy as sa

ENTRY_TAG_TABLE_NAME = 'entry_tag'
ENTRY_TAG_ASSOCIATION_TABLE_NAME = 'entry_tag_association'
ENTRY_TABLE_NAME = 'entry'
SERIES_TABLE_NAME = 'series'


# These are the horus mod extensions
class BaseModel(horus.models.BaseModel):
    pass

class UserMixin(horus.models.UserMixin):
    @declared_attr
    def entries(self):
        return sa.orm.relationship(
            'Entry'
            , secondary=ENTRY_TABLE_NAME
            , passive_deletes=True
            , passive_updates=True
            , backref=pluralize(UserMixin.__tablename__)
        )

class GroupMixin(horus.models.GroupMixin):
    pass

class UserGroupMixin(horus.models.UserGroupMixin):
    pass

class ActivationMixin(horus.models.ActivationMixin):
    pass
