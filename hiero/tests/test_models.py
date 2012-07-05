from hiero.tests        import BaseTestCase
from sqlalchemy.types   import DateTime
from sqlalchemy         import Column
from datetime           import datetime
from hiero.tests.models import Base

class TestModel(Base):
    start_date = Column(DateTime)

class TestModels(BaseTestCase):
    def test_tablename(self):
        model = TestModel()
        assert model.__tablename__ == 'test_model'

    def test_json(self):
        model = TestModel()
        model.pk = 1
        model.start_date = datetime.now()

        assert model.__json__() == {'pk': 1, 'start_date': model.start_date.isoformat()}

class TestEntry(BaseTestCase):
    def test_create_entry(self):
        from hiero.tests.models import User
        from hiero.tests.models import Entry
        owner = User(user_name='sontek', email='sontek@gmail.com')
        owner.set_password('foo')
        self.session.add(owner)
        self.session.flush()

        entry = Entry(owner_pk=owner.pk)


