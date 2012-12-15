from hiero.tests            import BaseTestCase
from hiero.views            import BaseController
from pyramid                import testing

class TestViewController(BaseTestCase):
    def test_init(self):
        from hem.db                 import IDBSession
        from horus.interfaces       import IUserClass
        from horus.interfaces       import IActivationClass

        self.config.registry.registerUtility(Activation, IActivationClass)
        self.config.registry.registerUtility(User, IUserClass)
        self.config.registry.registerUtility(self.session, IDBSession)

        request = testing.DummyRequest()
        controller = BaseController(request)

        assert controller.Entry == Entry
