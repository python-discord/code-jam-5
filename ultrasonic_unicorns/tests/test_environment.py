from unittest import TestCase


class TestAlwaysPass(TestCase):
    def test_true_is_true(self):
        self.assertTrue(True)

    def test_false_is_false(self):
        self.assertFalse(False)
