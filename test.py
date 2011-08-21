'''
File to add test data to the cassandra database
'''

import main
sample_username = ['mohit','kedar','maullik','nikhil','naman','ishani','hetaswi']

sample_data = {'mohit':'asda', 'kedar':'rsdf', 'maullik':'erww', 'nikhil':'rewa', 'naman':'sdfas', 'ishani':'hgjf',
'hetaswi':'asde'}

sample_user_profile ={'mohit':['Mohit','Kothari','23','Single'], 'kedar':['Kedar','Bhatt','23','Single'],'maullik':['Maullik','Padia','23','Single'],'nikhil':['Nikhil','Marathe','23','Single'],'naman':['Naman','Muley','23','Single'],'ishani':['Ishani','Parekh','23','Single'],'hetaswi':['Hetaswi','Vankani','23','Single']}

sample_friends = {'mohit':['kedar','maullik'], 'kedar':['mohit','nikhil'], 'maullik':['mohit','nikhil'], 'nikhil':['kedar','maullik'], 'naman':['ishani','hetaswi'], 'ishani':['naman','hetaswi'], 'hetaswi':['naman','ishani']}

sample_posts = {'mohit':['first','seoncd'], 'kedar':['hello everybody','hi how are you'], 'maullik':['i am maullik','my friends i like'], 'nikhil':['hell is here','god bless you'], 'naman':['philosphy','my asd'], 'ishani':['hellogs','porty'], 'hetaswi':['toeier','jai shree shyam']}

def test_insert():
    for user in sample_data:
        main.insert_new(usern = user,passw = sample_data[user])

def test_profile():
    for i in range(1,len(sample_username)):
        username = sample_username[i]
        main.authenticate(username,sample_data[username])
        main.modifyUserProfile(first_name=sample_user_profile[username][0], last_name=sample_user_profile[username][1], age=sample_user_profile[username][2],relation=sample_user_profile[username][3])

def test_friends():
    for i in range(1,len(sample_username)):
        username = sample_username[i]
        main.authenticate(username,sample_data[username])
        for friend in sample_friends[username]:
            main.addFriends(friend)
        main.viewFriends()

def test_posts():
    for i in range(1,len(sample_username)):
        username = sample_username[i]
        main.authenticate(username,sample_data[username])
        for post in sample_posts[username]:
            main.postNew(body=post)
def test_viewPost():
    for i in range(1,len(sample_username)):
        username = sample_username[i]
        main.authenticate(username,sample_data[username])
        main.viewPosts()

if __name__=="__main__":
    main.init()
    test_insert()
    test_profile()
    test_friends()
    test_posts()
    test_viewPost()
