import random
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

    def test_cap_truncates_overflow(self):
        self.assertEqual(Bag(2).add("r1", 5), (2, 3))

    def test_overflow_goes_to_mail(self):
        book = Bag(2)
        book.add("r1", 5)
        book.add("r2", 4)
        self.assertEqual(book.mail_count(), 7)
        self.assertEqual(book.total_count(), 2)

    def test_duplicate_req_id_settles_once(self):
        book = Bag(10)
        self.assertEqual(book.add("r1", 4), (4, 0))
        self.assertEqual(book.add("r1", 4), (0, 0))
        self.assertEqual(book.total_count(), 4)
        self.assertEqual(book.mail_count(), 0)

    def test_conservation_and_invariants(self):
        book = Bag(3)
        stream = [("a", 2), ("b", 5), ("b", 5), ("c", 1)]
        for index, (req_id, count) in enumerate(stream):
            put, over = book.add(req_id, count)
            if index == 2:
                self.assertEqual((put, over), (0, 0))
            else:
                self.assertEqual(put + over, count)
            self.assertLessEqual(book.total_count(), 3)
        self.assertEqual(book.total_count(), 3)
        self.assertEqual(book.mail_count(), 5)

    def test_queries_do_not_scan(self):
        book = Bag(1000000)
        for index in range(3000):
            book.add("r-%d" % index, 1)
        for _ in range(3000):
            book.total_count()
            book.mail_count()
        self.assertLessEqual(book.scanned_count(), 3000)

    def test_against_reference_random_200(self):
        rng = random.Random(20261004)
        for _ in range(200):
            cap = rng.randint(0, 8)
            book = Bag(cap)
            ref_total = 0
            ref_mail = 0
            seen = set()
            ids = ["req-%d" % i for i in range(rng.randint(1, 6))]
            for _ in range(rng.randint(1, 40)):
                req_id = rng.choice(ids)
                count = rng.randint(0, 12)
                put, over = book.add(req_id, count)
                if req_id in seen:
                    exp_put, exp_over = 0, 0
                else:
                    seen.add(req_id)
                    exp_put = min(count, cap - ref_total)
                    exp_over = count - exp_put
                    ref_total += exp_put
                    ref_mail += exp_over
                self.assertEqual((put, over), (exp_put, exp_over))
                self.assertEqual(put + over, exp_put + exp_over)
                self.assertEqual(book.total_count(), ref_total)
                self.assertEqual(book.mail_count(), ref_mail)
                self.assertLessEqual(book.total_count(), cap)


if __name__ == "__main__":
    unittest.main()
