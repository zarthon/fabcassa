Day 1
=====

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

