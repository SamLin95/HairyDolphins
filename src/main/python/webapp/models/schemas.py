from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from models import * 

class RoleSchema(ModelSchema):
    entities = fields.Nested('EntitySchema', many=True, exclude=('role',))
    class Meta:
        model = Role

class EntitySchema(ModelSchema):
    role = fields.Nested(RoleSchema, exclude=('entities',))
    local_advisor_profile = fields.Nested('LocalAdvisorProfileSchema', exclude=('entity',))
    post_reviews = fields.Nested('ReviewSchema', many=True, exclude=('reviwer',))
    entity_photos = fields.Nested('EntityPhotoSchema', many=True, exclude=('entity',))
    class Meta:
        model = Entity

class LocalAdvisorProfileSchema(ModelSchema):
    entity = fields.Nested(EntitySchema, exclude=('local_advisor_profile',))
    reviews = fields.Nested('ReviewSchema', many=True, exclude=('local_advisor_profile',))
    city = fields.Nested('CitySchema', exclude=('local_advisor_profile',))
    class Meta:
        model = LocalAdvisorProfile

class ReviewSchema(ModelSchema):
    reviewer = fields.Nested(EntitySchema, exclude=('post_reviews',))
    local_advisor_profile = fields.Nested(LocalAdvisorProfileSchema, exclude=('reviews',))
    class Meta:
        model = Review

class CitySchema(ModelSchema):
    state = fields.Nested('StateSchema', exclude=('cities',))
    local_advisor_profiles = fields.Nested(LocalAdvisorProfileSchema, many=True, exclude=('city',))
    class Meta:
        model = City

class EntityPhotoSchema(ModelSchema):
    entity = fields.Nested(EntitySchema, exclude=('entity_photos',))
    file = fields.Nested('FileSchema', exclude=('file',))
    class Meta:
        model = EntityPhoto

class FileSchema(ModelSchema):
    file_type = fields.Nested('FileTypeSchema')
    class Meta:
        model = File

class FileTypeSchema(ModelSchema):
    class Meta:
        model = FileType

class StateSchema(ModelSchema):
    country = fields.Nested('CountrySchema', exclude=('states',))
    class Meta:
        model = State

class CountrySchema(ModelSchema):
    class Meta:
        model = Country
