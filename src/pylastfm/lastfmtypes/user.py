#!/usr/bin/env python

from lastfm_type import AbstractType

class User(AbstractType):
    def __init__(self, etree):
        """
        @param etree: An ElementTree that is the data of a
        single user on last.fm
        """
        
        self.int_types = ["age", "playcount", "playlists", "registered_timestamp"]
        self.bool_types = ["subscriber", "bootstrap"]
        
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
    