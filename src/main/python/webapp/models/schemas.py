from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema, field_for
from models import *

class RoleSchema(ModelSchema):
    class Meta:
        model = Role

class EntitySchema(ModelSchema):
    role = fields.Nested(RoleSchema, exclude=('entities',))
    local_advisor_profile = fields.Nested('LocalAdvisorProfileSchema', exclude=('entity',))
    entity_photos = fields.Nested('EntityPhotoSchema', many=True, exclude=('entity',))
    average_rating = fields.Float()
    profile_photo_url = fields.String()
    contacts = fields.Nested('EntitySchema', only=('id','first_name','last_name', 'profile_photo_url'), many=True)
    class Meta:
        model = Entity
        exclude = ('search_vector',)

class LocalAdvisorProfileSchema(ModelSchema):
    reviews = fields.Nested('ReviewSchema', many=True, exclude=('local_advisor_profile',))
    city = fields.Nested('CitySchema')
    available_dates = fields.Nested('DateSchema', many=True)
    class Meta:
        model = LocalAdvisorProfile
        exclude = ('search_vector',)

class ReviewSchema(ModelSchema):
    reviewer = fields.Nested(EntitySchema, only=('id', 'role', 'username', 'email', 'first_name', 'last_name'))
    class Meta:
        model = Review

class CitySchema(ModelSchema):
    state = fields.Nested('StateSchema', exclude=('cities',))
    class Meta:
        model = City
        exclude = ('search_vector',)

class EntityPhotoSchema(ModelSchema):
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
        exclude = ('search_vector',)

class CountrySchema(ModelSchema):
    class Meta:
        model = Country
        exclude = ('search_vector',)

class DateSchema(ModelSchema):
    class Meta:
        model = Date

class RecommendationSchema(ModelSchema):
    recommender = fields.Nested(EntitySchema, only=('id', 'role', 'username', 'email', 'first_name', 'last_name'))
    reviews = fields.Nested(ReviewSchema, exclude=('recommendation',), many=True)
    entity_recommendations = fields.Nested('EntityRecommendationSchema', many=True, exclude=('recommendation',))
    recommendation_photos = fields.Nested('RecommendationPhotoSchema', many=True, exclude=('recommendation',))
    recommendation_category = fields.Nested('RecommendationCategorySchema', exclude=('recommendations',))
    city = fields.Nested('CitySchema', exclude=('recommendations',))
    average_rating = fields.Float()
    class Meta:
        model = Recommendation

class RecommendationCategorySchema(ModelSchema):
    class Meta:
        model = RecommendationCategory

class EntityRecommendationSchema(ModelSchema):
    entity = fields.Nested(EntitySchema, only=('id', 'role', 'username', 'email', 'first_name', 'last_name', 'profile_photo_url'))
    recommendation = fields.Nested(RecommendationSchema, only=('id', 'title', 'description', 'address_line_one', 'address_line_two', 'city', 'zip_code', 'is_draft'))
    entity_recommendation_type = fields.Nested('EntityRecommendationTypeSchema', exclude=('entity_recommendations'))
    class Meta:
        model = EntityRecommendation

class EntityRecommendationTypeSchema(ModelSchema):
    class Meta:
        model = EntityRecommendationType

class RecommendationPhotoSchema(ModelSchema):
    entity = fields.Nested(EntitySchema, only=('id', 'role', 'username', 'email', 'first_name', 'last_name'))
    recommendation = fields.Nested(RecommendationSchema, only=('id', 'title', 'description', 'address_line_one', 'address_line_two', 'city', 'zip_code', 'is_draft'))
    file = fields.Nested(FileSchema, exclude=('file',))
    class Meta:
        model = RecommendationPhoto

class MessageSchema(ModelSchema):
    class Meta:
        model = Message
