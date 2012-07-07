% for entry in entries:
  ${render_entry(entry)}
% endfor

<%def name="render_entry(entry)">
  title: ${entry.title}
  slug: ${entry.slug}
  html_content: ${entry.html_content}
</%def>
