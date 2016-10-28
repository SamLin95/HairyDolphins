if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import test
from datetime import date
import random
import testdata

def createTest():
	dates1 = []
	for i in range(0, 20):
		dates = date(random.choice(range(1950, 1995)), random.choice(range(1, 13)), random.choice(range(1, 29)))
		dates1.append(test.Date(date=dates))

	dates2 = []
	for i in range(0, 20):
		dates = date(2016, random.choice(range(12, 13)), random.choice(range(1, 29)))
		dates2.append(test.Date(date=dates))

	# generating entities
	visitor1 = test.createEntity('Visitor', 'jing@gmail.com', 'jing', 'helloworld',
							     'Jing', 'Hong', birthday=dates1[0])
	advisor_profile1 = test.createAdvisorProfile('im your advisor Jing', test.createCity('Atlanta', 'GA', 'USA'), dates=dates2[0:3])
	advisor1 = test.createEntity('Local Advisor', 'jing_advisor@gmail', 'jing_advisor', 'pwd', 
								  'Jing', 'Hong', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile1)

	visitor2 = test.createEntity('Visitor', 'dun@gmail.com', 'Dun', 'helloworld',
							     'Dun', 'Huang', birthday=dates1[1])
	advisor_profile2 = test.createAdvisorProfile('im your advisor Dun and I really I really love this place roadtrips', test.createCity('Atlanta', 'GA', 'USA'), dates=dates2[1:4])
	advisor2 = test.createEntity('Local Advisor', 'dun_advisor@gmail', 'dun_advisor', 'pwd', 
								  'Dun', 'Huang', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile2)

	visitor3 = test.createEntity('Visitor', 'slin77@gatech.edu', 'samlin_95', 'linsizhe123',
							     'Sizhe', 'Lin')
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
							     'Branson', 'Dupuy', birthday=dates1[19])

	# generating messages
	print '\nsending message !!!!!\n'
	message1 = test.createMessage('this a message from visitor jing, sent to advisor dun', visitor1, advisor2)
	# message1.sender_id = visitor1.id
	visitor1.sent_messages.append(message1)
	visitor1.phone_number = '4044363903'
	visitor1.add(visitor1)

	message2 = test.createMessage('this a message from visitor dun, sent to advisor kelvin', visitor2, advisor5)
	visitor2.sent_messages.append(message2)
	visitor2.add(visitor2)	

	message3 = test.createMessage('this a message from visitor kyrsten, sent to advisor sam', visitor4, advisor3)
	visitor4.sent_messages.append(message3)
	visitor4.add(visitor4)	

	message4 = test.createMessage('this a message from visitor jing, sent to advisor kelvin', visitor1, advisor5)
	visitor1.sent_messages.append(message4)
	visitor1.add(visitor1)	

	message5 = test.createMessage('this a message from visitor kelvin, sent to advisor sam', visitor5, advisor3)
	visitor5.sent_messages.append(message5)
	visitor5.add(visitor5)

	message6 = test.createMessage('this a message from advisor dun, sent to visitor jing', advisor2, visitor1)
	advisor2.sent_messages.append(message6)
	advisor2.phone_number = '4044363904'
	advisor2.add(advisor2)

	message7 = test.createMessage('this a message from advisor yang, sent to visitor jing', visitor9, visitor1)
	visitor9.sent_messages.append(message7)
	visitor9.add(visitor9)	

	message8 = test.createMessage('this a message advisor jing, sent to visitor sam', advisor1, visitor3)
	advisor1.sent_messages.append(message8)
	advisor1.phone_number = '4044364903'
	advisor1.add(advisor1)	

	message9 = test.createMessage('this a message from advisor david, sent ot visitor branson', advisor8, visitor20)
	advisor8.sent_messages.append(message9)
	advisor8.add(advisor8)

	message10 = test.createMessage('this a message from advisor david, sent ot visitor sam', advisor8, visitor3)
	advisor8.sent_messages.append(message10)
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
	test.createReview(5, 'this guide is so nice', testdata.guide_review1, visitor4, advisor_profile3)
	print '\nreview from visitor jing for advisor kyrsten'
	test.createReview(4, 'this guide is so nice', testdata.guide_review2, visitor1, advisor_profile4)
	print '\nreview from visitor kelvin for advisor dun'
	test.createReview(3, 'this guide is so nice', testdata.guide_review3,  visitor5, advisor_profile2)
	print '\nreview from visitor sam for advisor jing'
	test.createReview(2, 'this guide is so nice', testdata.guide_review4, visitor3, advisor_profile1)


	test.createReview(5, 'this guild is so great!', testdata.guide_review5, visitor20, advisor_profile1)
	test.createReview(5, 'this guild is soo great!', testdata.guide_review1, visitor19, advisor_profile1)
	test.createReview(4, 'this guide is so nice', testdata.guide_review2, visitor19, advisor_profile1)
	test.createReview(4, 'this guide is so nice', testdata.guide_review4, visitor18, advisor_profile4)
	test.createReview(4, 'this guide is so nice', testdata.guide_review5, visitor17, advisor_profile4)
	test.createReview(4, 'this guide is so nice', testdata.guide_review4, visitor17, advisor_profile7)
	test.createReview(4, 'this guide is so nice', testdata.guide_review2, visitor20, advisor_profile7)
	test.createReview(4, 'this guide is so nice', testdata.guide_review3, visitor16, advisor_profile7)
	test.createReview(4, 'this guide is so nice', testdata.guide_review4, visitor15, advisor_profile5)
	test.createReview(4, 'this guide is so nice', testdata.guide_review1, visitor14, advisor_profile5)
	test.createReview(4, 'this guide is so nice', testdata.guide_review2, visitor14, advisor_profile5)
	test.createReview(4, 'this guide is so nice', testdata.guide_review3, visitor13, advisor_profile6)
	test.createReview(4, 'this guide is so nice', testdata.guide_review5, visitor12, advisor_profile6)
	test.createReview(4, 'this guide is so nice', testdata.guide_review1, visitor10, advisor_profile6)


	# generating entity recommendations
	print '\nvisitor dun recommends an attraction'
	recommend1 = test.createRecommendation('Atalant Cyclorama & Civil War Museum', testdata.atl_museum, '800 Cherokee Ave., C', '30315', test.createCity('Atlanta', 'GA', 'USA'),
										   'attraction', visitor2)
	print '\njing and kelvin I really love this place this recommendation!!'
	test.createEntityRecommendation(visitor1, 'This museum is amazing!', recommend1)
	test.createEntityRecommendation(visitor5, 'I really love this museum', recommend1)

	print '\nkyrsten and sam I highly recommend this place this recommendation!!'
	test.createEntityRecommendation(visitor3, 'I highly recommend this place', recommend1)
	test.createEntityRecommendation(visitor4, 'I highly recommend this place', recommend1)

	print '\nvisitor dun write a review for a place'
	test.createReview(5, 'Awesome Experience', testdata.atl_museum_review, visitor2, recommend=recommend1)

	print '\nvisitor sam recommends an attraction'
	recommend2 = test.createRecommendation('Atlanta Botanical Garden', testdata.atl_garden, '1345 Piedmont Ave. NE', '30309', test.createCity('Atlanta', 'GA', 'USA'),
										   'attraction', visitor3)
	print '\nI really love this place!'
	test.createEntityRecommendation(visitor1, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor2, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor4, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor5, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor6, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor7, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor8, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor9, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor10, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor11, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor12, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor13, 'I really love this place', recommend2)
	test.createEntityRecommendation(visitor14, 'I really love this place', recommend2)

	print '\nI highly recommend this place!'
	test.createEntityRecommendation(visitor15, 'I highly recommend this place', recommend2)
	test.createEntityRecommendation(visitor16, 'I highly recommend this place', recommend2)
	test.createEntityRecommendation(visitor18, 'I highly recommend this place', recommend2)
	test.createEntityRecommendation(visitor19, 'I highly recommend this place', recommend2)

	print '\nvisitor sam write a review for a place'
	test.createReview(5, 'The Botanical Garden is great', testdata.atl_garden_review, visitor3, recommend=recommend2)

	print '\nvisitor jing recommends a restaurant'
	recommend3 = test.createRecommendation('Bacchanalia', testdata.atl_bacchanalia, '1198 Howell Mill Rd.', '30318', test.createCity('Atlanta', 'GA', 'USA'),
										   'restaurant', visitor1)
	test.createEntityRecommendation(visitor2, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor3, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor4, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor5, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor6, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor7, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor8, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor9, 'I highly recommend this place', recommend3)
	test.createEntityRecommendation(visitor10, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor11, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor12, 'I highly recommend this place', recommend3)
	test.createEntityRecommendation(visitor13, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor14, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor15, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor16, 'I highly recommend this place', recommend3)
	test.createEntityRecommendation(visitor17, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor18, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor19, 'I really love this place', recommend3)
	test.createEntityRecommendation(visitor20, 'I really love this place', recommend3)

	print '\nvisitor jing write a review for a restaurant'
	test.createReview(5, 'An Uncommon Dining Experience', testdata.atl_bacchanalia_review, visitor1, recommend=recommend3)
	
	print '\nvisitor kelvin recommends an attraction'
	recommend4 = test.createRecommendation('Centennial Olympic Park', testdata.atl_park, '265 Park Ave. West, Marietta St. and Centennial Olympic Park Dr', '30313', test.createCity('Atlanta', 'GA', 'USA'),
										   'attraction', visitor5)
	test.createEntityRecommendation(visitor1, 'I really love this place', recommend4)	
	test.createEntityRecommendation(visitor2, 'I highly recommend this place', recommend4)
	test.createEntityRecommendation(visitor3, 'I highly recommend this place', recommend4)
	test.createEntityRecommendation(visitor4, 'I highly recommend this place', recommend4)
	test.createEntityRecommendation(visitor6, 'I really love this place', recommend4)
	test.createEntityRecommendation(visitor7, 'I really love this place', recommend4)
	test.createEntityRecommendation(visitor8, 'I really love this place', recommend4)
	test.createEntityRecommendation(visitor9, 'I highly recommend this place', recommend4)
	test.createEntityRecommendation(visitor10, 'I really love this place', recommend4)
	test.createEntityRecommendation(visitor11, 'I really love this place', recommend4)
	test.createEntityRecommendation(visitor12, 'I highly recommend this place', recommend4)
	test.createEntityRecommendation(visitor13, 'I really love this place', recommend4)
	test.createEntityRecommendation(visitor14, 'I really love this place', recommend4)
	test.createEntityRecommendation(visitor15, 'I highly recommend this place', recommend4)
	test.createEntityRecommendation(visitor16, 'I highly recommend this place', recommend4)
	test.createEntityRecommendation(visitor17, 'I really love this place', recommend4)
	test.createEntityRecommendation(visitor18, 'I really love this place', recommend4)
	test.createEntityRecommendation(visitor19, 'I highly recommend this place', recommend4)
	test.createEntityRecommendation(visitor20, 'I highly recommend this place', recommend4)

	print '\nvisitor kelvin write a review for an attraction'
	test.createReview(5, 'Love this place', testdata.atl_park_review,  visitor5, recommend=recommend4)

	print '\nvisitor jing recommends an attraction'
	recommend5 = test.createRecommendation('The Forbidden City', testdata.pk_city, '4 Jingshan Front St', '100000', test.createCity('Dongcheng', 'Beijing', 'China'),
										   'attraction', visitor1)

	test.createEntityRecommendation(visitor2, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor3, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor4, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor5, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor6, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor7, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor8, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor9, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor10, 'I highly recommend this place', recommend5)
	test.createEntityRecommendation(visitor11, 'I highly recommend this place', recommend5)
	test.createEntityRecommendation(visitor12, 'I highly recommend this place', recommend5)
	test.createEntityRecommendation(visitor13, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor14, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor15, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor16, 'I highly recommend this place', recommend5)
	test.createEntityRecommendation(visitor17, 'I highly recommend this place', recommend5)
	test.createEntityRecommendation(visitor18, 'I highly recommend this place', recommend5)
	test.createEntityRecommendation(visitor19, 'I really love this place', recommend5)
	test.createEntityRecommendation(visitor20, 'I really love this place', recommend5)

	print '\nvisitor jing write a review for an attraction'
	test.createReview(5, 'The Forbidden City is AMAZING', testdata.pk_city_review,  visitor1, recommend=recommend5)

	# generating photoes
	print '\ncreating photoes for advisors and recommendations!!!'
	src = path.dirname(path.realpath('__file__')) + "/utils/test_files/"

	test.createEntityPhoto(advisor1, 'advisor1.jpg', 32, src + '/advisors/advisor1.jpg', 'jpg')
	test.createEntityPhoto(advisor2, 'advisor2.jpg', 32, src + '/advisors/advisor2.jpg', 'jpg')
	test.createEntityPhoto(advisor3, 'advisor3.jpg', 32, src + '/advisors/advisor3.jpg', 'jpg')
	test.createEntityPhoto(advisor4, 'advisor4.jpg', 32, src + '/advisors/advisor4.jpg', 'jpg')
	test.createEntityPhoto(advisor5, 'advisor5.jpg', 32, src + '/advisors/advisor5.jpg', 'jpg')
	test.createEntityPhoto(advisor6, 'advisor6.jpg', 32, src + '/advisors/advisor6.jpg', 'jpg')
	test.createEntityPhoto(advisor7, 'advisor7.jpg', 32, src + '/advisors/advisor7.jpg', 'jpg')
	test.createEntityPhoto(advisor8, 'advisor8.jpg', 32, src + '/advisors/advisor8.jpg', 'jpg')
	test.createEntityPhoto(advisor9, 'advisor9.jpg', 32, src + '/advisors/advisor9.jpg', 'jpg')

	test.createEntityPhoto(visitor1, 'visitor1.jpg', 32, src + '/visitors/visitor1.jpg', 'jpg')
	test.createEntityPhoto(visitor2, 'visitor2.jpg', 32, src + '/visitors/visitor2.jpg', 'jpg')
	test.createEntityPhoto(visitor3, 'visitor3.jpg', 32, src + '/visitors/visitor3.jpg', 'jpg')
	test.createEntityPhoto(visitor4, 'visitor4.jpg', 32, src + '/visitors/visitor4.jpg', 'jpg')
	test.createEntityPhoto(visitor5, 'visitor5.jpg', 32, src + '/visitors/visitor5.jpg', 'jpg')
	test.createEntityPhoto(visitor6, 'visitor6.jpg', 32, src + '/visitors/visitor6.jpg', 'jpg')
	test.createEntityPhoto(visitor7, 'visitor7.jpg', 32, src + '/visitors/visitor7.jpg', 'jpg')
	test.createEntityPhoto(visitor8, 'visitor8.jpg', 32, src + '/visitors/visitor8.jpg', 'jpg')
	test.createEntityPhoto(visitor9, 'visitor9.jpg', 32, src + '/visitors/visitor9.jpg', 'jpg')

	test.createRecommendationPhoto(visitor2, recommend1, 'recommendation1.jpg', 32, src + '/recommendations/recommendation1.jpg', 'jpg')
	test.createRecommendationPhoto(visitor3, recommend2, 'recommendation2.jpg', 32, src + '/recommendations/recommendation2.jpg', 'jpg')
	test.createRecommendationPhoto(visitor1, recommend3, 'recommendation3.jpg', 32, src + '/recommendations/recommendation3.jpg', 'jpg')
	test.createRecommendationPhoto(visitor5, recommend4, 'recommendation4.jpg', 32, src + '/recommendations/recommendation4.jpg', 'jpg')
	test.createRecommendationPhoto(visitor1, recommend5, 'recommendation5.png', 32, src + '/recommendations/recommendation5.png', 'png')

	print '\ncreating recommendations provided by advisors!!!'
	test.createLocalAdvisorRecommendation(advisor_profile1, recommend1)
	test.createLocalAdvisorRecommendation(advisor_profile2, recommend1)
	test.createLocalAdvisorRecommendation(advisor_profile3, recommend1)
	test.createLocalAdvisorRecommendation(advisor_profile4, recommend1)
	test.createLocalAdvisorRecommendation(advisor_profile2, recommend2)
	test.createLocalAdvisorRecommendation(advisor_profile4, recommend2)
	test.createLocalAdvisorRecommendation(advisor_profile7, recommend2)
	test.createLocalAdvisorRecommendation(advisor_profile9, recommend2)
	test.createLocalAdvisorRecommendation(advisor_profile1, recommend3)
	test.createLocalAdvisorRecommendation(advisor_profile3, recommend3)
	test.createLocalAdvisorRecommendation(advisor_profile5, recommend3)
	test.createLocalAdvisorRecommendation(advisor_profile7, recommend3)
	test.createLocalAdvisorRecommendation(advisor_profile8, recommend3)
	test.createLocalAdvisorRecommendation(advisor_profile2, recommend4)
	test.createLocalAdvisorRecommendation(advisor_profile3, recommend4)
	test.createLocalAdvisorRecommendation(advisor_profile4, recommend4)
	test.createLocalAdvisorRecommendation(advisor_profile8, recommend4)
	test.createLocalAdvisorRecommendation(advisor_profile9, recommend4)
	test.createLocalAdvisorRecommendation(advisor_profile1, recommend5)
	test.createLocalAdvisorRecommendation(advisor_profile4, recommend5)
	test.createLocalAdvisorRecommendation(advisor_profile6, recommend5)
	test.createLocalAdvisorRecommendation(advisor_profile7, recommend5)
	test.createLocalAdvisorRecommendation(advisor_profile8, recommend5)
	test.createLocalAdvisorRecommendation(advisor_profile9, recommend5)
createTest()
