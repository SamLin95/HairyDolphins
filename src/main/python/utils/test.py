if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from webapp.models.models import Date, RecommendationPhoto, AdminProfile, EntityPhoto, Review, Message, EntityRecommendation, EntityRecommendationType, RecommendationCategory, Recommendation, File, FileType, Role, Entity, db, City, State, Country, LocalAdvisorProfile
import datetime
import boto

def createEntity(label, email, username, password, first_name, last_name, phone_number=None, is_active=True, birthday=None, local_advisor_profile=None, admin_profile=None, message=None):
    role = Role.query.filter_by(label=label).first()
    if role == None:
        print '----- new role, updating ------'
        role = Role(label=label)
        role.add(role)
    else:
        print role
    print '------ role checked -----'

    user = Entity.query.filter_by(email=email).first() 
    if (user or Entity.query.filter_by(username=username).first()) == None:
        print '----- new user, updating ------'
        user = Entity(username=username, password=password, email=email,
                      first_name=first_name, last_name=last_name, phone_number=phone_number, 
                      is_active=is_active, birthday=birthday, role=role, 
                      local_advisor_profile=local_advisor_profile, admin_profile=admin_profile)
        if message != None:
            print 'list of message'
            user.sent_messages = message
        user.add(user)
    else:
        print 'duplicate email or username'
    print '------ user added -----'
    return user

def createMessage(body, receiver):
    message = Message(message_body=body, receiver=receiver)
    message.add(message)
    print '----- message sent ------'
    return message

def checkCategory(label):
    recommendation_category = RecommendationCategory.query.filter_by(label=label).first()
    if recommendation_category == None:
        print '----- new category, updating ------'
        recommendation_category = RecommendationCategory(label=label)
        recommendation_category.add(recommendation_category)
    else:
        print recommendation_category
    print '------ category checked -----'
    return recommendation_category

def checkType(label):
    recommendation_type = EntityRecommendationType.query.filter_by(label=label).first()
    if recommendation_type == None:
        print '----- new recommendation type, updating ------'
        recommendation_type = EntityRecommendationType(label=label)
        recommendation_type.add(recommendation_type)
    else:
        print recommendation_type
    print '------ recommendation type checked -----'
    return recommendation_type

def createEntityRecommendation(entity, entity_recommendation_type, recommend):
    entity_recommendation = EntityRecommendation(entity=entity, entity_recommendation_type=EntityRecommendationType(label=entity_recommendation_type), recommendation=recommend)
    entity_recommendation.add(entity_recommendation)
    print '----- entity recommendation updated -----'
    return entity_recommendation

def createRecommendation(title, description, address_line_one, zip_code, city, category, recommender, 
                         recommender_idaddress_line_two=None, is_draft=False):  
    recommendation_category = checkCategory(category)
    recommend = Recommendation(title=title, description=description, address_line_one=address_line_one, zip_code=zip_code, city=city, 
                               recommendation_category=recommendation_category, recommender=recommender)
    recommend.add(recommend)
    print recommend
    print '----- recommendation updated -----'
    return recommend

def createFile(name, checksum, download_link, type_name):
    file_type = FileType.query.filter_by(label=type_name).first()
    if file_type == None:
        print '----- new type, updating ------'
        file_type = FileType(label=type_name)
        file_type.add(file_type)
    else:
        print file_type
    print '------ type checked -----'
    files = File(name=name, checksum=checksum, download_link=download_link, file_type=file_type)
    files.add(files)
    print files
    print '------ file added -----'
    return files


def createCity(city_name, state_name, country_name):
    country = Country.query.filter_by(label=country_name).first()
    if country == None:
        print '----- new country, updating ------'
        country = Country(label=country_name)
        country.add(country)
    else:
        print country
    print '------ country checked -----'

    state = State.query.filter_by(label=state_name, country=country).first()
    if state == None:
        print '----- new state, updating ------'
        state = State(label=state_name, country=country)
        state.add(state)
    else:
        print state
    print '------ state checked -----'

    # city_name = 'ATL'
    city = City.query.filter_by(label=city_name, state=state).first()
    if city == None:
        print '----- new city, updating ------'
        city = City(label=city_name, state=state)
        city.add(city)
    else:
        print city
    print '------ city checked -----'
    return city

def createAdvisorProfile(description, city=None, dates=None):
    advisor = LocalAdvisorProfile(description=description, city=city)
    if dates != None:
        print '---- available dates set for advisor ----'
        advisor.available_dates = dates
    advisor.add(advisor)
    print advisor
    print '------ advisor checked -----'
    return advisor

def createReview(rating, title, reviewer, advisor_profile=None, posted=None, recommend=None):
    review = Review(rating=rating, title=title, reviewer=reviewer)
    if posted != None:
        review.posted = posted
    if advisor_profile != None:
        review.local_advisor_profile = advisor_profile
    elif recommend != None:
        review.recommendation = recommend
    review.add(review)
    print review
    print '----- review checked -----'
    return review


def createEntityPhoto(entity, files):
    photo = EntityPhoto(entity=entity, file=files, is_profile_picture=True)
    photo.add(photo)
    print photo
    print '----- entity photo checked -----'
    return photo

def createRecommendationPhoto(uploader, recommendation, files):
    photo = RecommendationPhoto(uploader=uploader, recommendation=recommendation, file=files)
    photo.add(photo)
    print photo
    print '----- recommendation photo checked -----'
    return photo

def uploadPhoto(phote_type, name):
    bucket = s3.get_bucket('hairydolphins')
    key = bucket.new_key(photo_type + '/' + name)
    key.set_contents_from_filename('/Users/jinghong/Desktop/Icons/CP.png')
    
