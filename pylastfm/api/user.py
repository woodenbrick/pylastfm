#!/usr/bin/env python
from error import LastfmError, LastfmParamError, LastfmAuthenticationError
from _basetype import AbstractType, AbstractMethod

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
        self.realname = None
        self.url = None
        self.image = None
        self.country = None
        self.age = None
        self.gender = None
        """one of 'M' or 'F'"""
        self.subscriber = None
        self.playcount = None
        """How many tracks this user has scrobbled"""
        self.playlists = None
        self.bootstrap = None
        """Not sure what this is but this it is a boolean"""
        self.registered_unixtime = None
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
    


class UserMethod(AbstractMethod):
    def __init__(self, conn):
        self.conn = conn
    

    
    def getEvents(self, user=None):
        """
        Fetch the events this user is attending. Authentication not required.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session
        @return: A list of L{Event} objects
        """
        pass
    
    def getFriends(self, user=None, recenttracks=False, limit=50, page=1):
        """
        Fetch the friends of this user. Authentication not required.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session
        @param recenttracks: (Optional) Whether or not to include information
        about friends latest tracks.
        @param limit: (Optional) Limit the amount of friends to fetch.
        @param page: (Optional) The page number to fetch.
        @return: A list of L{User} objects
        """
        pass
    
    
    def getInfo(self, user=None):
        """
        Get information about a user. Authentication not required.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session
        @raise LastfmError : if user name is not set. 
        @return: A L{User} object
        """
        user = self._getUsername(user)
        xml = self.conn._api_get_request(user=user, method="user.getInfo")
        return self.conn.create_objects(xml, User)  
    
    
    def getLovedTracks(self, user=None, limit=None, page=None):
        """
        Get the last 50 tracks loved by a user. Authentication not required.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session
        @param limit: (Optional) An integer used to limit the number of tracks
        returned per page. The default is 50.
        @param page: (Optional) The page number to fetch.
        @raise LastfmError : if user name is not set
        @return: A list of L{Track} objects
        """
        user = self._getUsername(user)
        xml = self.conn._api_get_request(user=user, method="user.getLovedTracks")
        return self.conn.create_objects(xml, Track)
    
    
    def getNeighbours(self, user=None, limit=None):
        """
        Get the neighbours for this user.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session
        @param limit: (Optional) n integer used to limit the number of neighbours
        fetched.
        @return: A list of L{User} objects
        """
        pass
    
    def getPastEvents(self, user=None, page=None, limit=None):
        """
        A list of events the user has attended in the past. Authentication not
        required.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session
        @param page: (Optional) The page number to scan to.
        @param limit: (Optional) The maximum number of events to return per page.
        @return: A list of L{Event} objects
        """
        pass
    
    def getPlaylists(self, user=None):
        """
        Get a list of a user's playlists on Last.fm. Authentication not required.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session
        @return: A list of L{Playlist} objects.
        """
        pass
    
    def getRecentStations(self, user=None, limit=10, page=None):
        """
        Get a list of the recent Stations listened to by this user.
        Authentication required.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session.
        @param limit: (Optional) An integer used to limit the number of
        stations returned per page. The default is 10, the maximum is 25.
        @param page: (Optional) The page number to fetch.
        @return a list of L{Station} objects.
        """
        #make sure limit is under 25
        pass
    
    def getRecentTracks(self, user=None, limit=None, page=None):
        """
        Get a list of the recent tracks listened to by this user. Also
        includes the currently playing track with the nowplaying="true"
        attribute if the user is currently listening. This service does not 
        require authentication.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session
        @param limit: (Optional) An integer used to limit the number of
        tracks returned.
        @param page: (Optional) An integer used to fetch a specific page of tracks.
        @return: A list of L{Track} objects
        """
        pass
    
    def getRecommendedArtists(self, page=None, limit=None):
        """
        Get Last.fm artist recommendations for a user. This service requires
        authentication.
        @param page: The page to scan to.
        @param limit: The number of artists to return per page.
        @return: A list of L{Artist} objects
        """
        pass
        
    def getRecommendedEvents(self, page=None, limit=None):
        """
        Get a paginated list of all events recommended to a user by Last.fm,
        based on their listening profile. This service requires authentication.
        @param page: (Optional) The page number to scan to.
        @param limit: (Optional) The number of events to return per page.
        @return: A list of L{Event} objects.
        """
        pass
    
    def getShouts(self, user=None):
        """
        Get shouts for this user. Also available as an rss feed. This service
        does not require authentication.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session.
        @return: A list of L{Shout} objects.
        """
        pass
    
    def getTopAlbums(self, user=None, period="overall"):
        """
        Get the top albums listened to by a user. You can stipulate a time 
        period. Sends the overall chart by default. This service does not
        require authentication.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session
        @param period: (Optional) overall | 7day | 3month | 6month | 12month
        The time period over which to retrieve top albums for.
        @return: A list of L{Album} objects.
        """
        pass
    
    def getTopArtists(self, user=None, period="overall"):
        """
        Get the top artists listened to by a user. You can stipulate a time
        period. Sends the overall chart by default. This service does not
        require authentication.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session.
        @param period: (Optional) overall | 7day | 3month | 6month | 12month
        The time period over which to retrieve top artists for.
        """
        pass
    
    def getTopTags(self, user=None, limit=None):
        """
        Get the top tags used by this user. This service does not require
        authentication.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session.
        @param limit: (Optional) Limit the number of tags returned
        @return: A list of L{Tag} objects.
        """
        pass
    
    def getTopTracks(self, user=None, period="overall"):
        """
        Get the top tracks listened to by a user. You can stipulate a time
        period. Sends the overall chart by default. This service does not
        require authentication.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session.
        period (Optional) : overall | 7day | 3month | 6month | 12month
        The time period over which to retrieve top tracks for.
        @return: A list of L{Track} objects.
        """
        pass
    
    def getWeeklyAlbumChart(self, user=None, _from=None, to=None):
        """
        Get an album chart for a user profile, for a given date range.
        If no date range is supplied, it will return the most recent album
        chart for this user. This service does not require authentication.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session.
        @param _from: (Optional) The date at which the chart should start from.
        See L{getWeeklyChartList()} for more.
        @param to: (Optional) : The date at which the chart should end on.
        See L{getWeeklyChartList()} for more.
        @return: A list of L{Album} objects
        """
        pass
    
    def getWeeklyArtistChart(self, user=None, _from=None, to=None):
        """
        Get an artist chart for a user profile, for a given date range.
        If no date range is supplied, it will return the most recent artist
        chart for this user. This service does not require authentication.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session.
        @param _from: (Optional) The date at which the chart should start from.
        See L{getWeeklyChartList()} for more.
        @param to: (Optional) : The date at which the chart should end on.
        See L{getWeeklyChartList()} for more.
        @return: A list of L{Artist} objects
        """
        pass
    
    def getWeeklyChartList(self, user=None):
        """
        Get a list of available charts for this user, expressed as date ranges
        which can be sent to the chart services. This service does not require
        authentication.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session.
        @return: A list of L{Chart} objects
        """
        pass

    def getWeeklyTrackChart(self, user=None, _from=None, to=None):
        """
        Get a track chart for a user profile, for a given date range.
        If no date range is supplied, it will return the most recent track
        chart for this user. This service does not require authentication.
        @param user: (Optional) A string of the user to fetch results for,
        a L{User} object or None for user of the current session.
        @param _from: (Optional) The date at which the chart should start from.
        See L{getWeeklyChartList()} for more.
        @param to: (Optional) : The date at which the chart should end on.
        See L{getWeeklyChartList()} for more.
        @return: A list of L{Track} objects
        """
        pass

    def shout(self, user, message):
        """
        Shout on this user's shoutbox. This service requires authentication.
        @param user: (Optional) A string of the user to to shout on or 
        a L{User} object.
        @param message: (Optional) The message to post to the shoutbox.
        @return: True if posting was successful.
        """
        pass
