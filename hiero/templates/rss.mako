<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>${title}</title>
    <description>${description}</description>
    <link>${link}</link>
    <language>${language}</language>
    <copyright>${copyright}</copyright>
    <pubDate>${pub_date}</pubDate>
    <lastBuildDate>${last_build_date}</lastBuildDate>
    <generator>Hiero</generator>
    <ttl>60</ttl>
    % for entry in entries:
      <item>
        <title>${entry.title}</title>
        <description>${entry.html_content}</description>
        <link>url</link>
        <guid isPermaLink="true">${request.route_url('hiero_entry_detail', slug=entry.slug)}</guid>
        <pubDate>${entry.published_on}</pubDate>
        <source url="">url</source>
      </item>
    % endfor
  </channel>
</rss>
