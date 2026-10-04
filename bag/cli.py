"""命令行入口：跑背包溢出样例。"""

import argparse

from .core import Bag


def build_parser():
    parser = argparse.ArgumentParser(prog="bag-overflow", description="背包溢出转邮件")
    parser.add_argument("--sample", default="cap", help="cap / overflow / dup / scan")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample == "cap":
        put, over = Bag(2).add("r1", 5)
        print("put=%d over=%d" % (put, over))
    elif args.sample == "overflow":
        book = Bag(2)
        book.add("r1", 5)
        print("mail=%d" % book.mail_count())
    elif args.sample == "dup":
        book = Bag(10)
        book.add("r1", 4)
        put, _ = book.add("r1", 4)
        print("put=%d total=%d" % (put, book.total_count()))
    elif args.sample == "scan":
        book = Bag(1000000)
        for index in range(3000):
            book.add("r-%d" % index, 1)
        for _ in range(3000):
            book.total_count()
        print("scanned=%d" % book.scanned_count())
    else:
        raise SystemExit("需要 --sample cap|overflow|dup|scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
