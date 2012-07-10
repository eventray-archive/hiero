<%inherit file="hiero:templates/layout.mako"/>

<a href="${request.route_url('hiero_admin_series_create')}">Create New series</a>
<br />
% for s in series:
  ${s.title} [ <a href="${request.route_url('hiero_admin_series_edit', slug=s.slug) }">Edit</a>]<br />
% endfor
