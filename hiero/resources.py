from horus.resources import RootFactory
from hiero.interfaces   import IHieroEntryClass
from hiero.interfaces   import IHieroCategoryClass
from hiero.interfaces   import IHieroSeriesClass
from hiero.interfaces   import IHieroTagClass

class EntryFactory(RootFactory):
    def __init__(self, request):
        self.request = request
        self.Entry = request.registry.getUtility(IHieroEntryClass)

    def __getitem__(self, key):
        entry = self.Entry.get_by_slug(self.request, key).one()

        if entry:
            entry.__parent__ = self
            entry.__name__ = key

        return entry

class CategoryFactory(RootFactory):
    def __init__(self, request):
        self.request = request
        self.Category = request.registry.getUtility(IHieroCategoryClass)

    def __getitem__(self, key):
        category = self.Category.get_by_slug(self.request, key).one()

        if category:
            category.__parent__ = self
            category.__name__ = key

        return category

class TagFactory(RootFactory):
    def __init__(self, request):
        self.request = request
        self.Tag = request.registry.getUtility(IHieroTagClass)

    def __getitem__(self, key):
        tag = self.Tag.get_by_title(self.request, key).one()

        if tag:
            tag.__parent__ = self
            tag.__name__ = key

        return tag


class SeriesFactory(RootFactory):
    def __init__(self, request):
        self.request = request
        self.Series = request.registry.getUtility(IHieroSeriesClass)

    def __getitem__(self, key):
        series = self.Series.get_by_slug(self.request, key).one()

        if series:
            series.__parent__ = self
            series.__name__ = key

        return series
