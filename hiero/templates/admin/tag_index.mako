<%inherit file="hiero:templates/layout.mako"/>

<a href="${request.route_url('hiero_admin_tag_create')}">Create New Tag</a>
<br />
% for tag in tags:
  ${tag.title} [ <a href="${request.route_url('hiero_admin_tag_edit', tag=tag.title) }">Edit</a>]<br />
% endfor
