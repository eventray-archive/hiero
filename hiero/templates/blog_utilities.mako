<%def name="render_entry(entry)">
  <div class="entry">
  <h1><a href="${request.route_url('hiero_entry_detail', slug=entry.slug)}">${entry.title}</a></h1>
      <div class="entry-content">
      ${entry.html_content | n }
      </div>
  </div>
</%def>
