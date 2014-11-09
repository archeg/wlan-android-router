#!/usr/bin/env python
from unittest import *
from pymongo import MongoClient
from db import DbService

__author__ = 'archeg'


class TestDbService(TestCase):

    def setUp(self):
        self.client = MongoClient()
        self.client.drop_database("TestWOL")
        self.db = self.client['TestWOL']
        self.dbClient = DbService(self.db)
        self.userTable = self.db['UserTable']

    def test_Authenticate(self):
        login = "archeg@gmail.com"
        id = "uuser_id_arch"

        self.assertFalse(self.userTable.find_one({"login": login}))
        self.dbClient.authenticate(login, id)
        foundUser = self.userTable.find_one({"login": login})
        self.assertTrue(foundUser)
        self.assertEqual(foundUser['user_id'], id)

    def test_Authenticate_double(self):
        login = "archeg@gmail.com"
        id = "uuser_id_arch"

        self.dbClient.authenticate(login, id)
        self.assertEqual(id, self.userTable.find_one({"login": login})['user_id'])
        self.dbClient.authenticate(login, id)

    def test_AddFriend(self):
        pass
        #self.fail()

    def test_GetFriendsUserIds(self):
        pass
        #self.fail()
