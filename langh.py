#!/usr/bin/env
#-*- coding: utf-8 -*-

# Python >= 3000


iput = '''––––––––––––––––––––––––––––––––––––––––
(patt ) ê (replacement)
( patt) y (replacement)
( p) ê ( r)

  patt <---
'''.decode('utf-8')

rule_string = u'ê'
raw = iput



print raw
print "⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣"
### Algorithm
#while there_are_rules_in( raw ):
  # Applies to a subpart of the input AND removes the first rule
#  raw = apply_first_rule_found( raw )  # Assignment b/c Python doesn't pass by ref.
#print raw
###


l = len(iput)
i = 0
c = ''
while i < l:
  c = iput[i]
  if 
  i = i + 1

#def f_string( start, what, string
def trim_escaped_text( text ):
  for (i, c) in enumerate(text):
    if ( c in [' ', '\t'] ) and text[i +1] != '\\':
      text = text[: i] + text[i+1 :]
  return text

trim_escaped_text(raw)



















