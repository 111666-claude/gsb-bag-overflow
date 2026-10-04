"""背包溢出：按容量上限放入物品，放不下的部分转成溢出邮件。

缺陷：超容量照收、溢出直接丢弃、req_id 不幂等、溢出件数算错、每次查询全扫台账。
"""


class Bag:
    """背包与溢出邮件台账。"""

    def __init__(self, cap):
        self.cap = cap
        self.total = 0
        self.mail = 0
        self.records = []
        self.scanned = 0

    def add(self, req_id, count):
        """放入物品，返回 (放入数, 溢出数)。缺陷：不看容量、不幂等、溢出丢弃。"""
        self.records.append((req_id, count))
        self.total += count
        return count, 0

    def mail_count(self):
        """溢出邮件件数。缺陷：全扫台账。"""
        self.scanned += len(self.records)
        return self.mail

    def total_count(self):
        """背包内件数。缺陷：全扫台账。"""
        self.scanned += len(self.records)
        return self.total

    def scanned_count(self):
        return self.scanned
