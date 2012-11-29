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
import traceback
from PIL import ImageFont, ImageDraw

class spritedb(object):

    markupfont = ImageFont.load("font1.pil")

    def addsprite(self, sprtype, subtype, sprite):
        if sprtype not in self.sprites:
            self.sprites[sprtype] = {}
        self.sprites[sprtype][subtype] = sprite

    def debug__init__(self, graphics):
        self.sprites = {}
        self.graphics = graphics

    def __init__(self, graphics):
        self.sprites = {}

        # Manually-defined sprites (i.e. special handling needed
        self.addsprite(0, 4, sprite(graphics.records[6].images[9], yoffs=-8)) # Player

        # Keys and Locks:
        for i in range (4):
            self.addsprite(9, i, sprite(graphics.records[31].images[32+i], xoffs=6, yoffs=8)) # Lock
            self.addsprite(20, i, sprite(graphics.records[31].images[i*8])) # Key

        self.addsprite(9, 1, sprite(graphics.records[31].images[33], xoffs=6, yoffs=8)) # Green Lock
        self.addsprite(9, 3, sprite(graphics.records[31].images[35], xoffs=6, yoffs=8)) # Blue Lock

        # Text sprites:
        self.addsprite(6, 0, textsprite(ImageFont.load("font2.pil"), graphics))
        self.addsprite(7, 0, textsprite(ImageFont.load("font1.pil"), graphics))

        # Compound Sprite for Centipede Monster
        self.addsprite(52, 7, sprite(graphics.compositeimage((76, 22), [(0, 0, 52, 0),
            (16, 5, 52, 1), (24, 5, 52, 2), (32, 5, 52, 3), (40, 5, 52, 4),
            (48, 5, 52, 5), (56, 5, 52, 6), (64, 7, 52, 7)] )))

        # Variant of Compound and semi-transparent for hidden platform(s)
        self.addsprite(11, 0, variablesprite({
            6: graphics.semitransparent(
               graphics.compositeimage((32, 16), [(0, 0, 25, 14),
               (16, 0, 25, 15)]), 128),
            7: graphics.semitransparent(
               graphics.compositeimage((32, 16), [(0, 0, 51, 10),
               (16, 0, 51, 11)]), 128) }
             ))

        # Simple sprite mapping. Stage sprites, then Map sprites
        for (sprtype, subtype, recnum, imagenum) in [(0, 0, 6, 10), # Menu Player
                (4, 0, 40, 20), # Mine
                (5, 0, 47, 8), # Map Player
                (13, 0, 36, 2), # Springboard
                (16, 0, 36, 13), (16, 1, 36, 13), # Elevator Platform
                (18, 0, 36, 0), # Manual Elevator
                (21, 0, 37, 33), # Health Pickup
                (22, 0, 30, 28), # Emerald
                (23, 17, 45, 1), # Eagle
                (24, 0, 34, 0), # EPIC Points
                (25, 0, 35, 2), # Clawface Monster
                (28, 6, 40, 21), # Diving Pod
                (28, 0, 30, 15), (28, 4, 30, 17), (28, 5, 30, 18),
                (28, 7, 30, 20), (28, 8, 30, 21), (28, 9, 30, 22), # Powerups
                (28, 1, 30, 16), # Purple Key
                (29, 0, 36, 23), (29, 1, 36, 24), # Toggle Switch
                (33, 28, 37, 28), # Fireball
                (38, 0, 30, 50), (38, 1, 30, 51), (38, 2, 30, 52), # Menu Bullets
                (40, 0, 30, 62), # Star
                (42, 3, 37, 32), # Yellow Gem
                (44, 0, 15, 2), # Stalagtite
                (45, 0, 36, 19), # Boulder Trap
                (46, 0, 51, 7), (46, 1, 51, 7), # Spike ball
                (48, 0, 40, 16), (48, 1, 40, 17), # Bubbles
                (49, 0, 48, 12), # Torch
                (51, 0, 36, 33), # Clouds
                (53, 0, 58, 1), # Alien Rat Thing
                (55, 0, 61, 8), # Brute
                (60, 0, 59, 0), (60, 1, 59, 3), (60, 2, 59, 6), # Flying Robots
                (64, 0, 39, 6), # Shrimp
                (67, 0, 39, 15), # Eel
                (68, 0, 40, 6), # Big Fish
                (72, 0, 55, 0), (72, 1, 55, 1), (72, 2, 55, 2), # Pillar
                (72, 7, 55, 3), (72, 8, 55, 4), (72, 9, 55, 5), (72, 10, 55, 6), # Foliage
                (72, 4, 36, 35), (72, 11, 36, 36), # Exit Sign
                (74, 0, 59, 9), # Ceiling Turret
                (75, 0, 62, 2), # Skull Slug
                (77, 0, 32, 0), # Bee!
                (78, 0, 50, 0), # Climbing Monster
                (79, 0, 43, 9), # Spider!
                (81, 0, 39, 22), # Water Bed Creature
                (82, 0, 59, 18), # Robot with Treads
                (83, 0, 40, 22), # Small fish
                (84, 0, 30, 31), (84, 1, 30, 32), (84, 2, 30, 33), # Artefacts
                (88, -1, 47, 16), (88, 0, 47, 18), (88, 1, 47, 19),
                (88, 2, 47, 20), (88, 3, 47, 21), (88, 4, 47, 22),
                (88, 5, 47, 23), (88, 6, 47, 24) # Map images
                ]:
            self.addsprite(sprtype, subtype, sprite(graphics.records[recnum].images[imagenum]))

        # Crushing Ceilings:
        for i in range (16):
            self.addsprite(15, i, sprite(graphics.records[36].images[6]))

        # Illusionary Walls:
        self.addsprite(72, 12, sprite(graphics.semitransparent(
                graphics.records[19].images[16], 160) ))
        self.addsprite(72, 5, sprite(graphics.semitransparent(
                graphics.records[11].images[23], 160) ))

        # Treasures (+ contents)
        treasurelookup = {0 : graphics.records[37].images[24],
            1 : graphics.records[37].images[25],
            2 : graphics.records[37].images[26],
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

        # Pickup Switches:
        self.addsprite(12, 0, variablesprite({
            0 : graphics.records[30].images[19],
            1 : graphics.records[51].images[0]}))

        # TODO: The following sprite types COULD draw corresponding trigger identifiers:
        # 8 : Switchable Wall/Floor
        # 11 : Hidden Platforms
        # 12 : Pickup Switch
        # 29 : Toggle switch
        # 26 : Treasure (Drops)
        # 44 : Stalagtites (Drops)
        # 61. 62 : Warp Doorways (link number)

        # Menu Flame Jets:
        self.addsprite(47, 0, variablesprite({
            6 : graphics.records[48].images[3],
            8 : graphics.records[48].images[4]},
            field='info'))

        # Spikes:
        self.addsprite(59, 0, variablesprite({
            0 : graphics.records[36].images[28],
            1 : graphics.records[36].images[32]},
            field='variant'))

        # Ceiling Spear
        self.addsprite(43, 0, variablesprite({
            0 : graphics.records[36].images[9],
            1 : graphics.records[36].images[12]},
            offsets={0: (0, 0), 1:(0, -4) },
            field='variant'))

        # Snake Face
        self.addsprite(50, 0, variablesprite({
            0 : graphics.records[60].images[1],
            1 : graphics.records[60].images[4]},
            offsets={0: (0, 0), 1:(-8, 0) }))

        # Pickups appear to be in the same order as their corresponding record.
        # There are two types of pickups: normal and hidden.
        for subtype in range(24):
            self.addsprite(33, subtype, sprite(graphics.records[37].images[subtype]))
            self.addsprite(73, subtype, sprite(graphics.semitransparent(
                graphics.records[37].images[subtype], 128) ))

        # Special case for 73, type 0. Variant 4 appears to be the pickup item.
        # Other variants (all rendered invisible) appear to be:
        # 1 : Flaming Face Jet (Down)
        # 2 : Flaming Lava Jet (Up)
        # 3 : TBC
        self.addsprite(73, 0, variablesprite({
            1 : graphics.records[30].images[19],
            2 : graphics.records[30].images[19],
            3 : graphics.debugimage(73, 'T3', 16, 16),
            4 : graphics.semitransparent(
                graphics.records[37].images[0], 128)},
            field='variant'))

        # Story Scenes:
        for subtype in range(24):
            self.addsprite(85, subtype, sprite(graphics.records[56].images[subtype]))
            self.addsprite(86, subtype, sprite(graphics.records[57].images[subtype]))


        # Empty sprites:
        # -------------------------
        # For future reference, possible meanings are:
        # 17-# (and other numbers): Respawn point
        # 63-# Start?
        for sprtype in [17, 63]:
            for subtype in range(-1, 11):
                self.addsprite(sprtype, subtype, sprite(graphics.records[30].images[19]))

        # 63-3: Start??
        # 61:0, 62:0: Doorway
        # 71-0: Sign? 71-1 Popup message?
        for sprtype, subtype in [
            (61,0), (62,0), # Warp Doorway
            (19,0), # Map label? (TODO: Implement via compound sprite?)
            (71,0), (71,1), # Sign & Popup Message?
            (8, 0), (8, 1), # Switchable Pillar Wall
            (9, -1) # Locked Map Gate
            ]:
            self.addsprite(sprtype, subtype, sprite(graphics.records[30].images[19]))

        # Cache a reference to the graphics object for future use
        self.graphics = graphics

    def drawsprite(self, mappicture, objrec, mapdata):
        try:
            if objrec.sprtype not in self.sprites or \
                    objrec.subtype not in self.sprites[objrec.sprtype]:
                self.addsprite(objrec.sprtype, objrec.subtype, sprite(
                    self.graphics.debugimage(objrec.sprtype, objrec.subtype,
                    objrec.width, objrec.height)))

            self.sprites[objrec.sprtype][objrec.subtype].draw(mappicture, objrec, mapdata)

            #if objrec.info != 0:
            #    self.drawlabel(mappicture, (objrec.x -8, objrec.y -8), str(objrec.info))
        except:
            print "Problem with Sprite {}, Type {}, Appearance {}, Variant {} at ({}, {})".format(
                objrec.sprtype, objrec.subtype, objrec.appearance, objrec.variant,
                objrec.x, objrec.y)
            traceback.print_exc()



    def drawlabel(self, mappicture, coords, text):
        # Draw the text 5 times to create an outline
        # (4 x black then 1 x white)
        pen = ImageDraw.Draw(mappicture)
        for offset, colour in [( (-1,-1), (0,0,0) ),
                ( (-1,1), (0,0,0) ),
                ( (1,-1), (0,0,0) ),
                ( (1,1), (0,0,0) ),
                ( (0,0), (255,255,255) )]:
            pen.text((coords[0] + offset[0], coords[1] + offset[1]),
                text, font=self.markupfont, fill=colour)



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
        pen.text((objrec.x, objrec.y), mapdata.getstring(objrec.stringref),
                font=self.font, fill=self.graphics.getcolour(objrec.appearance))


class variablesprite(sprite):
    def __init__(self, imagelookup, contents=None, field='appearance', offsets=None):
        # Create a lookup of possible boxes
        self.types = imagelookup
        self.xoffs = 0
        self.yoffs = 0
        self.contents = contents
        self.offsets = offsets
        self.field = field

    def draw(self, mappicture, objrec, mapdata):
        # Pick the correct image then use the parent routine to draw the box
        self.image = self.types[objrec.__dict__[self.field]]
        if self.offsets != None:
            (self.xoffs, self.yoffs) = self.offsets[objrec.__dict__[self.field]]
        super(variablesprite, self).draw(mappicture, objrec, mapdata)

        # Place contents immediately above the current sprite
        if self.contents != None:
            mappicture.paste(self.contents, (objrec.x +self.xoffs,
                objrec.y +self.yoffs - self.contents.size[1]), self.contents)
