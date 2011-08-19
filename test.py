'''
File to add test data to the cassandra database
'''

import main

sample_data = {'mohit':'asda', 'kedar':'rsdf', 'maullik':'erww', 'nikhil':'rewa', 'naman':'sdfas', 'ishani':'hgjf',
'hetaswi':'asde'}

def test_insert():
    for user in sample_data:
        main.insert_new(usern = user,passw = sample_data[user])

if __name__=="__main__":
    main.init()
    test_insert()
