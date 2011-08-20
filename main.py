'''
    A simple application to emulate a facebook like database in cassandra
'''

author="""
NAME: Mohit Kothari
Profile: http://www.facebook.com/zarthon#!/zarthon?v=info
Blog: http://zarthon.wordpress.wordpress.com
"""

import uuid
import pycassa
import time
import sys
import getpass
#global variables

CONNECTION = 'localhost:9160'
KEYSPACE = None
USERS = None
USERNAME = None
FRIENDS = None
WALLPOST = None
COMMENT = None
USERPROFILE = None
LOGED_USER = None
MAPWALL = None
MAPCOMMENT = None
#Column def for each column family

COL_USERS = ['id', 'username', 'password']
COL_USERNA = ['id']
COL_USP = ['first_name', 'last_name', 'age', 'relation']
COL_FRND = ['friend_list']
COL_WALL = ['wallpost_id','body','timestamp']
COL__COMMENT = ['comment_id','user_id','body','timestamp']
COL_MAPWALL = ['post_list']
COL_MAPCOMMENT = ['commment_list']


#Initialise Connections
def init():
    global KEYSPACE, USERS, USERNAME, USERPROFILE, FRIENDS, WALLPOST, COMMENT, MAPWALL, MAPCOMMENT
    try:
        KEYSPACE = pycassa.connect( 'fabcassa', [CONNECTION] )
        USERS = pycassa.ColumnFamily( KEYSPACE,'Users' )
        USERNAME = pycassa.ColumnFamily( KEYSPACE, 'Username' )
        USERPROFILE = pycassa.ColumnFamily( KEYSPACE, 'UserProfile' )
        FRIENDS = pycassa.ColumnFamily( KEYSPACE, 'Friends' )
        WALLPOST = pycassa.ColumnFamily( KEYSPACE, 'WallPosts' )
        COMMENT = pycassa.ColumnFamily( KEYSPACE, 'Comment')
        MAPWALL = pycassa.ColumnFamily(KEYSPACE,'MapWall')
        MAPCOMMENT = pycassa.ColumnFamily(KEYSPACE,'MapComment')
    except:
        print sys.exc_info()
        sys.exit()

#Insert a new username if not present
def insert_new(usern=None,passw=None):
    global USERS, USERNAME
    
    if USERS is None or USERNAME is None:
        print "Not connected to Column Family\n"
        sys.exit()
    try:
        if usern is None:
            username = str(raw_input("Enter new Username: "))
        else:
            username = usern
#Check if username already present
        try:
            if USERNAME.get(username):
                print "Username",username,"already exists\n"
                return 
        except:
            pass

        if passw is not None:
            password = passw
            password2 = passw
        else:
            password = getpass.getpass("Enter new password: ")
            password2 = getpass.getpass("Re-Enter new password: ")
           
        if password != password2:
            print "Passwords dont match\n"
        else:
            user_id = str(uuid.uuid4())
            FRIENDS.insert(username,{COL_FRND[0]:{username:user_id} })
            USERS.insert(user_id,{COL_USERS[0]:user_id, COL_USERS[1]:username, COL_USERS[2]:password})
            USERNAME.insert(username,{COL_USERNA[0]:user_id })
            print "User with username ",username," successfully created\n"
    except:
            print sys.exc_info()

def authenticate(usern=None,passw=None):
    global USERS, USERNAME, LOGED_USER
    if usern is None:
        username = str(raw_input("Enter the username: "))
    else:
        username = usern
    try:
        user_exist = USERNAME.get(username)
        if user_exist is not None:
            if passw is None:
                password = getpass.getpass("Enter the password: ")
            else:
                password = passw
            user_info = USERS.get(user_exist['id'])
            if user_info['password'] == password:
                LOGED_USER = user_info
                print "You are successfully logged in\n"
            else:
                print "Wrong Password\n"
                return
    except:
        print "Username does not exist"
        return

def modifyUserProfile(usern=None, passw=None, first_name=None, last_name=None, age=None, relation=None):
    global LOGED_USER, USERPROFILE
    if LOGED_USER is None:
        print "User is not Logged in !!"
        authenticate(usern,passw)
    else:
        print "Welcome",LOGED_USER['username'],"!!"
        if first_name is None:
            first_name = str(raw_input("Enter First Name: "))
        if last_name is None:
            last_name = str(raw_input("Enter Last Name: "))
        if age is None:
            age = str(raw_input("Enter your age: "))
        if relation is None:
            relation = str(raw_input("Enter you relationship status: "))
        
        USERPROFILE.insert( LOGED_USER['id'], { COL_USP[0]:first_name, COL_USP[1]:last_name, COL_USP[2]:age, COL_USP[3]:relation })
        print "Your profile is successfully saved!"

def viewProfile():
    global LOGED_USER
    if LOGED_USER is None:
        print "User is not Logged in !!"
        authenticate()
    else:
        print "Your Profile details!!"
        user_prof = USERPROFILE.get(LOGED_USER['id'])
        print user_prof

def addFriends(frnd_user=None):
    global LOGED_USER
    if LOGED_USER is None:
        print "User is not Logged in !!"
        authenticate()
    else:
        try:
            if frnd_user is None:
                frnd_user = str(raw_input("Enter Friend Username: "))
            username_frnd = USERNAME.get(frnd_user)
            username_user = USERNAME.get(LOGED_USER['username'])
            if username_frnd is not None:
                friends_user = FRIENDS.get(LOGED_USER['username'])
                friends_frnd = FRIENDS.get(frnd_user)
                friends_frnd['friend_list'][LOGED_USER['username']] = username_user['id']
                friends_user['friend_list'][frnd_user] = username_frnd['id']
                FRIENDS.insert( frnd_user,{ COL_FRND[0]:friends_frnd['friend_list'] })
                FRIENDS.insert( LOGED_USER['username'],{COL_USERNA[0]:friends_user['friend_list'] })
        except:
            print sys.exc_info()
            print "User doesn't exist"
            return

def viewFriends():
    global LOGED_USER

    if LOGED_USER is None:
        print "User is not Logged in !!"
        authenticate()
    else:
        friend_row = FRIENDS.get(LOGED_USER['username'])
        print "Welconme ",LOGED_USER['username']," !!"
        print "Following is the list of friends you currently have:-"
        friends = friend_row['friend_list']
        for friend in friends:
            print friend

def postNew():
    global LOGED_USER
    
    if LOGED_USER is None:
        print "User is not Logged in !!"
        authenticate()
    else:
        body = str(raw_input("Enter the body of post"))
        wallid = str(uuid.uuid4())
        timestamp = time.time()
        WALLPOST.insert(wallid,{COL_WALL[0]:wallid,COL_WALL[1]:body,COL_WALL[2]:timestamp})
        #Get the user who is posting from MAP_WALL
        user = MAPWALL.get(LOGED_USER['username'])
        if user is None:
            ptrint "User does not exist !! Please Register..:P"
        else:
            wall_list = user['post_list']
            wall_list[timestamp] = wallid
            MAPWALL.insert(LOGED_USER['username'],{'post_list':wall_list})


def main():
    print "Welcome to Sample facassa!!!\n"
    print "1)Register New User\n2)Log In\n3)Modify User Profile\n4)View Your Profile\n5)Add Friends\n6)View your Friends\n7)Exit the APP"
    option = int(raw_input("Please select an Option:"))
    while option != 7:
        if option == 1:
            insert_new()
        elif option == 2:
            authenticate()
        elif option == 3:
            modifyUserProfile()
        elif option == 4:
            viewProfile()
        elif option == 5:
            addFriends()
        elif option == 6:
            viewFriends()
        print "1)Register New User\n2)Log In\n3)Modify User Profile\n4)View Your Profile\n5)Add Friends\n6)View your Friends\n7)Exit the APP"
        option = int(raw_input("Please select an Option:"))

if __name__ == "__main__":
    init()
    main()
     
