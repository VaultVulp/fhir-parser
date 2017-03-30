#!/usr/bin/env python

from unittest import TestCase, main

from datetime import date, datetime

from Python.fhirdate import FHIRDate


class CastDateTestCase(TestCase):
    def test_from_valid_str_datetime(self):
        el = FHIRDate('1986-09-21T021234')
        self.assertEqual(el.as_json(), '1986-09-21T021234')

        el = FHIRDate('19860921T02:12:34')
        self.assertEqual(el.date, datetime(1986, 9, 21, 2, 12, 34))

    def test_from_valid_str_date(self):
        el = FHIRDate('19860921')
        self.assertEqual(el.as_json(), '19860921')

        el = FHIRDate('1986-09-21')
        self.assertEqual(el.date, date(1986, 9, 21))

    def test_from_pratial_str_date(self):
        el = FHIRDate('1986-09')
        self.assertEqual(el.as_json(), '1986-09')

        el = FHIRDate('1986-09')
        self.assertEqual(el.date, date(1986, 9, 1))

    def test_from_obj_date(self):
        el = FHIRDate(date(1986, 9, 21))
        self.assertEqual(el.date, date(1986, 9, 21))

    def test_from_obj_date_to_str(self):
        el = FHIRDate(date(1986, 9, 21))
        self.assertEqual(el.as_json(), '1986-09-21')

    def test_from_not_valid_str_date(self):
        el = FHIRDate('1986-21-21')
        self.assertEqual(el.as_json(), '1986-21-21')

if __name__ == '__main__':
    main()
