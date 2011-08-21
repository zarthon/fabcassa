import pycassa
from pycassa.system_manager import *

if __name__ == "__main__":
    sys = SystemManager('127.0.0.1:9160')
    sys.create_keyspace('fabcassa',1)
    sys.create_column_family('fabcassa','Users')
    sys.create_column_family('fabcassa','Username')
    sys.create_column_family('fabcassa','Friends',super=True)
    sys.create_column_family('fabcassa','UserProfile')
    sys.create_column_family('fabcassa','WallPosts')
    sys.create_column_family('fabcassa','MapWall',super=True)
    sys.create_column_family('fabcassa','Comments')
    sys.create_column_family('fabcassa','MapComment',super=True)
