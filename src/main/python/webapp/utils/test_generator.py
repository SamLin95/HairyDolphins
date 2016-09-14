if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import test

def createTest():
	entity = test.createEntity('Visitor', 'Test@gmail.com', 'Test1', 'hello_world', 'kyrsten', 'Greenfield', '123')
	message = test.createMessage('this is body', entity)
	message2 = test.createMessage('this is body2', entity)
	message = [message, message2]
	entity = test.createEntity('Visitor', 'Test2@gmail.com', 'Test2', 'hello_world', 'kyrsten', 'Greenfield', '123', message=message)
	recommendation_type = test.checkType('attraction')
	recommend = test.createRecommendation('recommend', 'description of place', 'university house', '30332', 'shopping', entity)
	entity_recommendation = test.createEntityRecommendation(entity, recommendation_type, recommend)
	files = test.createFile('firstFile', 123, 'www.test.com', 'Text')
	city = test.checkCity('ATL', 'GA', 'America')
	advisor = test.createAdvisorProfile('hello im advisor', city)
	review = test.createReview(4, 'first review', advisor, entity)
	entity_photo = test.createEntityPhoto(entity, files)
	recommend_photo = test.creatRecommendationPhoto(entity, recommend, files)


	print '1 should succeed'
	test.createEntity('Visitor', 'jing@gmail.com', 'Jing', 'hello_world', 'Jing', 'Hong', '123', local_advisor_profile=advisor, admin_profile=test.AdminProfile(), message=message)
	print '2 shoud fail as duplicate email'
	test.createEntity('Local Advisor', 'jing@gmail.com', 'Dun', 'hello_world', 'Jing', 'Hong', '123')
	print '3 should fail as duplicate username'
	test.createEntity('Visitor', 'dun@gmail.com', 'Jing', 'hello_world', 'Jing', 'Hong', '123')
	print '4 should succeed'
	test.createEntity('Local Advisor', 'dun@gmail.com', 'Dun', 'hello_world', 'Dun', 'Huang', '123')
	print '5 should fail as duplicate email'
	test.createEntity('Visitor', 'dun@gmail.com', 'Sizhe', 'hello_world', 'Dun', 'Huang')
	print '6 should fail as duplicate username'
	test.createEntity('Local Advisor', 'sizhe@gmail.com', 'Dun', 'hello_world', 'Dun', 'Huang', '123')
	print '7 should succeed'
	test.createEntity('Visitor', 'sizhe@gmail.com', 'Sizhe', 'hello_world', 'Sizhe', 'Lin', '123')
	print '8 should fail as duplicate email'
	test.createEntity('Visitor', 'sizhe@gmail.com', 'Kelvin', 'hello_world', 'Sizhe', 'Lin')
	print '9 should fail as duplicate username'
	test.createEntity('Local Advisor', 'kelvin@gmail.com', 'Sizhe', 'hello_world', 'Sizhe', 'Lin', '123')
	print '10 should succeed'
	test.createEntity('Local Advisor', 'kelvin@gmail.com', 'Kelvin', 'hello_world', 'Kelvin', 'Vhora', '123')
	print '11 should succeed'
	test.createEntity('Visitor', 'kyrsten@gmail.com', 'Krysten', 'hello_world', 'Krysten', 'Greenfield', '123')
	print '---------- create entity test finished ----------'

createTest()