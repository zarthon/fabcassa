Day 1
=====
I will be creating an  independent as well as automated application. It can be used from command line as well as by
scripts.


* Fixed on creating an database schema in cassandra first and than move ahead on hadoop
* Looked on mainly 2 of the high level clients available for cassandra i.e Pycassa for python and pelops for Java.
* Found Pycassa documentation much richer than that of pelops so decided to go ahead creating the application in python.
* before creating the schema in python, will first describe the same in MySql schema but will not populate the table

* I am proposing the following sample relational schema for the fabcassa, it only contains very basic storage facilities
  like profile and wall posts along with comments database. At present it doesnt contain any like database.

CREATE TABLE User (
    id INTEGER PRIMARY KEY,
    username VARCHAR(64),
    password VARCHAR(64)
);

CREATE TABLE UserProfile (
    user_id INTEGER REFERENCES User(id),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INTEGER
    relationship_status VARCHAR(10)
);

CREATE TABLE Friends (
    user_id INTEGER REFERENCES User(id),
    friend_id INTEGER REFERENCES User(id),
    PRIMARY KEY (user_id,friend_id)
);

CREATE TABLE WallPosts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES User(id),
    body VARCHAR (200),
    timestamp TIMESTAMP
);

CREATE TABLE Comments (
    id INTEGER,
    wall_id INTEGER REFERENCES WallPosts(id),
    body VARCHAR(200),
    timestamp TIMESTAMP
);

* Following scripts used to create key space and column families
    * create keyspace fabcassa;  
    * create column family Users with comparator=UTF8Type and default_validation_class=UTF8Type;  
    * create column family Username with comparator=UTF8Type and default_validation_class=UTF8Type;
    * create column family UserProfile with comparator=UTF8Type and default_validation_class=UTF8Type;
    * create column family Friends with comparator=UTF8Type and default_validation_class=UTF8Type;
    * create column family WallPosts with comparator=UTF8Type and default_validation_class=UTF8Type;

* Added functionality to inser new users and exit if user is already present
* Added functionality to insert new friends and if friends already exist than nothing will happen
* Also created an initialisation script to prepare cassandra before running the app
* Added sample data to populate the DB
* Modified the connection for localhost as I have access to other box only at college and am leaving now

Day 2
======
* Finalised on the design for Wall Posts and Comments
* Started on skeleton code for the Wall Post and also modified test.py as moved on
* Defined the column families in Cassandra
* Also defined the skeletons for the rest of the function that is required in the final application
* Found it hard to implement the wall post and display them
* Instead of adding wall post only on users account, also add the to all the friends account
* Wall functionality is finally implemented

Day 3
=====
* Tested the Wall functionality and removed errors encountered when testing
* Fixed on the design of the Comments design
* Started on the coding and on the way encountered problems related to wall posts, no user specified when all the posts
  displayed
* Changed the design to include the user_id of the posting user so that it can be displayed_
* Also merged the two different functions of displaying posts i.e viewPosts and viewPostwithComment
* Completed the functional requirements
* Also added the test.py to test the above functionalities
* Removed the debug statements

This is the following design implemented:-

Users
-----
    * Key user_id_
    * Value: userid,username,password

Username
--------
    * Key username
    * Value: userid

Friends(SuperColumn)
--------------------
    * Key: username 
    * Value: column list with mapping (username:id)

UserProfile
-----------
    * Key: userid
    * Value: first_name, last_name, age, relation

WallPost
--------
    * Key: wallpostid
    * Value: wallid, userid, body, timestamp

Comment
-------
    * Key: commentid
    * Value: commentid, userid, body, timestamp

MapWall(SuperColumn)
--------------------
    * Key: username
    * Value: column list with mapping(wallid:timestamp)

MapComment(SuperColumn)
-----------------------
    * Key: wallid
    * Value: column list with mapping(commentid:username)
