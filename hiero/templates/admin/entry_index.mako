<%inherit file="hiero:templates/layout.mako"/>

<a href="${request.route_url('hiero_admin_entry_create')}">Create New Entry</a>
<br />
% for entry in entries:
  ${entry.title} [ <a href="${request.route_url('hiero_admin_entry_edit', slug=entry.slug) }">Edit</a>]<br />
% endfor
