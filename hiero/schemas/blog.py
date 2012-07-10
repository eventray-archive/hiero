from hem.schemas        import CSRFSchema
from horus.resources    import RootFactory
from horus.interfaces   import IHorusUserClass
from hiero.interfaces   import IHieroSeriesClass
from hiero.interfaces   import IHieroCategoryClass

import colander
import deform

@colander.deferred
def owner_widget(node, kw):
    choices = []
    request = kw.get('request')
    User = request.registry.getUtility(IHorusUserClass)

    for user in User.get_all(request):
        choices.append((str(user.pk), user.user_name))

    return deform.widget.SelectWidget(values=choices)

@colander.deferred
def owner_default(node, kw):
    request = kw.get('request')

    if not isinstance(request.context, RootFactory):
        return request.context.owner_pk

@colander.deferred
def series_widget(node, kw):
    choices = []
    request = kw.get('request')
    Series = request.registry.getUtility(IHieroSeriesClass)

    for series in Series.get_all(request):
        choices.append((str(series.pk), series.title))

    return deform.widget.SelectWidget(values=choices)

@colander.deferred
def series_default(node, kw):
    request = kw.get('request')

    if not isinstance(request.context, RootFactory):
        return request.context.series_pk

@colander.deferred
def category_widget(node, kw):
    choices = []
    request = kw.get('request')
    Series = request.registry.getUtility(IHieroCategoryClass)

    for category in Category.get_all(request):
        choices.append((str(category.pk), category.title))

    return deform.widget.SelectWidget(values=choices)

@colander.deferred
def category_default(node, kw):
    request = kw.get('request')

    if not isinstance(request.context, RootFactory):
        return request.context.category_pk

class EntryAdminSchema(CSRFSchema):

    title = colander.SchemaNode(colander.String(),
        validator=colander.Length(max=128)
    )

    slug = colander.SchemaNode(
        colander.String()
        , validator=colander.Length(max=128)
        , missing = None
    )

    content = colander.SchemaNode(
        colander.String()
        , widget = deform.widget.RichTextWidget()
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
        , widget = series_widget
        , default = series_default
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
