#!/usr/bin/env python
import webbrowser

class Auth(object):
    def __init__(self, conn):
        self.conn = conn
    
    def auth_getToken(self, open_browser=True):
        """
        Downloads a token from last.fm. For desktop applications only.
        @param open_browser: True if you wish pylastfm to open the users browser
        to authenticate your application. This would normally be the desired
        behaviour. After the user has allowed your application call
        L{auth_getSession()}
        @raise LastfmAuthenticationError: if the token couldnt be acquired
        @return: A token which can be used to authenticate your session
        """
        if open_browser:
            webbrowser.open_new_tab(LastfmApiConnection.AUTH_URL)
        data = self._create_api_signature(method="auth.getToken")
        xml = self._api_get_request(**data)
        tree = ElementTree.parse(xml)
        if self._get_xml_response_code(tree):
            return tree.find("token").text
        else:
            raise LastfmAuthenticationError(tree.find("error").text)
            return False
        
        
    def auth_getSession(self, token):
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
        data = self._create_api_signature(method="auth.getSession",
                                          token=token)
        response = self._api_get_request(**data)
        tree = ElementTree.parse(response)
        if self._get_xml_response_code(tree):
            self.session_key = tree.find("key").text
            return True
        else:
            return False