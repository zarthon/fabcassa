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
def insert_new():
    global USERS, USERNAME
    
    if USERS is None or USERNAME is None:
        print "Not connected to Column Family"
        sys.exit()
    try:
        username = str(raw_input("Enter new Username: "))
#Check if username already present
        try:
            if USERNAME.get(username):
                print "Username already exists"
                return 
        except:
            pass

        password = getpass.getpass("Enter new password: ")
        password2 = getpass.getpass("Re-Enter new password: ")
        if password != password2:
            print "Passwords dont match"
        else:
            user_id = str(uuid.uuid4())
            USERS.insert(user_id,{COL_USERS[0]:user_id, COL_USERS[1]:username, COL_USERS[2]:password})
            USERNAME.insert(username,{COL_USERNA[0]:user_id})
            print "User with username ",username," successfully created"
    except:
            print sys.exc_info()

def authenticate():
    global USERS, USERNAME, LOGED_USER
    username = str(raw_input("Enter the username: "))
    try:
        user_exist = USERNAME.get(username)
        if user_exist is not None:
            password = getpass.getpass("Enter the password: ")
            user_info = USERS.get(user_exist['id'])
            if user_info['password'] == password:
                LOGED_USER = user_info
                print "You are successfully logged in"
            else:
                print "Wrong Password"
                return
    except:
        print "Username does not exist"
        return

if __name__ == "__main__":
    init()
    authenticate()
    
