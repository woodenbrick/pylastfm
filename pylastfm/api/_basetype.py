#!/usr/bin/env python

from xml.etree import ElementTree as ET
from error import LastfmAuthenticationError, LastfmError, LastfmParamError

class AbstractType(object):
    """Abstract class for all Last.fm API methods"""
    def __init__(self, int_types=[], bool_types=[], float_types=[]):
        """
        @param int_types: A list of attributes that should be integers
        @param bool_types: A list of attributes that should be boolean
        @param float_types: A list of attributes that should be floats
        """
        self.int_types = int_types
        self.bool_types = bool_types
        self.float_types = float_types
    
    
    def _parse_etree(self, etree):
        """
        Looks at attributes for the subclass and adds any it finds in the etree
        @param etree: An ElementTree for the subclass
        """
        iter = etree.getiterator()
        for attribute in iter:
            self._set_attribute(attribute.tag, attribute.text)
            if attribute.attrib != {}:
                for key, val in attribute.attrib.iteritems():
                    self._set_attribute(attribute.tag + "_" + key, val)


    def _set_attribute(self, name, value):
        """
        Sets this attribute to the correct type, if this class requires it
        @param name: The name of the attribute eg. realname
        @param value: The value of the attribute eg. Daniel Woodhouse
        """
        if hasattr(self, name):
            if name in self.int_types:
                try:
                    value = int(value)
                except: pass
            if name in self.bool_types:
                value = False if value == "0" else True
                value = bool(value)           
            setattr(self, name, value)
    

class AbstractMethod(object):
    
    def _getUsername(self, user):
        if user is None:
            if self.conn.username is None:
                raise LastfmError("Username not set")
            return self.conn.username
        else:
            if isinstance(user, AbstractMethod):
                return user.name
    
    def _create_comma_delimited_string(self, items, wanted_attrib="name"):
        """Return a strings fromthat can be used as tags"""
        # could be either : a string, a list of strings, a AbstractType object, a list
        #of AbstractType objects
        if not isinstance(items, list):
            tags = [items]
        #last.fm only allows 10 items per api call
        if len(items) > 10:
            raise LastfmParamError("Maximum of 10 items allowed")
        if isinstance(tags[0], AbstractType):
            items = [self._get_attribute(item, wanted_attrib) for item in items]
        return ",".join(items)
        
    def _get_attribute(self, obj, attribute="name"):
        """If this object is derived from AbstractType we will return the
        required attribute, otherwise we return the object (a string)"""
        if isinstance(obj, AbstractType):
            return getattr(obj, attribute)
        else:
            return obj