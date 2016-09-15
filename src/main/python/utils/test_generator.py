if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import test
from datetime import date



def createTest():
	before	= [date(1995, 9, 16), date(1995, 9, 17), date(1995, 9, 18),
			   date(1995, 10, 16), date(1995, 10, 17), date(1995, 10, 18),
			   date(1995, 11, 16), date(1995, 11, 17), date(1995, 11, 18)]
	dates1 = []
	for dates in before:
		dates1.append(test.Date(date=dates))

	after	= [date(2016, 9, 16), date(2016, 9, 17), date(2016, 9, 18),
			   date(2016, 10, 16), date(2016, 10, 17), date(2016, 10, 18),
			   date(2016, 11, 16), date(2016, 11, 17), date(2016, 11, 18)]
	dates2 = []
	for dates in after:
		dates2.append(test.Date(date=dates))

	visitor1 = test.createEntity('Visitor', 'jing@gmail.com', 'jing', 'helloworld',
							     'Jing', 'Hong', birthday=dates1[0])
	advisor_profile1 = test.createAdvisorProfile('im your advisor Jing', test.createCity('Atlanta', 'GA', 'USA'), dates=dates2[0:3])
	advisor1 = test.createEntity('Local Advisor', 'jing_advisor@gmail', 'jing_advisor', 'pwd', 
								  'Jing', 'Hong', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile1)
	
	# 
	visitor2 = test.createEntity('Visitor', 'dun@gmail.com', 'Dun', 'helloworld',
							     'Dun', 'Huang', birthday=dates1[1])
	advisor_profile2 = test.createAdvisorProfile('im your advisor Dun', test.createCity('Atlanta', 'GA', 'USA'), dates=dates2[1:4])
	advisor2 = test.createEntity('Local Advisor', 'dun_advisor@gmail', 'dun_advisor', 'pwd', 
								  'Dun', 'Huang', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile2)
	# user2 = test.createEntity('Local Advisor', 'jingh@gmail.com', 'jingh', 'helloworld',
	# 						  'Jing', 'Hong', birthday=before[1], admin_profile=AdminProfile())

	# entity = test.createEntity('Visitor', 'Test@gmail.com', 'Test1', 'hello_world', 'kyrsten', 'Greenfield', '123')
	# message = test.createMessage('this is body', entity)
	# message2 = test.createMessage('this is body2', entity)
	# message = [message, message2]
	# entity = test.createEntity('Visitor', 'Test2@gmail.com', 'Test2', 'hello_world', 'kyrsten', 'Greenfield', '123', message=message)
	# recommendation_type = test.checkType('attraction')
	# recommend = test.createRecommendation('recommend', 'description of place', 'university house', '30332', 'shopping', entity)
	# entity_recommendation = test.createEntityRecommendation(entity, recommendation_type, recommend)
	# files = test.createFile('firstFile', 123, 'www.test.com', 'Text')
	# city = test.checkCity('ATL', 'GA', 'America')
	# advisor = test.createAdvisorProfile('hello im advisor', city)
	# review = test.createReview(4, 'first review', advisor, entity)
	# entity_photo = test.createEntityPhoto(entity, files)
	# recommend_photo = test.creatRecommendationPhoto(entity, recommend, files)


	# print '1 should succeed'
	# test.createEntity('Visitor', 'jing@gmail.com', 'Jing', 'hello_world', 'Jing', 'Hong', '123', local_advisor_profile=advisor, admin_profile=test.AdminProfile(), message=message)
	# print '2 shoud fail as duplicate email'
	# test.createEntity('Local Advisor', 'jing@gmail.com', 'Dun', 'hello_world', 'Jing', 'Hong', '123')
	# print '3 should fail as duplicate username'
	# test.createEntity('Visitor', 'dun@gmail.com', 'Jing', 'hello_world', 'Jing', 'Hong', '123')
	# print '4 should succeed'
	# test.createEntity('Local Advisor', 'dun@gmail.com', 'Dun', 'hello_world', 'Dun', 'Huang', '123')
	# print '5 should fail as duplicate email'
	# test.createEntity('Visitor', 'dun@gmail.com', 'Sizhe', 'hello_world', 'Dun', 'Huang')
	# print '6 should fail as duplicate username'
	# test.createEntity('Local Advisor', 'sizhe@gmail.com', 'Dun', 'hello_world', 'Dun', 'Huang', '123')
	# print '7 should succeed'
	# test.createEntity('Visitor', 'sizhe@gmail.com', 'Sizhe', 'hello_world', 'Sizhe', 'Lin', '123')
	# print '8 should fail as duplicate email'
	# test.createEntity('Visitor', 'sizhe@gmail.com', 'Kelvin', 'hello_world', 'Sizhe', 'Lin')
	# print '9 should fail as duplicate username'
	# test.createEntity('Local Advisor', 'kelvin@gmail.com', 'Sizhe', 'hello_world', 'Sizhe', 'Lin', '123')
	# print '10 should succeed'
	# test.createEntity('Local Advisor', 'kelvin@gmail.com', 'Kelvin', 'hello_world', 'Kelvin', 'Vhora', '123')
	# print '11 should succeed'
	# test.createEntity('Visitor', 'kyrsten@gmail.com', 'Krysten', 'hello_world', 'Krysten', 'Greenfield', '123')
	# print '---------- create entity test finished ----------'

createTest()
