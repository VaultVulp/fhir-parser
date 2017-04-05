#!/usr/bin/env python

from unittest import TestCase, main
from datetime import date, datetime

from isodate import FixedOffset

from ..resource import Resource
from ..fhirdate import FHIRDate


class TestFHIRDateAsJson(TestCase):
    def test_from_valid_str_datetime(self):
        el = FHIRDate('1986-09-21T021234')
        self.assertEqual(el.as_json(), '1986-09-21T02:12:34')
        self.assertEqual(el.date, datetime(1986, 9, 21, 2, 12, 34))

        el = FHIRDate('19860921T02:12:34')
        self.assertEqual(el.as_json(), '1986-09-21T02:12:34')
        self.assertEqual(el.date, datetime(1986, 9, 21, 2, 12, 34))

        el = FHIRDate('2015-02-09T11:04:15.817-05:00')
        self.assertEqual(el.as_json(), '2015-02-09T11:04:15.817-05:00')
        self.assertEqual(
            el.date,
            datetime(2015, 2, 9, 11, 4, 15, 817000,  tzinfo=FixedOffset(-5))
        )

        el = FHIRDate('2013-01-01T10:50:00+00:00')
        self.assertEqual(el.as_json(), '2013-01-01T10:50:00+00:00')
        self.assertEqual(
            el.date,
            datetime(2013, 1, 1, 10, 50, tzinfo=FixedOffset())
        )

        el = FHIRDate('2013-01-01T10:50Z')
        self.assertEqual(el.as_json(), '2013-01-01T10:50Z')
        self.assertEqual(
            el.date,
            datetime(2013, 1, 1, 10, 50, tzinfo=FixedOffset())
        )
        self.assertEqual(el.format, '%Y-%m-%dT%H:%M%Z')

        el = FHIRDate('2013-01-01T10')
        self.assertEqual(el.as_json(), '2013-01-01T10')
        self.assertEqual(el.date, datetime(2013, 1, 1, 10))
        self.assertEqual(el.format, '%Y-%m-%dT%H%Z')

    def test_from_valid_str_date(self):
        el = FHIRDate('19860921')
        self.assertEqual(el.as_json(), '1986-09-21')
        self.assertEqual(el.date, date(1986, 9, 21))
        self.assertEqual(el.format, '%Y-%m-%d')

    def test_from_partial_str_date(self):
        el = FHIRDate('1986-09')
        self.assertEqual(el.as_json(), '1986-09')
        self.assertEqual(el.date, date(1986, 9, 1))
        self.assertEqual(el.format, '%Y-%m')

        el = FHIRDate('1986')
        self.assertEqual(el.as_json(), '1986')
        self.assertEqual(el.date, date(1986, 1, 1))
        self.assertEqual(el.format, '%Y')

        # Date with century
        el = FHIRDate('19')
        self.assertEqual(el.as_json(), '19')
        self.assertEqual(el.date, date(1901, 1, 1))
        self.assertEqual(el.format, '%C')

        # Date with weeks and weekdays
        el = FHIRDate('1986-W20-5')
        self.assertEqual(el.as_json(), '1986-W20-5')
        self.assertEqual(el.date, date(1986, 5, 16))
        self.assertEqual(el.format, '%Y-W%W-%w')

        el = FHIRDate('1986-W20')
        self.assertEqual(el.as_json(), '1986-W20')
        self.assertEqual(el.date, date(1986, 5, 12))
        self.assertEqual(el.format, '%Y-W%W')

        # Date with years and days
        el = FHIRDate('1986-211')
        self.assertEqual(el.as_json(), '1986-211')
        self.assertEqual(el.date, date(1986, 7, 30))
        self.assertEqual(el.format, '%Y-%j')

    def test_from_obj_date(self):
        el = FHIRDate(date(1986, 9, 21))
        self.assertEqual(el.date, date(1986, 9, 21))
        self.assertEqual(el.as_json(), '1986-09-21')
        self.assertEqual(el.format, None)

    def test_from_obj_datetime(self):
        el = FHIRDate(datetime(1986, 9, 21, 10, 15, 49))
        self.assertEqual(el.date, datetime(1986, 9, 21, 10, 15, 49))
        self.assertEqual(el.as_json(), '1986-09-21T10:15:49')
        self.assertEqual(el.format, None)

    def test_from_invalid_str_date(self):
        with self.assertLogs() as log:
            el = FHIRDate('1986-21-21')
            self.assertEqual(el.as_json(), None)
        self.assertIn(
            'Failed to initialize FHIRDate from "1986-21-21"',
            ''.join(log.output)
        )


class TestFHIRDateConstructor(TestCase):
    def test_cast(self):
        res = Resource()
        self.assertEqual(
            res._cast({'key': 'value'}, FHIRDate),
            {'key': 'value'}
        )
        res = Resource()
        self.assertEqual(
            res._cast(123, FHIRDate),
            None
        )

    def test_exceptions(self):
        with self.assertRaises(TypeError) as err:
            self.assertEqual(
                FHIRDate({'key1': 'value1'}),
                {'key1': 'value1'}
            )
        self.assertEqual(
            "Expecting string or datetime when initializing <class "
            "'fhirmodels.fhirdate.FHIRDate'>, but got <class 'dict'>",
            str(err.exception)
        )
        with self.assertRaises(TypeError) as err:
            self.assertEqual(
                FHIRDate(123),
                {'key1': 'value1'}
            )
        self.assertEqual(
            "Expecting string or datetime when initializing <class "
            "'fhirmodels.fhirdate.FHIRDate'>, but got <class 'int'>",
            str(err.exception)
        )

if __name__ == '__main__':
    main()
