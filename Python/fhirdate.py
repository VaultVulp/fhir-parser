#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Facilitate working with dates.
#  2014, SMART Health IT.

import sys
import logging
import isodate
from datetime import date, datetime


class FHIRDate(object):
    """ Facilitate working with dates.

    - `date`: datetime object representing the receiver's date-time
    """

    def __init__(self, jsonval=None):
        self.date = None
        if jsonval is not None:
            if isinstance(jsonval, (date, datetime)):
                self.date = jsonval
            else:
                isstr = isinstance(jsonval, str)
                if not isstr and sys.version_info[0] < 3:  # Python 2.x has 'str' and 'unicode'
                    isstr = isinstance(jsonval, basestring)
                if not isstr:
                    raise TypeError(
                        "Expecting string or datetime when initializing {}, but got {}"
                        .format(type(self), type(jsonval)))
                try:
                    if 'T' in jsonval:
                        self.date = isodate.parse_datetime(jsonval)
                    else:
                        self.date = isodate.parse_date(jsonval)
                except Exception as e:
                    logging.warning("Failed to initialize FHIRDate from \"{}\": {}"
                                    .format(jsonval, e))

                self.origval = jsonval

    def __setattr__(self, prop, value):
        if 'date' == prop:
            self.origval = None
        object.__setattr__(self, prop, value)

    @property
    def isostring(self):
        if self.date is None:
            return None
        if isinstance(self.date, datetime):
            return isodate.datetime_isoformat(self.date)
        return isodate.date_isoformat(self.date)

    @classmethod
    def with_json(cls, jsonobj):
        """ Initialize a date from an ISO date string.
        """
        if isinstance(jsonobj, cls):
            return jsonobj
        elif isinstance(jsonobj, list):
            return [cls(jsonval) for jsonval in jsonobj]
        else:
            return cls(jsonobj)

    @classmethod
    def with_json_and_owner(cls, jsonobj, owner, cast=False):
        """ Added for compatibility reasons to FHIRElement; "owner" is
        discarded.
        """
        return cls.with_json(jsonobj)

    def as_json(self):
        if self.origval is not None:
            return self.origval
        return self.isostring
