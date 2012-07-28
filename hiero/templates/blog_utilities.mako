<%def name="render_entry(entry)">
  title: ${entry.title}<br />
  slug: ${entry.slug}<br />
  html_content: ${entry.html_content | n }
  <hr />
</%def>
