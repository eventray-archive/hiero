# import re
# import code
# import transaction

# from pyramid.httpexceptions import (
#      HTTPFound
#     ,HTTPNotFound
#     )

# from pyramid.view import (
#      view_config
#     ,forbidden_view_config
#     )

# from ..models import (
#     DBSession
#     )

# from ..models.page import (
#     Page
#     )

# def escapeNewlines(s):
#   return s.replace("\n", "\\n")



# @view_config (route_name='home',
#               renderer='index.mako')
# def home(request):
#   return {
#       "logged_in": True
#       }

# @view_config (route_name='get_pages',    
#               renderer='json')
# def get_pages(request):
#   pages = DBSession.query(Page).all()
#   result = []
#   for page in pages:
#     result.append({
#       "id": page.id,
#       "link_title": page.link_title,
#       "url": request.route_url('get_page', link_title=page.link_title)
#       }) 
#   return result

# @view_config (route_name='get_page', 
#               renderer='page/view_add_edit.mako')
# @view_config (route_name='edit_page',
#               renderer='json')
# @view_config (route_name='add_page',
#               renderer='json')
# @view_config (route_name='remove_page',
#               renderer='json')
# def get_page (request):

#   route = request.matched_route.name
#   if route == "add_page":
#     untitled_number = 1
#     def link_title():
#       return "untitled_"+str(untitled_number)
#     while DBSession.query(Page).filter_by(link_title=link_title()).count() != 0L:
#       untitled_number += 1
#     page = Page(
#         link_title(),
#         "",
#         "",
#         "custom",
#         None,
#         None
#     )
#     with transaction.manager:
#       DBSession.add(page)

#     return {
#         "redirect_url": request.route_url('get_page', link_title=link_title())
#     }



#   page_link_title = request.matchdict['link_title']
#   print "page: "+page_link_title
#   resultset = DBSession.query(Page).filter_by(link_title=page_link_title)
#   if resultset.count() == 0L:
#     return HTTPNotFound("There is no page called '"+page_link_title+"'. Sorry.")
#   page = resultset.one()
#   if route == "remove_page":
#     with transaction.manager:
#       DBSession.delete(page)
#     return {
#         "redirect_url": request.route_url('home')
#         }
#   if route == "edit_page":
#     print "editing page"
#     params = request.params
#     original_link_title = page.link_title
#     print "new link_title: " + params["link_title"]
#     page.link_title   = params[u"link_title"]
#     page.title        = params[u"title"] 
#     page.subtitle     = params[u"subtitle"]
#     page.type         = params[u"type"]
#     page.content      = escapeNewlines(params[u"content"])
#     with transaction.manager:
#       DBSession.add(page) 
#     if original_link_title != params["link_title"]:
#       print "link_title changed"
#       return dict(
#           redirect_url=request.route_url('get_page', link_title=params["link_title"])
#       )
#     else:
#       return {}
#   else:
#     return {
#         "page": page,
#         "logged_in": True
#         }


