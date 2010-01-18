
from _basetype import AbstractType

class Album(AbstractType):
    def __init__(self, etree):
        AbstractType.__init__(self, int_types=["listeners", "playcount"])
        self.album_rank = None
        """How this album ranks against others"""
        self.id = None
        self.name = None
        self.playcount = None
        """How many times tracks from this album have been played (this can
        refer to a single user or many)"""
        self.release_date = None
        self.listeners = None
        self.playcount = None
        self.mbid = None
        self.top_tags = None
        self.url = None
        self.artist = None
        self.artist_url = None
        self.image_small = None
        self.image_medium = None
        self.image_large = None
        self.image_xlarge = None
        self.wiki = None
        
        self._parse_etree(etree)

class AlbumMethod(object):
    
    def __init__(self, conn):
        self.conn = conn
    
    def addTags(self, artist, album, tags):
        """
        Tag an album using a list of user supplied tags. Requires authentication.
        @param artist: A string of the artist's name or an L{Artist} object
        @param album: A string of the album's name or an L{Album} object
        @param tags: A list of user supplied tags to apply to this
        album. Accepts a maximum of 10 tags. These can be strings or L{Tag} objects
        """
        #tags could be either : a string, a list of strings, a Tag object, a list
        #of tag objects
        if not isinstance(tags, list):
            tags = [tags]
        if len(tags) > 10:
            raise LastfmParamError("Maximum of 10 tags allowed")
        if isinstance(tags[0], Tag):
            for i, tag in enumerate(tags):
                tags[i] = tag.name
        tags = ",".join(tags)
        data = self.conn._create_api_signature(artist=artist, album=album,
                                          tags=tags, method="album.addTags")
        return self.conn._api_post_request(data)
    
    
    def getInfo(self, artist=None, album=None, mbid=None, username=None,
                      lang=None):
        """
        Get the metadata for an album on Last.fm using the album name or
        a musicbrainz id. See playlist.fetch on how to get the album playlist.
        Doesn't require authentication.
        @param artist: (Optional) The artist name/an L{Artist} object
        @param album: (Optional) The album name/an L{Album} object
        @param mbid: (Optional) The musicbrainz id for the album
        @param username: (Optional) If supplied, the user's playcount for this
        album is included in the response.
        @param lang: (Optional) The language to return the biography in,
        expressed as an ISO 639 alpha-2 code.
        @return An L{Album} object, or None
        """
        if album is None and mbid is None:
            raise LastfmParamError("Requires an album name or musicbrainz id")
        if isinstance(artist, Artist):
            artist = artist.name
        if isinstance(album, Album):
            album = album.name
        xml = self.conn._api_get_request(artist=artist, album=album, mbid=mbid,
                                     username=username, lang=lang,
                                     method="album.getInfo")
        return self.conn.create_objects(xml, "Album")
    
    
    def getTags(self, artist, album):
        """
        Get the tags applied by users to an album on Last.fm.
        @param artist: (Required) The artist name or an L{Artist} object
        @param album: (Required) The album name or an L{Album} object
        @return a list of L{Tag} objects or None
        """
        if isinstance(artist, Artist):
            artist = artist.name
        if isinstance(album, Album):
            album = album.name
        xml = self.conn._api_get_request(artist=artist, album=album,
                                    method="album.getTags")
        return self.conn.create_objects(xml, Tag)
        
    
    def removeTag(self, artist, album, tag):
        """
        Remove a user's tag from an album.
        @param artist: (Required) The artist name or an L{Artist} object
        @param album: (Required) The album name or an L{Album} object
        @param tag: (Required) A single user tag to remove from this album. Can
        be a string or L{Tag} object
        """
        if isinstance(artist, Artist):
            artist = artist.name
        if isinstance(album, Album):
            album = album.name
        if isinstance(tag, Tag):
            tag = tag.name
        data = self.conn._create_api_signature(artist=artist, album=album, tag=tag,
                                      method="album.removeTag")
        return self.conn._api_post_request(data)
        
    def search(self, album, limit=30, page=1):
        """
         Search for an album by name. Returns album matches sorted by relevance.
        @param album: (Required) The album name or an L{Album} object
        @param limit: (Optional) Limit the number of albums returned at
        one time. Default (maximum) is 30.
        @param page: (Optional) Scan into the results by specifying a page
        number. Defaults to first page.
        @return a list of L{Album} objects or None
        """
        if isinstance(album, Album):
            album = album.name
        xml = self.conn._api_get_request(album=album, limit=limit, page=page,
                                    method="album.search")
        return self.conn.create_objects(xml, Album)
