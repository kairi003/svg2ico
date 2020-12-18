#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import argparse
from . import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('-o', '--output', type=Path)
    def tp(x): return list(map(int, x.split(',')))
    parser.add_argument('-s', '--size', type=tp)
    args = parser.parse_args()
    svg2ico(args.input, args.output, args.size)


if __name__ == '__main__':
    main()
