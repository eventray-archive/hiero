<%inherit file="hiero:templates/layout.mako"/>

<a href="${request.route_url('hiero_admin_entry_create')}">Create New</a>
<ul>
  <li><a href="${request.route_url('hiero_admin_entry_index')}">Entry List</a></li>
</ul>
