

$(document).ready () ->
  console.log("here we go...")
  window.editor = new EpicEditor(
    basePath: "/static/EpicEditor/epiceditor"
  )
  editor.load()
  page = getPageDefaults()
  $(".page-link-title-original").val(page.link_title)
  setPage page
  renderPage(page)

  # view event callbacks
  $("#preview-button").click (e) ->
    page = getPage()
    setPage(page)
    $("#view").show()
    $("#add_edit").hide()
  $("#edit-button").click (e) ->
    $("#view").hide()
    $("#add_edit").show()
  $("#save-button").click (e) ->
    page = getPage()
    original_link_title = $(".page-link-title-original").val()
    console.log("lt: #{page.link_title}")
    console.log("olt: #{original_link_title}")

    # using backticks to interpolate javascript, there has to be a better way to do this in coffee
    if `original_link_title != page.link_title`
      console.log("link title changed")
      modal = $("#confirm-change-link-title-modal")
      modal.modal('show')
      modal.find(".btn-primary").click (e) ->
        savePage(page, (e) ->
            modal.modal('hide')
        )
    else
      savePage(page)
  window.setInterval(
    (e) ->
      original_link_title = $(".page-link-title-original").val()
      if original_link_title == page.link_title
        savePage(getPage())
    5000
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
  else
    $(".if-logged-in").hide()
    $(".if-not-logged-in").show()

  if page.type is "custom"
    $(".if-custom-page").show()
    $(".if-not-custom-page").hide()
  else
    $(".if-not-custom-page").show()
    $(".if-custom-page").hide()


window.savePage = (page, success_callback) ->
  console.log("saving ", page)
  $.ajax(
    type: 'POST'
    url:  "/pages/#{page.link_title_original}/edit"
    data: page
    success: (e) ->
      console.log "successful postback :)"
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
  editor.setContents(data.content)
  return undefined

window.getPage = () ->
  data =
    link_title_original:
                     $("input.page-link-title-original").val()
    link_title:      $("input.page-link-title").val()
    title:           $("input.page-title").val()
    subtitle:        $("input.page-subtitle").val()
    type:            $("select.page-type").val()
    content:        editor.getContents()
  return data
