from hiero.interfaces   import IHieroEntryClass
from hiero.interfaces   import IHieroCategoryClass
from hiero.interfaces   import IHieroTagClass
from hiero.interfaces   import IHieroEntryTagClass
from hiero.interfaces   import IHieroSeriesClass
from hem.db             import get_session

class BaseController(object):
    def __init__(self, request):
        self.request = request
        self.session = get_session(request)
        self.Entry = request.registry.getUtility(IHieroEntryClass)
        self.Category = request.registry.getUtility(IHieroCategoryClass)
        self.EntryTag = request.registry.getUtility(IHieroEntryTagClass)
        self.Tag = request.registry.getUtility(IHieroTagClass)
        self.Series = request.registry.getUtility(IHieroSeriesClass)

