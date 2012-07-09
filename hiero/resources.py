from horus.resources import RootFactory
from hiero.interfaces   import IHieroEntryClass

class EntryFactory(RootFactory):
    def __init__(self, request):
        self.request = request
        self.Entry = request.registry.getUtility(IHieroEntryClass)

    def __getitem__(self, key):
        entry = self.Entry.get_by_slug(self.request, key)

        if entry:
            entry.__parent__ = self
            entry.__name__ = key

        return entry
