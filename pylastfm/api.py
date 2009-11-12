import os
import hashlib
import webbrowser
import re
import xmlrpclib
import urllib
import urllib2
import time
from xml.etree import ElementTree
from lastfmtypes._basetype import AbstractType
from lastfmtypes.user import User
from lastfmtypes.track import Track
from lastfmtypes.album import Album
from lastfmtypes.event import Event
from lastfmtypes.tag import Tag

class LastfmError(Exception):
    """Base class for all Last.fm Errors"""
    pass

class LastfmAuthenticationError(Exception):
    """Errors caused by authentication problems"""
    pass

class LastfmParamError(Exception):
    """Errors caused by passing incorrect parameters or invalid data"""

class LastfmApi(object):
    """The LastfmApi class is the main entry point into this library."""
    URL = "http://ws.audioscrobbler.com/2.0/"
    AUTH_URL = "http://www.last.fm/api/auth"
    
    def __init__(self, api_key, secret, session_key=None,
                 username=None, password=None, cache_enabled=False, cache_expiry=20):
        """
        Creates a new LastfmApi object.
        @param api_key: The api key provided by last.fm for your application
        @param secret: The secret key provided by last.fm
        @param session_key: A session key created in a previous session, or None
        @param username: The name of the user you wish to create a session for, or None,
        @param password: The users password, in plain text/md5 hash or None
        @param cache_enabled: Whether objects will be cached for reuse
        @param cache_expiry: The cache expiry time in minutes
        """
        self.api_key = api_key
        self.secret = secret
        self.session_key = session_key
        self.username = self.set_username(username)
        self.password = self.set_password(password)
        Cache.set_cache(cache_enabled, cache_expiry)


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
            webbrowser.open_new_tab(LastfmApi.AUTH_URL)
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
        #XXX kwargs with a value of None should not be encoded
        encoded_url = LastfmApi.URL + "?" + urllib.urlencode(kwargs)
        if Cache.ENABLED:
            object = Cache.return_object(kwargs['api_sig'])
            if object is not None:
                return object
        #download new data    
        request = urllib2.Request(url=encoded_url)
        return urllib2.urlopen(request)

        

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
            return False
        kwargs["sk"] = self.session_key
        kwargs["api_key"] = self.api_key
        encoded_data = urllib.urlencode(kwargs)
        request = urllib2.Request(url=self.url, data=encoded_data)
        response = urllib2.urlopen(request)
        tree = ElementTree.parse(response)
        return self._get_xml_response_code(tree)
    
    def _get_xml_response_code(self, etree):
        """
        Checks the status of a request
        @param etree: An ElementTree document to check
        @return: True if response was 'ok'
        """
        if etree.getroot().attrib['status'] == "ok":
            print etree.getroot().attrib['status']
            return True
        else:
            raise LastfmError(etree.find("error").text)
            return False
        

    @staticmethod
    def create_objects(doc, _class):
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
    #XXX need to return None for a dud object
    

    
    ##
    #Wrappers for calling Lastfm.Api methods
    ##
    
    #ALBUM
    
    def album_addTags(self, artist, album, tags):
        """
        Tag an album using a list of user supplied tags. Requires authentication.
        @param artist: (Required) The artist name in question
        @param album: (Required) The album name in question
        @param tags: (Required) A list of user supplied tags to apply to this
        album. Accepts a maximum of 10 tags.
        """
        if not isinstance(tags, list):
            raise LastfmParamError("argument tags requires a list")
            return False
        if len(tags) > 10:
            raise LastfmParamError("Maximum of 10 tags allowed")
            return False
        data = self._create_api_signature(artist=artist, album=album,
                                          tags=tags, method="album.addTags")
        return self._api_post_request(data)
    
    
    def album_getInfo(self, artist=None, album=None, mbid=None, username=None,
                      lang=None):
        """
        Get the metadata for an album on Last.fm using the album name or
        a musicbrainz id. See playlist.fetch on how to get the album playlist.
        Doesn't require authentication.
        @param artist: (Optional) The artist name in question
        @param album: (Optional) The album name in question
        @param mbid: (Optional) The musicbrainz id for the album
        @param username: (Optional) The username for the context of the request.
        If supplied, the user's playcount for this album is included in the response.
        @param lang: (Optional) The language to return the biography in,
        expressed as an ISO 639 alpha-2 code.
        @return An L{Album} object, or None
        """
        if album is None and mbid is None:
            raise LastfmParamError("Requires an album name or musicbrainz id")
            return False
        xml = self._api_get_request(artist=artist, album=album, mbid=mbid,
                                     username=username, lang=lang,
                                     method="album.getInfo")
        return LastfmApi.create_objects(xml, "Album")
    
    
    def album_getTags(self, artist, album):
        """
        Get the tags applied by users to an album on Last.fm.
        @param artist: (Required) The artist name in question
        @param album: (Required) The album name in question
        @return a list of L{Tag} objects or None
        """
        xml = self._api_get_request(artist=artist, album=album,
                                    method="album.getTags")
        return LastfmApi.create_objects(xml, Tag)
        
    
    def album_removeTag(self, artist, album, tag):
        """
        Remove a user's tag from an album.
        @param artist: (Required) The artist name in question
        @param album: (Required) The album name in question
        @param tag: (Required) A single user tag to remove from this album.
        """
        data = self._create_api_signature(artist=artist, album=album, tag=tag,
                                      method="album.removeTag")
        return self._api_post_request(data)
        
    def album_search(self, album, limit=30, page=1):
        """
         Search for an album by name. Returns album matches sorted by relevance.
        @param album: (Required) The album name in question
        @param limit: (Optional) Limit the number of albums returned at
        one time. Default (maximum) is 30.
        @param page: (Optional) Scan into the results by specifying a page
        number. Defaults to first page.
        @return a list of L{Album} objects or None
        """
        xml = self._api_get_request(album=album, limit=limit, page=page,
                                    method="album.search")
        return LastfmApi.create_objects(xml, Album)
        
    
    #ARTIST
    def artist_addTags():
        pass
    
    def artist_getEvents():
        pass
    
    def artist_getImages():
        pass
    
    def artist_getInfo():
        pass
    
    def artist_getPastEvents():
        pass
    
    def artist_getPodcast():
        pass
    
    def artist_getShouts():
        pass
    
    def artist_getSimilar():
        pass
    
    def artist_getTags():
        pass
    
    def artist_getTopAlbums():
        pass
    
    def artist_getTopFans():
        pass
    
    def artist_getTopTags():
        pass
    def artist_getTopTracks():
        pass
    def artist_removeTag():
        pass
    
    def artist_search():
        pass
    
    def artist_share():
        pass
    
    def artist_shout():
        pass

    def user_getLovedTracks(self, user=None, limit=None, page=None):
        """
        Get the last 50 tracks loved by a user. Authentication not required.
        @param user: (Optional) The user name to fetch the loved tracks for.
        If left blank the username for this session will be used.
        @param limit: (Optional) An integer used to limit the number of tracks
        returned per page. The default is 50.
        @param page: (Optional) The page number to fetch.
        @raise LastfmError : if user name is not set
        @return: A list of L{Track} objects
        """
        if user is None:
            if self.username is None:
                raise LastfmError("Username not set")
            user = self.username
        xml = self._api_get_request(user=user, method="user.getLovedTracks")
        return LastfmApi._create_objects(xml, Track)

    
    def users_getInfo(self, user=None):
        """
        Get information about a user. Authentication not required.
        @param user: (Optional) The user name to fetch info for.
        If left blank the username for this session will be used.
        @raise LastfmError : if user name is not set. 
        @return: A L{User} object
        """
        if user is None:
            if self.username is None:
                raise LastfmError("Username not set")
            user = self.username
        xml = self._api_get_request(user=user, method="user.getInfo")
        return LastfmApi.create_objects(xml, User)   

    def event_attend(self, event, status):
        """
        Mark a user as attendance status for an event
        @param event: (Required) The numeric last.fm event id
        @param status: (Required) The attendance status
        (0=Attending, 1=Maybe attending, 2=Not attending)
        @return: True if status was successfully changed
        """
        data = self._create_api_signature(event=event, status=status,
                                          method="event.attend")
        return self._api_post_request(data)


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
        