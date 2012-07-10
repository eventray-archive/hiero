<%inherit file="hiero:templates/layout.mako"/>

<a href="${request.route_url('hiero_admin_category_create')}">Create New Category</a>
<br />
% for category in categories:
  ${category.title} [ <a href="${request.route_url('hiero_admin_category_edit', slug=category.slug) }">Edit</a>]<br />
% endfor
