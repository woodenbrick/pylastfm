#!/usr/bin/env python
import webbrowser
from xml.etree import ElementTree
from error import LastfmAuthenticationError, LastfmError, LastfmParamError

class AuthMethod(object):
    AUTH_URL = "http://www.last.fm/api/auth"
    
    def __init__(self, conn):
        self.conn = conn
    
    def getToken(self, open_browser=True):
        """
        Downloads a token from last.fm. For desktop applications only.
        @param open_browser: True if you wish pylastfm to open the users browser
        to authenticate your application. This would normally be the desired
        behaviour. After the user has allowed your application call
        L{auth_getSession()}
        @raise LastfmAuthenticationError: if the token couldnt be acquired
        @return: The token which can be used to authenticate your session
        """
        data = self.conn._create_api_signature(method="auth.getToken")
        xml = self.conn._api_get_request(**data)
        tree = ElementTree.parse(xml)
        if self.conn._get_xml_response_code(tree):
            token = tree.find("token").text
            if open_browser:
                webbrowser.open_new_tab(AuthMethod.AUTH_URL +
                                        "?api_key=%s&token=%s" % (self.conn.api_key,
                                                                  token))
            return token
        else:
            raise LastfmAuthenticationError(tree.find("error").text)
            return False
        
        
    def getSession(self, token):
        """
        Sets the session_key variable which allows authenticated calls.
        
        If you are creating a WEB APPLICATION:
        ======================================
            Before calling this function you must do the following things:
            Web applications should send a user to last.fm/api/auth, sending an API key 
            as a parameter, in order to authenticate the user. This should be a
            HTTP GET request. Your request will look like this:
            http://www.last.fm/api/auth/?api_key=xxxxxxxxxx

            Once the user has granted permission to use their account on the Last.fm page, 
            Last.fm will redirect to your callback url, supplying an authentication
            token as a GET variable: <callback_url>/?token=yyyyyy
        
        If you are creating a DESKTOP APPLICATION:
        ==========================================
            First call L{auth_getToken()}  
        
        @param token: the token sent to your callback url (WEB APP) or 
        from L{auth_getToken()} (DESKTOP APP).
        @return: True if the session key was set, else False
        """    
        data = self.conn._create_api_signature(method="auth.getSession",
                                          token=token)
        response = self.conn._api_get_request(**data)
        tree = ElementTree.parse(response)
        if self.conn._get_xml_response_code(tree):
            #XXX yuck
            iter = tree.getiterator("key")
            self.conn.session_key = iter[0].text
            return True
        else:
            return False