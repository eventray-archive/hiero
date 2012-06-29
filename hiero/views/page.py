import re
import code
import transaction

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

@view_config (route_name='get_pages',    renderer='page/list.haml')
def get_pages(request):
  pages = DBSession.query(Page).all()
  return {
      "pages": pages,
      "logged_in": True
      }

@view_config (route_name='get_page', 
              renderer='page/view_add_edit.haml')
@view_config (route_name='edit_page',
              renderer='json')
@view_config (route_name='add_page')
@view_config (route_name='remove_page')
def get_page (request):
  page_link_title = request.matchdict['link_title']
  print "page: "+page_link_title
  resultset = DBSession.query(Page).filter_by(link_title=page_link_title)
  if resultset.count() == 0L:
    return HTTPNotFound("There is no page called '"+page_link_title+"'. Sorry.")
  page = resultset.one()
  if request.matched_route.name == "edit_page":
    print "editing page"
    params = request.params
    original_link_title = page.link_title
    print "new link_title: " + params["link_title"]
    page.link_title   = params[u"link_title"]
    page.title        = params[u"title"] 
    page.subtitle     = params[u"subtitle"]
    page.type         = params[u"type"]
    page.content      = params[u"content"]
    with transaction.manager:
      DBSession.add(page) 
    if original_link_title != params["link_title"]:
      return dict(
          redirect_url=request.route_url('get_page', link_title=params["link_title"])
      )
    else:
      return {}
  else:
    return {
        "page": page,
        "logged_in": True
        }


