#!/usr/bin/python
# Copyright 2012 Ryan Armstrong
#
# This file is part of Xargon Mapper Mapper.
#
# Xargon Mapper Mapper is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Xargon Mapper Mapper is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Xargon Mapper Mapper.
# If not, see <http://www.gnu.org/licenses/>.
import struct, sys, os, pdb, csv
from PIL import Image, ImageFont, ImageDraw

class tilefile(object):
    debugfont = ImageFont.truetype("DroidSans.ttf", 8)

    def __init__(self, filename):
        filesize = os.path.getsize(filename)
        infile = open(filename, 'rb')

        self.tiles = []

        commonheader = '<3HB'
        while infile.tell() < filesize:
            headerdata = struct.unpack(commonheader,
                infile.read(struct.calcsize(commonheader)) )
            stringlen = headerdata[3]
            print headerdata
            self.tiles.append(headerdata[0:3] +
                struct.unpack('<{}s'.format(stringlen), infile.read(stringlen)) )

    def debug_csv(self, filename):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for recnum, tiledata in enumerate(self.tiles):
                writer.writerow((recnum,) + tiledata)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print """Usage: python xargontiles.py [Tiles File]
TODO
"""
    else:
        for filename in sys.argv[1:]:
            xargontiles = tilefile(filename)
            xargontiles.debug_csv('tiles.csv')
