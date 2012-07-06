<%inherit file="../app_layout.mako" />

<%def name="local_assets()" >
		
  ${ stylesheet_link_tag(request, "/hiero/css/page.css") | n }

  ${ script_tag(request, "/EpicEditor/epiceditor/js/epiceditor.js") | n }
  ${ script_tag(request, "/hiero/js/xdate.js") | n }
  ${ script_tag(request, "/hiero/js/page.js") | n }

</%def>
