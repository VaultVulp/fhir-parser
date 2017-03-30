#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Subclassing Python's bool to add value casting capabilities.

import logging
import sys


class FHIRBoolean(object):
    """ Adds value casting capabilities.
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
                if jsonval in ('false', 'true'):
                    self.value = jsonval == 'true'
                else:
                    logging.warning(
                        'Failed to initialize FHIRBoolean from "{}'
                            .format(jsonval)
                    )

    @classmethod
    def with_json(cls, jsonobj):
        """ Initialize a FHIRBoolean object.
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
        return self.value
