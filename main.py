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

CONNECTION = 'cass01:9160'
KEYSPACE = None
USERS = None
USERNAME = None

LOGED_USER = None
#Column def for each column family

COL_USERS = ['id', 'username', 'password']
COL_USERNA = ['id']

#Initialise Connections
def init():
    global KEYSPACE, USERS, USERNAME
    try:
        KEYSPACE = pycassa.connect( 'fabcassa', [CONNECTION] )
        USERS = pycassa.ColumnFamily( KEYSPACE,'Users' )
        USERNAME = pycassa.ColumnFamily( KEYSPACE, 'Username' )
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
            USERS.insert(user_id,{COL_USERS[0]:user_id, COL_USERS[1]:username, COL_USERS[2]:password})
            USERNAME.insert(username,{COL_USERNA[0]:user_id})
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

def main():
    print "Welcome to Sample facassa!!!\n"
    print "1)Register New User\n2)Log In\n3)Exit the APP"
    option = int(raw_input("Please select an Option:"))
    while option != 3:
        if option == 1:
            insert_new()
        elif option == 2:
            authenticate()
        print "1)Register New User\n2)Log In\n3)Exit the APP"
        option = int(raw_input("Please select an Option:"))

if __name__ == "__main__":
    init()
    main()
     
