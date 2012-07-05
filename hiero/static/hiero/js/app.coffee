
$(document).ready () ->
  console.log("here we go...")
  options =
    logged_in: window.logged_in
  buildPagesMenu(options)
  render(options)

window.buildPagesMenu = (options) ->
  if options.logged_in
    $(".pages-nav-list").html("<li><a id='add-button'>New Page</a></li><li class='divider'></li>")

  jQuery.get("/pages", (pages) ->
    for page in pages
      $(".pages-nav-list").append("<li><a href='#{page.url}'>#{page.link_title}</a></li>")
  )

window.render = (options) ->
  if options.logged_in
    $(".if-logged-in").show()
    $(".if-not-logged-in").hide()
    $(".if-view-mode").hide()
  else
    $(".if-logged-in").hide()
    $(".if-not-logged-in").show()
