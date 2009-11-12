#!/usr/bin/env python

from xml.etree import ElementTree as ET

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
                value = int(value)
            if name in self.bool_types:
                value = False if value == "0" else True
                value = bool(value)           
            setattr(self, name, value)
    
