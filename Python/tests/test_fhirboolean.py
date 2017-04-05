#!/usr/bin/env python

from unittest import TestCase, main

from ..resource import Resource
from ..fhirboolean import FHIRBoolean

class CastToBoolTestCase(TestCase):
    def setUp(self):
        self.res = Resource()

    def test_valid_values(self):
        self.assertEqual(self.res._cast('true', FHIRBoolean).as_json(), True)
        self.assertEqual(self.res._cast('false', FHIRBoolean).as_json(), False)

        self.assertEqual(self.res._cast(True, FHIRBoolean).as_json(), True)
        self.assertEqual(self.res._cast(False, FHIRBoolean).as_json(), False)

        self.assertEqual(FHIRBoolean('true').as_json(), True)
        self.assertEqual(FHIRBoolean('false').as_json(), False)

        self.assertEqual(FHIRBoolean(True).as_json(), True)
        self.assertEqual(FHIRBoolean(False).as_json(), False)

        self.assertEqual(FHIRBoolean.with_json(True).as_json(), True)

        result = FHIRBoolean.with_json([False, True])
        self.assertEqual(
            [itm.as_json() for itm in result],
            [False, True]
        )

    def test_from_str(self):
        self.assertEqual(self.res._cast('0', FHIRBoolean).as_json(), None)
        self.assertEqual(self.res._cast('2', FHIRBoolean).as_json(), None)
        self.assertEqual(self.res._cast('Off', FHIRBoolean).as_json(), None)
        self.assertEqual(self.res._cast('DISABLE', FHIRBoolean).as_json(), None)
        self.assertEqual(self.res._cast('On', FHIRBoolean).as_json(), None)
        self.assertEqual(self.res._cast('ENABLE', FHIRBoolean).as_json(), None)

        self.assertEqual(FHIRBoolean('1').as_json(), None)
        self.assertEqual(FHIRBoolean('Off').as_json(), None)

    def test_from_int(self):
        self.assertEqual(self.res._cast(0, FHIRBoolean), None)
        self.assertEqual(self.res._cast(1, FHIRBoolean), None)
        self.assertEqual(self.res._cast(2, FHIRBoolean), None)
        self.assertEqual(self.res._cast(-1, FHIRBoolean), None)

        with self.assertRaises(TypeError) as err:
            FHIRBoolean(1)

        self.assertEqual(
            "Expecting bool or string when initializing <class "
            "'fhirmodels.fhirboolean.FHIRBoolean'>, but got <class 'int'>",
            str(err.exception)
        )

    def test_from_list(self):
        self.assertEqual(
            self.res._cast([None], FHIRBoolean),
            None
        )

        self.assertEqual(
            self.res._cast([None], FHIRBoolean, is_list=True),
            [None]
        )

        result = self.res._cast([False, True], FHIRBoolean, is_list=True)
        self.assertEqual(
            [itm.as_json() for itm in result],
            [False, True]
        )

        with self.assertRaises(TypeError) as err:
            FHIRBoolean([1])

        self.assertEqual(
            "Expecting bool or string when initializing <class "
            "'fhirmodels.fhirboolean.FHIRBoolean'>, but got <class 'list'>",
            str(err.exception)
        )

    def test_from_float(self):
        self.assertEqual(self.res._cast(0.0, FHIRBoolean), None)
        self.assertEqual(self.res._cast(0.00001, FHIRBoolean), None)

        with self.assertRaises(TypeError) as err:
            FHIRBoolean(-10.5)

        self.assertEqual(
            "Expecting bool or string when initializing <class "
            "'fhirmodels.fhirboolean.FHIRBoolean'>, but got <class 'float'>",
            str(err.exception)
        )

class FromDict(TestCase):
    def setUp(self):
        self.res = Resource()

    def test_from_dict(self):
        self.assertEqual(self.res._cast({}, FHIRBoolean), {})

        with self.assertRaises(TypeError) as err:
            FHIRBoolean({})

        self.assertEqual(
            "Expecting bool or string when initializing <class "
            "'fhirmodels.fhirboolean.FHIRBoolean'>, but got <class 'dict'>",
            str(err.exception)
        )

if __name__ == '__main__':
    main()
