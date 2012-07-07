from hiero.interfaces   import IHieroEntryClass
from hem.db             import get_session

class BaseController(object):
    def __init__(self, request):
        self.request = request
        self.session = get_session(request)
        self.Entry = request.registry.getUtility(IHieroEntryClass)

