<%namespace name="utils" file="hiero:templates/blog_utilities.mako"/>

% for entry in entries:
  ${utils.render_entry(entry)}
% endfor
