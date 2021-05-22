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
""" Module for the Xargon Font generator utility, for converting the
Xargon font to BDF.
"""
from xargongraphics import createpath, imagefile
import sys, os
from PIL import Image

class xargonfont(object):
    """ Class for collecting the Xargon font data and then converting
    to BDF format.
    """

    @staticmethod
    def conv1bit(inimage):
        """ Converts a given Xargon font image into a 1-bit image. """
        outimage = Image.new('1', inimage.size )
        imgdata = list(inimage.getdata())
        for index, pixel in enumerate(imgdata):
            imgdata[index] = 0 if pixel==3 else 1
        outimage.putdata(imgdata)
        return outimage

    def __init__(self, graphics, recnum, fontname):
        """ Initializes the font generator with the following parameters:
        graphics -- the Xargon graphics file
        recnum -- the record number corresponding to this font
        fontname -- the name to use when saving this font
        """
        self.size = graphics.records[recnum].images[0].size
        self.characters = [self.conv1bit(image) for image in graphics.records[recnum].origimages]
        self.name = fontname

    def debugimages(self, outfolder):
        """ Legacy function to write the font images as 1-bit images
        instead of a font.
        """
        createpath(outfolder)
        for glyphnum, glyph in enumerate(self.characters):
            if glyphnum >= 32:
                glyph.save(os.path.join(outfolder, '{:02}.png'.format(glyphnum)) )

    def createbdf(self, outname):
        """ Creates and saves a BDF file with the font information in
        this file to the provided output filename.
        """

        # Write the BDF header
        with open(outname, 'w') as outfile:
            outfile.write("""STARTFONT 2.1
FONT -{0}-medium-r-normal--{1[0]}-160-75-75-c-80-us-ascii
SIZE {1[0]} 75 75
FONTBOUNDINGBOX {1[0]} {1[1]} 0 0
STARTPROPERTIES 2
FONT_ASCENT {1[1]}
FONT_DESCENT 0
ENDPROPERTIES
CHARS {2}\n""".format(self.name, self.size, 95))

            # Write out the BDF encoding of each character
            for charnum, char in enumerate(self.characters):
                if charnum >= 32 and charnum < 127:
                    outfile.write("""STARTCHAR U+{0:04X}
ENCODING {0}
SWIDTH 0 0
DWIDTH {1[0]} 0
BBX {1[0]} {1[1]} 0 0
BITMAP\n""".format(charnum, self.size))
                    for y in range(self.size[1]):
                        value = 0
                        for x in range(self.size[0]):
                            value = value + (char.getpixel((x,y)) << 7-x)
                        # Note: this will break if font width is > 8 bits!
                        outfile.write("{:02X}\n".format(value))
                    outfile.write("ENDCHAR\n")
            outfile.write("ENDFONT\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Usage: python xargongraphics.py [Graphics File]

Generates BDF fotn files for the two identified fonts stored in the
Xargon GRAPHICS file. The BDF files can then be converted to .pil files
for use in the main mapper via the pilfont.py script. The BDF files can
also be used in any software that supports BDF.
""")
    else:
        for filename in sys.argv[1:]:
            graphics = imagefile(filename)
            font1 = xargonfont(graphics, 1, 'xargon-font1')
            font2 = xargonfont(graphics, 2, 'xargon-font1')
            #font1.debugimages('font1')
            #font2.debugimages('font2')
            font1.createbdf('font1.bdf')
            font2.createbdf('font2.bdf')
