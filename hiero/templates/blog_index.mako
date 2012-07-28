<%namespace name="render_entry" file="hiero:templates/blog_utilities.mako"/>

% for entry in entries:
  ${render_entry(entry)}
% endfor
