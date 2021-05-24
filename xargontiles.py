#!/usr/bin/python3
# Copyright 2012, 2021 Ryan Armstrong
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
""" Module for handling Xargon TILES files """

import struct, sys, os, csv

class tilefile(object):
    """ A Xargon TILES file, which contains the mapping between the tile
    index found in a map, and the record and field number in the
    GRAPHICS file corresponding to that tile.
    """
    def __init__(self, filename):
        """ Loads the given TILES file. """
        filesize = os.path.getsize(filename)
        infile = open(filename, 'rb')

        self.tiles = []
        self.lookup = {}

        # A Tiles file is just a series of lookup records. The field
        # order is:
        # int16 Tile number
        # int16 Record number
        # int16 Unknown flag
        # int8  String length
        # char* Tile name
        commonheader = '<3HB'
        while infile.tell() < filesize:
            headerdata = struct.unpack(commonheader,
                infile.read(struct.calcsize(commonheader)) )
            stringlen = headerdata[3]
            stringdata = struct.unpack('<{}s'.format(stringlen), 
                infile.read(stringlen))
            stringdata = (stringdata[0].decode(), )
            
            self.tiles.append(headerdata[0:3] + stringdata)

            self.lookup[headerdata[0]] = headerdata[1]

    def gettile(self, graphics, tilenum):
        """ Finds the correct tile image from the provided graphics
        object corresponding to the provided tile number.
        """
        # Most tiles numbers appear to be offset by 0xC000, for some reason.
        if tilenum < 0xC000:
            graphindex = self.lookup[tilenum]
        else:
            graphindex = self.lookup[tilenum - 0xC000]

        # The graphics record lookup is also offset by 64.
        recnum = graphindex // 256 - 64
        recindex = graphindex % 256

        return graphics.records[recnum].images[recindex]

    def debug_csv(self, filename):
        """ Writes a debug csv containing the fields in this TILES file."""
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for recnum, tiledata in enumerate(self.tiles):
                writer.writerow((recnum,) + tiledata)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Usage: python xargontiles.py [Tiles File]

Generates a debug CSV file for the mapping specified in the given
TILES file from Xargon. Output is written to tiles.csv.
""")
    else:
        for filename in sys.argv[1:]:
            xargontiles = tilefile(filename)
            xargontiles.debug_csv('tiles.csv')
