if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from webapp.models.models import Date, RecommendationPhoto, AdminProfile, EntityPhoto, Review, Message, EntityRecommendation, EntityRecommendationType, RecommendationCategory, Recommendation, File, FileType, Role, Entity, db, City, State, Country, LocalAdvisorProfile
import datetime

# TODO:
# entity sent_messages
# LocalAdvisorProfile available dates
# Recommendation entity_recommendations
# scripts
# test: google map api, address

def createEntity(label, email, username, password, first_name, last_name, phone_number=None, is_active=True, birthday=None, local_advisor_profile=None, admin_profile=None, message=None):

    role = Role.query.filter_by(label=label).first()
    if role == None:
        print '----- new role, updating ------'
        role = Role(label=label)
        role.add(role)
    else:
        print role
    print '------ role checked -----'

    if (Entity.query.filter_by(email=email).first() 
        or Entity.query.filter_by(username=username).first()) == None:
        print '----- new user, updating ------'
        # if message == None:
        user = Entity(username=username, password=password, email=email,
                      first_name=first_name, last_name=last_name, phone_number=phone_number, 
                      is_active=is_active, birthday=birthday, role=role, 
                      local_advisor_profile=local_advisor_profile, admin_profile=admin_profile)
        if message is list:
            print 'list of message'
            user.sent_messages = message
        user.add(user)
        return user
    else:
        print 'duplicate email or username'
    print '------ user added -----'
    return None



def createMessage(body, receiver):
    message = Message(message_body=body, receiver=receiver)
    print '----- message sent ------'
    return message


def checkCategory(label):
    recommendation_category = RecommendationCategory.query.filter_by(label='shopping').first()
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
    entity_recommendation = EntityRecommendation(entity=entity, entity_recommendation_type=entity_recommendation_type, recommendation=recommend)
    print '----- entity recommendation updated -----'
    return entity_recommendation

def createRecommendation(title, description, address_line_one, zip_code, category, recommender, 
                         recommender_idaddress_line_two=None, is_draft=False):  
    recommendation_category = checkCategory(category)
    recommend = Recommendation(title=title, description=description, address_line_one=address_line_one, zip_code=zip_code, 
                               recommendation_category=recommendation_category, recommender=recommender)
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

    print '------ file added -----'
    return files


def createCity(city_name, state_name, country_name):
    # country_name = 'America'
    country = Country.query.filter_by(label=country_name).first()
    if country == None:
        print '----- new country, updating ------'
        country = Country(label=country_name)
        country.add(country)
    else:
        print country
    print '------ country checked -----'

    # state_name = 'GA'
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

# TODO: availabe_dates
def createAdvisorProfile(description, city=None, dates=None):
    # date = datetime.datetime.now()
    advisor = LocalAdvisorProfile(description=description, city=city)
    advisor.add(advisor)
    print advisor
    print '------ advisor checked -----'
    return advisor

def createReview(rating, title, advisor, reviewer):

    review = Review(rating=rating, title=title, local_advisor_profile=advisor, reviewer=reviewer)

    print review
    print '----- review checked -----'
    return review


def createEntityPhoto(entity, files):
    photo = EntityPhoto(entity=entity, file=files, is_profile_picture=True)
    print photo
    print '----- entity photo checked -----'
    return photo

def creatRecommendationPhoto(uploader, recommendation, files):
    photo = RecommendationPhoto(uploader=uploader, recommendation=recommendation, file=files)
    print photo
    print '----- recommendation photo checked -----'
    return photo
