# Day 4 #

Before we start identifying tiles and creating the image map, there are
two things I noticed yesterday about the image data that I want to
investigate.

1) The GRAPHICS file table of contents had a few blank entries. My
    current algorithm skips those positions entirely. However, when we start
    identifying tile mappings, the fact that there was a field allocated for
    them may be important. I will therefore update my algorithm to
    specifically create blank places in order to keep the record alignment
    accurate. It also appears to have space for more records, so I'm going
    to at least process those regions in case there are more records in the
    registered version.

2) Record 4 and Record 49 have a garbage 64*12 image in each of them.
    Also, record 49 appears to have the wrong colour palette. The
    interesting thing about a 64*12 image is that it takes up 768 bytes. A
    full 256 colour palette also takes up 768 bytes, so I suspect these
    records are actually colour palettes. If so, we don't need our sample
    screenshot and we can pull the colour palette direct from the game data.
    It also means we can correct the palette for the Record 49 images, if
    this is accurate.

Also, as the source files are going to get a bit more plentiful (and of
increasing length) I'm also going to change to only posting snippets of
code and include the full listing in a zip at the end of this day's
post.

Finally, because I'm paranoid, I'm going to put in a warning of a
record still has data after we read the last image in that record. I
*think* I'm decoding that right, but if there's more data, we don't
want to miss it.

For the blank entries, it couldn't be easier. Increasing the size of
the record removes the need for the seek command and the IF on the list
comprehension:

```py
header = '<128L'
headerdata = struct.unpack(header,
    graphicsfile.read(struct.calcsize(header)) )
header2 = '<128H'
headerdata2 = struct.unpack(header2,
    graphicsfile.read(struct.calcsize(header2)) )

# Create the image records using list comprehension
self.records = [imagerecord(graphicsfile, offset, size, palette)
    for (offset, size) in zip(headerdata, headerdata2)]
```

Instead, the IF needs to go inside the image record instead. It also
needs to be added to the debug output so we don't get a ton of empty
folders. I'll let the debug CSV actually attempt to write out data for
these blank records so it's easier to see the breakdown. I'm also
going to add my paranoid sanity check to the __init__ method now.
Here is the updated imagerecord class:

```py
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

    def __init__(self, filedata, offset, size, palette):
        self.offset = offset
        self.size = size

        self.images = []

        if offset > 0:
            filedata.seek(offset)
            headerstruct = '<12B'
            self.header = struct.unpack(headerstruct,
                filedata.read(struct.calcsize(headerstruct)) )

            self.numimages = self.header[0]

            for tilenum in range(self.numimages):
                (width, height, unknown) = struct.unpack('<3B',
                    filedata.read(3))

                tile = Image.fromstring("P", (width, height),
                    filedata.read(width*height))
                tile.putpalette(palette)
                self.images.append(self.maskimage(tile))

            # Check to see if we actually loaded all data from this record
            leftover = self.offset + self.size - filedata.tell()
            if leftover > 0:
                print "Record at offset {} has {} bytes unaccounted for.".format(self.offset, leftover)
            elif leftover < 0:
                print "Record at offset {} read {} bytes beyond its boundary.".format(self.offset, -leftover)

        else:
            self.numimages = 0
            self.header = []


    def save(self, outpath):
        if self.numimages > 0:
            createpath(outpath)
            for tilenum, tile in enumerate(self.images):
                tile.save(os.path.join(outpath, '{:04}.png'.format(tilenum)) )
```

And running again...

```
Record at offset 768 has 3 bytes unaccounted for.
Record at offset 9359 has 3 bytes unaccounted for.
Record at offset 14366 has 39 bytes unaccounted for.
Record at offset 15087 has 39 bytes unaccounted for.
Record at offset 21646 has 131 bytes unaccounted for.
Record at offset 22560 has 39 bytes unaccounted for.
Record at offset 54601 has 963 bytes unaccounted for.
Record at offset 61481 has 259 bytes unaccounted for.
Record at offset 68227 has 259 bytes unaccounted for.
Record at offset 74973 has 39 bytes unaccounted for.
Record at offset 87197 has 259 bytes unaccounted for.
Record at offset 94720 has 259 bytes unaccounted for.
Record at offset 98099 has 259 bytes unaccounted for.
Record at offset 101737 has 39 bytes unaccounted for.
Record at offset 124062 has 259 bytes unaccounted for.
Record at offset 131326 has 259 bytes unaccounted for.
Record at offset 140144 has 259 bytes unaccounted for.
Record at offset 148185 has 259 bytes unaccounted for.
Record at offset 155708 has 259 bytes unaccounted for.
Record at offset 160382 has 259 bytes unaccounted for.
Record at offset 163761 has 259 bytes unaccounted for.
Record at offset 171284 has 259 bytes unaccounted for.
Record at offset 178030 has 259 bytes unaccounted for.
Record at offset 197467 has 259 bytes unaccounted for.
Record at offset 204731 has 259 bytes unaccounted for.
Record at offset 214326 has 259 bytes unaccounted for.
Record at offset 235317 has 259 bytes unaccounted for.
Record at offset 253718 has 259 bytes unaccounted for.
Record at offset 262277 has 259 bytes unaccounted for.
Record at offset 266692 has 259 bytes unaccounted for.
Record at offset 296888 has 531 bytes unaccounted for.
Record at offset 305411 has 243 bytes unaccounted for.
Record at offset 309719 has 243 bytes unaccounted for.
Record at offset 321156 has 899 bytes unaccounted for.
Record at offset 325931 has 243 bytes unaccounted for.
Record at offset 343340 has 531 bytes unaccounted for.
Record at offset 353794 has 515 bytes unaccounted for.
Record at offset 363293 has 259 bytes unaccounted for.
Record at offset 374943 has 259 bytes unaccounted for.
Record at offset 395189 has 171 bytes unaccounted for.
Record at offset 407614 has 171 bytes unaccounted for.
Record at offset 415826 has 259 bytes unaccounted for.
Record at offset 433431 has 259 bytes unaccounted for.
Record at offset 439659 has 259 bytes unaccounted for.
Record at offset 451922 has 259 bytes unaccounted for.
Record at offset 473916 has 147 bytes unaccounted for.
Record at offset 481227 has 515 bytes unaccounted for.
Record at offset 485490 has 243 bytes unaccounted for.
Record at offset 488542 has 147 bytes unaccounted for.
Record at offset 491213 has 3 bytes unaccounted for.
Record at offset 554159 has 259 bytes unaccounted for.
Record at offset 563460 has 903 bytes unaccounted for.
Record at offset 566188 has 259 bytes unaccounted for.
Record at offset 597635 has 259 bytes unaccounted for.
Record at offset 629082 has 1299 bytes unaccounted for.
Record at offset 650040 has 1299 bytes unaccounted for.
Record at offset 662219 has 323 bytes unaccounted for.
Record at offset 664428 has 787 bytes unaccounted for.
Record at offset 689851 has 1539 bytes unaccounted for.
```

Well, we are missing data. Now, is this actual data, or blank regions?
Let's investigate one. Offset 54601 is record #7, and according to my
debug CSV has a size of 6880. If we have 969 unaccounted bytes, that
puts at offset 54601+6880-963 = 60518. And it looks like there's a
header for a 24 * 40 pixel image here. This implies that we are off by
1 on the number of images in a region. However, the 3 byte misalignments
look a bit too small. Sure enough, investigating one of those shows that
it actually is a 0, 0, 0 header. So, let's expand to grab that last
image, but provide the ability to ignore an empty image if needed.

```py
self.numimages = self.header[0] + 1

for tilenum in range(self.numimages):
    (width, height, unknown) = struct.unpack('<3B',
        filedata.read(3))
    if width > 0 and height > 0:
        tile = Image.fromstring("P", (width, height),
            filedata.read(width*height))
        tile.putpalette(palette)
        self.images.append(self.maskimage(tile))
```

No more warnings, but some of these extra images seem a bit out of
place. Hrm, maybe it is just garbage data after all. It doesn't hurt to
decode it though.

Now for palette time! This will require delaying loading the picture
data a bit later, so we can load the palette explicitly first. Here are
the updates to the imagerecord class:

```py
    def __init__(self, filedata, offset, size):
        self.offset = offset
        self.size = size

        self.images = []
        # Store the file handle for future use
        self.filedata = filedata

        if offset > 0:
            filedata.seek(offset)
            headerstruct = '<12B'
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
```

And the main load routine:

```py
# Create the image records using list comprehension
self.records = [imagerecord(graphicsfile, offset, size)
    for (offset, size) in zip(headerdata, headerdata2)]

palette1 = self.records[5].getpalette()
palette2 = self.records[53].getpalette()

for recnum, record in enumerate(self.records):
    if recnum == 53:
        record.loadimages(palette2, skipimages=1)
    elif recnum == 5:
        record.loadimages(palette1, skipimages=1)
    else:
        record.loadimages(palette1, skipimages=1)
```

Weird. Everything looks like the correct colours, just VERY dark. Either
it's in some strange format, or it's an alternate palette. A quick
comparison using GIMP and a Hex editor doesn't show any direct
correlation. Bah. It's not worth it right now. I'll keep the code in,
but I will limit it for group 53 data and leave the main data using the
screenshot for the palette. Let's get to the mapping!

In order to get started on the mapping, I need to refactor how I load
the map. Previously, we loaded the map byte-at-a-time to make
visualization easy. Now we should load as a series of 16-bit halfwords
instead. I should also add a quick routine to generate a map csv so I
can see the data values for each tile easily. Before I do that, let's
get the previous functionality refactored and try it on a few other maps
for comparison.

```py
import struct, sys, os
from PIL import Image

class xargonmap(object):
    def __init__(self, filename):
        # Grab the map from the file name (sans ext)
        # TODO: Maps may have embedded names. To consider
        (temppath, tempfname) = os.path.split(filename)
        (self.name, tempext) = os.path.splitext(tempfname)

        # Load the map data as a 98 x 98 array of 2-byte positions:
        mapfile = open(filename, 'rb')
        pattern = '<{}H'.format(64*128)

        self.tiles = struct.unpack(pattern,
            mapfile.read(struct.calcsize(pattern)) )
        mapfile.close()

    def debugcsv(self):
        # Remember that the map is height-first. We need to convert to
        # width-first
        pass

    def debugimage(self):
        # Turn the map data into a list of 3-byte tuples to visualize it.
        # Start by pre-creating an empty list of zeroes then copy it in
        visualdata = [None] * (64*128)
        for index in range(64*128):
            visualdata[index] = (self.tiles[index]%256, self.tiles[index]/256, 0)

        # Tell PIL to interpret the map data as a RAW image:
        mapimage = Image.new("RGB", (64, 128) )
        mapimage.putdata(visualdata)
        mapimage.rotate(-90).save(self.name + '.png')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print """Usage: python xargonmap.py [Map File]
TODO
"""
    else:
        for filename in sys.argv[1:]:
            themap = xargonmap(filename)
            themap.debugcsv()
            themap.debugimage()
```
