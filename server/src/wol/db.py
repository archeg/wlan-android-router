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
        self.auth_timeout = datetime.timedelta(minutes=20)

    def authenticate(self, login, pwd, device_id):
        """
        Authenticates the user to be able to work with the server
        @returns: token to be used when talking to the server.
        """
        from passlib.hash import pbkdf2_sha256
        storedlogin = self.usertable.find_one({"login": login}, {"tokens": 1, "devices": 1, "pwd": 1})
        if not storedlogin:
            # create a record
            storedloginid = self.usertable.insert(
                {
                    "login": login,
                    "devices": [device_id],
                    "pwd": pbkdf2_sha256.encrypt(pwd, rounds=20000, salt_size=16),
                    "registered_date": datetime.datetime.utcnow(),
                    "reg_ids": {},
                    "tokens": {device_id: {"token": uuid.uuid1(), "logintime": datetime.datetime.utcnow()}}
                })

            storedlogin = self.usertable.find_one({"_id": storedloginid})

            self.usertable.ensure_index("login", unique=1)
        else:
            # quit if password is incorrect
            if not pbkdf2_sha256.verify(pwd, storedlogin["pwd"]):
                return False

            # Add device
            if device_id not in storedlogin['devices']:
                generated_token = uuid.uuid1()
                # Update user id if it is expired
                self.usertable.update({"login": login},
                                      {
                                          # Add device to the list
                                          "$addToSet": {"devices": device_id},
                                          # Add token and current login time
                                          "$set": {"tokens." + device_id: {"token": generated_token, "logintime": datetime.datetime.utcnow()}}
                                      })
                return generated_token

        return storedlogin['tokens'][device_id]["token"]

    def update_regid(self, login, device_id, regid):
        """
        Renews google reg id record
        """
        self.usertable.update({"login": login}, {
            "$set": {"reg_ids."+device_id: regid}
        })

    def get_regid(self, login, deviceid):
        """
        @return regid from the database.
        """
        record = self.usertable.find_one({"login": login}, {"reg_ids": 1})
        return record["reg_ids"][deviceid]

    def check_token(self, login, device_id, token):
        """
        Checks token for being authenticated.
        """
        #self.check_timeout(login)
        storedlogin = self.usertable.find_one(
            {
                "login": login,
                "devices": {"$elemMatch": {"$eq": device_id}},
                "tokens."+device_id+".token": token
            })

        if storedlogin:
            return True
        return False

    def check_timeout(self, login):
        """
        Checks given login for possible expired devices (they should re-authenticate from time to time)
        """
        storedlogin = self.usertable.find_one({"login": login}, {"tokens": 1})
        expired_devices = set()
        for device_id, details in storedlogin["tokens"].iteritems():
            logintime = details["logintime"]
            if logintime + self.auth_timeout < datetime.datetime.utcnow():
                expired_devices.add(device_id)

        # Removing expired devices
        for device_id in expired_devices:
            self.usertable.update({"login": login},
                {
                    "$pull": {"devices": device_id},
                    "$unset": {"tokens."+device_id: 1}
                })