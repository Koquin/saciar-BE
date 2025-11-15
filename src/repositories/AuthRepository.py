from pymongo import MongoClient 

class AuthRepository :
    def __init__ (self ,db_name :str ,db_url :str ):
        print (f'Initiating AuthRepository, variables: \ndb_name: {db_name }\ndb_url: {db_url }')
        self .db_client =MongoClient (db_url )
        self .db =self .db_client [db_name ]
        self .collection =self .db ['auth_users']

    def get_user_by_username (self ,username ):
        print (f'In AuthRepository, method: getUserByUsername, variables: \nusername: {username }')
        user_data =self .collection .find_one ({"username":username })
        return user_data 
