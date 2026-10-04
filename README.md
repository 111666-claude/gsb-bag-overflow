# bag-overflow

背包溢出：按容量上限放入物品，放不下的部分转成溢出邮件，只用 Python 标准库。

```
python3 -m bag.cli --sample cap
python3 -m bag.cli --sample overflow
python3 -m bag.cli --sample dup
python3 -m bag.cli --sample scan
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **容量上限**：背包内件数不超过 `cap`；本次放不下的部分返回为溢出数。
- **溢出转邮件**：溢出件数必须累进溢出邮件，一件都不能丢。
- **幂等**：同一个 `req_id` 只结算一次，重复调用返回 `(0, 0)`，不再占容量也不再进邮件。
- **守恒**：放入数加溢出数恒等于本次请求件数；背包内件数永远不大于 `cap`。
- **查询代价**：`total_count` 与 `mail_count` 不许全扫台账，`scanned_count()` 不随请求数乘查询次数增长。
- **规模**：200 万次请求、每秒 10 万次放入与查询，单次摊还 O(1)。

## 输出契约（不改格式）

```
put=.. over=..
mail=..
put=.. total=..
scanned=..
```

## 目录

```
bag/core.py   容量上限、溢出转邮件与幂等
bag/cli.py    命令行入口
tests/        unittest 用例
```
