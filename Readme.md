About and Dependencies
----------------------

This is a series of Python scripts to generate maps of Xargon, as well 
as extract most of the Xargon image resources. These scripts require 
[the Pillow fork of the Python Imaging Library (PIL)][pil] and [Python 
3.x][py]. This was tested with Python 3.9.2, but it does not use any 
recently-introduced features. As such, it should run with just about 
any version of Python 3. At the time of writing, the oldest version of 
Python still receiving updates is 3.6, so I do not recommend anything 
older.

Windows and macOS users should be able to download Python from the 
above links and use ``pip`` to install Pillow. Most Linux/Unix varients 
should be able to install Python and Pillow via your package manager of 
choice; Ubuntu users can install the **python3** and **python3-pil** 
libraries.

The scripts also obviously require **Xargon**, either the shareware or 
full versions. The full version [has been released as 
Freeware][xargon], so it should be easy for you to get what you need.

A full development log for this tool is available on the [VGMaps 
Forums][vgmaps] (or the **logs** folder). This tool was developed 
without the use of the Xargon source code by manually decoding the game 
resources, so some of the techniques may be useful for decoding other 
games.

Please note the **palimage\#.png** image files are used to obtain the
assorted Xargon colour paletted variations, and are required for this
tool to work.

[pil]: https://pillow.readthedocs.io/en/stable/
[py]:  http://python.org/
[xargon]: http://www.classicdosgames.com/game/Xargon.html
[vgmaps]: http://www.vgmaps.com/forums/index.php?topic=1867.0

Usage
-----

There are two scripts included in the package that are intended to be
executed directly. **xargonmapper.py** is the main map generation
script, **xargongraphics.py** is a script to extract the contents of a
Xargon GRAPHICS resource file. In addition to the three scripts above,
several supplimentary scripts can be run to gather debug outputs of one
form or another, and are listed under the **Other Scripts** heading.

The **genep1.sh, genep2.sh and genep3.sh** are pre-made shell scripts to
generate map images for each episode of the game. You can edit these
files to change the path to Xargon for alternate configurations. Sorry,
no .BAT files are provided for Windows users, but the .sh files and the
below instructions should get you going.

### xargonmapper.py

**Usage: python xargonmapper.py \[Graphics File\] \[Tiles File\] \[Map
File(s)\...\]**

Generates map images for every Xargon map file indicated. Requires the
corresponding GRAPHICS file for the images to use, and the TILES file
for the map tile to graphics resource mapping. All files should be from
the same Episode of Xargon.

## xargongraphics.py

**Usage: python xargongraphics.py \[Graphics File\]**

Extracts all graphics resources from the specified GRAPHICS file from
Xargon. Output is stored in the Episode\#Images and
Episode\#OriginalImages folders, where \# is the episode number of the
input file. The OriginalImages folder contains the original 256-colour
images without any additional processing, while the Images folder
contains 32-bit RGBA images after colour index 0 has been set
transparent.

## Other Scripts

### xargonmap.py

**Usage: python xargonmap.py \[Map File(s)\]** Generates the following
debug information for each specified Xargon map file:

\[mapname\]\_flat.png
:   A false-colour image of the map, where each tile value is
    represented as a different colour.

\[mapname\].csv
:   A simple CSV containing each tile value

\[mapname\]\_info.csv
:   Auxiliary information about a map from the footer. Contains all the
    unknown header-type information, as well as the strings.

\[mapname\]\_objs.csv
:   A full listing of all objects in the specified map, and all their
    associated fields.

\[mapname\]\_strings.csv
:   A listing of all the strings in the map, as well as the guessed
    mapping to object reference values.

### xargontiles.py

**Usage: python xargontiles.py \[Tiles File\]**

Generates a debug CSV file for the mapping specified in the given TILES
file from Xargon. Output is written to tiles.csv.

### xargonfontgen.py

**Usage: python xargongraphics.py \[Graphics File\]**

Generates BDF fotn files for the two identified fonts stored in the
Xargon GRAPHICS file. The BDF files can then be converted to .pil files
for use in the main mapper via the pilfont.py script. The BDF files can
also be used in any software that supports BDF.
