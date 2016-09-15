from marshmallow_sqlalchemy import ModelSchema
from models import * 

class EntitySchema(ModelSchema):
    class Meta:
        model = Entity
