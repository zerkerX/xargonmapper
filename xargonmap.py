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
import struct, sys, os, csv, pdb
from PIL import Image, ImageOps

class xargonmap(object):
    def __init__(self, filename):
        # Grab the map from the file name (sans ext)
        (temppath, tempfname) = os.path.split(filename)
        (self.name, tempext) = os.path.splitext(tempfname)

        # Load the map data as a 64*128 array of 16 bit values:
        mapfile = open(filename, 'rb')
        pattern = '<{}H'.format(64*128)

        self.tiles = struct.unpack(pattern,
            mapfile.read(struct.calcsize(pattern)) )

        # Decode the object header then the object list
        objrecord = '<B12h2B2H'

        (numobjs,) = struct.unpack('<H', mapfile.read(2) )

        self.objs = [struct.unpack(objrecord,
            mapfile.read(struct.calcsize(objrecord)) )
            for i in range(numobjs)]

        # There always appears to be a 0x61 byte unknown region between
        # the records and strings. Let's just collect it as bytes for now.
        unknownregion = '<97B'
        self.unknown = struct.unpack(unknownregion,
            mapfile.read(struct.calcsize(unknownregion)) )

        # Capture any strings until the end of the file
        self.strings = []
        sizebytes = mapfile.read(2)
        while (len(sizebytes) == 2):
            (stringlen,) = struct.unpack('<H', sizebytes)
            self.strings.append(mapfile.read(stringlen))
            mapfile.read(1)
            sizebytes = mapfile.read(2)

        mapfile.close()


    def debugcsv(self):
        # Remember that the map is height-first. We need to convert to
        # width-first. This only outputs tile data for now.
        with open(self.name + '.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for y in range(64):
                writer.writerow([self.tiles[x*64+y] for x in range(128)])

        # Next, output the object list:
        with open(self.name + '_objs.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.objs)

        # Finally, the header and strings list:
        with open(self.name + '_info.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(list(self.unknown) + self.strings)

    def debugimage(self):
        # Turn the map data into a list of 3-byte tuples to visualize it.
        # Start by pre-creating an empty list of zeroes then copy it in
        visualdata = [None] * (64*128)
        for index in range(64*128):
            visualdata[index] = (self.tiles[index]%256, self.tiles[index]/256, 0)

        # Tell PIL to interpret the map data as a RAW image:
        mapimage = Image.new("RGB", (64, 128) )
        mapimage.putdata(visualdata)
        ImageOps.mirror(mapimage.rotate(-90)).save(self.name + '_flat.png')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print """Usage: python xargonmap.py [Map File(s)]
TODO
"""
    else:
        for filename in sys.argv[1:]:
            themap = xargonmap(filename)
            themap.debugcsv()
            themap.debugimage()
