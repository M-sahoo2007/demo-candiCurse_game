from django.test import TestCase


class SmokeTest(TestCase):
    def test_basic_math(self):
        """A simple test to ensure the test runner executes at least one test."""
        self.assertEqual(1 + 1, 2)
