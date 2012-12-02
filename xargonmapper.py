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
import sys, pdb, os
from PIL import Image
from xargonmap import xargonmap
from xargongraphics import imagefile, createpath
from xargontiles import tilefile
from spritedb import spritedb

class xargonmapper(object):

    def __init__(self, graphics, tiledata, mapdata):
        self.name = mapdata.name
        self.epnum = mapdata.epnum

        if self.epnum == 2:
            # Episode 2
            if self.name.upper() in ['BOARD_01']:
                graphics.changepalette(8)
            elif self.name.upper() in ['BOARD_03']:
                graphics.changepalette(9)
            else:
                graphics.changepalette(6)
        elif self.epnum == 3:
            # Episode 3
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

    def save(self):
        epfolder = 'Episode{}'.format(self.epnum)
        createpath(epfolder)
        self.mappicture.save(os.path.join(epfolder, self.name + '.png'))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print """Usage: python xargonmapper.py [Graphics File] [Tiles File] [Map File(s)...]
TODO
"""
    else:
        xargonimages = imagefile(sys.argv[1])

        tiledata = tilefile(sys.argv[2])
        for filename in sys.argv[3:]:
            themap = xargonmap(filename)

            print "Generating Map '{}'".format(themap.name)
            mapper = xargonmapper(xargonimages, tiledata, themap)
            print "Saving Map '{}'".format(themap.name)
            mapper.save()
