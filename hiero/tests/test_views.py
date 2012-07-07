from hiero.tests            import BaseTestCase
from hiero.views            import BaseController
from pyramid                import testing

class TestViewController(BaseTestCase):
    def test_init(self):
        from hem.db                 import IDBSession
        from horus.interfaces       import IHorusUserClass
        from horus.interfaces       import IHorusActivationClass
        from hiero.interfaces       import IHieroEntryClass
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry
        from hiero.tests.models     import Activation

        self.config.registry.registerUtility(Activation, IHorusActivationClass)
        self.config.registry.registerUtility(User, IHorusUserClass)
        self.config.registry.registerUtility(Entry, IHieroEntryClass)
        self.config.registry.registerUtility(self.session, IDBSession)

        request = testing.DummyRequest()
        controller = BaseController(request)

        assert controller.Entry == Entry
