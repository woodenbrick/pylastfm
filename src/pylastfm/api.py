import md5
import webbrowser
import re
import xmlrpclib
import urllib
import urllib2
from xml.etree import ElementTree

from lastfmtypes.user import User

class LastfmError(Exception):
    """Base class for all Last.fm Errors"""
    pass

class LastfmAuthenticationError(Exception):
    """Errors caused by authentication problems"""
    pass

class LastfmApi(object):
    """The LastfmApi class is the main entry point into this library."""
    RESPONSE_OK = "ok"
    URL = "http://ws.audioscrobbler.com/2.0/"
    
    def __init__(self, api_key, secret, session_key=None):
        """
        Creates a new LastfmApi object.
        @param api_key: The api key provided by last.fm for your application
        @param secret: The secret key provided by last.fm
        @param session_key: A session key created in a previous session, or None
        """
        self.api_key = api_key
        self.secret = secret
        self.session_key = session_key
        self.username = None
        self.password = None
        


    def set_api_key(self, api_key, secret):
        """
        @param api_key: The api key provided by last.fm for your application
        @param secret: The secret key provided by last.fm
        """
        self.api_key = api_key
        self.secret = secret


    def set_username_and_password(self, username, password):
        """
        @param username: The users last.fm username
        @param password: The users password in plain text OR an md5 hash
        """
        self.username = username
        if not re.findall(r"^([a-fA-F\d]{32})$", password):
            self.password = md5.new(password).hexdigest()
        else:
            self.password = password

    def set_session_key(self, session_key):
        """
        Use a previously created session key
        @param session_key: A md5 hash string that can be used as a session key
        for the current user
        """
        self.session_key = session_key
        
        
    def create_authenticated_session(self, token):
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
            First call get_desktop_permissions()  
        
        @param token: the token sent to your callback url (WEB APP) or 
        from L{get_desktop_permissions()} (DESKTOP APP).
        @return: True if the session key was set, else False
        """    
        auth = Auth()
        signature = self._create_api_sig()
        request = auth.getSession(token, signature)
        response = get_response()
        if response == LastfmApi.RESPONSE_OK:
            #XXX NOT WRITTEN
            self.session_key = get_data()
        if self.session_key is None:
            return False
        return True
        
        
    def get_desktop_permissions(self, open_browser=True):
        """
        @param open_browser: True if you wish pylastfm to open the users browser
        to authenticate your application. This is usually the desired behaviour.
        @return: A token which can be used to authenticate your session
        
        After the user has allowed your application call create_authenticated_session()
        """
        signature = self.create_api_sig()
        token = Auth.getToken(signature)
        url = "http://www.last.fm/api/auth/?api_key=%s&token=%s" % (self.api_key, token)
        webbrowser.open_new_tab(url)

    
    
    def _create_api_signature(self, **kwargs):
        """
        Construct your api method signatures by first ordering all the
        parameters sent in your call alphabetically by parameter name
        and concatenating them into one string using a <name><value> scheme.
        So for a call to auth.getSession you may have:
        api_keyxxxxxxxxmethodauth.getSessiontokenxxxxxxx

        Ensure your parameters are utf8 encoded. Now append your secret to
        this string. Finally, generate an md5 hash of the resulting string.
        For example, for an account with a secret equal to 'mysecret', your
        api signature will be:

        api signature = md5("api_keyxxxxxxxxmethodauth.getSessiontokenxxxxxxxmysecret")

        @return: A dictionary containing all parameters and a md5 signature hash
        """
        kwargs['api_key'] = self.api_key
        kwargs.sort()
        data = ""
        for method, value in kwargs.iteritems():
            data += method + value
        data += self.secret
        kwargs['api_sig'] = hashlib.md5(data.encode('UTF-8')).hexdigest()
        return kwargs
    
    def _api_post_request(self, data_dict):
        """
        Connects to last.fm and makes a POST api request.
        @param data_dict: A dictionary of parameters to post to last.fm
        @raise LastfmAuthenticationError: if a session key is not found.
        @return: An XML document or False if no authentication was found
        """
        if self.session_key is None:
            raise LastfmAuthenticationError("This service requires authentication")
            return False
        encoded_data = urllib.urlencode(post_data)
        request = urllib2.Request(url=self.url, data=encoded_data)
        response = urllib2.urlopen(request)
        return url_handle.readlines()
        
    def _api_get_request(self, **kwargs):
        kwargs['api_key'] = self.api_key
        encoded_data = urllib.urlencode(kwargs)
        request = urllib2.Request(url=LastfmApi.URL + "?" + encoded_data)
        response = urllib2.urlopen(request)
        tree = self._parse_xml(response)
        iter = tree.getiterator()
        for i in iter:
            print i.tag, i.text
        #print tree.find("lfm").attrib['status']

        return tree
    
    def _parse_xml(self, doc):
        """
        Creates an ElementTree instance
        @param doc: An XML doc
        @return ElementTree
        """
        return ElementTree.parse(doc)

    def users_getLovedTracks(self, user=None, limit=None, page=None):
        """
        Get the last 50 tracks loved by a user. Authentication not required.
        
        @param user (Optional) : The user name to fetch the loved tracks for.
        If left blank the username for this session will be used.
        @param limit (Optional) : An integer used to limit the number of tracks
        returned per page. The default is 50.
        @param page (Optional) : The page number to fetch.
        @raise LastfmError : if user name is not set
        @return: A list of L{Track} objects
        """
        if user is None:
            if self.username is None:
                raise LastfmError("Username not set")
            user = self.username
        method = "user.getLovedTracks"
        xml = self._api_get_request(user=user, method=method)
        tree = ElementTree.parse(xml)
        
        return xml
    
    def users_getInfo(self, user=None):
        """
        Get information about a user. Authentication not required.
        
        @param user (Optional) : The user name to fetch info for.
        If left blank the username for this session will be used.
        @raise LastfmError : if user name is not set. 
        @return: A L{User} object
        """
        if user is None:
            if self.username is None:
                raise LastfmError("Username not set")
            user = self.username
        method = "user.getInfo"
        xml = open("tests/user.getInfo", "r")#self._api_get_request(user=user, method=method)
        tree = ElementTree.parse(xml)
        xml.close()
        iter = tree.getiterator("user")
        return User(iter[0])


