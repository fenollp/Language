#/usr/bin/env python
# -*- coding: utf-8 -*-

# First real implementation of Language's transcoder

### Enter Input code here
Input = \
"""  a+ =b  """

### Parsing the Input

# Tree-ing the input
import re
tree = re.findall(Input,
    """
        \s*
            (
                ( (?: \\= | [^=] )+ )   # Pattern
                \s* = \s*                   # Pattern = Replacement
                ( (?: \\= | [^=] )+ )   # Replacement
            )
        \s*
    """
, re.S | re.X)

### Printing the Output
print Input
print '•••'
print tree

Output = ''
