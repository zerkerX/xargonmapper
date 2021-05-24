#!/usr/bin/python3
# Copyright 2012, 2021 Ryan Armstrong
#
# This file is part of Xargon Mapper.
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

""" Module containing the sprite database """
import traceback
from PIL import ImageFont, ImageDraw

markupfont = ImageFont.load("font2.pil")

class spritedb(object):
    """ The sprite database is a database of all known Xargon sprites.
    It provides a lookup from the sprite ID and sub-id to the correct
    sprite type.
    """

    def addsprite(self, sprtype, subtype, sprite):
        """ Adds a sprite into the database. Creates the applicable
        sub-list as needed.

        sprtype -- the sprite type number (from the map object record)
        subtype -- the sprite sub-type number (also from the map object record)
        sprite -- a sprite object describing how to draw this sprite.
        """
        if sprtype not in self.sprites:
            self.sprites[sprtype] = {}
        self.sprites[sprtype][subtype] = sprite

    def __init__(self, graphics, epnum):
        """ Loads the sprite database according to the provided
        graphics file and episode number.
        """
        self.sprites = {}

        # Manually-defined sprites (i.e. special handling needed
        self.addsprite(0, 4, sprite(graphics.records[6].images[9], yoffs=-8)) # Player

        # Keys and Locks:
        for i in range (4):
            self.addsprite(9, i, sprite(graphics.records[31].images[32+i],
                xoffs=6, yoffs=8, hidelabel=True)) # Lock
            self.addsprite(20, i, sprite(graphics.records[31].images[i*8])) # Key

        # Text sprites:
        self.addsprite(6, 0, textsprite(ImageFont.load("font2.pil"), graphics))
        self.addsprite(7, 0, textsprite(ImageFont.load("font1.pil"), graphics))

        # Variant of Compound and semi-transparent for hidden platform(s)
        self.addsprite(11, 0, variablesprite({
            2: graphics.semitransparent(
               graphics.compositeimage((16, 32), [(0, 0, 8, 18),
               (0, 16, 8, 21)]), 128),
            4: graphics.semitransparent(
               graphics.compositeimage((48, 32), [(0, 0, 11, 1),
               (16, 0, 11, 1), (0, 16, 11, 2), (16, 16, 11, 2),
               (32, 0, 11, 19), (32, 16, 11, 19)]), 128),
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
                (16, 0, 36, 13), (16, 1, 36, 13), # Elevator Platform
                (18, 0, 36, 0), # Manual Elevator
                (21, 0, 37, 33), # Health Pickup
                (22, 0, 30, 28), # Emerald
                (24, 0, 34, 0), # EPIC Points
                (28, 6, 40, 21), # Diving Pod
                (28, 0, 30, 15), (28, 4, 30, 17), (28, 5, 30, 18),
                (28, 7, 30, 20), (28, 8, 30, 21), (28, 9, 30, 22), # Powerups
                (28, 1, 30, 16), # Purple Key
                (30, 0, 51, 9), (30, 1, 51, 8), # Ceiling Switch
                (31, 0, 51, 14), (31, 1, 51, 14), # Hidden Spikey Creature
                (33, 28, 37, 28), # Fireball
                (38, 0, 30, 50), (38, 1, 30, 51), (38, 2, 30, 52), # Menu Bullets
                (40, 0, 30, 62), # Star
                (42, 0, 37, 29), # Green Gem
                (42, 1, 37, 30), # Purple Gem
                (42, 2, 37, 31), # Red Gem
                (42, 3, 37, 32), # Yellow Gem
                (44, 0, 15, 2), # Stalagtite
                (45, 0, 36, 19), # Boulder Trap
                (48, 0, 40, 16), (48, 1, 40, 17), # Bubbles
                (51, 0, 36, 33), # Clouds
                (72, 0, 55, 0), (72, 1, 55, 1), (72, 2, 55, 2), # Pillar
                (72, 7, 55, 3), (72, 8, 55, 4), (72, 9, 55, 5), (72, 10, 55, 6), # Foliage
                (72, 4, 36, 35), (72, 11, 36, 36), # Exit Sign
                (72, 13, 38, 3), (72, 14, 38, 4), # Reactors
                (72, 15, 38, 5), (72, 16, 38, 6), # To Reactor
                (74, 0, 59, 9), # Ceiling Turret
                (78, 0, 50, 0), # Climbing Monster
                (81, 0, 39, 22), # Water Bed Creature
                (84, 0, 30, 31), (84, 1, 30, 32), (84, 2, 30, 33), # Artefacts
                (87, 0, 38, 0), (87, 1, 38, 1), # The Mighty Xargon!
                (88, 0, 47, 18), (88, 1, 47, 19),
                (88, 2, 47, 20), (88, 3, 47, 21), (88, 6, 47, 24) # Map images
                ]:
            self.addsprite(sprtype, subtype, sprite(graphics.records[recnum].images[imagenum]))

        # Simple mapping to hide info label:
        for (sprtype, subtype, recnum, imagenum) in [
                (13, 0, 36, 2), # Springboard
                (49, 0, 48, 12), # Torch
                ]:
            self.addsprite(sprtype, subtype, sprite(graphics.records[recnum].images[imagenum],
                hidelabel=True))

        # Map Images that need alignment:
        for (sprtype, subtype, recnum, imagenum) in [
                (5, 0, 47, 8), # Map Player
                (88, 4, 47, 22), (88, 5, 47, 23)]:
            self.addsprite(sprtype, subtype, sprite(
                graphics.records[recnum].images[imagenum], xoffs=4))
        self.addsprite(88, -1, sprite(
            graphics.records[47].images[16], xoffs=2, yoffs=2))

        # Xargon's castle:
        if epnum == 3:
            self.addsprite(88, 7,  sprite(graphics.records[47].images[25], yoffs=6, xoffs=4))
            self.addsprite(88, 8,  sprite(graphics.records[47].images[26], yoffs=6, xoffs=10))
            self.addsprite(88, 9,  sprite(graphics.records[47].images[27]))
            self.addsprite(88, 10, sprite(graphics.records[47].images[28], xoffs=4))
            self.addsprite(88, 11, sprite(graphics.records[47].images[29], xoffs=10))
            self.addsprite(88, 12, sprite(graphics.records[47].images[30]))

        # Silvertongue
        for i in range (25):
            self.addsprite(23, i, sprite(graphics.records[45].images[1]))

        # Crushing Ceilings:
        for i in range (16):
            self.addsprite(15, i, sprite(graphics.records[36].images[6]))

        # Illusionary Walls:
        self.addsprite(72, 3, sprite(graphics.semitransparent(
                graphics.records[20].images[8], 160) ))
        self.addsprite(72, 5, sprite(graphics.semitransparent(
                graphics.records[11].images[23], 160) ))
        self.addsprite(72, 6, sprite(graphics.semitransparent(
                graphics.records[19].images[15], 160) ))
        self.addsprite(72, 12, sprite(graphics.semitransparent(
                graphics.records[19].images[16], 160) ))

        # Treasures (+ contents)
        treasurelookup = {0 : graphics.records[37].images[24],
            1 : graphics.records[37].images[25],
            2 : graphics.records[37].images[26],
            3 : graphics.records[37].images[27] }

        for (sprtype, subtype, crecnum, cimagenum) in [
                (26, 0, 37, 33), # Health
                (26, 1, 37, 2), # Grapes
                (26, 2, 37, 6), # Cherry
                (26, 3, 37, 8), # Strawberries
                (26, 4, 37, 14), # Orange
                (26, 5, 37, 3), # Epic Disk
                (26, 6, 31, 0), # Yellow Key
                (26, 7, 31, 8), # Green Key
                (26, 8, 31, 16), # Red Key
                (26, 9, 31, 24), # Blue Key
                (26, 10, 30, 21), # High-jump shoes
                (26, 11, 30, 28), # Emerald
                (26, 12, 48, 2), # Nitro!
                (26, 13, 36, 29) # Empty
                ]:
            self.addsprite(sprtype, subtype, variablesprite(treasurelookup,
                contents=graphics.records[crecnum].images[cimagenum]))

        # Pickup Switches:
        self.addsprite(12, 0, variablesprite({
            0 : graphics.records[30].images[19],
            1 : graphics.records[51].images[0]},
            labelpref="TR ", labeloffs = (0, 4)) )

        # Toggle Switches:
        self.addsprite(29, 0, sprite(graphics.records[36].images[23],
            labelpref = "SW "))
        self.addsprite(29, 1, sprite(graphics.records[36].images[24],
            labelpref = "SW "))

        # Timers:
        for i in [30, 40, 50, 60]:
            self.addsprite(73, i, sprite(graphics.records[30].images[19],
                labelpref="Timer ", labeloffs = (-4, 4)) )

        # Menu Flame Jets:
        self.addsprite(47, 0, variablesprite({
            6 : graphics.records[48].images[3],
            8 : graphics.records[48].images[4]},
            field='info', hidelabel=True))

        # Bouncing Balls:
        for i in range(2):
            self.addsprite(46, i, variablesprite({
                0 : graphics.records[51].images[4],
                1 : graphics.records[51].images[5],
                2 : graphics.records[51].images[6],
                3 : graphics.records[51].images[7]},
                field='info', hidelabel=True))

        # Spikes:
        self.addsprite(59, 0, variablesprite({
            0 : graphics.records[36].images[28],
            1 : graphics.records[36].images[32]},
            field='variant', hidelabel=True))

        # Ceiling Spear
        for i in range(3):
            self.addsprite(43, i, variablesprite({
                0 : graphics.records[36].images[9],
                1 : graphics.records[36].images[12]},
                offsets={0: (0, 0), 1:(0, -4) },
                field='variant', hidelabel=True))

        # Snake Face
        self.addsprite(50, 0, variablesprite({
            0 : graphics.records[60].images[1],
            1 : graphics.records[60].images[4]},
            offsets={0: (0, 0), 1:(-8, 0) },
            hidelabel = True))


        # Monsters:
        # Assumed Convention: > 0 -- Right, <= 0 -- Left
        # Clawface Monster
        self.addsprite(25, 0, variablesprite({
            0 : graphics.records[35].images[2],
            2 : graphics.records[35].images[10],
            } ))

        # Brute
        self.addsprite(55, 0, variablesprite({
            -4 : graphics.records[61].images[12],
            -3 : graphics.records[61].images[11],
            -2 : graphics.records[61].images[10],
            -1 : graphics.records[61].images[9],
            0 : graphics.records[61].images[8],
            1 : graphics.records[61].images[0],
            2 : graphics.records[61].images[1],
            3 : graphics.records[61].images[2],
            4 : graphics.records[61].images[3]
            } ))

        # Centipede Monster
        self.addsprite(52, 7, sprite(graphics.compositeimage((76, 22), [(0, 0, 52, 0),
            (16, 5, 52, 1), (24, 5, 52, 2), (32, 5, 52, 3), (40, 5, 52, 4),
            (48, 5, 52, 5), (56, 5, 52, 6), (64, 7, 52, 7)] )))

        # Alien Rat Thing
        self.addsprite(53, 0, variablesprite({
            -1 : graphics.records[58].images[2],
            0 : graphics.records[58].images[1],
            2 : graphics.records[58].images[6]
            } ))

        if epnum == 3:
            # Snake-like thing
            self.addsprite(54, 0, variablesprite({
                -3 : graphics.records[42].images[3],
                -2 : graphics.records[42].images[2],
                -1 : graphics.records[42].images[1],
                0 : graphics.records[42].images[0],
                2 : graphics.records[42].images[5],
                4 : graphics.records[42].images[6]
                } ))

        if epnum == 2:
            # Goo Monster
            self.addsprite(56, 0, sprite(graphics.records[46].images[2]))

        if epnum != 1:
            # Mini Dino
            self.addsprite(58, 0, variablesprite({
                -2 : graphics.records[56].images[6],
                -1 : graphics.records[56].images[5],
                0 : graphics.records[56].images[4],
                1 : graphics.records[56].images[1],
                2 : graphics.records[56].images[0],
                } ))

        # Flying Robots
        self.addsprite(60, 0, sprite(graphics.records[59].images[1]))
        self.addsprite(60, 1, sprite(graphics.records[59].images[4]))
        self.addsprite(60, 2, sprite(graphics.records[59].images[7]))

        # Shrimp
        self.addsprite(64, 0, variablesprite({
            0 : graphics.records[39].images[2],
            2 : graphics.records[39].images[10],
            } ))

        # Evil Cloak Guy
        for i in range(2):
            self.addsprite(65, i, variablesprite({
                0 : graphics.records[54].images[5],
                2 : graphics.records[54].images[0],
                } ))

        # Eel
        self.addsprite(67, 0, variablesprite({
            -3 : graphics.records[39].images[14],
            0 : graphics.records[39].images[15],
            2 : graphics.records[39].images[20]
            } ))

        # Big Fish
        self.addsprite(68, 0, variablesprite({
            -3 : graphics.records[40].images[8],
            -2 : graphics.records[40].images[7],
            0 : graphics.records[40].images[6],
            2 : graphics.records[40].images[11],
            3 : graphics.records[40].images[12],
            4 : graphics.records[40].images[13]
            } ))


        if epnum != 1:
            # Bat
            self.addsprite(69, 0, sprite(graphics.records[56].images[8]))

            self.addsprite(70, 0, variablesprite({
                0 : graphics.records[63].images[4],
                2 : graphics.records[63].images[1],
                } ))


        # Skull Slug!
        if epnum != 2:
            self.addsprite(75, 0, variablesprite({
                -1 : graphics.records[62].images[2],
                0 : graphics.records[62].images[0],
                1 : graphics.records[62].images[5],
                2 : graphics.records[62].images[3]
                }, hidelabel=True ))

        # Bee!
        self.addsprite(77, 0, variablesprite({
            -2 : graphics.records[32].images[1],
            -1 : graphics.records[32].images[1],
            0 : graphics.records[32].images[0],
            1 : graphics.records[32].images[3],
            2 : graphics.records[32].images[2]
            } ))

        # Spider!
        self.addsprite(79, 0, variablesprite({
            -3 : graphics.records[43].images[12],
            -2 : graphics.records[43].images[11],
            -1 : graphics.records[43].images[10],
            0 : graphics.records[43].images[9],
            1 : graphics.records[43].images[0],
            2 : graphics.records[43].images[1],
            3 : graphics.records[43].images[2],
            4 : graphics.records[43].images[3]
            } ))

        # Robot with Treads
        self.addsprite(82, 0, variablesprite({
            -4 : graphics.records[59].images[21],
            -3 : graphics.records[59].images[21],
            -2 : graphics.records[59].images[20],
            -1 : graphics.records[59].images[19],
            0 : graphics.records[59].images[18],
            1 : graphics.records[59].images[14],
            2 : graphics.records[59].images[15],
            3 : graphics.records[59].images[16],
            4 : graphics.records[59].images[17],
            } ))

        # Small fish
        self.addsprite(83, 0, variablesprite({
            0 : graphics.records[40].images[22],
            2 : graphics.records[40].images[26]
            } ))

        # Pickups appear to be in the same order as their corresponding record.
        # There are two types of pickups: normal and hidden.
        for subtype in range(24):
            self.addsprite(33, subtype, sprite(graphics.records[37].images[subtype],
                hidelabel=True))
            self.addsprite(73, subtype, sprite(graphics.semitransparent(
                graphics.records[37].images[subtype], 128) ))

        # Special case for 73, Variant 4 appears to be the pickup item.
        # Other variants appear to be:
        # 0 : Unused??
        # 1 : Flaming Face Jet (Down) (Invisible)
        # 2 : Flaming Lava Jet (Up) (Invisible)
        # 3 : Robot Spawner
        # 5 : Slug Spawner
        # These alternate forms only appear to show up for subtypes 0 and 1,
        # so they will be added just for these two numbers:

        # Episode 2 doesn't have the skull slug, so we need an alternate
        # sprite so it doesn't crash.
        if epnum != 2:
            slugspawner = graphics.compositeimage((32, 14),
                    [(2, 0, 62, 2), (-3, 0, 62, 0)])
        else:
            slugspawner = graphics.records[30].images[19]

        for i in range(2):
            self.addsprite(73, i, variablesprite({
                0 : graphics.records[30].images[19],
                1 : graphics.records[30].images[19],
                2 : graphics.records[30].images[19],
                3 : graphics.compositeimage((32, 32), [(0, 0, 59, 1),
                   (16, 0, 59, 4), (8, 12, 59, 1)]),
                4 : graphics.semitransparent(
                    graphics.records[37].images[i], 128),
                5 : slugspawner},
                field='variant', hidelabel=True))

        # Story Scenes:
        if epnum == 1:
            for subtype in range(24):
                self.addsprite(85, subtype, sprite(graphics.records[56].images[subtype]))
                self.addsprite(86, subtype, sprite(graphics.records[57].images[subtype]))
        elif epnum == 3:
            # Fake sprite for the ending scene (which does not appear to have a sprite OR use Tiles):
            tilelist = []
            for x in range(10):
                for y in range(10):
                    tilelist.append( (x*16, y*16, 57, x + 10*y) )
            self.addsprite(1000, 0, sprite(graphics.compositeimage((160, 160), tilelist)))

        # Empty sprites:
        # -------------------------
        # For future reference, possible meanings are:
        # 17-# (and other numbers): Start? Warp?
        # 63-# Start?
        for sprtype in [17, 63]:
            for subtype in range(-1, 11):
                self.addsprite(sprtype, subtype, sprite(graphics.records[30].images[19],
                    hidelabel=True))

        for sprtype, subtype in [
                (19,0), # Map label? (TODO: Implement via compound sprite?)
                (8, 0), (8, 1), # Switchable Pillar Wall
                ]:
            self.addsprite(sprtype, subtype, sprite(graphics.records[30].images[19]))

        for sprtype, subtype in [
                (71,0), (71,1), # Sign & Popup Message?
                (9, -1) # Locked Map Gate
                ]:
            self.addsprite(sprtype, subtype, sprite(graphics.records[30].images[19],
                hidelabel=True))


        # Warp Doorways:
        self.addsprite(61, 0, sprite(graphics.records[30].images[19],
            labeloffs = (4, 4))) # Out Door
        self.addsprite(62, 0, sprite(graphics.records[30].images[19],
            labelpref='To ', labeloffs = (0, 4))) # In Door

        # Cache a reference to the graphics object for future use
        self.graphics = graphics

    def drawsprite(self, mappicture, objrec, mapdata):
        """ Draws the sprite described by the map object record into the
        map image.

        mappicture -- the in-progress map image
        objrec -- the object record for the sprite to be drawn
        mapdata -- a reference back to the data that is being mapped.
        """
        try:
            # Create a debug sprite when a sprite is unknown
            if objrec.sprtype not in self.sprites or \
                    objrec.subtype not in self.sprites[objrec.sprtype]:
                self.addsprite(objrec.sprtype, objrec.subtype, sprite(
                    self.graphics.debugimage(objrec.sprtype, objrec.subtype,
                    objrec.width, objrec.height)))

            # Draw the sprite
            self.sprites[objrec.sprtype][objrec.subtype].draw(mappicture, objrec, mapdata)

        except:
            print("Problem with Sprite {}, Type {}, Appearance {}, Variant {} at ({}, {})".format(
                objrec.sprtype, objrec.subtype, objrec.appearance, objrec.variant,
                objrec.x, objrec.y))
            traceback.print_exc()


class sprite(object):
    """ Sprite object which represents a standard Xargon sprite. It
    contains enough information to render the sprite into the map.
    """
    def __init__(self, image, xoffs=0, yoffs=0, hidelabel=False,
            labelpref='', labeloffs=(-8, -8)):
        """ Initializes this sprite according to the following info:

        image -- the PIL image for the sprite
        xoffs -- an X offset (in pixels) to shift this sprite by
        yoffs -- an Y offset (in pixels) to shift this sprite by
        hidelabel -- if true, and this sprite has an info value
                     (typically for switches), it is still not drawn.
        labelpref -- if a label is drawn for this sprite, this prefix
                     text is added first.
        labeloffs -- a tuple specifying how far from the upper-left
                     corner of the sprite to start the upper-left corner
                     of the label text.
        """

        self.image = image
        self.xoffs = xoffs
        self.yoffs = yoffs
        self.hidelabel = hidelabel
        self.labelpref = labelpref
        self.labeloffs = labeloffs

    def draw(self, mappicture, objrec, mapdata):
        """ Draws this sprite into the in-progress map image:

        mappicture -- the in-progress map image
        objrec -- the object record for the sprite to be drawn
        mapdata -- a reference back to the data that is being mapped.
        """

        # When pasting masked images, need to specify the mask for the paste.
        # RGBA images can be used as their own masks.
        mappicture.paste(self.image, (objrec.x +self.xoffs,
            objrec.y +self.yoffs), self.image)

        if objrec.info > 0 and objrec.info < 90 and not self.hidelabel:
            text = "{}{}".format(self.labelpref, objrec.info)

            # Draw the text 5 times to create an outline
            # (4 x black then 1 x white)
            pen = ImageDraw.Draw(mappicture)
            for offset, colour in [( (-1,-1), (0,0,0) ),
                    ( (-1,1), (0,0,0) ),
                    ( (1,-1), (0,0,0) ),
                    ( (1,1), (0,0,0) ),
                    ( (0,0), (255,255,255) )]:
                pen.text( (objrec.x +self.xoffs +offset[0] +self.labeloffs[0],
                    objrec.y +self.yoffs +offset[1] +self.labeloffs[0]),
                    text, font=markupfont, fill=colour)


class textsprite(sprite):
    """ A sprite intended to draw text into the map """

    def __init__(self, font, graphics):
        """ Initializes this sprite according to the following info:

        image -- the PIL image for the sprite
        xoffs -- an X offset (in pixels) to shift this sprite by
        yoffs -- an Y offset (in pixels) to shift this sprite by
        hidelabel -- if true, and this sprite has an info value
                     (typically for switches), it is still not drawn.
        labelpref -- if a label is drawn for this sprite, this prefix
                     text is added first.
        labeloffs -- a tuple specifying how far from the upper-left
                     corner of the sprite to start the upper-left corner
                     of the label text.
        """
        self.font = font
        self.graphics = graphics

    def draw(self, mappicture, objrec, mapdata):
        """ Draws this sprite into the in-progress map image:

        mappicture -- the in-progress map image
        objrec -- the object record for the sprite to be drawn
        mapdata -- a reference back to the data that is being mapped.
        """

        pen = ImageDraw.Draw(mappicture)

        if objrec.appearance == 8:
            # Simulate multi-colour appearance by creating a fake shadow effect
            pen.text((objrec.x, objrec.y), mapdata.getstring(objrec.stringref),
                    font=self.font, fill=self.graphics.getcolour(14))
            pen.text((objrec.x-1, objrec.y), mapdata.getstring(objrec.stringref),
                    font=self.font, fill=self.graphics.getcolour(6))
        else:
            pen.text((objrec.x, objrec.y), mapdata.getstring(objrec.stringref),
                    font=self.font, fill=self.graphics.getcolour(objrec.appearance))


class variablesprite(sprite):
    """ A sprite whos apperance changes due to some field other than the
    sub-type. The sprite is indexed according to the specified field
    and the correct image is drawn into the world.
    """

    def __init__(self, imagelookup, contents=None, field='appearance',
            offsets=None, hidelabel=False, labelpref='', labeloffs=(-8, -8)):
        """ Initializes this variable sprite according to the following info:

        imagelookup -- A dictionary of PIL images to use, keyed by
                       numbers in the lookup field of the object record.
        contents -- For treasure boxes. This is a secondary image that
                    is drawn above the main image to indicate what this
                    box actually contains.
        offsets -- a lookup of offset tuples, keyed by the numbers in
                   the lookup field of the object record. The selected
                   offset is used to shift the resulting image.
        hidelabel -- if true, and this sprite has an info value
                     (typically for switches), it is still not drawn.
        labelpref -- if a label is drawn for this sprite, this prefix
                     text is added first.
        labeloffs -- a tuple specifying how far from the upper-left
                     corner of the sprite to start the upper-left corner
                     of the label text.
        """

        # Create a lookup of possible boxes
        self.types = imagelookup
        self.xoffs = 0
        self.yoffs = 0
        self.contents = contents
        self.offsets = offsets
        self.field = field
        self.hidelabel = hidelabel
        self.labelpref = labelpref
        self.labeloffs = labeloffs

    def draw(self, mappicture, objrec, mapdata):
        """ Draws this sprite into the in-progress map image:

        mappicture -- the in-progress map image
        objrec -- the object record for the sprite to be drawn
        mapdata -- a reference back to the data that is being mapped.
        """

        # Pick the correct image then use the parent routine to draw the box
        self.image = self.types[objrec.__dict__[self.field]]
        if self.offsets != None:
            (self.xoffs, self.yoffs) = self.offsets[objrec.__dict__[self.field]]
        super(variablesprite, self).draw(mappicture, objrec, mapdata)

        # Place contents immediately above the current sprite
        if self.contents != None:
            mappicture.paste(self.contents, (objrec.x +self.xoffs,
                objrec.y +self.yoffs - self.contents.size[1]), self.contents)
