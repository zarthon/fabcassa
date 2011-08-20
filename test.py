'''
File to add test data to the cassandra database
'''

import main

sample_data = {'mohit':'asda', 'kedar':'rsdf', 'maullik':'erww', 'nikhil':'rewa', 'naman':'sdfas', 'ishani':'hgjf',
'hetaswi':'asde'}

sample_user_profile ={'mohit':['Mohit','Kothari','23','Single'], 'kedar':['Kedar','Bhatt','23','Single'],'maullik':['Maullik','Padia','23','Single'],'nikhil':['Nikhil','Marathe','23','Single'],'naman':['Naman','Muley','23','Single'],'ishani':['Ishani','Parekh','23','Single'],'hetaswi':['Hetaswi','Vankani','23','Single']}

sample_friends = {'mohit':['kedar','maullik'], 'kedar':['mohit','nikhil'], 'maullik':['mohit','nikhil'], 'nikhil':['kedar','maullik'], 'naman':['ishani','hetaswi'], 'ishani':['naman','hetaswi'], 'hetaswi':['naman','ishani']}

def test_insert():
    for user in sample_data:
        main.insert_new(usern = user,passw = sample_data[user])

def test_profile():
    for user in sample data:
        main.authenticate(user,sample_data[user])
        main.modifyUserProfile()
if __name__=="__main__":
    main.init()
    test_insert()
