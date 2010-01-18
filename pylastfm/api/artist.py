#!/usr/bin/env python
from _basetype import AbstractType, AbstractMethod
from error import LastfmParamError

class Artist(AbstractType):
    def __init__(self, etree):
        AbstractType.__init__(self, int_types=[])
        #init properties
        
        self._parse_etree(etree)

class ArtistMethod(AbstractMethod):
    def __init__(self, conn, name=None):
        """
        @param conn: A L{pylastfm.api.Connection} object
        @param name: The name of the artist.  Most methods require this and wont
        work if called and self.name is set to None"""
        self.conn = conn
        self.name = name
        
        
    def addTags(self, tags):
        """
        Tag an artist using a list of user supplied tags. Requires authentication.
        @param tags: A list of user supplied tags to apply to this
        album. Accepts a maximum of 10 tags. These can be strings or L{Tag} objects
        """
        tags = self._create_comma_delimited_string(tags)
        data = self.conn._create_api_signature(artist=self.name, tags=tags,
                                               method="artist.addTags")
        return self.conn._api_post_request(data)
    
    def getEvents(self):
        """
         Get a list of upcoming events for this artist.
        @return a list of L{Event} objects or None
        """
        xml = self.conn._api_get_request(artist=self.name, method="artist.getEvents")
        return self.conn.create_objects(xml, Event)
    
    def getImages(self, page=None, limit=50, order="popularity"):
        """
        Get Images for this artist in a variety of sizes.
        @param page: (Optional) Which page of limit amount to display.
        @param limit: (Optional) How many to return. Defaults and maxes out at 50.
        @param order: (Optional) Sort ordering can be either 'popularity'
        (default) or 'dateadded'. While ordering by popularity officially
        selected images by labels and artists will be ordered first.
        @return: A list of L{Image} objects."""
        if order != "popularity" or order != "dateadded":
            raise LastfmParamError("Invalid order parameter")
        xml = self.conn._api_get_request(artist=self.name, page=page, limit=limit,
                                         order=order, method="artist.getImages")
        return self.conn.create_objects(xml, Image)
        
        
    def getInfo(self, mbid=None, username=None, lang=None):
        """
        Get the metadata for an artist on Last.fm. Includes biography.
        @param mbid: (Optional) The musicbrainz id for the artist. This is
        discarded if the name attribute of this object is set.
        @param username: (Optional) The username for the context of the request.
        If supplied, the user's playcount for this artist is included in the response.
        @param lang: (Optional) The language to return the biography in,
        expressed as an ISO 639 alpha-2 code.
        @return: An L{Artist} object.
        """
        if self.name is not None:
            mbid = None
        xml = self.conn._api_get_request(artist=self.name, mbid=mbid,
                                         username=username, lang=lang,
                                         method="artist.getInfo")
        return self.conn.create_objects(xml, Artist)
    
    def getPastEvents(self, page=None, limit=None):
        """
        Get a paginated list of all the events this artist has played at in the past.
        @param page: (Optional) The page of results to return.
        @param limit: (Optional) The maximum number of results to return per page.
        @return: A list of L{Event} objects.
        """
        xml = self.conn._api_get_request(artist=self.name, page=page,
                                         limit=limit, method="artist.getPastEvents")
        return self.conn.create_objects(xml, Event)
    
    def getPodcast(self):
        """
        Get a podcast of free mp3s based on this artist.
        @return: A L{Podcast} object
        """
        xml = self.conn._api_get_request(artist=self.name, method="artist.getPodcast")
        return self.conn.create_objects(xml, Podcast)
    
    def getShouts(self, limit=None, page=None):
        """
        @param limit: (Optional) An integer used to limit the number of shouts
        returned per page. The default is 50.
        @param page: (Optional) The page number to fetch.
        @return: A list of L{Shout} objects.
        """
        xml = self.conn._api_get_request(artist=self.name, limit=limit,
                                         page=page, method="artist.getShouts")
        return self.conn.create_objects(xml, Shout)
    
    def getSimilar(self, limit=None):
        """
        Get all the artists similar to this artist
        @param limit: (Optional) Limit the number of similar artists returned
        @return: A list of L{Artist} objects.
        """
        xml = self.conn._api_get_request(artist=self.name, limit=limit,
                                         method="artist.getSimilar")
        return self.conn.create_objects(xml, Artist)
        
    def getTags(self):
        """
        Get the tags applied by an individual user to an artist on Last.fm.
        This service requires authentication.
        @return: A list of L{Tag} objects.
        """
        xml = self.conn._api_get_request(artist=self.name, method="artist.getTags")
        return self.conn.create_objects(xml, Tag)
    
    def getTopAlbums(self):
        """
        Get the top albums for an artist on Last.fm, ordered by popularity.
        @return: A list of L{Album} objects.
        """
        xml = self.conn._api_get_request(artist=self.name, method="artist.getTopAlbums")
        return self.conn.create_objects(xml, Album)
    
    def getTopFans(self):
        """
        Get the top fans for an artist on Last.fm, based on listening data.
        @return: A list of L{User} objects.
        """
        xml = self.conn._api_get_request(artist=self.name, method="artist.getTopFans")
        return self.conn.create_objects(xml, User)
    
    def getTopTags(self):
        """
        Get the top tags for an artist on Last.fm, ordered by popularity.
        @return: A list of L{Tag} objects.
        """
        xml = self.conn._api_get_request(artist=self.name, method="artist.getTopTags")
        return self.conn.create_objects(xml, Tag)
    
    def getTopTracks(self):
        """
        Get the top tracks by an artist on Last.fm, ordered by popularity
        @return: A list of L{Track} objects.
        """
        xml = self.conn._api_get_request(artist=self.name, method="artist.getTopTracks")
        return self.conn.create_objects(xml, Track)
    
    def removeTag(self, tag):
        """
        Remove a user's tag from an artist.
        @param tag: A L{Tag} object or a string
        This service requires authentication.
        """
        tag = self._get_attribute(tag)
        data = self.conn._create_api_signature(artist=self.name, tag=tag,
                                            method="artist.removeTag")
        return self.conn._api_post_request(data)
    
    def search(self, limit=None, page=None):
        """
        Search for an artist by name. Returns artist matches sorted by relevance.
        @param limit: (Optional) Limit the number of artists returned at one time.
        Default (maximum) is 30.
        @param page: (Optional) Scan into the results by specifying a page number.
        Defaults to first page.
        @return A list of L{Artist} objects
        """
        xml = self.conn._api_get_request(artist=self.name, limit=limit,
                                         page=page, method="artist.search")
        return self.conn.create_objects(xml, Artist)
        
    
    def share(self, recipient, message=None):
        """
        Share an artist with Last.fm users or other friends.
        @param recipient: A list of email addresses, Last.fm usernames or
        L{User} objects. Maximum is 10.
        @param message: (Optional) An optional message to send with the
        recommendation. If not supplied a default message will be used.
        This method requires authentication.
        """
        recipient = self._create_comma_delimited_string(recipient)
        data = self.conn._create_api_signature(artist=self.name, recipient=recipient,
                                    message=message, method="artist.share")
        return self.conn._api_post_request(data)
    
    def shout(self, message):
        """
        @param message: The message to post to the artists shoutbox.
        """
        data = self.conn._create_api_signature(artist=self.name, message=message,
                                            method="artist.shout")
        return self.conn._api_post_request(data)