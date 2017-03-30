#!/usr/bin/env python

from unittest import TestCase, main

from Python.fhirabstractbase import FHIRAbstractBase
from Python.fhirboolean import FHIRBoolean
from Python.fhirdate import FHIRDate

class CastToBoolTestCase(TestCase):
    def setUp(self):
        self.res = FHIRAbstractBase()

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


class CastToIntTestCase(TestCase):
    def setUp(self):
        self.res = FHIRAbstractBase()

    def test_from_str(self):
        self.assertEqual(self.res._cast('314', int), 314)

    def test_from_float(self):
        self.assertEqual(self.res._cast(3.1415, int), 3)
        self.assertEqual(self.res._cast(2.71828, int), 2)

    def test_from_bool(self):
        self.assertEqual(self.res._cast(True, int), 1)
        self.assertEqual(self.res._cast(False, int), 0)

    def test_from_int(self):
        self.assertEqual(self.res._cast(123, int), 123)


class CastToFloatTestCase(TestCase):
    def setUp(self):
        self.res = FHIRAbstractBase()

    def test_from_str(self):
        self.assertEqual(self.res._cast('314', float), 314.0)
        self.assertEqual(self.res._cast('3.14', float), 3.14)
        self.assertEqual(self.res._cast('3.14e2', float), 314.0)
        self.assertEqual(self.res._cast('-3.14e2', float), -314.0)
        self.assertEqual(self.res._cast('3.14e-2', float), 0.0314)
        self.assertEqual(self.res._cast('string', float), None)

    def test_from_int(self):
        self.assertEqual(self.res._cast(31415, float), 31415.0)

    def test_from_bool(self):
        self.assertEqual(self.res._cast(True, float), 1.0)
        self.assertEqual(self.res._cast(False, float), 0.0)

    def test_from_float(self):
        self.assertEqual(self.res._cast(3.14, float), 3.14)


class CastToStringTestCase(TestCase):
    def setUp(self):
        self.res = FHIRAbstractBase()

    def test_from_int(self):
        self.assertEqual(self.res._cast(0, str), '0')

    def test_from_float(self):
        self.assertEqual(self.res._cast(3.14, str), '3.14')

    def test_from_bool(self):
        self.assertEqual(self.res._cast(True, str), 'True')
        self.assertEqual(self.res._cast(False, str), 'False')

    def test_from_list(self):
        self.assertEqual(self.res._cast([1, 2, '3'], str), "[1, 2, '3']")


    def test_from_null(self):
        self.assertEqual(self.res._cast(None, str), None)

    def test_from_str(self):
        self.assertEqual(self.res._cast('text', str), 'text')


class CastListOfStringsToListOfInTestCase(TestCase):
    def setUp(self):
        self.res = FHIRAbstractBase()

    def test_from_str(self):
        self.assertEqual(
            self.res._cast(['314', '123'], int, True),
            [314, 123]
        )

    def test_from_float(self):
        self.assertEqual(self.res._cast([3.1415, 2.71828], int, True), [3, 2])

    def test_from_bool(self):
        self.assertEqual(self.res._cast([True, False], int, True), [1, 0])

    def test_from_int(self):
        self.assertEqual(self.res._cast([123], int, True), [123])

    def test_from_non_list(self):
        self.assertEqual(self.res._cast(123, int, True), None)


class CastDict(TestCase):
    def setUp(self):
        self.res = FHIRAbstractBase()

    def test_from_dict(self):
        self.assertEqual(self.res._cast({}, FHIRBoolean), {})
        self.assertEqual(
            self.res._cast({'key': 'value'}, FHIRDate),
            {'key': 'value'}
        )
        self.assertEqual(self.res._cast({1: '3.14'}, str), {1: '3.14'})
        self.assertEqual(
            self.res._cast({'list': [1, 2]}, int),
            {'list': [1, 2]}
        )


if __name__ == '__main__':
    main()
