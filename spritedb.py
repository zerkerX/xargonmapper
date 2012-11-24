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
from PIL import ImageFont, ImageDraw

class spritedb(object):
    def addsprite(self, sprtype, subtype, sprite):
        if sprtype not in self.sprites:
            self.sprites[sprtype] = {}
        self.sprites[sprtype][subtype] = sprite

    def __init__(self, graphics):
        self.sprites = {}
        self.mapsprites = {}

        # Manually-defined sprites (i.e. special handling needed
        self.addsprite(0, 4, sprite(graphics.records[6].images[9], yoffs=-8)) # Player
        self.addsprite(9, 3, sprite(graphics.records[31].images[35], xoffs=6, yoffs=8)) # Blue Lock


        # Text sprites:
        self.addsprite(6, 0, textsprite(ImageFont.truetype("FreeMonoBold.ttf", 9), graphics))
        self.addsprite(7, 0, textsprite(ImageFont.truetype("FreeMonoBold.ttf", 12), graphics))

        # Compound Sprite for Centipede Monster
        self.addsprite(52, 7, sprite(graphics.compositeimage((76, 22), [(0, 0, 52, 0),
            (16, 5, 52, 1), (24, 5, 52, 2), (32, 5, 52, 3), (40, 5, 52, 4),
            (48, 5, 52, 5), (56, 5, 52, 6), (64, 7, 52, 7)] )))

        # Compound and semi-transparent for hidden platform
        self.addsprite(11, 0, sprite(graphics.semitransparent(
            graphics.compositeimage((32, 16), [(0, 0, 25, 14),
            (16, 0, 25, 15)]), 128) ))

        # Simple sprite mapping. Stage sprites, then Map sprites
        for (sprtype, subtype, recnum, imagenum) in [(4, 0, 40, 20), # Mine
                (5, 0, 47, 8), # Map Player
                (13, 0, 36, 2), # Springboard
                (20, 3, 31, 24), # Blue Key
                (21, 0, 37, 33), # Health Pickup
                (22, 0, 30, 28), # Emerald
                (25, 0, 35, 2), # Clawface Monster
                (28, 0, 30, 15), (28, 4, 30, 17), (28, 6, 40, 21),
                (28, 8, 30, 21), (28, 9, 30, 22), # Powerups
                (28, 1, 30, 16), # Purple Key
                (48, 0, 40, 16), (48, 1, 40, 17), # Bubbles
                (51, 0, 36, 33), # Clouds
                (55, 0, 61, 8), # Brute
                (59, 0, 36, 28), # Spikes
                (68, 0, 40, 6), # Big Fish
                (72, 7, 55, 3), (72, 8, 55, 4), (72, 9, 55, 5), (72, 10, 55, 6), # Foliage
                (72, 4, 36, 35), (72, 11, 36, 36), # Exit Sign
                (77, 0, 32, 0), # Bee!
                (83, 0, 40, 22), # Small fish
                (88, -1, 47, 16), (88, 2, 47, 20), (88, 3, 47, 21) # Map images
                ]:
            self.addsprite(sprtype, subtype, sprite(graphics.records[recnum].images[imagenum]))

        # Treasures (+ contents)
        treasurelookup = {0 : graphics.records[37].images[24],
            1 : graphics.records[37].images[25],
            2 : graphics.debugimage('T', 2, 16, 16),
            3 : graphics.records[37].images[27] }

        for (sprtype, subtype, crecnum, cimagenum) in [
                (26, 0, 37, 33), # Health
                (26, 1, 37, 2), # Grapes
                (26, 2, 37, 6), # Cherry
                (26, 4, 37, 14), # Orange
                (26, 11, 30, 28), # Emerald
                (26, 12, 48, 2), # Nitro!
                (26, 13, 36, 29) # Empty
                ]:
            self.addsprite(sprtype, subtype, variablesprite(treasurelookup,
                contents=graphics.records[crecnum].images[cimagenum]))

        # Switches:
        self.addsprite(12, 0, variablesprite({
            0 : graphics.records[30].images[19],
            1 : graphics.records[51].images[0]}))

        # Pickups appear to be in the same order as their corresponding record.
        # There are two types of pickups: normal and hidden.
        for subtype in range(24):
            self.addsprite(33, subtype, sprite(graphics.records[37].images[subtype]))
            self.addsprite(73, subtype, sprite(graphics.semitransparent(
                graphics.records[37].images[subtype], 128) ))

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
        for sprtype, subtype in [(63,3), # Start?
            (61,0), (62,0), # Warp Doorway
            (19,0), # Map label? (TODO: Implement via compound sprite?)
        #    (12,0), # Switch/Trigger
            (71,0), (71,1), # Sign & Popup Message?
            (9, -1) # Locked Map Gate
            ]:
            self.addsprite(sprtype, subtype, sprite(graphics.debugimage(sprtype, subtype, 0, 0)))

        # Cache a reference to the graphics object for future use
        self.graphics = graphics

    def drawsprite(self, mappicture, objrec, mapdata):
        if objrec.sprtype not in self.sprites or \
                objrec.subtype not in self.sprites[objrec.sprtype]:
            self.addsprite(objrec.sprtype, objrec.subtype, sprite(
                self.graphics.debugimage(objrec.sprtype, objrec.subtype,
                objrec.width, objrec.height)))

        self.sprites[objrec.sprtype][objrec.subtype].draw(mappicture, objrec, mapdata)

class sprite(object):
    def __init__(self, image, xoffs=0, yoffs=0):
        self.image = image
        self.xoffs = xoffs
        self.yoffs = yoffs

    def draw(self, mappicture, objrec, mapdata):
        # When pasting masked images, need to specify the mask for the paste.
        # RGBA images can be used as their own masks.
        mappicture.paste(self.image, (objrec.x +self.xoffs,
            objrec.y +self.yoffs), self.image)

class textsprite(sprite):
    def __init__(self, font, graphics):
        self.font = font
        self.graphics = graphics

    def draw(self, mappicture, objrec, mapdata):
        pen = ImageDraw.Draw(mappicture)
        pen.text((objrec.x, objrec.y-2), mapdata.getstring(objrec.stringref),
                font=self.font, fill=self.graphics.getcolour(objrec.colour))

class variablesprite(sprite):
    def __init__(self, imagelookup, contents=None):
        # Create a lookup of possible boxes
        self.types = imagelookup
        self.xoffs = 0
        self.yoffs = 0
        self.contents = contents

    def draw(self, mappicture, objrec, mapdata):
        # Pick the correct image then use the parent routine to draw the box
        self.image = self.types[objrec.colour]
        super(variablesprite, self).draw(mappicture, objrec, mapdata)

        # Place contents immediately above the current sprite
        if self.contents != None:
            mappicture.paste(self.contents, (objrec.x +self.xoffs,
                objrec.y +self.yoffs - self.contents.size[1]), self.contents)
