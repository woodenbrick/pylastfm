#!/usr/bin/env python

from _basetype import AbstractType

class Event(AbstractType):
    def __init__(self, etree):
        """
        A Last.fm event object.
        @param etree: An ElementTree for this event
        """
        AbstractType.__init__(self, int_types=["reviews", "attendance"],
            float_types=["longitude", "latitude"])
        self.id = None
        """Unique id of this event"""
        self.title = None
        """The name of this event"""
        self.artists = []
        """A list of artists playing at this event"""
        self.headliner = []
        """The main artist(s) playing at this event"""
        self.venue = None
        """The venue where the event is taking place"""
        self.city = None
        """The city where the event is taking place"""
        self.country = None
        """The country where the event is taking place"""
        self.street = None
        """The street the venue is on"""
        self.postalcode = None
        """The postcode of the venue"""
        self.longitude = None
        """The longitude coordinates of the venue"""
        self.latitude = None
        """The latitude coordinates of the venue"""
        self.timezone = None
        """The 3 letter timezone code"""
        self.venue_url = None
        """The last.fm page for this venue"""
        self.start_date = None
        """When this event takes place"""
        self.description = None
        """A description of the event"""
        self.image_small = None
        """A small thumbnail for this event"""
        self.image_medium = None
        """A medium thumbnail for this event"""
        self.image_large = None
        """A large thumbnail for this event"""
        self.attendance = None
        """The number of people planning to attend this event"""
        self.reviews = None
        """The number of reviews of this event made by last.fm users"""
        self.tag = None
        """Not sure what this is"""
        self.url = None
        """Link to event page on last.fm"""
        self.website = None
        """Link to external band/event webpage"""
        self.tickets = []
        """A list of urls where tickets for this event can be purchased"""


class EventMethod(object):
    def __init__(self, conn):
        self.conn = conn
        
    
    def attend(self, event, status):
        """
        Mark a user as attendance status for an event
        @param event: (Required) The numeric last.fm event id
        @param status: (Required) The attendance status
        (0=Attending, 1=Maybe attending, 2=Not attending)
        @return: True if status was successfully changed
        """
        return self.conn._api_post_request(event=event, status=status,
                                          method="event.attend")
