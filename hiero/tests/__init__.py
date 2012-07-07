from sqlalchemy             import engine_from_config
from sqlalchemy.orm         import scoped_session
from sqlalchemy.orm         import sessionmaker
from zope.sqlalchemy        import ZopeTransactionExtension
from paste.deploy.loadwsgi  import appconfig
from pkg_resources          import resource_filename
from pyramid                import testing
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization  import ACLAuthorizationPolicy
from pyramid.response       import Response
from hem.interfaces         import IDBSession
from horus.interfaces       import IHorusUserClass
from horus.interfaces       import IHorusActivationClass
from hiero.interfaces       import IHieroEntryClass
from hiero.tests.models     import Base
from hiero.tests.models     import User
from hiero.tests.models     import Activation
from hiero.tests.models     import Entry
from pyramid_beaker         import session_factory_from_settings
from webtest                import TestApp

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
        self.config.registry.registerUtility(Entry, IHieroEntryClass)

        Base.metadata.bind=connection

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.trans.rollback()
        self.session.close()

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

class IntegrationTestBase(unittest.TestCase):
    def main(self, global_config, **settings):
        config = global_config
        config.add_settings(settings)

        self.config.registry.registerUtility(Activation, IHorusActivationClass)
        self.config.registry.registerUtility(User, IHorusUserClass)

        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)


        authn_policy = AuthTktAuthenticationPolicy('secret')
        config.set_authentication_policy(authn_policy)

        session_factory = session_factory_from_settings(settings)

        config.set_session_factory(session_factory)

        config.registry.registerUtility(DBSession, IDBSession)

        config.include('hiero')

        app = config.make_wsgi_app()

        return app

    def setUp(self):
        self.engine = engine_from_config(settings, prefix='sqlalchemy.')
        self.config = testing.setUp()
        app = self.main(self.config, **settings)
        self.app = TestApp(app)
        self.connection = connection = self.engine.connect()

        self.session = app.registry.getUtility(IDBSession)
        self.session.configure(bind=connection)
        # begin a non-ORM transaction
        self.trans = connection.begin()

        Base.metadata.bind=connection

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.trans.rollback()
        self.session.close()
