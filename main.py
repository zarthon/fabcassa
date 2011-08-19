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
#Column def for each column family

COL_USERS = ['id', 'username', 'password']
COL_USERNA = ['id']

def init():
    global KEYSPACE, USERS, USERNAME
    try:
        KEYSPACE = pycassa.connect( 'fabcassa', [CONNECTION] )
        USERS = pycassa.ColumnFamily( KEYSPACE,'Users' )
        USERNAME = pycassa.ColumnFamily( KEYSPACE, 'Username' )
    except:
        print sys.exc_info()
        sys.exit()

def insert_new():
    global USERS, USERNAME
    username = str(raw_input("Enter new Username: "))
    password = getpass.getpass("Enter new password")
    password2 = getpass.getpass("Re-Enter new password")
    if password != password2:
        print "Passwords dont match"
    elif USERS is None or USERNAME is None:
        print "Not connected to Column Family"
        sys.exit()
    else:
        try:
            user_id = str(uuid.uuid4())
            USERS.insert(user_id,{COL_USERS[0]:user_id, COL_USERS[1]:username, COL_USERS[2]:password})
            USERNAME.insert(username,{COL_USERNA[0]:user_id})
        except:
            print sys.exc_info()
if __name__ == "__main__":
    init()
    insert_new()
