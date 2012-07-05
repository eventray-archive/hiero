from hiero.tests        import BaseTestCase
from hiero.tests.models import Base
from sqlalchemy.types   import DateTime
from sqlalchemy         import Column
from datetime           import datetime

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
