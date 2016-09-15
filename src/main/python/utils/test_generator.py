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
	advisor_profile4 = test.createAdvisorProfile('im your advisor Sam', test.createCity('Duluth', 'GA', 'USA'), dates=dates2[3:9])
	advisor4 = test.createEntity('Local Advisor', 'kyrsten_advisor@gmail', 'kyrsten_advisor', 'pwd', 
								  'Kyrsten', 'Greenfield', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile4)
	


	visitor5 = test.createEntity('Visitor', 'kelvin@gmail.com', 'kelvin', 'helloworld',
							     'Kelvin', 'Vohra', birthday=dates1[4])
	advisor_profile5 = test.createAdvisorProfile('im your advisor Sam', test.createCity('Duluth', 'GA', 'USA'), dates=dates2[2:7])
	advisor5 = test.createEntity('Local Advisor', 'sam_advisor@gmail', 'sam_advisor', 'pwd', 
								  'Kelvin', 'Vohra', admin_profile=test.AdminProfile(), local_advisor_profile=advisor_profile5)

	print '\nsending\nmessage\n!!!!!\n'
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
	
createTest()
