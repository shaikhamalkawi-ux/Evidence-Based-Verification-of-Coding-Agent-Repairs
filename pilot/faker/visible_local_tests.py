"""Visible issue-derived tests for Faker frozen benchmark source.

These tests use ONLY the natural-language task description and public APIs.
They are not the benchmark's withheld test_patch or FAIL_TO_PASS/PASS_TO_PASS.
"""
import unittest
from datetime import datetime, timedelta, timezone
from faker import Faker


class VisibleFakerRelativeTimeTests(unittest.TestCase):
    def setUp(self):
        self.fake = Faker("en_US")
        self.fake.seed_instance(20261117)

    def test_relative_end_without_start_has_nonnegative_unix_timestamp(self):
        self.assertGreaterEqual(self.fake.unix_time(end_datetime="-1w"), 0)

    def test_relative_end_without_start_is_bounded_by_now(self):
        before=datetime.now(timezone.utc)
        value=self.fake.unix_time(end_datetime="-1w")
        after=datetime.now(timezone.utc)
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, (after-timedelta(days=6)).timestamp())
        self.assertGreater(value, -604800)

    def test_date_time_with_timezone_and_negative_one_week(self):
        dt=self.fake.date_time(tzinfo=timezone.utc,end_datetime="-1w")
        self.assertGreaterEqual(dt, datetime(1970,1,1,tzinfo=timezone.utc))
        self.assertLess(dt, datetime.now(timezone.utc)-timedelta(days=6))

    def test_relative_now_end_without_start(self):
        value=self.fake.unix_time(end_datetime="now")
        self.assertGreaterEqual(value,0)
        self.assertLessEqual(value,datetime.now(timezone.utc).timestamp()+3)

    def test_absolute_unix_end_remains_supported(self):
        value=self.fake.unix_time(end_datetime=1700000000)
        self.assertGreaterEqual(value,0)
        self.assertLessEqual(value,1700000000)

    def test_both_relative_bounds_are_current_time_referenced(self):
        lo=datetime.now(timezone.utc)-timedelta(days=22)
        hi=datetime.now(timezone.utc)-timedelta(days=6)
        value=self.fake.unix_time(start_datetime="-3w",end_datetime="-1w")
        self.assertGreater(value,lo.timestamp())
        self.assertLess(value,hi.timestamp())

    def test_epoch_endpoint_without_start(self):
        self.assertEqual(self.fake.unix_time(end_datetime=0),0)

    def test_default_endpoint_is_valid_timestamp(self):
        value=self.fake.unix_time()
        self.assertGreater(value,0)
        self.assertLessEqual(value,datetime.now(timezone.utc).timestamp()+3)


if __name__=="__main__":
    unittest.main()
