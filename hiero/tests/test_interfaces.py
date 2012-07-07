from hiero.tests import BaseTestCase

class TestInterfaces(BaseTestCase):
    def test_entry_class(self):
        """ Shouldn't be able to instantiate the interface """
        from hiero.interfaces import IHieroEntryClass

        def make_session():
            IHieroEntryClass('1')

        self.assertRaises(TypeError, make_session)
