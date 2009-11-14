#!/usr/bin/env python

import unittest
import sys
import time
from xml.etree import ElementTree
#append system path
sys.path.insert(0, "../")
from pylastfm.scrobbler import Scrobbler

class ScrobblerTest(unittest.TestCase):
    def setUp(self):
        self.scrobbler = Scrobbler()
        self.scrobbler.set_username_and_password("Tard", "qwerty")
        self.timestamp = "1234567890"
        
    def test_auth_code(self):
        auth_code = self.scrobbler._create_authentication_code(self.timestamp)
        self.assertEqual(auth_code, "24ae6230c55c80bdbdce4bdd7ef42987")
        
    def test_to_post_string(self):
        data = [{"a" : "Foo Fighters", "t" : "Monkey Wrench", "i" : 1234567890,
          "o" : "P", "r" : "", "l" : 200, "b" : "The Color and the Shape",
          "n" : 2, "m" : ""},
        {"a" : "Gerling", "t" : "Death to the Apple Gerls", "i" : 1234567789,
          "o" : "P", "r" : "", "l" : 220, "b" : "The Apple", "n" : 3, "m" : ""}]
        known_data = """a[0]=Foo+Fighters&t[0]=Monkey+Wrench&i=1234567890&o[0]=P&r[0]=&l[0]=200&b[0]=The+Color+and+the+Shape&n[0]=2&m[0]=&a[1]=Gerling&t[1]=Death+to+the+Apple+Gerls&i[1]=1234567789&o[1]=P&r[1]=&l[1]=220&b[1]=The+Apple&n[1]=3&m[1]="""
        self.assertEqual(self.scrobbler._to_post_string(data), known_data)

    
if __name__ == "__main__":
    unittest.main()
