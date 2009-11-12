#!/usr/bin/env python

class LastfmError(Exception):
    """Base class for all Last.fm Errors"""
    pass

class LastfmAuthenticationError(Exception):
    """Errors caused by authentication problems"""
    pass

class LastfmParamError(Exception):
    """Errors caused by passing incorrect parameters or invalid data"""
    pass
