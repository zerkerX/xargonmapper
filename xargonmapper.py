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
""" This is the Xargon Mapper script, which generates an image map of a
level in Xargon.
"""

import sys, os
from PIL import Image
from xargonmap import xargonmap, objrecord
from xargongraphics import imagefile, createpath
from xargontiles import tilefile
from spritedb import spritedb

class xargonmapper(object):
    """ The main Xargon mapper class. This will generate
    a map image for a given Xargon stage.
    """
    def __init__(self, graphics, tiledata, mapdata):
        """ Initializes and generates a map image for the provided map.

        graphics -- a xargongraphics object representing all the
                    available image records for this episode of Xargon.
        tiledata -- a xargontile objrect containing the tile to image
                    mappings for this episode of Xargon.
        mapdata -- a xargonmap object to generate an image map for.
        """

        self.name = mapdata.name
        self.epnum = mapdata.epnum

        # Select the correct colour palette.
        if self.epnum == 2:
            # Episode 2
            if self.name.upper() in ['BOARD_01', 'BOARD_08',
                    'BOARD_15', 'BOARD_32']:
                graphics.changepalette(8)
            elif self.name.upper() in ['BOARD_03']:
                graphics.changepalette(9)
            elif self.name.upper() in ['BOARD_05']:
                graphics.changepalette(10)
            elif self.name.upper() in ['BOARD_07']:
                graphics.changepalette(11)
            elif self.name.upper() in ['BOARD_10']:
                graphics.changepalette(13)
            elif self.name.upper() in ['BOARD_11']:
                graphics.changepalette(12)
            else:
                graphics.changepalette(6)
        elif self.epnum == 3:
            # Episode 3
            if self.name.upper() in ['BOARD_01']:
                graphics.changepalette(14)
            elif self.name.upper() in ['BOARD_02']:
                graphics.changepalette(15)
            elif self.name.upper() in ['BOARD_03']:
                graphics.changepalette(16)
            elif self.name.upper() in ['BOARD_07']:
                graphics.changepalette(17)
            elif self.name.upper() in ['BOARD_11']:
                graphics.changepalette(18)
            elif self.name.upper() in ['BOARD_13']:
                graphics.changepalette(19)
            elif self.name.upper() in ['BOARD_12']:
                graphics.changepalette(20)
            else:
                graphics.changepalette(7)
        else:
            # Episode 1
            if self.name.upper() in ['BOARD_01', 'BOARD_02', 'BOARD_04']:
                graphics.changepalette(0)
            elif self.name.upper() == 'DEMO3':
                graphics.changepalette(2)
            elif self.name.upper() == 'BOARD_05':
                graphics.changepalette(4)
            elif self.name.upper() in ['BOARD_08', 'BOARD_33']:
                graphics.changepalette(5)
            else:
                graphics.changepalette(1)

        self.mappicture = Image.new("RGB", (128*16, 64*16), graphics.getcolour(250) )
        sprites = spritedb(graphics, mapdata.epnum)

        self.preprocessmap(mapdata)

        for index, tileval in enumerate(mapdata.tiles):
            # Remember: maps are height first
            (x, y) = (index/64, index%64)
            tileimg = tiledata.gettile(graphics, tileval)
            self.mappicture.paste(tileimg, (x*16, y*16), tileimg )

        for objrecord in mapdata.sprites:
            sprites.drawsprite(self.mappicture, objrecord, mapdata)
        for objrecord in mapdata.text:
            sprites.drawsprite(self.mappicture, objrecord, mapdata)

    def preprocessmap(self, mapdata):
        """ Performs some minor corrections on the map in order to
        work around some incomplete interpretations, and also to
        ensure a cleaner map image.
        """
        switchlocations = []
        doorinfos = []

        # First loop: find all door info values
        for objrec in mapdata.sprites:
            if objrec.sprtype == 9:
                doorinfos.append(objrec.info)

        # Second loop: Erase switches that align with doors and move doubled up sprites.
        for objrec in mapdata.text:
            if objrec.sprtype == 12:
                while (objrec.x + objrec.y*128*16) in switchlocations:
                    objrec.y += 8
                switchlocations.append(objrec.x + objrec.y*128*16)
                if objrec.info in doorinfos:
                    objrec.info = 0

        # String adjust for STORY map:
        if mapdata.name.upper() == 'STORY' and mapdata.epnum == 1:
            page3to5 = mapdata.stringlookup[117:120]
            page6 = mapdata.stringlookup[82]
            page7 = mapdata.stringlookup[81]
            page8 = mapdata.stringlookup[84]
            page9 = mapdata.stringlookup[83]
            page10 = mapdata.stringlookup[116]

            del mapdata.stringlookup[116:120]
            del mapdata.stringlookup[81:85]

            mapdata.stringlookup[81:81] = page3to5 + [page6, page7, page8, page9, page10]

        # String adjust for Episode 2 Ending:
        if mapdata.name.upper() == 'BOARD_32' and mapdata.epnum == 2:
            blank = mapdata.stringlookup[-1]

            del mapdata.stringlookup[-1]
            mapdata.stringlookup.insert(8, blank)

        # Fake Sprite for Episode 3 Ending:
        if mapdata.name.upper() == 'BOARD_32' and mapdata.epnum == 3:
            mapdata.sprites.append(objrecord( (1000, 48, 240, 0, 0, 160, 160,
                0, 0, 0, 0, 0, 0, 0, 0) ))

    def save(self):
        """ Saves the generated map to a folder based on episode,
        and name based on the input map filename.
        """
        epfolder = 'Episode{}'.format(self.epnum)
        createpath(epfolder)
        self.mappicture.save(os.path.join(epfolder, self.name + '.png'))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("""Usage: python xargonmapper.py [Graphics File] [Tiles File] [Map File(s)...]

Generates map images for every Xargon map file indicated. Requires the
corresponding GRAPHICS file for the images to use, and the TILES file
for the map tile to graphics resource mapping. All files should be from
the same Episode of Xargon.
""")
    else:
        xargonimages = imagefile(sys.argv[1])

        tiledata = tilefile(sys.argv[2])
        for filename in sys.argv[3:]:
            themap = xargonmap(filename)

            print("Generating Map '{}'".format(themap.name))
            mapper = xargonmapper(xargonimages, tiledata, themap)
            print("Saving Map '{}'".format(themap.name))
            mapper.save()
