#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Subclassing Python's bool to add value casting capabilities.

import logging
import sys


class FHIRBoolean(object):
    """ Subclassing FHIR's boolean to add value casting capabilities.
    """

    def __init__(self, jsonval=None):
        self.value = None
        if jsonval is not None:
            if isinstance(jsonval, bool):
                self.value = jsonval
            else:
                isstr = isinstance(jsonval, str)
                if not isstr and sys.version_info[0] < 3:  # Python 2.x has 'str' and 'unicode'
                    isstr = isinstance(jsonval, basestring)
                if not isstr:
                    raise TypeError(
                        "Expecting bool or string when initializing {}, but got {}"
                        .format(type(self), type(jsonval))
                    )
                l_val = jsonval.lower()
                if l_val in ('false', 'true'):
                    self.value = l_val == 'true'
                else:
                    logging.warning(
                        'Failed to initialize FHIRBoolean from "{}'
                            .format(jsonval)
                    )

    @classmethod
    def with_json(cls, jsonobj):
        """ Initialize a FHIRBoolean object from a string.
        """
        if isinstance(jsonobj, cls):
            return jsonobj
        elif isinstance(jsonobj, bool):
            return cls(jsonobj)
        elif isinstance(jsonobj, list):
            return [cls(jsonval) for jsonval in jsonobj]
        else:
            isstr = isinstance(jsonobj, str)
            if not isstr and sys.version_info[0] < 3:  # Python 2.x has 'str' and 'unicode'
                isstr = isinstance(jsonobj, basestring)
            if isstr:
                return cls(jsonobj)

        raise TypeError(
            "`cls.with_json()` only takes string or list of strings, but you provided {}"
            .format(type(jsonobj)))

    @classmethod
    def with_json_and_owner(cls, jsonobj, owner, cast=False):
        """ Added for compatibility reasons to FHIRElement; "owner" is
        discarded.
        """
        return cls.with_json(jsonobj)

    def as_json(self):
        return self.value
