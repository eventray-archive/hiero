<%def name="render_entry(entry)"> 
  <a href="${request.route_url('hiero_entry_detail', slug=entry.slug)}"><h1 class="entry-title">${entry.title}</h1></a>
  <p class="entry-metadata">
    Posted by ${entry.owner.user_name} on ${entry.published_on}
  </p>
  <div class="entry-content">
    ${entry.html_content | n }
  </div>
</%def>

