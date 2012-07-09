% if appstruct:
  ${form.render(appstruct=appstruct)|n}
% else:
  ${form.render()|n}
% endif
