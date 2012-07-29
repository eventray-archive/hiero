from hem.schemas        import CSRFSchema
from horus.resources    import RootFactory
from horus.interfaces   import IHorusUserClass
from hiero.interfaces   import IHieroSeriesClass
from hiero.interfaces   import IHieroCategoryClass

import colander
import deform

@colander.deferred
def owner_widget(node, kw):
    choices = [('', '')]
    request = kw.get('request')
    User = request.registry.getUtility(IHorusUserClass)

    for user in User.get_all(request):
        choices.append((str(user.pk), user.user_name))

    widget = deform.widget.SelectWidget(values=choices,
            template='hiero:templates/widgets/select_user')
    widget.request = request
    return widget

@colander.deferred
def owner_default(node, kw):
    request = kw.get('request')

    if not isinstance(request.context, RootFactory):
        return request.context.owner_pk

@colander.deferred
def series_widget(node, kw):
    choices = [('', '')]
    request = kw.get('request')
    Series = request.registry.getUtility(IHieroSeriesClass)

    for series in Series.get_all(request):
        choices.append((str(series.pk), series.title))

    widget = deform.widget.SelectWidget(values=choices,
        template='hiero:templates/widgets/select_series')
    widget.request = request

    return widget

@colander.deferred
def series_default(node, kw):
    request = kw.get('request')

    if not isinstance(request.context, RootFactory):
        return request.context.series_pk

@colander.deferred
def category_widget(node, kw):
    choices = [('', '')]
    request = kw.get('request')
    Category = request.registry.getUtility(IHieroCategoryClass)

    for category in Category.get_all(request):
        choices.append((str(category.pk), category.title))

    widget = deform.widget.SelectWidget(values=choices,
        template='hiero:templates/widgets/select_category'
    )

    widget.request = request

    return widget

@colander.deferred
def category_default(node, kw):
    request = kw.get('request')

    if not isinstance(request.context, RootFactory):
        return request.context.category_pk

@colander.deferred
def markup_widget(node, kw):
    choices = [('', '')]
    request = kw.get('request')
    formatters = ['markdown', 'htmlblock', 'rst']
    for formatter in formatters:
        choices.append((formatter, formatter))

    widget = deform.widget.SelectWidget(values=choices)
    widget.request = request

    return widget

@colander.deferred
def markup_default(node, kw):
    request = kw.get('request')

    if not isinstance(request.context, RootFactory):
        return request.context.markup


class EntryAdminSchema(CSRFSchema):

    title = colander.SchemaNode(colander.String(),
        validator=colander.Length(max=128)
    )

    slug = colander.SchemaNode(
        colander.String()
        , validator=colander.Length(max=128)
        , missing = None
    )

    markup = colander.SchemaNode(
        colander.String()
        , widget = markup_widget
        , default = markup_default
    )

    content = colander.SchemaNode(
        colander.String()
        , widget = deform.widget.TextAreaWidget(rows=25, css_class='content')
    )

    owner = colander.SchemaNode(
        colander.String()
        , widget = owner_widget
        , default = owner_default
    )

    series = colander.SchemaNode(
        colander.String()
        , widget = series_widget
        , default = series_default
        , missing = None
    )

    category = colander.SchemaNode(
        colander.String()
        , widget = category_widget
        , default = category_default
        , missing = None
    )

    is_featured = colander.SchemaNode(
        colander.Boolean()
        , missing = False
    )

    is_published = colander.SchemaNode(
            colander.Boolean()
            , missing = False
    )

    enable_comments = colander.SchemaNode(
        colander.Boolean()
        , missing = False
    )

    published_on = colander.SchemaNode(
        colander.DateTime()
        , missing = None
    )


class CategoryAdminSchema(CSRFSchema):
    title = colander.SchemaNode(colander.String(),
        validator=colander.Length(max=128)
    )

    slug = colander.SchemaNode(
        colander.String()
        , validator=colander.Length(max=128)
        , missing = None
    )

class SeriesAdminSchema(CSRFSchema):
    title = colander.SchemaNode(colander.String(),
        validator=colander.Length(max=128)
    )

    slug = colander.SchemaNode(
        colander.String()
        , validator=colander.Length(max=128)
        , missing = None
    )
