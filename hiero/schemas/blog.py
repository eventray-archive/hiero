from hem.schemas import CSRFSchema
import colander

class EntryAdminSchema(CSRFSchema):
    title = colander.SchemaNode(colander.String(),
        validator=colander.Length(max=128)
    )

    slug = colander.SchemaNode(colander.String(),
        validator=colander.Length(max=128)
    )

    content = colander.SchemaNode(colander.String())
    owner = colander.SchemaNode(colander.Integer())
    series = colander.SchemaNode(colander.Integer())
    category = colander.SchemaNode(colander.Integer())
    is_featured = colander.SchemaNode(colander.Boolean())
    is_published = colander.SchemaNode(colander.Boolean())
    enable_comments = colander.SchemaNode(colander.Boolean())
    published_on = colander.SchemaNode(colander.DateTime())
    created_on = colander.SchemaNode(colander.DateTime())

