from models import Role, Entity, db
db.create_all()



def createEntity(label, email, username, password, first_name, last_name, phone_number=None, is_active=True, local_advisor_profile=None, admin_profile=None):

    role = Role.query.filter_by(label=label).first()
    if Role.query.filter_by(label=label).first() == None:
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
    else:
        return 'duplicate email or username'
    print '------ user added -----'

print '1 should succeed'
createEntity('Visitor', 'jing@gmail.com', 'Jing', 'hello_world', 'Jing', 'Hong', '123')
print '2 shoud fail as duplicate email'
createEntity('Local Advisor', 'jing@gmail.com', 'Dun', 'hello_world', 'Jing', 'Hong', '123')
print '3 should fail as duplicate username'
createEntity('Visitor', 'dun@gmail.com', 'Jing', 'hello_world', 'Jing', 'Hong', '123')
print '4 should succeed'
createEntity('Local Advisor', 'dun@gmail.com', 'Dun', 'hello_world', 'Dun', 'Huang', '123')
print '5 should fail as duplicate email'
createEntity('Visitor', 'dun@gmail.com', 'Sizhe', 'hello_world', 'Dun', 'Huang')
print '6 should fail as duplicate username'
createEntity('Local Advisor', 'sizhe@gmail.com', 'Dun', 'hello_world', 'Dun', 'Huang', '123')
print '7 should succeed'
createEntity('Visitor', 'sizhe@gmail.com', 'Sizhe', 'hello_world', 'Sizhe', 'Lin', '123')
print '8 should fail as duplicate email'
createEntity('Visitor', 'sizhe@gmail.com', 'Kelvin', 'hello_world', 'Sizhe', 'Lin')
print '9 should fail as duplicate username'
createEntity('Local Advisor', 'kelvin@gmail.com', 'Sizhe', 'hello_world', 'Sizhe', 'Lin', '123')
print '10 should succeed'
createEntity('Local Advisor', 'kelvin@gmail.com', 'Kelvin', 'hello_world', 'Kelvin', 'Vhora', '123')
print '11 should succeed'
createEntity('Visitor', 'kyrsten@gmail.com', 'Krysten', 'hello_world', 'Krysten', 'Greenfield', '123')
print '---------- create entity test finished ----------'
