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
    recommendations = fields.Nested('RecommendationSchema', many=True, exclude=('recommender',))
    entity_recommendations = fields.Nested('EntityRecommendationSchema', many=True, exclude=('entity',))
    uploaded_recommendation_photos = fields.Nested('RecommendationPhotoSchema', many=True, exclude=('uploader',))
    class Meta:
        model = Entity
        exclude = ('search_vector',)

class LocalAdvisorProfileSchema(ModelSchema):
    entity = fields.Nested(EntitySchema, exclude=('local_advisor_profile',))
    reviews = fields.Nested('ReviewSchema', many=True, exclude=('local_advisor_profile',))
    city = fields.Nested('CitySchema')
    available_dates = fields.Nested('DateSchema', many=True)
    class Meta:
        model = LocalAdvisorProfile
        exclude = ('search_vector',)

class ReviewSchema(ModelSchema):
    reviewer = fields.Nested(EntitySchema, exclude=('post_reviews',))
    local_advisor_profile = fields.Nested(LocalAdvisorProfileSchema, exclude=('reviews',))
    recommendation = fields.Nested('RecommendationSchema', exclude=('reviews',))
    class Meta:
        model = Review

class CitySchema(ModelSchema):
    state = fields.Nested('StateSchema', exclude=('cities',))
    class Meta:
        model = City
        exclude = ('search_vector',)

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
        exclude = ('search_vector',)

class CountrySchema(ModelSchema):
    class Meta:
        model = Country
        exclude = ('search_vector',)

class DateSchema(ModelSchema):
    class Meta:
        model = Date

class RecommendationSchema(ModelSchema):
    recommender = fields.Nested(EntitySchema, exlcude=('recommender',))
    reviews = fields.Nested(ReviewSchema, exclude=('recommendation',))
    entity_recommendations = fields.Nested('EntityRecommendationSchema', many=True, exclude=('recommendation',))
    recommendation_photos = fields.Nested('RecommendationSchema', many=True, exclude=('recommendation',))
    recommendation_category = fields.Nested('RecommendationCategorySchema', exclude=('recommendations',))
    city = fields.Nested('CitySchema', exclude=('recommendations',))
    class Meta:
        model = Recommendation

class RecommendationCategorySchema(ModelSchema):
    recommendations = fields.Nested('RecommendationSchema', exclude=('recommendation_category',))
    class Meta:
        model = RecommendationCategory

class EntityRecommendationSchema(ModelSchema):
    entity = fields.Nested(EntitySchema, exclude=('entity_recommendations', 'recommendations', 'post_reviews'))
    recommendation = fields.Nested(EntitySchema, exclude=('entity_recommendations', 'recommender', 'reviews'))
    entity_recommendation_type = fields.Nested('EntityRecommendationTypeSchema', exclude=('entity_recommendations'))
    class Meta:
        model = EntityRecommendation

class EntityRecommendationTypeSchema(ModelSchema):
    class Meta:
        model = EntityRecommendationType

class RecommendationPhotoSchema(ModelSchema):
    uploader = fields.Nested(EntitySchema, exclude=('uploaded_recommendation_photos',))
    recommendation = fields.Nested(RecommendationSchema, exclude=('recommendation_photos',))
    file = fields.Nested(FileSchema, exclude=('file',))
    class Meta:
        model = RecommendationPhoto
