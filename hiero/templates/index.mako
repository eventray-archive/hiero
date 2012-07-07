<%inherit file="hiero:templates/app_layout.mako" />

<%def name="body()">
  <script> 
    if('${logged_in}' === 'True')
      window.logged_in = true;
    else
      window.logged_in = false;
  </script>

  <div class="subnav if-logged-in">
    <ul class="nav nav-pills">
      <li class="dropdown pull-right">
        <a class="dropdown-toggle" data-toggle="dropdown">
          Pages <b class="caret"></b>
        </a> 
        <ul class="pages-nav-list dropdown-menu">
          <li>
             <a id="add-button" href="#">New Page</a>
          </li>
          <li class="divider"></li>
        </ul>
      </li>
    </ul>
  </div>

</%def>

<%def name="title()">
  Home
</%def>
