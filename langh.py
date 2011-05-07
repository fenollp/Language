#/usr/bin/env python
# -*- coding: utf-8 -*-

# First real implementation of Language's transcoder

# Regarding the encoding (utf-8), it limits the Input's scope to utf-8! BAD.
# MUST handle Unicode For Real

### Enter Input code here
Input = \
""" {  < a+ >  =  ( b )  } """

### Parsing the Input
# May help
Braces = {"string": '',
"raw": # MUST be two distinct characters (for the moment)
#    {"name": '', "begin": '', "end": ''},
    {"name": 'style_quote',    "begin": '«', "end": '»'},
    {"name": 'single_quote',   "begin": '‘', "end": '’'},
    {"name": 'double_quote',   "begin": '“', "end": '”'},
    {"name": 'small_triangle', "begin": '‹', "end": '›'},
    {"name": 'triangle',       "begin": '<', "end": '>'},
    {"name": 'square',         "begin": '[', "end": ']'},
    {"name": 'curly',          "begin": '{', "end": '}'},
    {"name": 'circle',         "begin": '(', "end": ')'}
}

# Braces -> {"list": …}
Braces["list"] = []
for item in Braces["raw"]:
    Braces["list"].append({"name": item[0], "begin": item[1][0], "end": item[1][1]})


# Braces -> {"string": '()[]{}…', "list": …}
Braces["string"] = ''
for item in Braces["list"]:
    Braces["string"] += item["begin"] + item["end"]


def is_it_a_brace( char ):
    """
    True if the entry is an openning or closing brace (of any known kind).
    """
    global Braces
    return char in Braces["string"]


# Tree-ing the input
l = len(Input)


# Split in words || Tokenize (A token is everything but a Brace)
i = 0   # Strings[] start at 0
isBlock = None      # Set to True if the current char is part of a "word" // "brace" ("//" <> instead of)
block = ''          # Stores the current Word
nb = []             # Stores the number of openned Brace by kind of Brace
for item in Braces["list"]:
    nb.append({ item["name"]: 0})   # Adds Braces' kind

while i < l:
    c = Input[i]
    print i, Input[i]

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
