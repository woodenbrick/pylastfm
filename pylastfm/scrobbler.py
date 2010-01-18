import re
import hashlib

class Scrobbler(object):
    SCROBBLE_URL = "http://post.audioscrobbler.com:80"
    
    def __init__(self, client='tst', version='1.0', max_tracks=50):
        self.client = client
        self.version = version
        self.max_tracks = max_tracks
        
    def _create_authentication_code(self, timestamp):
        return hashlib.md5(self.password + timestamp).hexdigest()

    def _to_post_string(self, tracks):
        data = {}
        for i, track in enumerate(tracks):
            track_iter = track.get_iterator()
            item = track_iter.next()
            data["%s[%s]" % (track.get_short(), i)]
            
        

    def handshake(self):
        pass
    
    def set_username_and_password(self, username, password):
        self.username = username
        if not re.match(r"^([a-fA-F\d]{32})$", password):
            self.password = hashlib.md5(password).hexdigest()
        else:
            self.password = password
    
    def scrobble(self, tracklist):
        pass
    
    
class ScrobbleTrack(object):
    def __init__(self, artist, track, timestamp, length, album="",
                 track_number="", rating="", source="P", mbid=""):
        self.artist = artist
        self.track = track
        self.timestamp = timestamp
        self.source = source
        self.rating = rating
        self.length = length
        self.album= album
        self.track_number = track_number
        self.mbid = mbid
    
