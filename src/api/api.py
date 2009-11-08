
class LastfmError(object):
    pass

class LastfmApi(object):
    def __init__(self, username=None, password=None):
        """Creates a new LastfmApi object.  If username and/or password are set to None
        only methods that dont require authenticated will be allowed"""
        self.artist = Artist()
        self.album = Album()
        self.tag = Tag()

    def _create_authenticated_session(self):
        """Creates a new authenticated session"""
        pass

    def getTags(self):
        pass
    
    def removeTag(self):
        pass


class LastfmMethod(object):
    """Abstract class for all Last.fm API methods"""
    def addTags(self):
        pass
    
    def addTrack(self):
        pass

    def getInfo(self):
        pass
    
    def search(self):
        pass
    
    def getEvents(self):
        pass
    
    def getPastEvents(self):
        pass
    
    def getShouts(self):
        pass
    
    def getSimilar(self):
        pass

    def getTags(self):
        pass
    
    def getTopAlbums(self):
        pass
    
    def getTopArtists(self):
        pass
    
    def getTopFans(self):
        pass
    
    def getTopTags(self):
        pass
    
    def getTopTracks(self):
        pass
    
    def getWeeklyAlbumChart(self):
        pass
    
    def getWeeklyArtistChart(self):
        pass
    
    def getWeeklyChartList(self):
        pass
    
    def getWeeklyTrackChart(self):
        pass
    
    def removeTag(self):
        pass
    
    def search(self):
        pass
    
    def share(self):
        pass
    
    def shout(self):
        pass
    
    
class Album(LastfmMethod):
    pass

    
    
class Artist(LastfmMethod):
    def getImages(self):
        pass
    
    def getPodcast(self):
        pass
    

class Auth(LastfmMethod):
    def getMobileSession(self):
        pass
    
    def getSession(self):
        pass
    
    def getToken(self):
        pass


class Event(LastfmMethod):
    def attend(self):
        pass
    
    def getAttendees(self):
        pass


class Geo(LastfmMethod):
    def getMetroArtistChart(self):
        pass
    
    def getMetroTrackChart(self):
        pass
    
    def getMetroUniqueArtistChart(self):
        pass
    
    def getMetroUniqueTrackChart(self):
        pass
    
    def getMetroWeeklyChartlist(self):
        pass
    

class Group(LastfmMethod):
    def getMembers(self):
        pass


class Library(LastfmMethod):
    def addAlbum(self):
        pass
    
    def addArtist(self):
        pass
    
    def getAlbums(self):
        pass
    
    def getArtists(self):
        pass
    
    def getTracks(self):
        pass

class Playlist(LastfmMethod):
    def create(self):
        pass
    
    def fetch(self):
        pass

class Radio(LastfmMethod):
    
    def getPlaylist(self):
        pass
    
    def tune(self):
        pass
    

class Tag(LastfmMethod):
    pass

class Tasteometer(LastfmMethod):
    def compare(self):
        pass


class Track(LastfmMethod):
    def ban(self):
        pass
    
    def love(self):
        pass
    

class User(LastfmMethod):
    def getFriends(self):
        pass
    
    def getLovedTracks(self):
        pass
    
    def getNeighbours(self):
        pass

    def getPlaylists(self):
        pass
    
    def getRecentStations(self):
        pass
    
    def getRecentTracks(self):
        pass
    
    def getRecommendedArtists(self):
        pass
    
    def getRecommendedEvents(self):
        pass
    
    
class Venue(LastfmMethod):
    pass

