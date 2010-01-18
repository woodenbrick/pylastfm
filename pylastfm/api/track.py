#!/usr/bin/env python

from _basetype import AbstractType, AbstractMethod
from error import LastfmAuthenticationError, LastfmError, LastfmParamError

class Track(AbstractType):
    ROOT_NODE = "track"
    def __init__(self):
        pass      


class TrackMethod(AbstractMethod):
    def __init__(self, conn):
        self.conn = conn
        
    def addTags(self, artist, track, tags):
        """
        Tag an album using a list of user supplied tags. Authentication required.
        @param artist: (Required) The artist name in question or an
        L{Artist} object.
        @param track: (Required) The track name in question or a L{Track} object.
        @param tags: (Required) A list of user supplied tags to
        apply to this track. Accepts a maximum of 10 tags.
        """
        pass
    
    def ban(self, track, artist):
        """
        Ban a track for a given user profile. This needs to be supplemented
        with a scrobbling submission containing the 'ban' rating (see the
        audioscrobbler API).
        @param track: (Required) A track name (utf8 encoded)
        or a L{Track} object.
        @param artist: (Required) An artist name (utf8 encoded)
        or an L{Artist} object.
        """
        pass
    
    def getInfo(self, artist=None, track=None, mbid=None, username=None):
        """
        Get the metadata for a track on Last.fm using the artist/track name
        or a musicbrainz id. Authentication not required.
        @param: artist (Optional) The artist name or an L{Artist} object.
        @param track: (Optional) The track name or a L{Track} object.
        @param mbid: (Optional) The musicbrainz id for the track.
        @param username: (Optional) The username for the context of the request.
        If supplied, the user's playcount for this track and whether they have
        loved the track is included in the response. This can be a string or a
        L{User} object.
        """
        pass
    
    def getSimilar(self, track=None, artist=None, mbid=None):
Get the similar tracks for this track on Last.fm, based on listening data.

e.g. http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist=cher&track=believe&api_key=b25...
Params
track (Optional) : The track name in question
artist (Optional) : The artist name in question
mbid (Optional) : The musicbrainz id for the track
    