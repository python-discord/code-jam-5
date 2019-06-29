from unittest import TestCase


class TestAlwaysPass(TestCase):
    def test_true_is_true(self):
        self.assertTrue(True)
