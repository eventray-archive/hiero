<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>${self.title()}</title>

    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
    ${ stylesheet_link_tag(request, "/hiero/css/app.css") | n }

    ${ script_tag(request, "/hiero/js/jquery-1.7.1.js") | n }
    ${ script_tag(request, "/hiero/js/underscore.js") | n }
    ${ script_tag(request, "/hiero/js/backbone.js") | n }
    ${ script_tag(request, "/hiero/js/jquery.pjax.js") | n }
    ${ script_tag(request, "/hiero/js/bootstrap-transition.js") | n }
    ${ script_tag(request, "/hiero/js/bootstrap-modal.js") | n }
    ${ script_tag(request, "/hiero/js/bootstrap-dropdown.js") | n }
    ${ script_tag(request, "/hiero/js/app.js") | n }

    ${ self.local_assets() }

    <!-- [if lte IE 6]
    stylesheet_link_tag(request, "ie6.css")
    -->

  </head>
  <body>
    ${self.body()}
  </body>
</html>

<%def name="local_assets()">
</%def>

<%def name="title()">
  <title>Home</title>
</%def>
