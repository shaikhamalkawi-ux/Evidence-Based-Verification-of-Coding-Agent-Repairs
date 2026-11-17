"""Predeclared visible tests for python-babel__babel-1163.

These are plain-language expected behaviors authored from the public issue only,
not from the benchmark reference patch, hidden suite, or final solution.
"""
from datetime import timedelta
import unittest
from babel.dates import format_timedelta

class DirectionWidthTests(unittest.TestCase):
    def test_forward_short_three_hours(self):
        self.assertEqual(format_timedelta(timedelta(hours=3),add_direction=True,format="short",locale="en_US"),"in 3 hrs")
    def test_forward_narrow_three_hours(self):
        self.assertEqual(format_timedelta(timedelta(hours=3),add_direction=True,format="narrow",locale="en_US"),"in 3h")
    def test_forward_long_unchanged(self):
        self.assertEqual(format_timedelta(timedelta(hours=3),add_direction=True,format="long",locale="en_US"),"in 3 hours")
    def test_reverse_short(self):
        self.assertEqual(format_timedelta(timedelta(hours=-3),add_direction=True,format="short",locale="en_US"),"3 hrs ago")
    def test_reverse_narrow(self):
        self.assertEqual(format_timedelta(timedelta(hours=-3),add_direction=True,format="narrow",locale="en_US"),"3h ago")
    def test_default_short_without_direction(self):
        self.assertEqual(format_timedelta(timedelta(hours=3),add_direction=False,format="short",locale="en_US"),"3 hr")
    def test_default_narrow_without_direction(self):
        self.assertEqual(format_timedelta(timedelta(hours=3),add_direction=False,format="narrow",locale="en_US"),"3h")

if __name__=="__main__":
    unittest.main()
