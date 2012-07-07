from hiero.tests    import BaseTestCase
from hiero.tests    import IntegrationTestBase
from pyramid        import testing
from mock           import Mock

class TestBlogController(BaseTestCase):
    def test_index_inactive(self):
        from hem.db                 import IDBSession
        from hiero.views.blog       import EntryController
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

        self.config.add_route('hiero_entry_index', '/')

        request = testing.DummyRequest()

        owner = User(user_name='sontek', email='sontek@gmail.com')
        owner.set_password('foo')

        self.session.add(owner)

        entry = Entry(owner=owner, title='test entry', content='hi',
            html_content='hi<br />'
        )

        entry1 = Entry(owner=owner, title='test entry 2', content='hi',
            html_content='hi<br />'
        )

        self.session.add(entry)
        self.session.add(entry1)

        self.session.flush()

        controller = EntryController(request)

        results = controller.index()

        entries = results['entries']

        assert len(entries) == 0

    def test_index_active(self):
        from hem.db                 import IDBSession
        from hiero.views.blog       import EntryController
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

        self.config.add_route('hiero_entry_index', '/')

        request = testing.DummyRequest()

        owner = User(user_name='sontek', email='sontek@gmail.com')
        owner.set_password('foo')

        self.session.add(owner)

        entry = Entry(owner=owner, title='test entry', content='hi',
            html_content='hi<br />', is_published=True
        )

        entry1 = Entry(owner=owner, title='test entry 2', content='hi',
            html_content='hi<br />', is_published=True
        )

        self.session.add(entry)
        self.session.add(entry1)

        self.session.flush()

        controller = EntryController(request)

        results = controller.index()

        entries = results['entries']

        assert len(entries) == 2
        assert entries[0] == entry
        assert entries[1] == entry1

    def test_detail(self):
        from hem.db                 import IDBSession
        from hiero.views.blog       import EntryController
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

        self.config.add_route('hiero_entry_index', '/')

        request = testing.DummyRequest()
        request.matchdict = Mock()

        owner = User(user_name='sontek', email='sontek@gmail.com')
        owner.set_password('foo')

        self.session.add(owner)

        entry = Entry(owner=owner, title='test entry', content='hi',
            html_content='hi<br />', is_published=True
        )

        entry1 = Entry(owner=owner, title='test entry 2', content='hi',
            html_content='hi<br />', is_published=True
        )

        self.session.add(entry)
        self.session.add(entry1)

        self.session.flush()

        def get(key, default):
            if key == 'slug':
                return entry1.slug

        request.matchdict.get = get

        controller = EntryController(request)

        results = controller.detail()

        returned_entry = results['entry']
        returned_entry == entry

class TestBlogIntegrationViews(IntegrationTestBase):
    def test_index(self):
        """ Call the index view, make sure routes are working """
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry

        owner = User(user_name='sontek', email='sontek@gmail.com')
        owner.set_password('foo')


        entry = Entry(owner=owner, title='test entry', content='hi',
            html_content='hi<br />foo', is_published=True
        )

        entry1 = Entry(owner=owner, title='test entry 1', content='hi',
            html_content='hi<br />bar', is_published=True
        )

        self.session.add(owner)
        self.session.add(entry)
        self.session.add(entry1)

        res = self.app.get('/')
        assert res.status_int == 200
        assert 'foo' in res.body
        assert 'bar' in res.body

    def test_detail(self):
        """ Call the detail view, make sure routes are working """
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry

        owner = User(user_name='sontek', email='sontek@gmail.com')
        owner.set_password('foo')


        entry = Entry(owner=owner, title='test entry', content='hi',
            html_content='hi<br />', is_published=True
        )

        self.session.add(owner)
        self.session.add(entry)
        self.session.flush()

        res = self.app.get('/test-entry')
        assert res.status_int == 200
        assert 'hi' in res.body

    def test_edit(self):
        """ Call the edit view, make sure routes are working """
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry

        owner = User(user_name='sontek', email='sontek@gmail.com')
        owner.set_password('foo')


        entry = Entry(owner=owner, title='test entry', content='hi',
            html_content='hi<br />', is_published=True
        )

        self.session.add(owner)
        self.session.add(entry)
        self.session.flush()

        res = self.app.get('/test-entry/edit')
        assert res.status_int == 200
        assert 'EDIT' in res.body
