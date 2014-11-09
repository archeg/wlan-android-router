#!/usr/bin/env python
from unittest import *
import datetime
from pymongo import MongoClient
from wol.db import DbService

__author__ = 'archeg'


class TestDbService(TestCase):

    def setUp(self):
        self.client = MongoClient()
        self.client.drop_database("TestWOL")
        self.db = self.client['TestWOL']
        self.dbclient = DbService(self.db)
        self.usertable = self.db['UserTable']
        if self.usertable.count() != 0:
            self.fail("TestWOL was not clean-up before running test")

    def test_Authenticate(self):
        from passlib.hash import pbkdf2_sha256
        login = "archeg@gmail.com"
        pwd = "1234"
        device_id = "HD1"

        self.assertFalse(self.usertable.find_one({"login": login}))
        token = self.dbclient.authenticate(login, pwd, device_id)
        found_user = self.usertable.find_one({"login": login})
        self.assertTrue(token)
        self.assertTrue(found_user)
        self.assertEqual(found_user['login'], login)
        self.assertTrue(pbkdf2_sha256.verify(pwd, found_user['pwd']))
        self.assertTrue(device_id in found_user['devices'])
        self.assertEqual(found_user['tokens'][device_id]['token'], token)
        token2 = self.dbclient.authenticate(login, pwd, device_id)
        self.assertEqual(token, token2)

    def test_Authenticate_wrong_pwd(self):
        from passlib.hash import pbkdf2_sha256

        login = "archeg@gmail.com"
        pwd = "1234"
        device_id = "HD1"

        self.assertFalse(self.usertable.find_one({"login": login}))
        self.dbclient.authenticate(login, pwd, device_id)
        token = self.dbclient.authenticate(login, "1235", device_id)
        self.assertFalse(token)
        found_user = self.usertable.find_one({"login": login})
        self.assertTrue(pbkdf2_sha256.verify(pwd, found_user['pwd']))

    def test_Authenticate_two_devices(self):
        login = "archeg@gmail.com"
        pwd = "1234"
        device_id1 = "HD1"
        device_id2 = "HD2"

        self.assertFalse(self.usertable.find_one({"login": login}))
        token = self.dbclient.authenticate(login, pwd, device_id1)
        token2 = self.dbclient.authenticate(login, pwd, device_id2)
        self.assertNotEqual(token, token2)

        found_user = self.usertable.find_one({"login": login})
        self.assertTrue(token)
        self.assertTrue(token2)
        self.assertTrue(found_user)
        self.assertEqual(found_user['login'], login)
        self.assertTrue(device_id1 in found_user['devices'])
        self.assertTrue(device_id2 in found_user['devices'])
        self.assertEqual(found_user['tokens'][device_id1]['token'], token)
        self.assertEqual(found_user['tokens'][device_id2]['token'], token2)

    def test_checktoken_success(self):
        login = "archeg@gmail.com"
        dev = "dev1"
        token = self.dbclient.authenticate(login, "1234", dev)
        result = self.dbclient.check_token(login, dev, token)
        self.assertTrue(result)

    def test_checktoken_fail(self):
        login = "archeg@gmail.com"
        dev = "dev1"
        token = self.dbclient.authenticate(login, "1234", dev)
        result = self.dbclient.check_token(login, dev, "sadvb")
        result2 = self.dbclient.check_token("faillogin@gmail.com", dev, token)
        result3 = self.dbclient.check_token(login, "dev2", token)
        self.assertFalse(result)
        self.assertFalse(result2)
        self.assertFalse(result3)

    def test_update_regid(self):
        login = "archeg@gmail.com"
        dev = "dev1"
        dev2 = "dev2"
        token = self.dbclient.authenticate(login, "1234", dev)
        self.dbclient.update_regid(login, dev, "AA")
        self.assertEqual("AA", self.usertable.find_one({"login": login})["reg_ids"][dev])
        self.dbclient.update_regid(login, dev, "AB")
        self.assertEqual("AB", self.usertable.find_one({"login": login})["reg_ids"][dev])

        #updating different device
        self.dbclient.update_regid(login, dev2, "AC")
        self.assertEqual("AB", self.usertable.find_one({"login": login})["reg_ids"][dev])
        self.assertEqual("AC", self.usertable.find_one({"login": login})["reg_ids"][dev2])

    def test_get_regid(self):
        login = "archeg@gmail.com"
        login2 = "john@gmail.com"
        dev = "dev1"
        dev2 = "dev2"
        dev3 = "dev3"
        dev4 = "dev2"
        token = self.dbclient.authenticate(login, "1234", dev)
        token = self.dbclient.authenticate(login2, "1234", dev3)
        self.dbclient.update_regid(login, dev, "AB")
        self.dbclient.update_regid(login, dev2, "AC")
        self.dbclient.update_regid(login2, dev3, "AD")
        self.dbclient.update_regid(login2, dev4, "AE")

        self.assertEqual("AB", self.dbclient.get_regid(login, dev))
        self.assertEqual("AC", self.dbclient.get_regid(login, dev2))
        self.assertEqual("AD", self.dbclient.get_regid(login2, dev3))
        self.assertEqual("AE", self.dbclient.get_regid(login2, dev4))

    def test_checktimeout(self):
        login = "archeg@gmail.com"
        dev = "dev1"
        token = self.dbclient.authenticate(login, "1234", dev)
        self.assertTrue(self.dbclient.check_token(login, dev, token))
        self.dbclient.check_timeout(login)
        self.assertTrue(self.dbclient.check_token(login, dev, token))

        # change time to be quite a while ago
        self.usertable.update({"login": login}, {"$set": {"tokens.dev1.logintime": datetime.datetime.utcnow() - datetime.timedelta(days=1)}})
        self.assertTrue(self.dbclient.check_token(login, dev, token))
        self.dbclient.check_timeout(login)
        self.assertFalse(self.dbclient.check_token(login, dev, token))

        # the token can be renewed
        token = self.dbclient.authenticate(login, "1234", dev)
        self.assertTrue(self.dbclient.check_token(login, dev, token))

    def test_getdeviceids(self):
        login = "archeg@gmail.com"
        login2 = "niceguy@gmail.com"
        dev = "dev1"
        dev1 = "dev2"
        dev2 = "dev3"
        dev3 = "dev3"
        token = self.dbclient.authenticate(login, "1234", dev)
        token = self.dbclient.authenticate(login, "1234", dev1)
        token = self.dbclient.authenticate(login, "1234", dev2)
        token2 = self.dbclient.authenticate(login2, "1234", dev3)

        devices1 = self.dbclient.get_deviceids(login)
        devices2 = self.dbclient.get_deviceids(login2)

        self.assertTrue(dev in devices1)
        self.assertTrue(dev1 in devices1)
        self.assertTrue(dev2 in devices1)
        self.assertTrue(dev3 in devices2)

        self.assertEqual(3, len(devices1))
        self.assertEqual(1, len(devices2))
