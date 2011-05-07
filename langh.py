#!/usr/bin/env
#-*- coding: utf-8 -*-

# Python >= 2.6.1

import re

def there_are_rules_in( text ):
  return ( len(find_first_rule( text )) >= 1 )



def apply_first_rule_found( text ):
  (patt, rep, (start, end)) = find_first_rule( text )
  # remove the rule & split text: the rule applies in the second part
  t1 = text[: start]
  t2 = text[end :]
  print re.escape(patt), len(re.escape(patt)), patt, len(patt), re.escape(rep), len(re.escape(rep)), rep, len(rep)#
  t2 = re.sub( re.escape(patt), rep, t2 )  # replace
  return t1 + t2



def find_first_rule( text ):
  global rule_string

  regex  = ur' (\(|\[|\{) \s* ([^' + rule_string + ur'\n \1 ]+) \s* \1 '
  regex += ur'\s*' + rule_string + ur'\s*'
  regex += ur' (\(|\[|\{) \s* ([^' + rule_string + ur'\n \2 ]+) \s* \2 '

  mask = re.compile(regex, re.S | re.X)
  matches = mask.findall( text )

  if len(matches) is 0:
    return matches
  else:
    (pos_s, pos_e) = mask.search( text ).span()
    print matches
    return (
      matches[0][1].decode('utf-8'),  # Pattern
      matches[0][2].decode('utf-8'),  # Replacement
      (pos_s , pos_e +1)  # Start, End
    )




iput = '''––––––––––––––––––––––––––––––––––––––––
(patt ) ê (replacement)
( patt) y (replacement)
( p) ê ( r)

  patt <---
'''.decode('utf-8')

rule_string = u'ê'
raw = iput


# Tests
# print find_first_rule(raw)
# print there_are_rules_in(raw)
# apply_first_rule_found(raw)



print raw
print "⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣⇣"
### Algorithm
while there_are_rules_in( raw ):
  # Applies to a subpart of the input AND removes the first rule
  raw = apply_first_rule_found( raw )  # Assignment b/c Python doesn't pass by ref.
print raw
###





