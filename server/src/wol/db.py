#!/usr/bin/env python
import datetime
import uuid

__author__ = 'archeg'


class DbService():
    
    def __init__(self, db):
        """
        @type db: Database
        """
        self.db = db
        self.usertable = self.db['UserTable']

    def authenticate(self, login, user_id):
        """Creates a record for the user or changes it's user_id"""
        storedlogin = self.usertable.find_one({"login": login}, {"uuid": 1, "user_id": 1})
        if not storedlogin:
            # create a record
            storedloginid = self.usertable.insert(
                {
                    "login" : login,
                    "friends": [],
                    "user_id": user_id,
                    "date": datetime.datetime.utcnow(),
                    "uuid": uuid.uuid1()
                })
            storedlogin = self.usertable.find_one({"_id": storedloginid})

            self.usertable.ensure_index("login", unique=1)

        if user_id != storedlogin['user_id']:
            # Update user id if it is expired
            self.usertable.update({"login": login}, {"$set": {"user_id": user_id}})

        return storedlogin['uuid']

    def add_friend(self, login, friendlogin):
        """ Adds a friend to the user """

        self.usertable.update({"login": login}, {"$addToSet": {"friends": friendlogin}})

    def get_friends_user_ids(self, login, friendslogins):
        """ Returns the user_ids for the friend login`s, or throws if one o the friends does not have a permission """

        # Check permissions
        allowedfriends = self.usertable.find_one({"login": login}, {"friends": 1}).friends
        for friend in friendslogins:
            if friend not in allowedfriends:
                raise Exception('No permission for %s' % friend)

        return [self.usertable.find_one({"login": x}, {"user_id": 1})['user_id'] for x in friendslogins]
