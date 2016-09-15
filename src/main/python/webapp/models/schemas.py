from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from models import * 

class RoleSchema(ModelSchema):
    class Meta:
        model = Role

class EntitySchema(ModelSchema):
    role = fields.Nested(RoleSchema)
    class Meta:
        model = Entity

