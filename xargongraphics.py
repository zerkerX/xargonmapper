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

def createpath(pathname):
    """ Simple utility method for creating a path only if it does
    not already exist.
    """
    if not os.path.exists(pathname):
        os.mkdir(pathname)

class imagefile(object):
    debugfont = ImageFont.truetype("DroidSans.ttf", 12)

    @staticmethod
    def debugimage(index, width, height):
        """ Creates a debug image for sprites """
        if width > 0 and height > 0:
            colour = (index, index, index)
            tempimage = Image.new("RGBA", (width, height), colour)
            textcolor = (255, 255, 255) if index < 96 else (0, 0, 0)
            pen = ImageDraw.Draw(tempimage)
            pen.text((width/2 - 7, height/2 - 6), '{:02}'.format(index),
                font=imagefile.debugfont, fill=textcolor)
            return tempimage
        else:
            # 1 pixel transparent image
            return Image.new("RGBA", (width, height))

    def __init__(self, filename):
        filesize = os.path.getsize(filename)
        graphicsfile = open(filename, 'rb')

        header = '<128L'
        headerdata = struct.unpack(header,
            graphicsfile.read(struct.calcsize(header)) )
        header2 = '<128H'
        headerdata2 = struct.unpack(header2,
            graphicsfile.read(struct.calcsize(header2)) )

        # Create the image records using list comprehension
        self.records = [imagerecord(graphicsfile, offset, size)
            for (offset, size) in zip(headerdata, headerdata2)]

        palimage = Image.open('screeny.png')
        palette1 = palimage.getpalette()

        palettealt = self.records[5].getpalette()
        palette2 = self.records[53].getpalette()

        # Load the image data
        for recnum, record in enumerate(self.records):
            if recnum == 53:
                record.loadimages(palette2, skipimages=1)
            elif recnum == 5:
                record.loadimages(palette1, skipimages=1)
            else:
                record.loadimages(palette1)

    def debug_csv(self, filename):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for recnum, record in enumerate(self.records):
                writer.writerow([recnum, record.offset, record.size] + list(record.header))

    def save(self, outpath):
        createpath(outpath)
        for recnum, record in enumerate(self.records):
            record.save(os.path.join(outpath, '{:02}-{}'.format(recnum, record.offset)))


class imagerecord(object):

    @staticmethod
    def maskimage(inimage):
        """ Masks colour 0 in the given image, turning those pixels
        transparent. Returns the resulting RGBA image.
        """
        tempmask = Image.new('L', inimage.size, 255)
        maskdata = list(tempmask.getdata())
        outimage = inimage.convert("RGBA")

        for pos, value in enumerate(inimage.getdata()):
            if value == 0:
                maskdata[pos] = 0

        tempmask.putdata(maskdata)
        outimage.putalpha(tempmask)
        return outimage

    def __init__(self, filedata, offset, size):
        self.offset = offset
        self.size = size

        self.images = []
        # Store the file handle for future use
        self.filedata = filedata

        if offset > 0:
            filedata.seek(offset)
            headerstruct = '<B4H3B'
            self.header = struct.unpack(headerstruct,
                filedata.read(struct.calcsize(headerstruct)) )

            self.numimages = self.header[0] + 1

        else:
            self.numimages = 0
            self.header = []

    def loadimages(self, palette, skipimages=0):
        if self.offset > 0:
            self.filedata.seek(self.offset + 12)

            for tilenum in range(self.numimages):
                (width, height, unknown) = struct.unpack('<3B',
                    self.filedata.read(3))
                # Skip past this image if requested (i.e. for palettes)
                if skipimages > 0:
                    self.filedata.seek(width*height, os.SEEK_CUR)
                    skipimages = skipimages - 1
                elif width > 0 and height > 0:
                    tile = Image.fromstring("P", (width, height),
                        self.filedata.read(width*height))
                    tile.putpalette(palette)
                    self.images.append(self.maskimage(tile))

            # Check to see if we actually loaded all data from this record
            leftover = self.offset + self.size - self.filedata.tell()
            if leftover > 0:
                print "Record at offset {} has {} bytes unaccounted for.".format(self.offset, leftover)
            elif leftover < 0:
                print "Record at offset {} read {} bytes beyond its boundary.".format(self.offset, -leftover)

    def getpalette(self):
        """ Loads the first image in this record as a palette."""
        self.filedata.seek(self.offset + 12)
        (width, height, unknown) = struct.unpack('<3B',
            self.filedata.read(3))
        if width*height != 768:
            raise Exception('This image is not a palette!')
        else:
            return self.filedata.read(width*height)


    def save(self, outpath):
        if self.numimages > 0:
            createpath(outpath)
            for tilenum, tile in enumerate(self.images):
                tile.save(os.path.join(outpath, '{:04}.png'.format(tilenum)) )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print """Usage: python xargongraphics.py [Graphics File]
TODO
"""
    else:
        for filename in sys.argv[1:]:
            xargonimages = imagefile(filename)
            xargonimages.debug_csv('debug.csv')
            xargonimages.save('output')
