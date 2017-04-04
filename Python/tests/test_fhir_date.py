#!/usr/bin/env python

from unittest import TestCase, main
from datetime import date, datetime

from isodate import FixedOffset

from ..resource import Resource
from ..fhirdate import FHIRDate


class CastDateTestCase(TestCase):
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
            datetime(2013, 1, 1, 10, 50,tzinfo=FixedOffset())
        )

    def test_from_valid_str_date(self):
        el = FHIRDate('19860921')
        self.assertEqual(el.as_json(), '1986-09-21')
        self.assertEqual(el.date, date(1986, 9, 21))

    def test_from_partial_str_date(self):
        el = FHIRDate('1986-09')
        self.assertEqual(el.as_json(), '1986-09')
        self.assertEqual(el.date, date(1986, 9, 1))
        self.assertEqual(el.format, '%Y-%m')

        el = FHIRDate('1986')
        self.assertEqual(el.as_json(), '1986')
        self.assertEqual(el.date, date(1986, 1, 1))
        self.assertEqual(el.format, '%Y')

    def test_from_obj_date(self):
        el = FHIRDate(date(1986, 9, 21))
        self.assertEqual(el.date, date(1986, 9, 21))

    def test_from_obj_date_to_str(self):
        el = FHIRDate(date(1986, 9, 21))
        self.assertEqual(el.as_json(), '1986-09-21')

    def test_from_invalid_str_date(self):
        el = FHIRDate('1986-21-21')
        self.assertEqual(el.as_json(), None)


class CastFromDict(TestCase):
    def setUp(self):
        self.res = Resource()

    def test_from_dict(self):
        self.assertEqual(
            self.res._cast({'key': 'value'}, FHIRDate),
            {'key': 'value'}
        )

if __name__ == '__main__':
    main()
