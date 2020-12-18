#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import argparse
import cairosvg

SIZE = [
    16,
    32,
    64,
    180,
    256
]


class Png:
    _MASIC = b'\x89PNG\r\n\x1a\n'

    def __init__(self, data: bytes):
        if not data.startswith(self._MASIC):
            raise TypeError('This is NOT PNG file.')
        self.__data = data

    @property
    def data(self):
        return self.__data

    @property
    def width(self):
        return int.from_bytes(self.__data[16:20], 'big')

    @property
    def height(self):
        return int.from_bytes(self.__data[16:20], 'big')

    @property
    def size(self):
        return len(self.__data)


class PngIco:
    def __init__(self):
        self.icon = []

    def append(self, png):
        self.icon.append(png)

    @property
    def num(self):
        return len(self.icon)

    @property
    def header(self):
        hdr = b'\x00\x00\x01' + self.num.to_bytes(2, 'little')
        return hdr

    @property
    def directory(self):
        dir = bytearray(16 * self.num)
        file_offset = 6 + 16 * self.num
        for i, png in enumerate(self.icon):
            h = i << 4
            dir[h+0] = 0xff & png.width
            dir[h+1] = 0xff & png.height
            dir[h+8:h+12] = png.size.to_bytes(4, 'little')
            dir[h+12:h+16] = file_offset.to_bytes(4, 'little')
            file_offset += png.size
        return dir

    def to_bytes(self):
        icon_bytes = map(lambda x: x.data, self.icon)
        return b''.join([self.header, self.directory, *icon_bytes])


def svg2ico(src_path, dst_path=None, size=None):
    src = Path(src_path)
    dst = Path(dst_path or src.with_suffix('.ico'))
    svg_data = src.read_bytes()
    ico = PngIco()
    for s in size or SIZE:
        w = h = s
        data = cairosvg.svg2png(bytestring=svg_data,
                                output_width=w, output_height=h)
        png = Png(data)
        ico.append(png)
    dst.write_bytes(ico.to_bytes())
    return


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
