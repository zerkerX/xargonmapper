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
""" Module to interpret the Xargon graphics archive format. """

import struct, sys, os, csv
from PIL import Image, ImageFont, ImageDraw, ImageChops

def createpath(pathname):
    """ Simple utility method for creating a path only if it does
    not already exist.
    """
    if not os.path.exists(pathname):
        os.mkdir(pathname)

class imagefile(object):
    """ Represents the Xargon GRAPHICS file, which contains all the images
    used by Xargon.
    """
    debugfont = ImageFont.load("font1.pil")

    @staticmethod
    def debugimage(index, subindex, width, height):
        """ Creates a debug image for sprites

        index -- the sprite index to identify with (main number)
        subindex -- the sprite subindex to identify with (second number)
        width -- the nominal width of this debug sprite
        height -- the nominal height of this debug sprite
        """
        # Provide sufficient space to display text
        imgwidth = max(width, 48)
        imgheight = max(height, 16)
        tempimage = Image.new("RGBA", (imgwidth, imgheight))
        pen = ImageDraw.Draw(tempimage)
        if width > 0 and height > 0:
            pen.rectangle(((0, 0), (width, height)), fill=(64, 64, 64, 128))
        pen.text((imgwidth/2 - 22, imgheight/2 - 6), '{}:{}'.format(index,subindex),
            font=imagefile.debugfont, fill=(255,255,255))
        return tempimage

    def __init__(self, filename):
        """ Loads the specified GRAPHICS file and decodes all images
        in the file,
        """

        filesize = os.path.getsize(filename)
        graphicsfile = open(filename, 'rb')

        self.epnum = int(filename[-1])

        header = '<128L'
        headerdata = struct.unpack(header,
            graphicsfile.read(struct.calcsize(header)) )
        header2 = '<128H'
        headerdata2 = struct.unpack(header2,
            graphicsfile.read(struct.calcsize(header2)) )

        # Create the image records using list comprehension
        self.records = [imagerecord(graphicsfile, offset, size)
            for (offset, size) in zip(headerdata, headerdata2)]

        # Load all image palettes from screenshots.
        self.palette = {}
        for i in range(21):
            palimage = Image.open('palimage{}.png'.format(i) )
            self.palette[i] = palimage.getpalette()

        # Alternate palettes from the game data. Not properly decoded:
        self.palette[-1] = self.records[5].getpalette()
        self.palette[-2] = self.records[53].getpalette()

        # Select the default palette according to episode for the
        # image extraction method of operation.
        if self.epnum == 2:
            self.activepal = 6
        elif self.epnum == 3:
            self.activepal = 7
        else:
            self.activepal = 0

        # Load the image data
        for recnum, record in enumerate(self.records):
            if recnum == 53:
                record.loadimages(self.palette[3], skipimages=1)
            elif recnum == 5:
                record.loadimages(self.palette[self.activepal], skipimages=1)
            else:
                record.loadimages(self.palette[self.activepal])

    def debug_csv(self, filename):
        """ Writes a debug CSV containing info on the records in this file."""
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for recnum, record in enumerate(self.records):
                writer.writerow([recnum, record.offset, record.size] + list(record.header))

    def save(self, outpath, masked=True):
        """ Saves all the images in this file to the specified path

        outpath -- the location to save the this file's images
        masked -- if set, the masked versions of the files are saved (RGBA
                  with appropriate transparency. If cleared, the original
                  256 colour indexed image is saved.
        """
        createpath(outpath)
        for recnum, record in enumerate(self.records):
            record.save(outpath, recnum, masked)

    def changepalette(self, palnum):
        """ Changes the palette used by this graphics object to
        the specified pre-loaded palette number. Updates all masked
        images accordingly.
        """
        if self.activepal != palnum:
            self.activepal = palnum
            for record in self.records:
                record.changepalette(self.palette[self.activepal])

    def getcolour(self, index):
        """ Obtains the requested palette colour index from the currently
        active palette.
        """
        return tuple(self.palette[self.activepal][index*3:index*3+3])

    def compositeimage(self, dimensions, imgrequests):
        """ Creates a combined image based on a set of individual images
        inside this graphics record:

        dimensions -- a tuple containing the x,y dimensions of the
                      resulting combined image.
        imgrequests -- a list of 4-tuples, one for each image to add
                       to the composite. The tuple contains, in order:
                       x offset, y offset, record number, image number
        """
        tempimage = Image.new("RGBA", dimensions)
        for (x, y, recnum, imgnum) in imgrequests:
            pasteimage = self.records[recnum].images[imgnum]
            tempimage.paste(pasteimage, (x, y), pasteimage)
        return tempimage

    @staticmethod
    def semitransparent(inimage, alpha):
        """ Creates a semi-transparent version of the given image
        with the specified alpha value, where 0 is transparent and 255
        is opaque.
        """
        alphaimage = Image.new("RGBA", inimage.size, (255, 255, 255, alpha))
        return ImageChops.multiply(inimage, alphaimage)

class imagerecord(object):
    """ A record of images inside the graphics file. """

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
        """ Loads the header information for this record, and all images
        described therein.

        filedata -- an open file object to the graphics file.
        offset -- the offset (in bytes) into the file for this record
        size -- the size of this record (in bytes)
        """
        self.offset = offset
        self.size = size

        self.images = []
        self.origimages = []
        # Store the file handle for future use
        self.filedata = filedata

        if offset > 0:
            # Non-zero offsets have content to be loaded
            filedata.seek(offset)
            headerstruct = '<B4H3B'
            self.header = struct.unpack(headerstruct,
                filedata.read(struct.calcsize(headerstruct)) )

            self.numimages = self.header[0] + 1

        else:
            # Zero offset records should be skipped.
            self.numimages = 0
            self.header = []

    def loadimages(self, palette, skipimages=0):
        """ Loads all the images inside this record.

        palette -- the palette to use for loading the images
        skipimages -- if > 0, this skips the specified number of images
        """
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
                    self.origimages.append(tile)
                    self.images.append(self.maskimage(tile))

            # Check to see if we actually loaded all data from this record
            leftover = self.offset + self.size - self.filedata.tell()
            if leftover > 0:
                print("Record at offset {} has {} bytes unaccounted for.".format(self.offset, leftover))
            elif leftover < 0:
                print("Record at offset {} read {} bytes beyond its boundary.".format(self.offset, -leftover))

    def changepalette(self, palette):
        """ Changes the palette used by this record object to
        the specified palette. Updates all masked
        images accordingly.
        """
        for imagepos, image in enumerate(self.origimages):
            image.putpalette(palette)
            self.images[imagepos] = self.maskimage(image)

    def getpalette(self):
        """ Loads the first image in this record as a palette. Does
        not appear to fully decode the palette properly yet.
        """
        self.filedata.seek(self.offset + 12)
        (width, height, unknown) = struct.unpack('<3B',
            self.filedata.read(3))
        if width*height != 768:
            raise Exception('This image is not a palette!')
        else:
            return self.filedata.read(width*height)

    def save(self, outpath, recnum, masked=True):
        """ Saves all images in this record to the specified path.

        outpath -- the location to save the this file's images
        recnum -- this record's number. Used for naming the output file.
        masked -- if set, the masked versions of the files are saved (RGBA
                  with appropriate transparency. If cleared, the original
                  256 colour indexed image is saved.
        """
        if self.numimages > 0:
            createpath(outpath)
            if (masked):
                for tilenum, tile in enumerate(self.images):
                    tile.save(os.path.join(outpath, '{:02}-{:04}.png'.format(recnum, tilenum)) )
            else:
                for tilenum, tile in enumerate(self.origimages):
                    tile.save(os.path.join(outpath, '{:02}-{:04}.png'.format(recnum, tilenum)) )



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Usage: python xargongraphics.py [Graphics File]

Extracts all graphics resources from the specified GRAPHICS file from
Xargon. Output is stored in the Episode#Images and
Episode#OriginalImages folders, where # is the episode number of the
input file. The OriginalImages folder contains the original 256-colour
images without any additional processing, while the Images folder
contains 32-bit RGBA images after colour index 0 has been set
transparent.
""")
    else:
        for filename in sys.argv[1:]:
            xargonimages = imagefile(filename)
            xargonimages.debug_csv('debug.csv')
            xargonimages.save('Episode{}Images'.format(xargonimages.epnum))
            xargonimages.save('Episode{}OriginalImages'.format(xargonimages.epnum), masked=False)
