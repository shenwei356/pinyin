#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse
import sys
import re
import os
from collections import Counter
from pypinyin import lazy_pinyin, TONE2


def parse_args():
    parser = argparse.ArgumentParser(description="按汉语拼音和声调排序汉字",
                                     epilog="https://github.com/shenwei356")

    parser.add_argument('files', nargs='*', type=argparse.FileType('r'),
                        default=sys.stdin, help='输入文件需utf8编码，若未指定文件则为stdin')

    args = parser.parse_args()
    return args


def gen_tone2_split():
    re1 = re.compile('[a-z]+')
    re2 = re.compile('\d+')

    def tone2_split(pinyin):
        return re2.sub('', pinyin), re1.sub('', pinyin)

    return tone2_split


if __name__ == '__main__':
    args = parse_args()
    tone2_split = gen_tone2_split()
    
    words = dict()
    counter = Counter()
    for file in args.files:
        for line in file:
            for w in line.strip():
                pinyin = lazy_pinyin(w, style=TONE2, errors='ignore')
                if len(pinyin) == 0:
                    continue
                counter[w] += 1
                p, t = tone2_split(pinyin[0])
                words[w] = [pinyin[0], p, t]
                    
    keys = sorted(words.keys(), key=lambda k: (words[k][1], words[k][2], k))
    if len(keys) > 0:
        print('\t'.join(['pinyin', 'tone', 'word', 'count']))
        for word in keys:
            pinyin, p, t = words[word]
            print('\t'.join([p, t, word, str(counter[word])]))
