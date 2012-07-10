<%inherit file="hiero:templates/layout.mako"/>

<a href="${request.route_url('hiero_admin_entry_create')}">New Entry</a> | 
<a href="${request.route_url('hiero_admin_category_create')}">New Category</a> |
<a href="${request.route_url('hiero_admin_series_create')}">New Series</a>

<ul>
  <li><a href="${request.route_url('hiero_admin_entry_index')}">Entry List</a></li>
  <li><a href="${request.route_url('hiero_admin_category_index')}">Category List</a></li>
  <li><a href="${request.route_url('hiero_admin_series_index')}">Series List</a></li>
</ul>
