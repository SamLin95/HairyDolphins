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

	visitor3 = test.createEntity('Visitor', 'sam@gmail.com', 'Sam', 'helloworld',
							     'Sizhe', 'Lin', birthday=dates1[2])
	advisor_profile3 = test.createAdvisorProfile('im your advisor Sam', test.createCity('Duluth', 'GA', 'USA'), dates=dates2[2:8])
	advisor3 = test.createEntity('Local Advisor', 'sam_advisor@gmail', 'sam_advisor', 'pwd', 
								  'Sizhe', 'Lin', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile3)

	visitor4 = test.createEntity('Visitor', 'kyrsten@gmail.com', 'kyrsten', 'helloworld',
							     'Kyrsten', 'Greenfield', birthday=dates1[3])
	advisor_profile4 = test.createAdvisorProfile('im your advisor Sam', test.createCity('Duluth', 'GA', 'USA'), dates=dates2[3:8])
	advisor4 = test.createEntity('Local Advisor', 'kyrsten_advisor@gmail', 'kyrsten_advisor', 'pwd', 
								  'Kyrsten', 'Greenfield', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile4)
	


	visitor5 = test.createEntity('Visitor', 'kelvin@gmail.com', 'kelvin', 'helloworld',
							     'Kelvin', 'Vohra', birthday=dates1[4])
	advisor_profile5 = test.createAdvisorProfile('im your advisor Sam', test.createCity('Duluth', 'GA', 'USA'), dates=dates2[2:7])
	advisor5 = test.createEntity('Local Advisor', 'sam_advisor@gmail', 'sam_advisor', 'pwd', 
								  'Kelvin', 'Vohra', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile5)

	print 'sending\nmessage\n!!!!!\n'
	message1 = test.createMessage('this a message from jing, sent to dun', advisor2)
	visitor1.sent_messages.append(message1)
	visitor1.add(visitor1)

	message2 = test.createMessage('this a message from dun, sent to kelvin', advisor5)
	visitor2.sent_messages.append(message2)
	visitor2.add(visitor2)	

	message3 = test.createMessage('this a message from kyrsten, sent to sam', advisor3)
	visitor4.sent_messages.append(message3)
	visitor4.add(visitor4)	

	message4 = test.createMessage('this a message from jing, sent to kelvin', advisor5)
	visitor1.sent_messages.append(message4)
	visitor1.add(visitor1)	

	message5 = test.createMessage('this a message from kelvin, sent to sam', advisor3)
	visitor5.sent_messages.append(message5)
	visitor5.add(visitor5)	

	print '\nmore avaliable dates for advisor jing'
	advisor_profile1.available_dates += dates2[5:7]
	advisor1.local_advisor_profile = advisor_profile1
	advisor1.add(advisor1)

	print '\nfewer avaliable date for advisor dun'
	advisor_profile2.available_dates.remove(dates2[2])
	advisor2.local_advisor_profile = advisor_profile2
	advisor2.add(advisor2)

	print '\nreview from visitor kyrsten for advisor sam'
	review1 = test.createReview(5, 'this guide is so nice', advisor_profile3, visitor4)
	print '\nreview from visitor jing for advisor kyrsten'
	review2 = test.createReview(4, 'this guide is so nice', advisor_profile4, visitor1)
	print '\nreview from visitor kelvin for advisor dun'
	review3 = test.createReview(3, 'this guide is so nice', advisor_profile2, visitor5)
	print '\nreview from visitor sam for advisor jing'
	review4 = test.createReview(2, 'this guide is so nice', advisor_profile1, visitor3)


	print '\nvisitor dun recommends an attraction'
	recommend1 = test.createRecommendation('ATL is a great place', 'I love atlanta', 'georgia tech', '30332',
										   'attraction', visitor2)
	print '\ncreating entity recommendation for dun'
	entity_recommend1 = test.createEntityRecommendation(visitor2, 'dun_recommendation', recommend1)

	print '\nvisitor sam recommends an attraction'
	recommend2 = test.createRecommendation('GT is a great place', 'I love gt', 'georgia tech', '30332',
										   'attraction', visitor3)
	print '\ncreating entity recommendation for sam'
	entity_recommend2 = test.createEntityRecommendation(visitor3, 'sam_recommendation', recommend2)

	print '\nvisitor jing recommends a restaurant'
	recommend3 = test.createRecommendation('Jia is a great place', 'I love jia', 'georgia tech', '30332',
										   'restaurant', visitor1)
	print '\ncreating entity recommendation for jing'
	entity_recommend3 = test.createEntityRecommendation(visitor1, 'jing_recommendation', recommend3)
	
	print '\nvisitor kelvin recommends an attraction'
	recommend4 = test.createRecommendation('ATL is a great place', 'I love atlanta', 'georgia tech', '30332',
										   'attraction', visitor5)
	print '\ncreating entity recommendation for kelvin'
	entity_recommend4 = test.createEntityRecommendation(visitor5, 'dune_recommendation', recommend4)

createTest()
