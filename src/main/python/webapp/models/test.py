from models import EntityRecommendation, EntityRecommendationType, RecommendationCategory, Recommendation, File, FileType, Role, Entity, db, City, State, Country, LocalAdvisorProfile
import datetime

db.create_all()

def createEntity(label, email, username, password, first_name, last_name, phone_number=None, is_active=True, local_advisor_profile=None, admin_profile=None):

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
        user = Entity(username=username, password=password, email=email,
                      first_name=first_name, last_name=last_name, 
                      phone_number=phone_number, is_active=is_active, role=role, 
                      local_advisor_profile=local_advisor_profile, admin_profile=admin_profile)
        user.add(user)
        return user
    else:
        print 'duplicate email or username'
    print '------ user added -----'
    return None

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

recommendation_type = checkType('attraction')

def createEntityRecommendation(entity, entity_recommendation_type, recommendation):
    entity_recommendation = EntityRecommendation(entity=entity, entity_recommendation_type=entity_recommendation_type)
    return entity_recommendation

entity = createEntity('Visitor', 'Test@gmail.com', 'Test1', 'hello_world', 'kyrsten', 'Greenfield', '123')

def createRecommendation(title, description, address_line_one, zip_code, category, recommender, 
                         recommender_idaddress_line_two=None, is_draft=False):
    
    recommendation_category = checkCategory(category)
    
    
    recommend = Recommendation(title=title, description=description, address_line_one=address_line_one, zip_code=zip_code, 
                               recommendation_category=recommendation_category, recommender=recommender)
    print recommend
    print '----- recommendation updated -----'
    return recommend

recommend = createRecommendation('recommend', 'description of place', 'university house', '30332', 'shopping', entity)

entity_recommendation = createEntityRecommendation(entity, recommendation_type, recommend)





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

    print '------ fileFi added -----'

# createFile('firstFile', 123, 'www.test.com', 'Text')


def checkCity(city_name, state_name, country_name):
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

# city = checkCity('ATL', 'GA', 'America')

# TODO: availabe_datesa
def createAdvisorProfile(description, city=None, available_dates=None):
    # date = datetime.datetime.now()
    advisor = LocalAdvisorProfile(description=description, city=city)
    advisor.add(advisor)
    print advisor



# createAdvisorProfile('hello im advisor', city)



# print '1 should succeed'
# createEntity('Visitor', 'jing@gmail.com', 'Jing', 'hello_world', 'Jing', 'Hong', '123')
# print '2 shoud fail as duplicate email'
# createEntity('Local Advisor', 'jing@gmail.com', 'Dun', 'hello_world', 'Jing', 'Hong', '123')
# print '3 should fail as duplicate username'
# createEntity('Visitor', 'dun@gmail.com', 'Jing', 'hello_world', 'Jing', 'Hong', '123')
# print '4 should succeed'
# createEntity('Local Advisor', 'dun@gmail.com', 'Dun', 'hello_world', 'Dun', 'Huang', '123')
# print '5 should fail as duplicate email'
# createEntity('Visitor', 'dun@gmail.com', 'Sizhe', 'hello_world', 'Dun', 'Huang')
# print '6 should fail as duplicate username'
# createEntity('Local Advisor', 'sizhe@gmail.com', 'Dun', 'hello_world', 'Dun', 'Huang', '123')
# print '7 should succeed'
# createEntity('Visitor', 'sizhe@gmail.com', 'Sizhe', 'hello_world', 'Sizhe', 'Lin', '123')
# print '8 should fail as duplicate email'
# createEntity('Visitor', 'sizhe@gmail.com', 'Kelvin', 'hello_world', 'Sizhe', 'Lin')
# print '9 should fail as duplicate username'
# createEntity('Local Advisor', 'kelvin@gmail.com', 'Sizhe', 'hello_world', 'Sizhe', 'Lin', '123')
# print '10 should succeed'
# createEntity('Local Advisor', 'kelvin@gmail.com', 'Kelvin', 'hello_world', 'Kelvin', 'Vhora', '123')
# print '11 should succeed'
# createEntity('Visitor', 'kyrsten@gmail.com', 'Krysten', 'hello_world', 'Krysten', 'Greenfield', '123')
# print '---------- create entity test finished ----------'
