
from _basetype import AbstractType

class Album(AbstractType):
    def __init__(self, etree):
        AbstractType.__init__(self, int_types=[])
        self.album_rank = None
        """How this album ranks against others"""
        self.name = None
        """The name of the album"""
        self.playcount = None
        """How many times tracks from this album have been played (this can
        refer to a single user or many)"""
        self.mbid = None
        """Musicbrainz id"""
        self.url = None
        """The last.fm url for this album"""
        self.artist = None
        """The artist that created the album"""
        self.artist_url = None
        """The last.fm url for this artist"""
        self.image_small = None
        """A url for the album image"""
        self.image_medium = None
        """A url for the album image"""
        self.image_large = None
        """A url for the album image"""
        self.image_xlarge = None
        """A url for the album image"""
        
        self._parse_etree(etree)

class AlbumMethod(object):
    
    def __init__(self, conn):
        self.conn = conn
    
    def addTags(self, artist, album, tags):
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
        data = self.conn._create_api_signature(artist=artist, album=album,
                                          tags=tags, method="album.addTags")
        return self.conn._api_post_request(data)
    
    
    def getInfo(self, artist=None, album=None, mbid=None, username=None,
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
        xml = self.conn._api_get_request(artist=artist, album=album, mbid=mbid,
                                     username=username, lang=lang,
                                     method="album.getInfo")
        return self.conn.create_objects(xml, "Album")
    
    
    def getTags(self, artist, album):
        """
        Get the tags applied by users to an album on Last.fm.
        @param artist: (Required) The artist name in question
        @param album: (Required) The album name in question
        @return a list of L{Tag} objects or None
        """
        xml = self.conn._api_get_request(artist=artist, album=album,
                                    method="album.getTags")
        return self.conn.create_objects(xml, Tag)
        
    
    def removeTag(self, artist, album, tag):
        """
        Remove a user's tag from an album.
        @param artist: (Required) The artist name in question
        @param album: (Required) The album name in question
        @param tag: (Required) A single user tag to remove from this album.
        """
        data = self.conn._create_api_signature(artist=artist, album=album, tag=tag,
                                      method="album.removeTag")
        return self.conn._api_post_request(data)
        
    def search(self, album, limit=30, page=1):
        """
         Search for an album by name. Returns album matches sorted by relevance.
        @param album: (Required) The album name in question
        @param limit: (Optional) Limit the number of albums returned at
        one time. Default (maximum) is 30.
        @param page: (Optional) Scan into the results by specifying a page
        number. Defaults to first page.
        @return a list of L{Album} objects or None
        """
        xml = self.conn._api_get_request(album=album, limit=limit, page=page,
                                    method="album.search")
        return self.conn.create_objects(xml, Album)
