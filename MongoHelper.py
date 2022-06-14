# My MongoDB Helper class
# https://github.dev/Reecepbcups/minecraft-panel/blob/main/src/panels/database_panel.py
import pymongo

import bson

from pymongo.database import Database
from pymongo.results import InsertOneResult

class MongoHelper():
    '''
    Helper class to make functions easier with MongoDB collections
    '''
    def __init__(self, uri):
        self.client = pymongo.MongoClient(uri)

    def get_databases(self) -> list:         
        return self.client.list_database_names()

    def get_collections(self, myDB: Database) -> list:
        if isinstance(myDB, str):
            myDB = Database(self.client, myDB) 
        return myDB.list_collection_names()

    def get_users(self, db: Database, debug=False):
        if isinstance(db, str):
            db = Database(self.client, db)        

        listing = db.command('usersInfo')
        if debug == True:
            for document in listing['users']:
                print("user: " + document['user'] +" roles: "+ str(document['roles']))
        return listing['users'] # what are other listings?
    # --------------
    def insert(self, dbName, collectionName, values={}) -> InsertOneResult:
        myCol = self.client[dbName][collectionName]
        x = myCol.insert_one(values)
        return x.inserted_id

    def find_one(self, dbName, collectionName, filter=None) -> dict:
        # find_one(dbname, collection, {"name": "Reece"})
        myCol = self.client[dbName][collectionName]
        return myCol.find_one(filter)

    def get_all_documents(self, dbName, collectionName, limit=0) -> list:
        # get_all_documents(dbname, collection)
        myCol = self.client[dbName][collectionName]
        return [doc for doc in myCol.find().limit(limit)]

    def delete_one(self, dbName, collectionName, filter=None) -> int:
        # delete_one(dbname, collection, filter={"name": "reece"})
        myCol = self.client[dbName][collectionName]
        return myCol.delete_one(filter)

    def delete_all_documents(self, dbName, collectionName) -> int:
        '''
        Deletes all documents in a collection. 
        @Returns the number of documents deleted.
        '''
        myCol = self.client[dbName][collectionName]
        x = myCol.delete_many({})
        return x.deleted_count

    def drop_collection(self, dbName, collectionName) -> bool:
        return self.client[dbName][collectionName].drop()

    def drop_database(self, dbName) -> bool:
        return self.client[dbName].drop()

    def update_one(self, dbName, collectionName, filter={}, newValue={}):
        # update_one(db, collection, filter={"address": "123 street"}, newValue={"address": "124 main"})
        myCol = self.client[dbName][collectionName]
        myCol.update_one(filter, { "$set": newValue})

    ## -- test
    def create_new_user(self, username, password, database):
        print("""ROLES:""")
        shortHand = { # db.getRoles({showPrivileges:false,showBuiltinRoles: true})
            "rw": "readWrite",
            "r": "read",
            "w": "write",
            "dbo": "dbOwner",
            "backup": "backup",
            "restore": "restore",
            "-": "", # seperator
            "rad": "readAnyDatabase",
            "rwad": "readWriteAnyDatabase",
            "uad": "userAdminAnyDatabase",
            "dbaad": "dbAdminAnyDatabase",
            "--": "", # seperator
            "dba": "dbAdmin",            
            "ua": "userAdmin",
            "---": "", # seperator
            "ca": "clusterAdmin",
            "cm": "clusterManager",
            "root": "root",
        }
        for k, v in shortHand.items():
            if '-' in k:
                print(); continue
            print(f"[{k} ({v})]", end=" ")
            
        print(f"\n\n&eExample Input as>>> &fr;rw test;dbo reece;  &7(if no db is provided, {database} is used)")

        userRoles = input("Roles: ") # make copy paste / builder for this?
        
        if userRoles.endswith(";"): # remove last ;
            userRoles = userRoles[:-1]

        roles = []
        for action in userRoles.split(";"):
            values = action.split(" ") # rw, r, w, d, etc
            
            permission = values[0] # rw (even if its the only thing, it has to be index 0)
            db = database # our database name by default            
            # print(f"{values}=")

            if len(values) != 1: # ['rw']
                db = values[1] # supplied name ['rw', 'myDB']

            if permission in shortHand:
                permission = shortHand[permission]

            roles.append({"role": permission, "db": db})

        # confirm roles is correct:
        print(f"\n\nRoles: {roles}")
        if input("\nConfirm? (y/n): ").lower() != "y":
            self.create_new_user()

        self._actual_create_user(database, username, password, roles)
        # does not create any databases if they do not exist.

    def _actual_create_user(self, db, username, password, roles: list):
        db = self.client[db]
        db.command('createUser', username, 
            pwd=password,
            roles=roles
            # roles=[{'role': 'read', 'db': 'admin'}, {'role': 'readWrite', 'db': 'test'}]
        )
    def drop_user(self, db, username):
        db = self.client[db]
        db.command('dropUser', username)