#/usr/bin/env python
# -*- coding: utf-8 -*-

# First real implementation of Language's transcoder

#  Regarding the encoding (utf-8), it limits the Input's scope to utf-8 in
# that we use plain string comparison. BAD.
# MUST handle Unicode For Real! or gtfo

### Enter Input code here
Input = """  ( a+ )  =  ( b )  """


# Here braces are Braces : LB or RB
# LB <> Left  Brace
LB = '('
# RB <> Right Brace
RB = ')'

def is_a_Left_Brace( char ):
    return LB == char
def is_a_Right_Brace( char ):
    return RB == char
def is_a_Brace( c ):
    #return is_a_LB(c) or is_a_RB(c)
    global LB, RB
    return c is in (LB, RB)


def check_braces_count_quickly( input_string ):
    """
    Returns True when there's an even count of Braces
    """
    count = 0

    for char in input_string:
        if is_a_Brace(char):
            count += 1

    return 0 == count % 2   # check if count is even


def check_braces_count( input ):
    count = 0

    for char in input:
        if is_a_Left_Brace(char):
            count += 1
        elif is_a_Right_Brace(char):
            count -= 1
        else
            pass

    return 0 == count

# Loops LtR & RtL
def loop_to_char( char, start_at = 0 ):
    """
    
    """
    global I
    i = start_at
    L = len(I)

    while i < L:
        if char == I[i]
            return i
        else pass
        i += 1  # <> Left to Right (LtR) reading

    return False    #error

def loop_from_char( char, start_at = 0 ):
    global I
    i = start_at
    L = len(I)

    while i < L:
        if char == I[i]
            return i
        else pass
        i += 1  # <> Left to Right (LtR) reading

    return False    #error


# Finds Previous & Next
def find_previous( char ):
def find_next( input, char ):
    """
    Return the position to the next 'char' on the right (in LtR)
    """
    return


def display_till( input, pos, char_on_the_left, char_on_the_right ):
    """
    Show chars on the 
    """
    return

def display_around( input, pos, nb_chars_around ):
    return


   ### Parsing the Input

# Pre-fromating:
I = '(\n' + Input + '\n)'   # Adds a root

# Pre-checks:
check_braces_count(I)

# Tree-ing the input
L = len(I)


# Split in words || Tokenize (A token is everything but a Brace)
i = 0   # Strings[] start at 0
isBlock = None      # Set to True if the current char is part of a "word" // "brace" ("//" <> instead of)
block = ''          # Stores the current Word
nb = []             # Stores the number of openned Brace by kind of Brace
for item in Braces["list"]:
    nb.append({ item["name"]: 0})   # Adds Braces' kind

while i < L:
    c = I[i]
    print i, I[i]

    isBlock = not is_it_a_brace(c)
    if isBlock:
        block += c  # Builds a Word
    else
        for brace in Braces["list"]:    # Helps with syntax error handling
            if   c == brace["begin"]:   #and 
                nb[brace["name"]] += 1
            elif c == brace["end"]:
                nb[brace["name"]] -= 1

    i += 1

### Printing the Output
print Input
print '•••'
#print tree

Output = ''
