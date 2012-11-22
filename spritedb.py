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
    def addsprite(self, sprtype, subtype, sprite):
        if sprtype not in self.sprites:
            self.sprites[sprtype] = {}
        self.sprites[sprtype][subtype] = sprite

    def __init__(self, graphics):
        self.sprites = {}
        self.mapsprites = {}

        # Manually-defined sprites (i.e. special handling needed
        self.addsprite(0, 4, sprite(graphics.records[6].images[9], yoffs=-8))

        # Simple sprite mapping. Stage sprites, then Map sprites
        for (sprtype, subtype, recnum, imagenum) in [(5, 0, 47, 8), # Map Player
                (25, 0, 35, 2), # Monsters
                (21, 0, 37, 33), # Health Pickup
                (22, 0, 30, 28), # Emerald
                (26, 2, 37, 27), # Treasure (Cherry)
                (26, 13, 37, 27), # Treasure (Empty)
                (26, 0, 37, 27), # Treasure (Health)
                (28, 4, 30, 17), # Powerups
                (51, 0, 36, 33), # Clouds
                (59, 0, 36, 28), # Spikes
                (72, 9, 55, 5), (72, 10, 55, 6), # Foliage
                (72, 4, 36, 35), (72, 11, 36, 36), # Exit Sign
                (88, -1, 47, 16), (88, 2, 47, 20), (88, 3, 47, 21) # Map images
                ]:
            self.addsprite(sprtype, subtype, sprite(graphics.records[recnum].images[imagenum]))

        # Pickups appear to be in the same order as their corresponding record:
        for subtype in range(24):
            self.addsprite(33, subtype, sprite(graphics.records[37].images[subtype]))

        # Empty sprites:
        # For future reference, possible meanings are:
        # 17-# (and other numbers): Respawn point
        for sprtype in [17]:
            for subtype in range(11):
                self.addsprite(sprtype, subtype, sprite(graphics.debugimage(sprtype, subtype, 0, 0)))

        # 63-3: Start??
        # 61:0, 62:0: Doorway
        # 12: Treasure Drop Trigger?
        # 71-0: Sign? 71-1 Popup message?
        for sprtype, subtype in [(63,3), (61,0), (62,0), (19,0), (12,0), (71,0), (71,1)]:
            self.addsprite(sprtype, subtype, sprite(graphics.debugimage(sprtype, subtype, 0, 0)))

        # Cache a reference to the graphics object for future use
        self.graphics = graphics

    def drawsprite(self, mappicture, objrec):
        if objrec.sprtype not in self.sprites or \
                objrec.subtype not in self.sprites[objrec.sprtype]:
            self.addsprite(objrec.sprtype, objrec.subtype, sprite(
                self.graphics.debugimage(objrec.sprtype, objrec.subtype,
                objrec.width, objrec.height)))

        self.sprites[objrec.sprtype][objrec.subtype].draw(mappicture, objrec)

class sprite(object):
    def __init__(self, image, xoffs=0, yoffs=0):
        self.image = image
        self.xoffs = xoffs
        self.yoffs = yoffs

    def draw(self, mappicture, objrec):
        # When pasting masked images, need to specify the mask for the paste.
        # RGBA images can be used as their own masks.
        mappicture.paste(self.image, (objrec.x +self.xoffs,
            objrec.y +self.yoffs), self.image)
