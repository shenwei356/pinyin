#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse
import sys
from itertools import permutations


def parse_args():
    parser = argparse.ArgumentParser(description="组合hanzi_sort_by_pinyin.py结果",
                                     epilog="https://github.com/shenwei356/pinyin")

    parser.add_argument('files', nargs='*', type=argparse.FileType('r'),
                        default=sys.stdin, help='输入文件需utf8编码，若未指定文件则为stdin')
    parser.add_argument('-l',  '--length', type=int,  default=2,
                        help='名字长度[2]')

    args = parser.parse_args()
    if args.length < 2:
        args.length = 2
    return args


if __name__ == '__main__':
    args = parse_args()

    words, pinyin, tone = set(), dict(), dict()

    for file in args.files:
        for line in file:
            p, t, w = line.strip().split()[0:3]
            words.add(w)
            pinyin[w]=p
            tone[w]=t

    for perm in permutations(words, args.length):
        out = [pinyin[w] for w in perm]
        out.extend([tone[w] for w in perm])
        out.append(''.join(perm))

        print('\t'.join(out))