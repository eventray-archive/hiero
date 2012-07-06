<%inherit file="page_layout.mako" />

<%def name="body()">
	<script>
    if('${logged_in}' === 'True') 
			window.logged_in = true;
		else
			window.logged_in = false;
		function getPageDefaults() { 
			return {
        link_title:     "${page.link_title}",
        new_link_title: "${page.link_title}",
        title:          "${page.title}",
        subtitle:       "${page.subtitle}",
        type:           "${page.type}",
        content:        "${page.content}"
			}
		}
	</script>
	<div class="subnav if-logged-in">
		<ul class="nav nav-pills">
			<li class="active pull-right">
				<a id="save-button" class="if-edit-mode">
					Save
				</a>
			</li>
			<li class="active pull-right">
				<a id="edit-button" class="if-view-mode">
					Edit
				</a>
			</li>
			<li class="pull-right">
				<a id="remove-button">
					Delete
				</a>
			</li>
			<li class="pull-right">
				<a id="preview-button" class="if-edit-mode">
					Preview
				</a>
			</li>
			<li class="pull-right">
				<a id="fullscreen-button" class="if-custom-page if-edit-mode">
					Fullscreen
				</a>
			</li>
			<li class="dropdown pull-right">
				<a class="dropdown-toggle" data-toggle="dropdown">
					Pages
					<b class="caret"></b>
				</a>
				<ul class="pages-nav-list dropdown-menu">
					<li>
						<a id="add-button">New Page</a>
					</li>
					<li class="divider"></li>
				</ul>
			</li>
			<li class="pull-right">
				<span class="page-last-saved-time"></span>
			</li>
		</ul>
	</div>
	<div class="subnav if-not-logged-in">
		<ul class="nav nav-pills pages-nav-list"></ul>
	</div>
	<div class="if-view-mode if-not-logged-in">
		<h1 class="page-title if-not-custom-page"></h1>
		<h2 class="page-subtitle if-not-custom-page"></h2>
		<div class="page-content"></div>
	</div>
	<div class="if-edit-mode if-logged-in">
		<div class="form-horizontal">
			<fieldset>
				<input class="page-link-title-original" type="hidden" />
				<div class="control-group">
					<label class="control-label">Link Title:</label>
					<div class="controls">
						<input class="page-link-title" type="text" />
						<p class="help-block">The title used in menus, links and the page's URL</p>
					</div>
				</div>
				<div class="control-group">
					<label class="control-label">Page Type:</label>
					<div class="controls">
						<select class="page-type">
							<option value="custom">Custom</option>
							<option value="blog">Blog</option>
							<option value="contact">Contact</option>
						</select>
					</div>
				</div>
				<div class="if-not-custom-page">
					<div class="control-group">
						<label class="control-label">Title</label>
						<div class="controls">
              <input class="input-xlarge page-title" value="${page.title}" />
						</div>
					</div>
					<div class="control-group">
						<label class="control-label">Subtitle</label>
						<div class="controls">
              <input class="input-xlarge page-subtitle" value="${page.subtitle}" />
						</div>
					</div>
				</div>
				<div class="if-custom-page">
					<div class="control-group">
						<label class="control-label">
              <h1>${page.link_title}:</h1>
						</label>
						<div class="controls">
							<div id="epiceditor"></div>
						</div>
					</div>
				</div>
			</fieldset>
		</div>
	</div>
	<div id="confirm-change-link-title-modal" class="modal hide">
		<div class="modal-header">
			<button class="close" data-dismiss="model">&times;</button>
			<h3>Confirm Changes.</h3>
		</div>
		<div class="modal-body">
			If you change the link title, any URLs for this page already out there will need to be updated. Do you want to continue saving?
		</div>
		<div class="modal-footer">
			<a class="btn btn-cancel" href="#">Nevermind!</a>
			<a class="btn btn-primary btn-confirm" href="#">No big deal.</a>
		</div>
	</div>
	<div id="confirm-delete-modal" class="modal hide">
		<div class="modal-header">
			<button class="close" data-dismiss="model">&times;</button>
			<h3>Confirm Deletion</h3>
		</div>
		<div class="modal-body">
			Sure you want to delete this page?
		</div>
		<div class="modal-footer">
			<a class="btn btn-cancel" href="#">Nevermind</a>
			<a class="btn btn-primary btn-confirm" href="#">Do it!</a>
		</div>
	</div>
</%def>
