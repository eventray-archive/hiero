<form class="form-horizontal" method='POST'>
  <fieldset>
    <legend>Create Entry</legend>
    <div class="control-group">
      <label class="control-label" for="title">Title</label>
      <div class="controls">
        <input type="textbox" class="input-xlarge" id="title" name="title">
        </input>
        <p class="help-block">Supporting help text</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="content">Content</label>
      <div class="controls">
        <textarea class="input-xlarge" id="content" name="content">
        </textarea>
        <p class="help-block">Supporting help text</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="created_on">Created On</label>
      <div class="controls">
        <input type="textbox" class="input-xlarge" id="created_on" name="created_on">
        </input>
        <p class="help-block">Supporting help text</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="created_on">Published On</label>
      <div class="controls">
        <input type="textbox" class="input-xlarge" id="published_on" name="published_on">
        </input>
        <p class="help-block">Supporting help text</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="owner">Owner</label>
      <div class="controls">
        <select class="input-xlarge" id="owner" name="owner">
        </select>
        <p class="help-block">Supporting help text</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="series">Series</label>
      <div class="controls">
        <select class="input-xlarge" id="series" name="series">
        </select>
        <p class="help-block">Supporting help text</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="category">Category</label>
      <div class="controls">
        <select class="input-xlarge" id="category" name="category">
        </select>
        <p class="help-block">Supporting help text</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="is_featured">Is Featured</label>
      <div class="controls">
        <input type="checkbox" class="input-xlarge" id="is_featured" 
          name="is_featured">
        <p class="help-block">Supporting help text</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="is_published">Is Published</label>
      <div class="controls">
        <input type="checkbox" class="input-xlarge" id="is_published" 
          name="is_published">
        <p class="help-block">Supporting help text</p>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="enable_comments">Enable Comments</label>
      <div class="controls">
        <input type="checkbox" class="input-xlarge" id="enable_comments" 
          name="enable_comments">
        <p class="help-block">Supporting help text</p>
      </div>
    </div>
    <button type="submit" class="btn">Save</button>
  </fieldset>
</form>
