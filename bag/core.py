"""背包溢出：按容量上限放入物品，放不下的部分转成溢出邮件。"""


class Bag:
    """背包与溢出邮件台账。"""

    def __init__(self, cap):
        self.cap = cap
        self.total = 0
        self.mail = 0
        self._settled = set()
        self.scanned = 0

    def add(self, req_id, count):
        """放入物品，返回 (放入数, 溢出数)。

        容量截断：背包内件数不超过 cap，放不下的部分作为溢出数返回；
        溢出转邮件：溢出件数累进溢出邮件；
        幂等：同一个 req_id 只结算一次，重复调用返回 (0, 0)。
        """
        if req_id in self._settled:
            return 0, 0
        self._settled.add(req_id)
        room = self.cap - self.total
        put = count if count <= room else room
        if put < 0:
            put = 0
        over = count - put
        self.total += put
        self.mail += over
        return put, over

    def mail_count(self):
        """溢出邮件件数，O(1) 读缓存值，不全扫台账。"""
        return self.mail

    def total_count(self):
        """背包内件数，O(1) 读缓存值，不全扫台账。"""
        return self.total

    def scanned_count(self):
        return self.scanned
