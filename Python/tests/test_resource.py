#!/usr/bin/env python

from unittest import TestCase, main

from ..resource import Resource

class CastToIntTestCase(TestCase):
    def setUp(self):
        self.res = Resource()

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
        self.res = Resource()

    def test_from_str(self):
        result = self.res._cast('314', float)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 314.0)

        result = self.res._cast('3.14e2', float)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 314.0)

        result = self.res._cast('-3.14e2', float)
        self.assertIsInstance(result, float)
        self.assertEqual(result, -314.0)

        self.assertEqual(self.res._cast('3.14', float), 3.14)
        self.assertEqual(self.res._cast('3.14e-2', float), 0.0314)
        self.assertEqual(self.res._cast('string', float), None)

    def test_from_int(self):
        result = self.res._cast(31415, float)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 31415.0)

    def test_from_bool(self):
        result = self.res._cast(True, float)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

        result = self.res._cast(False, float)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)

    def test_from_float(self):
        self.assertEqual(self.res._cast(3.14, float), 3.14)


class CastToStringTestCase(TestCase):
    def setUp(self):
        self.res = Resource()

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
        self.res = Resource()

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


class CastFromDict(TestCase):
    def test_from_dict(self):
        res = Resource()
        self.assertEqual(res._cast({1: '3.14'}, str), {1: '3.14'})
        self.assertEqual(
            res._cast({'list': [1, 2]}, int),
            {'list': [1, 2]}
        )


class CastFromInstance(TestCase):
    def test_from_instance(self):
        res = Resource()
        self.assertIsInstance(
            res._cast(res, Resource),
            Resource
        )


class TestExceptions(TestCase):
    def test_wrong_resource_type(self):
        with self.assertRaises(Exception) as err:
            Resource({'id': 'some-id', 'resourceType': 'NotResource'})

        self.assertEqual(
            "Attempting to instantiate <class 'fhirmodels.resource.Resource'> "
            "with resource data that defines a resourceType of \"NotResource\"",
            str(err.exception)
        )

    def test_wrong_argument_type(self):
        with self.assertRaises(Exception) as err:
            Resource.with_json(123)

        self.assertIn(
            "`with_json()` on <class 'fhirmodels.resource.Resource'> only "
            "takes dict or list of dict, but you provided <class 'int'>",
            str(err.exception)
        )

    def test_tolerant(self):
        with self.assertLogs() as logged:
            res = Resource({'id': 'some-id', 'language': 123}, strict=False)

        self.assertEqual(
            res.as_json(),
            {'id': 'some-id', 'resourceType': 'Resource'}
        )
        self.assertIn(
            "Wrong type <class 'int'> for property \"language\" on <class "
            "'fhirmodels.resource.Resource'>, expecting <class 'str'>",
            ''.join(logged.output)
        )

if __name__ == '__main__':
    main()
