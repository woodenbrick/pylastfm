#!/usr/bin/env python
import unittest
import sys
import hashlib
from xml.etree import ElementTree
#append system path
sys.path.insert(0, "../")
from pylastfm.api.connection import LastfmApiConnection
from pylastfm.api.user import User
from pylastfm.api.error import LastfmError
f = open("../api_keys", "r")
api_key = f.readline().strip()
secret = f.readline().strip()
session_key = f.readline().strip()
f.close()

class LastfmObjects(unittest.TestCase):

    def setUp(self):
        self.objectlist = [
            ("data/user.getInfo", User)
        ]
        self.api = LastfmApiConnection(None, None)
        
    
    def test_objects(self):
        for item in self.objectlist:
            f = open(item[0], "r")
            user = self.api.create_objects(f, item[1])
            self.assertEqual(user.id, "6386116")
            self.assertEqual(user.name, "woodenbrick")
            self.assertEqual(user.url, "http://www.last.fm/user/woodenbrick")
            self.assertEqual(user.gender, "m")
            self.assertEqual(user.subscriber, False)
            self.assertEqual(user.registered_unixtime, 1178554666)


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.api = LastfmApiConnection(api_key, secret)
        self.api.set_session_key(session_key)
        self.api.set_username("woodenbrick")
        
        
    def test_sig(self):
        sig = self.api._create_api_signature(method="event.attend", user="woodenbrick",
                          event="43151", status=2)
        sig_check = """api_key%sevent43151methodevent.attendskb9c31fdbdd4bfe3cbcbb1f96d5ec8b6estatus2userwoodenbrick%s""" % (api_key, secret)
        self.assertEqual(sig['api_sig'], hashlib.md5(sig_check).hexdigest())

    
    
    def test_xml_response(self):
        f = open("data/auth.getToken", "r")
        tree = ElementTree.parse(f)
        f.close()
        response = self.api._get_xml_response_code(tree)
        self.assertTrue(response)
        f = open("data/auth.getSession", "r")
        tree = ElementTree.parse(f)
        f.close()
        self.assertRaises(LastfmError,
                          self.api._get_xml_response_code,
                          tree)
        
if __name__ == "__main__":
    unittest.main()

