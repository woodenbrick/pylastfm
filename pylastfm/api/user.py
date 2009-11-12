#!/usr/bin/env python
#from connection import LastfmError, LastfmParamError, LastfmAuthenticationError
from _basetype import AbstractType

class User(AbstractType):
    ROOT_NODE = "user"
    def __init__(self, etree):
        """
        @param etree: An ElementTree that is the data of a
        single user on last.fm
        """
        AbstractType.__init__(self, int_types=["age", "playcount", "playlists",
                                         "registered_unixtime"],
                              bool_types=["subscriber", "bootstrap"])
        
        self.id = None
        """Last.fm unique id"""
        self.name = None
        """Last.fm username"""
        self.realname = None
        """Users realname if known"""
        self.url = None
        """Link to users last.fm page"""
        self.image = None
        """Link to users image"""
        self.country = None
        """Country the user is from"""
        self.age = None
        """Age of user"""
        self.gender = None
        """one of 'M' or 'F'"""
        self.subscriber = None
        """True if user is a subscriber"""
        self.playcount = None
        """How many tracks this user has scrobbled"""
        self.playlists = None
        """How many playlists this user has"""
        self.bootstrap = None
        """Not sure what this is but this it is supposed to be boolean"""
        self.registered_unixtime = None
        """A unix timestamp of the users registration"""
        self.registered = None
        """Date string in the form of 2002-11-20 11:50"""
        
        self._parse_etree(etree)    
    
    
    def download_image(filename=None):
        """
        Downloads this users image
        @param filename: The path to download the file to. If this is blank
        the current directory is used and the filename will be in the form
        <username>.thumb
        @return: A string containing the download path
        """
        pass
    


class UserMethod(object):
    def __init__(self, api):
        self.api_obj = api
    
    def getLovedTracks(self, user=None, limit=None, page=None):
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
            if self.api_obj.username is None:
                raise LastfmError("Username not set")
            user = self.api_obj.username
        xml = self.api_obj._api_get_request(user=user, method="user.getLovedTracks")
        return self.api_obj.create_objects(xml, Track)
    
    
    def getInfo(self, user=None):
        """
        Get information about a user. Authentication not required.
        @param user: (Optional) The user name to fetch info for.
        If left blank the username for this session will be used.
        @raise LastfmError : if user name is not set. 
        @return: A L{User} object
        """
        if user is None:
            if self.api_obj.username is None:
                raise LastfmError("Username not set")
            user = self.api_obj.username
        xml = self.api_obj._api_get_request(user=user, method="user.getInfo")
        return self.api_obj.create_objects(xml, User)  