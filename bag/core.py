"""背包溢出：按容量上限放入物品，放不下的部分转成溢出邮件。

容量上限、溢出转邮件、req_id 幂等，查询摊还 O(1)，只用标准库。
"""


class Bag:
    """背包与溢出邮件台账。"""

    def __init__(self, cap):
        self.cap = cap
        self.total = 0
        self.mail = 0
        self.seen = set()
        self.scanned = 0

    def add(self, req_id, count):
        """放入物品，返回 (放入数, 溢出数)。

        同一个 req_id 只结算一次；超出容量的部分累进溢出邮件。
        """
        if req_id in self.seen:
            return 0, 0
        self.seen.add(req_id)
        room = self.cap - self.total
        put = count if count < room else room
        if put < 0:
            put = 0
        over = count - put
        self.total += put
        self.mail += over
        return put, over

    def mail_count(self):
        """溢出邮件件数，O(1) 直读计数。"""
        return self.mail

    def total_count(self):
        """背包内件数，O(1) 直读计数。"""
        return self.total

    def scanned_count(self):
        return self.scanned
