#!/usr/bin/env python

from xml.etree import ElementTree as ET
#from api import LastfmError
class AbstractType(object):
    """Abstract class for all Last.fm API methods"""
    
    def _parse_etree(self, etree):
        """
        Looks at attributes for the subclass and adds any it finds in the etree
        @param etree: An ElementTree for the subclass
        @raise LastfmError: If int_types or bool_types subclass variable wasnt set
        """
        try:
            self.__getattribute__("int_types")
            self.__getattribute__("bool_types")
        except:
            pass
            #raise LastfmError("Must set int_types and bool_types before calling \
            #                  this function")
        
        iter = etree.getiterator()
        for attribute in iter:
            self._set_attribute(attribute.tag, attribute.text)
            if attribute.attrib != {}:
                for key, val in attribute.attrib.iteritems():
                    self._set_attribute(attribute.tag + "_" + key, val)


    def _set_attribute(self, name, value):
        """Sets this attribute to the correct type, if this class requires it"""
        if hasattr(self, name):
                setattr(self, name, self._correct_type(name, value))
    
    def _correct_type(self, name, value):
        """
        Returns the item with its correct type set, as specified
        by the int_types and bool_types attributes
        @param name: The name of the attribute
        @value: its string value
        """
        if name in self.int_types:
            return int(value)
        if name in self.bool_types:
            return bool(value)
        return value