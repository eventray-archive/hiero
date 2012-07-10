<%inherit file="hiero:templates/layout.mako"/>

<% resources = form.get_widget_resources() %>

% for js in resources['js']:
  <script type="text/javascript" src="${js}"></script>
% endfor

% for css in resources['css']:
  <link rel="stylesheet" href="${css}"/>
% endfor 
% if appstruct:
  ${form.render(appstruct=appstruct)|n}
% else:
  ${form.render()|n}
% endif
