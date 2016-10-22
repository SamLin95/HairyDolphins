if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from webapp.models.models import Date, RecommendationPhoto, AdminProfile, EntityPhoto, Review, Message, EntityRecommendation, RecommendationCategory, Recommendation, File, FileType, Role, Entity, db, City, State, Country, LocalAdvisorProfile
import datetime
# amazon s3
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

def createMessage(body, sender, receiver):
    message = Message(message_body=body, sender=sender, receiver=receiver)
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

def createEntityRecommendation(entity, reason , recommend):
    entity_recommendation = EntityRecommendation(entity=entity, reason=reason, recommendation=recommend)
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

def createReview(rating, title, content, reviewer, advisor_profile=None, posted=None, recommend=None):
    review = Review(rating=rating, title=title, content=content, reviewer=reviewer)
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

def createFile(name, checksum, photo, format, type_name):
    link = uploadPhoto(type_name, name, photo)

    file_type = FileType.query.filter_by(label=format).first()
    if file_type == None:
        print '----- new type, updating ------'
        file_type = FileType(label=format)
        file_type.add(file_type)
    else:
        print file_type
    print '------ type checked -----'

    files = File(name=name, checksum=checksum, download_link=link, file_type=file_type)
    files.add(files)
    print files
    print '------ file added -----'
    return files

def createEntityPhoto(entity, name, checksum, photo, format):
    files = createFile(name, checksum, photo, format, 'entity_photo')
    photo = EntityPhoto.query.filter_by(entity=entity).first()
    if photo == None:
        photo = EntityPhoto(entity=entity, file=files, is_profile_picture=True)
        photo.add(photo)
    else:
        print 'entity exists!! updating profile'
        photo.file = files
        photo.update()
    print photo
    print '----- entity photo checked -----'
    return photo

def createRecommendationPhoto(uploader, recommendation, name, checksum, photo, format):
    files = createFile(name, checksum, photo, format, 'recommendation_photo')
    photo = RecommendationPhoto(uploader=uploader, recommendation=recommendation, file=files)
    photo.add(photo)
    print photo
    print '----- recommendation photo checked -----'
    return photo

def createLocalAdvisorRecommendation(advisor_profile, recommendation):
    advisor_profile.recommendations.append(recommendation)
    advisor_profile.update()

    print advisor_profile
    print '----- local advisor recommendation checked -----'
    return advisor_profile

def uploadPhoto(type_name, photo_name, photo):
    bucket = boto.connect_s3().get_bucket('hairydolphins')
    link = type_name + '/' + photo_name
    print link
    key = bucket.new_key(link)
    key.set_contents_from_filename(photo)
    key.set_acl('public-read')
    return 'https://s3.amazonaws.com/hairydolphins/' + link   
