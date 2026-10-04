import unittest

from bag.core import Bag


class BagTest(unittest.TestCase):
    def test_empty_bag(self):
        self.assertEqual(Bag(2).total_count(), 0)

    def test_add_within_cap(self):
        self.assertEqual(Bag(10).add("r1", 4), (4, 0))

    def test_mail_starts_at_zero(self):
        self.assertEqual(Bag(2).mail_count(), 0)

    def test_scanned_starts_at_zero(self):
        self.assertEqual(Bag(2).scanned_count(), 0)


if __name__ == "__main__":
    unittest.main()
