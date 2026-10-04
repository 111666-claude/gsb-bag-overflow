import random
import unittest

from bag.core import Bag


class ReferenceBag:
    """参考实现：容量截断 + 溢出转邮件 + 幂等。"""

    def __init__(self, cap):
        self.cap = cap
        self.total = 0
        self.mail = 0
        self.settled = set()

    def add(self, req_id, count):
        if req_id in self.settled:
            return 0, 0
        self.settled.add(req_id)
        put = min(count, max(self.cap - self.total, 0))
        over = count - put
        self.total += put
        self.mail += over
        return put, over


class BagTest(unittest.TestCase):
    def test_empty_bag(self):
        self.assertEqual(Bag(2).total_count(), 0)

    def test_add_within_cap(self):
        self.assertEqual(Bag(10).add("r1", 4), (4, 0))

    def test_mail_starts_at_zero(self):
        self.assertEqual(Bag(2).mail_count(), 0)

    def test_scanned_starts_at_zero(self):
        self.assertEqual(Bag(2).scanned_count(), 0)

    def test_add_truncates_at_cap(self):
        self.assertEqual(Bag(2).add("r1", 5), (2, 3))

    def test_total_never_exceeds_cap(self):
        book = Bag(2)
        book.add("r1", 5)
        book.add("r2", 5)
        self.assertEqual(book.total_count(), 2)

    def test_overflow_goes_to_mail(self):
        book = Bag(2)
        book.add("r1", 5)
        self.assertEqual(book.mail_count(), 3)

    def test_mail_accumulates_across_requests(self):
        book = Bag(2)
        book.add("r1", 5)
        book.add("r2", 4)
        self.assertEqual(book.mail_count(), 7)

    def test_duplicate_req_id_settles_once(self):
        book = Bag(10)
        self.assertEqual(book.add("r1", 4), (4, 0))
        self.assertEqual(book.add("r1", 4), (0, 0))
        self.assertEqual(book.total_count(), 4)
        self.assertEqual(book.mail_count(), 0)

    def test_conservation_put_plus_over_equals_count(self):
        book = Bag(3)
        for req_id, count in (("a", 2), ("b", 5), ("c", 1)):
            put, over = book.add(req_id, count)
            self.assertEqual(put + over, count)
        self.assertLessEqual(book.total_count(), 3)

    def test_queries_do_not_scan_ledger(self):
        book = Bag(1000000)
        for index in range(3000):
            book.add("r-%d" % index, 1)
        for _ in range(3000):
            book.total_count()
            book.mail_count()
        self.assertLessEqual(book.scanned_count(), 3000)

    def test_replay_is_deterministic(self):
        script = [("r%d" % (i % 7), i % 5) for i in range(50)]
        first = Bag(9)
        second = Bag(9)
        for req_id, count in script:
            self.assertEqual(first.add(req_id, count), second.add(req_id, count))
        self.assertEqual(first.total_count(), second.total_count())
        self.assertEqual(first.mail_count(), second.mail_count())

    def test_randomized_differential_against_reference(self):
        rng = random.Random(20261004)
        for _ in range(200):
            cap = rng.randint(0, 20)
            actual = Bag(cap)
            reference = ReferenceBag(cap)
            for step in range(rng.randint(1, 60)):
                req_id = "req-%d" % rng.randint(0, 30)
                count = rng.randint(0, cap + 5)
                self.assertEqual(
                    actual.add(req_id, count),
                    reference.add(req_id, count),
                    "step %d cap=%d req=%s count=%d" % (step, cap, req_id, count),
                )
                self.assertEqual(actual.total_count(), reference.total)
                self.assertEqual(actual.mail_count(), reference.mail)
                self.assertLessEqual(actual.total_count(), cap)


if __name__ == "__main__":
    unittest.main()
