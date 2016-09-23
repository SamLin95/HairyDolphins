if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import test
from datetime import date
import random

def createTest():
	dates1 = []
	for i in range(0, 20):
		dates = date(random.choice(range(1950, 1995)), random.choice(range(1, 13)), random.choice(range(1, 29)))
		dates1.append(test.Date(date=dates))

	dates2 = []
	for i in range(0, 20):
		dates = date(random.choice(range(2017, 2020)), random.choice(range(1, 13)), random.choice(range(1, 29)))
		dates2.append(test.Date(date=dates))

	# generating entities
	visitor1 = test.createEntity('Visitor', 'jing@gmail.com', 'jing', 'helloworld',
							     'Jing', 'Hong', birthday=dates1[0])
	advisor_profile1 = test.createAdvisorProfile('im your advisor Jing', test.createCity('Atlanta', 'GA', 'USA'), dates=dates2[0:3])
	advisor1 = test.createEntity('Local Advisor', 'jing_advisor@gmail', 'jing_advisor', 'pwd', 
								  'Jing', 'Hong', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile1)

	visitor2 = test.createEntity('Visitor', 'dun@gmail.com', 'Dun', 'helloworld',
							     'Dun', 'Huang', birthday=dates1[1])
	advisor_profile2 = test.createAdvisorProfile('im your advisor Dun and I really like roadtrips', test.createCity('Atlanta', 'GA', 'USA'), dates=dates2[1:4])
	advisor2 = test.createEntity('Local Advisor', 'dun_advisor@gmail', 'dun_advisor', 'pwd', 
								  'Dun', 'Huang', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile2)

	visitor3 = test.createEntity('Visitor', 'sam@gmail.com', 'Sam', 'helloworld',
							     'Sizhe', 'Lin', birthday=dates1[2])
	advisor_profile3 = test.createAdvisorProfile('im your advisor Sam', test.createCity('Duluth', 'GA', 'USA'), dates=dates2[2:8])
	advisor3 = test.createEntity('Local Advisor', 'sam_advisor@gmail', 'sam_advisor', 'pwd', 
								  'Sizhe', 'Lin', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile3)

	visitor4 = test.createEntity('Visitor', 'kyrsten@gmail.com', 'kyrsten', 'helloworld',
							     'Kyrsten', 'Greenfield', birthday=dates1[3])
	advisor_profile4 = test.createAdvisorProfile('im your advisor Kyrsten', test.createCity('Duluth', 'GA', 'USA'), dates=dates2[3:8])
	advisor4 = test.createEntity('Local Advisor', 'kyrsten_advisor@gmail', 'kyrsten_advisor', 'pwd', 
								  'Kyrsten', 'Greenfield', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile4)
	
	visitor5 = test.createEntity('Visitor', 'kelvin@gmail.com', 'kelvin', 'helloworld',
							     'Kelvin', 'Vohra', birthday=dates1[4])
	advisor_profile5 = test.createAdvisorProfile('im your advisor Kelvin', test.createCity('Duluth', 'GA', 'USA'), dates=dates2[2:17])
	advisor5 = test.createEntity('Local Advisor', 'kelvin_advisor@gmail', 'kelvin_advisor', 'pwd', 
								  'Kelvin', 'Vohra', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile5)

	visitor6 = test.createEntity('Visitor', 'jacob@gmail.com', 'jacob', 'helloworld',
							     'Jacob', 'Waston', birthday=dates1[5])
	advisor_profile6 = test.createAdvisorProfile('im your advisor Jacob', test.createCity('Birmingham', 'AL', 'USA'), dates=dates2[4:12])
	advisor6 = test.createEntity('Local Advisor', 'jacob_advisor@gmail.com', 'jacob_advisor', 'pwd', 
								  'Jacob', 'Waston', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile6)

	visitor7 = test.createEntity('Visitor', 'harry@gmail.com', 'harry', 'helloworld',
							     'Harry', 'Lane', birthday=dates1[6])
	advisor_profile7 = test.createAdvisorProfile('im your advisor Harry', test.createCity('Phoenix', 'AZ', 'USA'), dates=dates2[3:13])
	advisor7 = test.createEntity('Local Advisor', 'harry_advisor@gmail.com', 'harry_advisor', 'pwd', 
								  'Harry', 'Lane', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile7)

	visitor8 = test.createEntity('Visitor', 'david@gmail.com', 'david', 'helloworld',
							     'Davin', 'Zhu', birthday=dates1[7])
	advisor_profile8 = test.createAdvisorProfile('im your advisor David', test.createCity('Haidian', 'Beijing', 'China'), dates=dates2[5:18])
	advisor8 = test.createEntity('Local Advisor', 'david_advisor@gmail.com', 'david_advisor', 'pwd', 
								 'David', 'Zhu', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile8)

	visitor9 = test.createEntity('Visitor', 'yang@gmail.com', 'yang', 'helloworld',
							     'Yang', 'Yang', birthday=dates1[8])
	advisor_profile9 = test.createAdvisorProfile('im your advisor Yang', test.createCity('Suzhou', 'Jiangsu', 'China'), dates=dates2[7:13])
	advisor9 = test.createEntity('Local Advisor', 'yang_advisor@gmail.com', 'yang_advisor', 'pwd', 
								  'Yang', 'Yang', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile9)

	visitor10 = test.createEntity('Visitor', 'bhavani@gmail.com', 'bhavani', 'helloworld',
							     'Bhavani', 'Jaladanki', birthday=dates1[9])
	visitor11 = test.createEntity('Visitor', 'andrew@gmail.com', 'andrew', 'helloworld',
							     'Andrew', 'Farrow', birthday=dates1[10])
	visitor12 = test.createEntity('Visitor', 'keith@gmail.com', 'keith', 'helloworld',
							     'Keith', 'Cartledge', birthday=dates1[11])
	visitor13 = test.createEntity('Visitor', 'jarred@gmail.com', 'jarred', 'helloworld',
							     'Jarred', 'Aultman', birthday=dates1[12])
	visitor14 = test.createEntity('Visitor', 'alexander@gmail.com', 'alexander', 'helloworld',
							     'Alexander', 'Teichner', birthday=dates1[13])
	visitor15 = test.createEntity('Visitor', 'fuad@gmail.com', 'fuad', 'helloworld',
							     'Fuad', 'Hasbun', birthday=dates1[14])
	visitor16 = test.createEntity('Visitor', 'elizabeth@gmail.com', 'elizabeth', 'helloworld',
							     'Elizabeth', 'Dudley', birthday=dates1[15])
	visitor17 = test.createEntity('Visitor', 'thomas@gmail.com', 'thomas', 'helloworld',
							     'Thomas', 'Coe', birthday=dates1[16])
	visitor18 = test.createEntity('Visitor', 'ecclesia@gmail.com', 'ecclesia', 'helloworld',
							     'Ecclesia', 'Morain', birthday=dates1[17])
	visitor19 = test.createEntity('Visitor', 'brandon@gmail.com', 'brandon', 'helloworld',
							     'Brandon', 'Jackson', birthday=dates1[18])
	visitor20 = test.createEntity('Visitor', 'branson@gmail.com', 'branson', 'helloworld',
							     'Branson', 'Branson', birthday=dates1[19])

	# generating messages
	print 'sending\nmessage\n!!!!!\n'
	message1 = test.createMessage('this a message from visitor jing, sent to advisor dun', advisor2)
	visitor1.sent_messages.append(message1)
	visitor1.phone_number = '4044363903'
	visitor1.add(visitor1)

	message2 = test.createMessage('this a message from visitor dun, sent to advisor kelvin', advisor5)
	visitor2.sent_messages.append(message2)
	visitor2.add(visitor2)	

	message3 = test.createMessage('this a message from visitor kyrsten, sent to advisor sam', advisor3)
	visitor4.sent_messages.append(message3)
	visitor4.add(visitor4)	

	message4 = test.createMessage('this a message from visitor jing, sent to advisor kelvin', advisor5)
	visitor1.sent_messages.append(message4)
	visitor1.add(visitor1)	

	message5 = test.createMessage('this a message from visitor kelvin, sent to advisor sam', advisor3)
	visitor5.sent_messages.append(message5)
	visitor5.add(visitor5)

	message1 = test.createMessage('this a message from advisor dun, sent to visitor jing', visitor1)
	advisor2.sent_messages.append(message1)
	advisor2.phone_number = '4044363904'
	advisor2.add(advisor2)

	message2 = test.createMessage('this a message from advisor yang, sent to visitor jing', visitor1)
	visitor9.sent_messages.append(message2)
	visitor9.add(visitor9)	

	message3 = test.createMessage('this a message advisor jing, sent to visitor sam', visitor3)
	advisor1.sent_messages.append(message3)
	advisor1.phone_number = '4044364903'
	advisor1.add(advisor1)	

	message4 = test.createMessage('this a message from advisor david, sent ot visitor branson', visitor20)
	advisor8.sent_messages.append(message5)
	advisor8.add(advisor8)

	message5 = test.createMessage('this a message from advisor david, sent ot visitor sam', visitor3)
	advisor8.sent_messages.append(message5)
	advisor8.add(advisor8)

	print '\nmore avaliable dates for advisor jing'
	advisor_profile1.available_dates += dates2[5:7]
	advisor1.local_advisor_profile = advisor_profile1
	advisor1.add(advisor1)

	print '\nfewer avaliable date for advisor dun'
	advisor_profile2.available_dates.remove(dates2[2])
	advisor2.local_advisor_profile = advisor_profile2
	advisor2.add(advisor2)

	# generating reviews
	print '\nreview from visitor kyrsten for advisor sam'
	review1 = test.createReview(5, 'this guide is so nice', visitor4, advisor_profile3)
	print '\nreview from visitor jing for advisor kyrsten'
	review2 = test.createReview(4, 'this guide is so nice', visitor1, advisor_profile4)
	print '\nreview from visitor kelvin for advisor dun'
	review3 = test.createReview(3, 'this guide is so nice', visitor5, advisor_profile2)
	print '\nreview from visitor sam for advisor jing'
	review4 = test.createReview(2, 'this guide is so nice', visitor3, advisor_profile1)


	test.createReview(5, 'this guild is so great!', visitor20, advisor_profile1)
	test.createReview(5, 'this guild is soo great!', visitor19, advisor_profile1)
	test.createReview(4, 'this guide is so nice', visitor19, advisor_profile1)
	test.createReview(4, 'this guide is so nice', visitor18, advisor_profile4)
	test.createReview(4, 'this guide is so nice', visitor17, advisor_profile4)
	test.createReview(4, 'this guide is so nice', visitor17, advisor_profile7)
	test.createReview(4, 'this guide is so nice', visitor20, advisor_profile7)
	test.createReview(4, 'this guide is so nice', visitor16, advisor_profile7)
	test.createReview(4, 'this guide is so nice', visitor15, advisor_profile5)
	test.createReview(4, 'this guide is so nice', visitor14, advisor_profile5)
	test.createReview(4, 'this guide is so nice', visitor14, advisor_profile5)
	test.createReview(4, 'this guide is so nice', visitor13, advisor_profile6)
	test.createReview(4, 'this guide is so nice', visitor12, advisor_profile6)
	test.createReview(4, 'this guide is so nice', visitor10, advisor_profile6)


	# generating entity recommendations
	print '\nvisitor dun recommends an attraction'
	recommend1 = test.createRecommendation('Atlanta is a great place', 'I love atlanta', 'georgia tech', '30332', test.createCity('Atlanta', 'GA', 'USA'),
										   'attraction', visitor2)
	print '\ncreating entity recommendation for dun'
	entity_recommend1 = test.createEntityRecommendation(visitor2, 'dun_recommendation', recommend1)

	print '\nvisitor sam recommends an attraction'
	recommend2 = test.createRecommendation('GT is a great place', 'I love gt', 'georgia tech', '30332', test.createCity('Atlanta', 'GA', 'USA'),
										   'attraction', visitor3)
	print '\ncreating entity recommendation for sam'
	entity_recommend2 = test.createEntityRecommendation(visitor3, 'sam_recommendation', recommend2)

	print '\nvisitor jing recommends a restaurant'
	recommend3 = test.createRecommendation('Jia is a great place', 'I love jia', 'georgia tech', '30332', test.createCity('Atlanta', 'GA', 'USA'),
										   'restaurant', visitor1)
	print '\ncreating entity recommendation for jing'
	entity_recommend3 = test.createEntityRecommendation(visitor1, 'jing_recommendation', recommend3)
	
	print '\nvisitor kelvin recommends an attraction'
	recommend4 = test.createRecommendation('Atlanta is a great place', 'I love atlanta', 'georgia tech', '30332', test.createCity('Atlanta', 'GA', 'USA'),
										   'attraction', visitor5)
	print '\ncreating entity recommendation for kelvin'
	entity_recommend4 = test.createEntityRecommendation(visitor5, 'kelvin_recommendation', recommend4)

	print '\nvisitor jing recommends an attraction'
	recommend5 = test.createRecommendation('Suzhou is a great place', 'Suzhou is so beautiful', 'Suzhou', '215400', test.createCity('Suzhou', 'Jiangsu', 'China'),
										   'attraction', visitor1)
	print '\ncreating entity recommendation for jing'
	entity_recommend5 = test.createEntityRecommendation(visitor1, 'jing_recommendation2', recommend5)

	print '\nvisitor jing write a review for an attraction'
	test.createReview(5, 'this place is so great', visitor1, recommend=recommend5)

	print '\ncreating photoes!!!'

	src = path.dirname(path.realpath('__file__'))
	print src
	file1 = test.createFile('entity1.png', 32, src + '/test_files/entity1.png', 'entity_photo')
	file2 = test.createFile('entity2.png', 32, src + '/test_files/entity2.png', 'entity_photo')	
	file3 = test.createFile('entity3.png', 32, src + '/test_files/entity3.png', 'entity_photo')
	file4 = test.createFile('recommendation1.jpg', 32, src + '/test_files/atl1.jpg', 'recommendation_photo')
	file5 = test.createFile('recommendation2.jpg', 32, src + '/test_files/atl2.jpg', 'recommendation_photo')	
	file6 = test.createFile('recommendation3.jpg', 32, src + '/test_files/atl3.jpg', 'recommendation_photo')
	test.createEntityPhoto(visitor1, file1)
	test.createEntityPhoto(visitor2, file2)
	test.createEntityPhoto(advisor3, file3)
	test.createRecommendationPhoto(visitor1, recommend1, file4)
	test.createRecommendationPhoto(visitor2, recommend1, file5)
	test.createRecommendationPhoto(visitor3, recommend1, file6)
createTest()
