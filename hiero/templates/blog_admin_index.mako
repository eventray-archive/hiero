<a href="${request.route_url('hiero_admin_entry_create')}">Create New</a>
<br />
% for entry in entries:
  ${entry.title} <br />
% endfor
