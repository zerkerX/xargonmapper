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

# Lookup is keyed by sprite ID and contains a tuple of record number
# and sprite number inside the record
class spritedb(object):
    def __init__(self, graphics):
        self.sprites = [{}, {}]
        self.mapsprites = {}

        # Simple sprite mapping. Stage sprites, then Map sprites
        for (spriteid, recnum, imagenum) in [(0, 6, 9), (25, 35, 2),
                (33, 37, 5), (51, 36, 33)]:
            self.sprites[0][spriteid] = graphics.records[recnum].images[imagenum]
        for (spriteid, recnum, imagenum) in [(5, 47, 8), (72, 55, 6), (33, 37, 13)]:
            self.sprites[1][spriteid] = graphics.records[recnum].images[imagenum]

        # Empty sprites:
        # For future reference, possible meanings are:
        # 17: Respawn point
        # 63: Start??
        for spriteid in [17, 63]:
            self.sprites[0][spriteid] = graphics.debugimage(spriteid, 0, 0)
        for spriteid in [19]:
            self.sprites[1][spriteid] = graphics.debugimage(spriteid, 0, 0)

        # Cache a reference to the graphics object for future use
        self.graphics = graphics

    def drawsprite(self, mappicture, spriterecord, group=0):
        (spriteid, x, y) = spriterecord[0:3]
        (width, height) = spriterecord[5:7]

        if spriteid not in self.sprites[group]:
            self.sprites[group][spriteid] = self.graphics.debugimage(spriteid, width, height)

        # When pasting masked images, need to specify the mask for the paste.
        # RGBA images can be used as their own masks.
        mappicture.paste(self.sprites[group][spriteid], (x, y), self.sprites[group][spriteid])

