import re

import code

from pyramid.httpexceptions import (
     HTTPFound
    ,HTTPNotFound
    )

from pyramid.view import (
     view_config
    ,forbidden_view_config
    )

from ..models import (
    DBSession
    )

from ..models.page import (
    Page
    )

@view_config(route_name='view_page', renderer='page/view.haml')
def view_card(request):
  page_link_title = request.matchdict['link_title']
  page = DBSession.query(Page).filter_by(link_title=page_link_title).one()
  return dict(
      page=page
      )

