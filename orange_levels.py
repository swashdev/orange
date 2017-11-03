# Copyright (c) 2011-2017 Philip Pavlick
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
# Like most of the software that I write, this software has an additional
# "careware clause."  If you like this software and would like to support the
# creator, please read "letter.txt" (in this directory)

# Get the levels for Orange Guy's Quest from a text file
# This is how the game originally got its level data, but like an idiot I
# decided to hard-code it before saving the program and forgetting it forever.
# Now I have to basically rebuild this whole thing, but hopefully I now know
# a better way to do it...

# Returns a list of strings.
def get_levels( level_file_path, DEBUG = False ):
    level_file = None
    if DEBUG:
      print "Load: Opening level file"
    try:
        # Attempt to open the level file as a read-only file
        level_file = open( level_file_path, 'r' )
    except:
        # If we fail, we must abort
        raise SystemExit, "Unable to initialize orange.py--level file " \
                          + level_file_path + " does not exist."
  
    # Assuming success, we read the entire file in one fell swoop so that we
    # don't have to read it more than once.
    
    if DEBUG:
      print "Load: Reading level file"
    levels = level_file.read()
    
    if DEBUG:
      print "Load: Closing level file"
    level_file.close()
    
    if DEBUG:
      print "Work: Splitting level data" 
    # Separate the levels into a list; we are using "\n;\n" as a delimiter.
    levels = levels.split( "\n;\n" )

    if DEBUG:
      print "Work: Checking level data"
    # Before we pass this list up, we first have to check each level to make
    # sure it has a player start and an exit.
    level_has_player = False
    level_has_exit = False
    level_has_walls = False
    
    index = 0
    while index >= 0 and index < len( levels ):
        if levels[index] == "":
            if DEBUG:
              print "Work: Empty level found--removing..."
            del levels[index]
            continue
        else:
          character = 0
          while character >= 0 and character < len( levels[index] ):
              ch = levels[index][character]
              if ch == '\0':
                  index = -1
                  character = -1
                  break
              elif ch == 'P':
                  level_has_player = True
              elif ch in ['E','A']:
                  level_has_exit = True
              elif ch == 'W':
                  level_has_walls = True
              elif ch not in " abcdefghijklmnopqrstuvwxyzSM78946123!@#$^&*(":
                  # Treat all invalid characters as a space
                  levels[index].replace( ch, ' ' )
              if level_has_player and level_has_exit and level_has_walls:
                  character = -1
                  break
              character = character + 1
          if level_has_player and level_has_exit and level_has_walls:
              index = index + 1
          else:
              if DEBUG:
                print "Work: Invalid level found--removing..."
              del levels[index]
          level_has_player = False
          level_has_exit = False
          level_has_walls = False
    
    if DEBUG:
      print "Work: Butchering levels"
    # Before we can use this list of levels, the levels themselves need to be
    # cut into parts separated by newlines.
    index = 0
    while index < len( levels ):
        level = levels[index]
        levels[index] = level.split( '\n' )
        index = index + 1
    
    # What we should have now is a list of lists of strings. Ai ai ai!
    # What was I thinking when I was going through college, man?
    if DEBUG:
      print "Work: Passing levels up to main program"
    return levels

##################
# Test functions #
##################

def test_level_file( level_file_path ):
    level_file = None
    try:
        level_file = open( level_file_path, 'r' )
    except:
        return "No such level file: " + level_file_path
    test_data = level_file.read()
    level_file.close()
    return test_data

def test_file_levels( level_file_path ):
    level_file = None
    try:
        level_file = open( level_file_path, 'r' )
    except:
        return "No such level file: " + level_file_path
    test_data = level_file.read().split( ';' )
    level_file.close()
    return test_data

def test_file_level_splits( level_file_path ):
    level_file = None
    try:
        level_file = open( level_file_path, 'r' )
    except:
        return "No such level file: " + level_file_path
    levels = level_file.read().split( ';' )
    level_file.close()
    index = 0
    while index < len( levels ):
        level = levels[index]
        levels[index] = level.split( '\n' )
        index = index + 1
    return levels
