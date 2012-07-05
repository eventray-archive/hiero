from sqlalchemy             import engine_from_config
from sqlalchemy.orm         import sessionmaker
from paste.deploy.loadwsgi  import appconfig
from pkg_resources          import resource_filename
from pyramid                import testing
from hem.interfaces         import IDBSession
from horus.interfaces       import IHorusUserClass
from horus.interfaces       import IHorusActivationClass
from hiero.tests.models     import Base
from hiero.tests.models     import User
from hiero.tests.models     import Activation

import unittest

settings = appconfig('config:' + resource_filename(__name__, 'test.ini'))

class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        cls.Session = sessionmaker()

    def setUp(self):
        self.config = testing.setUp()

        self.connection = connection = self.engine.connect()

        # begin a non-ORM transaction
        self.trans = connection.begin()

        # bind an individual Session to the connection
        self.session = self.Session(bind=connection)

        self.config.registry.registerUtility(self.session, IDBSession)
        self.config.registry.registerUtility(Activation, IHorusActivationClass)
        self.config.registry.registerUtility(User, IHorusUserClass)

        Base.metadata.bind=connection

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.trans.rollback()
        self.session.close()
