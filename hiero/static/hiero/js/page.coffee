
window.page_prev_content = null
$(document).ready () ->
  console.log("here we go...")
  buildPagesMenu()
  $(".dropdown-toggle").dropdown()
  # jQuery.get("/pages", (pages) ->
  #   for page in pages
  #     $(".pages-nav-list").append("<li><a href='#{page.url}'>#{page.link_title}</a></li>")
  #   $(".dropdown-toggle").dropdown()
  # )

  window.editor = new EpicEditor(
    basePath: "/static/EpicEditor/epiceditor"
    file:
      autoSave: 10000
  )
  editor.load()
  page = getPageDefaults()
  $(".page-link-title-original").val(page.link_title)
  setPage page
  renderPage(page)

  # view event callbacks
  $(".page-link-title").change (e) ->
    page = getPage()
    console.log("link_title changed")
    original_link_title = $(".page-link-title-original").val()
    if `original_link_title != page.link_title` # todo: no backticks
      modal = $("#confirm-change-link-title-modal")
      modal.modal('show')
      window.auto_save_okay = false
      modal.find(".btn-confirm").click (e) ->
        window.auto_save_okay = true
        modal.modal('hide')
      modal.find(".btn-cancel").click (e) ->
        window.auto_save_okay = true
        modal.modal('hide')
        $("input.page-link-title").val(original_link_title)
  $("#fullscreen-button").click (e) ->
    editor.setFullscreen(true)

  $("#preview-button").click (e) ->
    page = getPage()
    if page.type is "custom"
      editor.preview()
    else
      setPage(page)
    $(".if-view-mode").show()
    $(".if-edit-mode").hide()

  $("#edit-button").click (e) ->
    page = getPage()
    if page.type is "custom"
      editor.edit()
    $(".if-view-mode").hide()
    $(".if-edit-mode").show()

  $("#save-button").click (e) ->
    page = getPage()
    console.log("saving link title as #{page.link_title}")
    savePage(page)

  $("#add-button").click (e) ->
    jQuery.post("/add_page", null, (e) ->
      window.location.href = e.redirect_url
    )

  $("#remove-button").click (e) ->
    modal = $("#confirm-delete-modal")
    modal.modal('show')

    modal.find(".btn-confirm").click (e) ->
      window.auto_save_okay = false
      modal.modal('hide')
      original_link_title = $(".page-link-title-original").val()
      jQuery.post("/pages/#{original_link_title}/remove", null, (e) ->
        window.location.href = e.redirect_url
      )
      
    modal.find(".btn-cancel").click (e) ->
      window.auto_save_okay = true
      modal.modal('hide')
      $("input.page-link-title").val(original_link_title)
      

  editor.on("save", () ->
    original_link_title = $(".page-link-title-original").val()
    # if original_link_title == page.link_title
    if auto_save_okay
      savePage(getPage())
  )

  $(this).keydown (e) ->
    console.log("Keycode: #{e.keyCode}")

  $(".page-type").change (e) ->
    console.log("page type changed")
    page = getPage()
    renderPage(page)


window.renderPage = (page) ->
  if window.logged_in
    $(".if-logged-in").show()
    $(".if-not-logged-in").hide()
    $(".if-view-mode").hide()
  else
    $(".if-logged-in").hide()
    $(".if-not-logged-in").show()

  if page.type is "custom"
    $(".if-custom-page").show()
    $(".if-not-custom-page").hide()
  else
    $(".if-not-custom-page").show()
    $(".if-custom-page").hide()


window.buildPagesMenu = () ->
  $(".pages-nav-list").html("<li><a id='add-button'>New Page</a></li><li class='divider'></li>")
  jQuery.get("/pages", (pages) ->
    for page in pages
      $(".pages-nav-list").append("<li><a href='#{page.url}'>#{page.link_title}</a></li>")
  )

window.auto_save_okay = true
window.savePage = (page, success_callback) ->
  $.ajax(
    type: 'POST'
    url:  "/pages/#{page.link_title_original}/edit"
    data: page
    success: (e) ->
      window.location.href = e.redirect_url if e.redirect_url?
      success_callback(e) if success_callback?
      prettyTime = (new XDate()).toString("dddd, h:mm:ss tt")

      $(".page-last-saved-time").text("Page was last saved on #{prettyTime}")
      dataType: "json"
  )

window.setPage = (data) ->
  $(".page-link-title").val(data.link_title)
  $(".page-title").val(data.title).text(data.title)
  $(".page-subtitle").val(data.subtitle).text(data.subtitle)
  $(".page-type").val(data.type)
  $(".page-content").html(marked(data.content))
  editor.setText(data.content)
  return undefined

window.getPage = () ->
  data =
    link_title_original:
                     $("input.page-link-title-original").val()
    link_title:      $("input.page-link-title").val()
    title:           $("input.page-title").val()
    subtitle:        $("input.page-subtitle").val()
    type:            $("select.page-type").val()
    content:        editor.getText()
  return data
