#!/usr/bin/env python
import unittest
import sys
from xml.etree import ElementTree
#append system path
sys.path.insert(0, "../")
from pylastfm import api
from pylastfm.lastfmtypes.user import User
f = open("data/api_keys", "r")
api_key = f.readline().strip()
secret = f.readline().strip()
session_key = f.readline().strip()
f.close()

class LastfmObjects(unittest.TestCase):

    def setUp(self):
        self.objectlist = [
            ("data/user.getInfo", User, "user")
        ]
        
    
    def test_objects(self):
        for item in self.objectlist:
            f = open(item[0], "r")
            user = api.LastfmApi._create_objects(f, item[1], item[2])
            self.assertEqual(user.id, "6386116")
            self.assertEqual(user.name, "woodenbrick")
            self.assertEqual(user.url, "http://www.last.fm/user/woodenbrick")
            self.assertEqual(user.gender, "m")
            self.assertEqual(user.subscriber, False)
            self.assertEqual(user.registered_unixtime, 1178554666)


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.api = api.LastfmApi(api_key, secret)
        self.api.set_session_key(session_key)
        self.api.set_username("woodenbrick")
        
        
    def test_sig(self):
        sig = self.api._create_api_signature(method="event.attend", user="woodenbrick",
                          event="43151", status=2)
        self.assertEqual(sig['api_sig'],"e7c213e72fb1d6cd246a5c9da28b3a6b")

    
    def test_xml_response(self):
        f = open("data/auth.getToken", "r")
        tree = ElementTree.parse(f)
        f.close()
        response = self.api._get_xml_response_code(tree)
        self.assertTrue(response)
        f = open("data/auth.getSession", "r")
        tree = ElementTree.parse(f)
        f.close()
        self.assertRaises(api.LastfmError,
                          self.api._get_xml_response_code,
                          tree)
        
if __name__ == "__main__":
    unittest.main()

