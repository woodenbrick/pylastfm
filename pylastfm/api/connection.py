import os
import hashlib
import webbrowser
import re
import urllib
import urllib2
import time
from xml.etree import ElementTree
from _basetype import AbstractType
from error import LastfmAuthenticationError, LastfmError, LastfmParamError

class LastfmApiConnection(object):
    """The LastfmApiConnection class is the main entry point into this library."""
    URL = "http://ws.audioscrobbler.com/2.0/"

    
    def __init__(self, api_key, secret, session_key=None,
                 username=None, password=None, cache_enabled=False, cache_expiry=20):
        """
        Creates a new LastfmApiConnection object.
        @param api_key: The api key provided by last.fm for your application
        @param secret: The secret key provided by last.fm
        @param session_key: A session key created in a previous session, or None
        @param username: The name of the user you wish to create a session for, or None,
        @param password: The users password, in plain text/md5 hash or None
        @param cache_enabled: Whether objects will be cached for reuse
        @param cache_expiry: The cache expiry time in minutes
        """
        from _basetype import AbstractType
        from user import UserMethod
        from auth import AuthMethod
        from event import EventMethod
        
        self.api_key = api_key
        self.secret = secret
        self.session_key = session_key
        self.username = self.set_username(username)
        self.password = self.set_password(password)
        Cache.set_cache(cache_enabled, cache_expiry)
        #self.album = AlbumMethod(self)
        self.user = UserMethod(self)
        self.auth = AuthMethod(self)
        self.event = EventMethod(self)

    def set_api_key(self, api_key, secret):
        """
        @param api_key: The api key provided by last.fm for your application
        @param secret: The secret key provided by last.fm
        """
        self.api_key = api_key
        self.secret = secret


    def set_username(self, username):
        """
        @param username: The users last.fm username
        """
        self.username = username
        
    def set_password(self, password):
        """
        @param password: The users password in plain text OR an md5 hash
        """
        if password is None:
            self.password = None
            return
        if not re.match(r"^([a-fA-F\d]{32})$", password):
            self.password = hashlib.md5(password).hexdigest()
        else:
            self.password = password

    def set_session_key(self, session_key):
        """
        Use a previously created session key
        @param session_key: A md5 hash string that can be used as a session key
        for the current user
        """
        self.session_key = session_key

    
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
        if self.session_key is not None:
            kwargs["sk"] = self.session_key
        data = ""
        for method, value in sorted(kwargs.iteritems()):
            data += "%s%s" % (method, value)
        data += self.secret
        kwargs['api_sig'] = hashlib.md5(data.encode('UTF-8')).hexdigest()
        return kwargs
    


    def _api_get_request(self, **kwargs):
        """
        Makes a GET request to last.fm
        @param kwargs: Any GET data that should be sent with the request
        eg. limit=1, user='woodenbrick'
        """
        kwargs['api_key'] = self.api_key
        encoded_url = LastfmApiConnection.URL + "?" + _encode_url_params(kwargs)
        if Cache.ENABLED:
            signature = self._create_api_signature(**kwargs)
            object = Cache.return_object(signature)
            if object is not None:
                return object
        #download new data    
        request = urllib2.Request(url=encoded_url)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
                response = e
        return response

        

    def _api_post_request(self, **kwargs):
        """
        Connects to last.fm and makes a POST api request.
        @param kwargs: Any POST data to be sent to last.fm
        @raise LastfmAuthenticationError: if a session key is not found.
        @raise LastfmError: If data couldnt be posted
        @return: True if the data was posted.
        """
        if self.session_key is None:
            raise LastfmAuthenticationError("This service requires authentication")
        kwargs = self._create_api_signature(**kwargs)
        encoded_data = _encode_lastfm_params(kwargs)
        request = urllib2.Request(url=LastfmApiConnection.URL, data=encoded_data)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            response = e
        tree = ElementTree.parse(response)
        return self._get_xml_response_code(tree)
    

    def _encode_lastfm_params(self, arg_dic):
        """Remove unwanted parameters from argument list and encode"""
        clean_dic = {}
        for key, value in arg_dic.items():
            if value is None:
                clean_dic[key] = value
        return urllib.urlencode(clean_dic)

    def _get_xml_response_code(self, etree):
        """
        Checks the status of a request
        @param etree: An ElementTree document to check
        @return: True if response was 'ok'
        """
        if etree.getroot().attrib['status'] == "ok":
            return True
        else:
            raise LastfmAuthenticationError(etree.find("error").text)
            return False
        

    def create_objects(self, doc, _class):
        """
        Creates an Object from an XML document.
        @param doc: an XML document
        @param _class: a class that subclasses L{AbstractType} eg. L{User}
        @return: A list or single instance of type _class or None if it couldnt
        be built
        """
        #sometimes we have a cached version, so we dont need to create objects
        if isinstance(doc, list) or isinstance(doc, AbstractType):
            return doc
        tree = ElementTree.parse(doc)
        iter = tree.getiterator(_class.ROOT_NODE)
        object_list = []
        for node in iter:
            object_list.append(_class(node))
        if len(object_list) == 1:
            return object_list[0]
        return object_list


class Cache(object):
    CACHE_DICT = {}
    EXPIRY = 20
    ENABLED = False
    
    def __init__(self, sig, object):
        Cache.CACHE_DICT['sig'] = object
        self.cache_time = time.time()
        
    @staticmethod
    def set_cache(enabled, expiry):
        Cache.ENABLED = enabled
        Cache.EXPIRY = expiry

    @staticmethod
    def return_object(signature):
        try:
            obj = Cache.CACHE_DICT['sig']
            if obj.cache_time - time.time() < Cache.EXPIRY:
                return Cache.CACHE_DICT['sig']
            return None
        except KeyError:
            return None
        
