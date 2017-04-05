#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Facilitate working with dates.
#  2014, SMART Health IT.

import sys
import logging
import isodate

from datetime import date, datetime

import re

class FHIRDate(object):
    """ Facilitate working with dates.

    - `date`: datetime object representing the receiver's date-time
    """
    timezone_regex = re.compile('.+(Z|[+-][0-9:]{0,5})$')

    def __init__(self, jsonval=None):
        self.date = None
        self._format = None

        if jsonval is not None:
            if isinstance(jsonval, (date, datetime)):
                self.date = jsonval
            else:
                isstr = isinstance(jsonval, str)
                # Python 2.x has 'str' and 'unicode'
                if not isstr and sys.version_info[0] < 3:
                    isstr = isinstance(jsonval, basestring)
                if not isstr:
                    raise TypeError(
                        "Expecting string or datetime when initializing {}, "
                        "but got {}".format(type(self), type(jsonval))
                    )
                try:
                    if 'T' in jsonval:
                        self.date = isodate.parse_datetime(jsonval)
                    else:
                        self.date = isodate.parse_date(jsonval)
                except Exception as e:
                    logging.warning(
                        "Failed to initialize FHIRDate from \"{}\": {}"
                            .format(jsonval, e)
                    )

                self._origval = jsonval

    def __setattr__(self, prop, value):
        if 'date' == prop:
            self._format = None
            self._origval = None
        object.__setattr__(self, prop, value)

    @property
    def format(self):
        if self._format is None and self._origval:
            self._format = self._datetime_format(self._origval)
        return self._format

    @property
    def isostring(self):
        if self.date is None:
            return None

        if self.format is not None:
            if '.%f' not in self.format:
                result = isodate.datetime_isoformat(self.date, self.format)
            else:
                # Replace microseconds with milliseconds
                formats = self.format.split('.%f')
                result = ''.join((
                    isodate.datetime_isoformat(self.date, formats[0]),
                    isodate.datetime_isoformat(self.date, '.%f')[:-3],
                    isodate.datetime_isoformat(self.date, formats[1])
                ))
            if self._origval and isinstance(self.date, datetime):
                # Restoring original timezone representation
                result_tz = isodate.datetime_isoformat(self.date, '%Z')
                match = self.timezone_regex.match(self._origval)
                if result_tz and match:
                    orig_tz = match.group(1)
                    if orig_tz != result_tz:
                        result = result[:-len(result_tz)] + orig_tz
            return result
        elif isinstance(self.date, datetime):
            return isodate.datetime_isoformat(self.date)
        else:
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
        """ Added for compatibility reasons to FHIRElement.

        "owner" and "cast" are discarded.
        """
        return cls.with_json(jsonobj)

    def as_json(self):
        return self.isostring

    def _date_format(self, date_string):
        for pattern in isodate.isodates.build_date_regexps():
            match = pattern.match(date_string)
            if match:
                groups = match.groupdict()
                if 'century' in groups:
                    return '%C'
                elif 'month' not in groups:
                    if 'week' in groups:
                        if 'day' in groups:
                            return '%Y-W%W-%w'
                        else:
                            return '%Y-W%W'
                    elif 'day' in groups:
                        return '%Y-%j'
                    else:
                        return '%Y'
                elif 'day' not in groups or groups['day'] is None:
                    return '%Y-%m'
                else:
                    return '%Y-%m-%d'

    def _time_format(self, time_string):
        if time_string:
            for pattern in isodate.isotime.build_time_regexps():
                match = pattern.match(time_string)
                if match:
                    groups = match.groupdict()
                    if 'second' in groups:
                        if '.' in groups['second']:
                            return '%H:%M:%S.%f%Z'
                        else:
                            return '%H:%M:%S%Z'
                    elif 'minute' in groups:
                        return '%H:%M%Z'
                    else:
                        return '%H%Z'

    def _datetime_format(self, datetime_string):
        if 'T' in datetime_string:
            date_string, time_string = datetime_string.split('T')
            time_format = self._time_format(time_string)
        else:
            date_string = datetime_string
            time_format = ''
        date_format = self._date_format(date_string)
        return date_format + ('T' + time_format if time_format else '')
