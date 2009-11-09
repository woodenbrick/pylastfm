#!/usr/bin/env python

class ErrorCode(object):
    error_dict = {
        "2" : "Invalid service -This service does not exist",
        "3" : "Invalid Method - No method with that name in this package",
        "4" : "Authentication Failed - You do not have permissions to access the service",
        "5" : "Invalid format - This service doesn't exist in that format",
        "6" : "Invalid parameters - Your request is missing a required parameter",
        "7" : "Invalid resource specified",
        "9" : "Invalid session key - Please re-authenticate",
        "10" : "Invalid API key - You must be granted a valid key by last.fm",
        "11" : "Service Offline - This service is temporarily offline. Try again later.",
        "12" : "Subscribers Only - This service is only available to paid last.fm subscribers"}
    
    def return_error_string(code):
        """
        @param code: An error code returned by the last.fm api
        @return: A string corresponding to the code
        """
        return error_dict[str(code)]
