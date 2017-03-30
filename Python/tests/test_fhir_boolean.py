#!/usr/bin/env python

from unittest import TestCase, main

from ..resource import Resource
from ..fhirboolean import FHIRBoolean

class CastToBoolTestCase(TestCase):
    def setUp(self):
        self.res = Resource()

    def test_from_str(self):
        self.assertEqual(self.res._cast('0', FHIRBoolean).as_json(), None)
        self.assertEqual(self.res._cast('1', FHIRBoolean).as_json(), None)
        self.assertEqual(self.res._cast('2', FHIRBoolean).as_json(), None)
        self.assertEqual(self.res._cast('false', FHIRBoolean).as_json(), False)
        self.assertEqual(self.res._cast('Off', FHIRBoolean).as_json(), None)
        self.assertEqual(self.res._cast('DISABLE', FHIRBoolean).as_json(), None)
        self.assertEqual(self.res._cast('true', FHIRBoolean).as_json(), True)
        self.assertEqual(self.res._cast('On', FHIRBoolean).as_json(), None)
        self.assertEqual(self.res._cast('ENABLE', FHIRBoolean).as_json(), None)

    def test_from_int(self):
        self.assertEqual(self.res._cast(0, FHIRBoolean), None)
        self.assertEqual(self.res._cast(1, FHIRBoolean), None)
        self.assertEqual(self.res._cast(2, FHIRBoolean), None)
        self.assertEqual(self.res._cast(-1, FHIRBoolean), None)

    def test_from_list(self):
        self.assertEqual(self.res._cast([], FHIRBoolean), None)
        self.assertEqual(self.res._cast([1], FHIRBoolean), None)
        self.assertEqual(self.res._cast([None], FHIRBoolean), None)

    def test_from_float(self):
        self.assertEqual(self.res._cast(0.0, FHIRBoolean), None)
        self.assertEqual(self.res._cast(0.00001, FHIRBoolean), None)

    def test_from_bool(self):
        self.assertEqual(self.res._cast(True, FHIRBoolean).as_json(), True)
        self.assertEqual(self.res._cast(False, FHIRBoolean).as_json(), False)


class CastFromDict(TestCase):
    def setUp(self):
        self.res = Resource()

    def test_from_dict(self):
        self.assertEqual(self.res._cast({}, FHIRBoolean), {})

if __name__ == '__main__':
    main()
