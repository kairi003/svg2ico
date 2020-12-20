#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import argparse
from . import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('-o', '--output', type=Path)
    parser.add_argument('-s', '--size', type=lambda x: map(int, x.split(',')))
    args = parser.parse_args()
    src = Path(args.input)
    ico_data = svg2ico(src.read_bytes(), args.size)
    dst = Path(args.output or src.with_suffix('.ico'))
    dst.write_bytes(ico_data)


if __name__ == '__main__':
    main()
