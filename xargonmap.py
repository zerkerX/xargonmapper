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
import struct, sys, os, csv
from PIL import Image, ImageOps

class xargonmap(object):
    def __init__(self, filename):
        # Grab the map from the file name (sans ext)
        # TODO: Maps may have embedded names. To consider
        (temppath, tempfname) = os.path.split(filename)
        (self.name, tempext) = os.path.splitext(tempfname)

        # Load the map data as a 98 x 98 array of 2-byte positions:
        mapfile = open(filename, 'rb')
        pattern = '<{}B'.format(64*128*2)

        tempdata = struct.unpack(pattern,
            mapfile.read(struct.calcsize(pattern)) )

        self.tiles = [tileval for index, tileval in enumerate(tempdata) if index%2 == 0]
        self.meta  = [tileval for index, tileval in enumerate(tempdata) if index%2 == 1]
        mapfile.close()

    def debugcsv(self):
        # Remember that the map is height-first. We need to convert to
        # width-first. This only outputs tile data for now.
        with open(self.name + '.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for y in range(64):
                writer.writerow([self.tiles[x*64+y] for x in range(128)])

    def debugimage(self):
        # Tell PIL to interpret the map data as a RAW image:
        mapimage1 = Image.new("L", (64, 128) )
        mapimage1.putdata(self.tiles)
        ImageOps.mirror(mapimage1.rotate(-90)).save(self.name + '_tile.png')
        mapimage1 = Image.new("L", (64, 128) )
        mapimage1.putdata(self.meta)
        ImageOps.mirror(mapimage1.rotate(-90)).save(self.name + '_meta.png')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print """Usage: python xargonmap.py [Map File]
TODO
"""
    else:
        for filename in sys.argv[1:]:
            themap = xargonmap(filename)
            themap.debugcsv()
            themap.debugimage()
